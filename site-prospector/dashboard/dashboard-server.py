#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Site Prospector - local dashboard server (SQLite). No dependencies: standard Python only.
Usage: python dashboard-server.py  (or double-click start-dashboard.bat)
Opens at http://localhost:8765 - edits, deletions and drag&drop save to prospector.db"""
import json, sqlite3, os, sys, webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(FOLDER)
DB = os.path.join(FOLDER, 'prospector.db')
CONFIG = os.path.join(FOLDER, 'prospector-config.json')

def read_config():
    try: return json.load(open(CONFIG, encoding='utf-8'))
    except Exception: return {}
PORT = 8765
FIELDS = ['slug','name','niche','city','rating','reviews','email','phone','whatsapp',
          'oldSite','reason','status','newUrl','proposalDate','value','notes',
          'contractStatus','contractDate','maintenance','paid','clientDoc','clientAddress']

def connection():
    c = sqlite3.connect(DB)
    c.execute('''CREATE TABLE IF NOT EXISTS leads(
        slug TEXT PRIMARY KEY, name TEXT, niche TEXT, city TEXT, rating REAL, reviews INTEGER,
        email TEXT, phone TEXT, whatsapp TEXT, oldSite TEXT, reason TEXT,
        status TEXT DEFAULT 'new', newUrl TEXT, proposalDate TEXT, value REAL, notes TEXT,
        contractStatus TEXT DEFAULT 'pending', contractDate TEXT, maintenance REAL, paid INTEGER DEFAULT 0,
        updated TEXT DEFAULT (datetime('now','localtime')))''')
    for col, kind in [('contractStatus',"TEXT DEFAULT 'pending'"),('contractDate','TEXT'),('maintenance','REAL'),('paid','INTEGER DEFAULT 0'),('clientDoc','TEXT'),('clientAddress','TEXT')]:
        try: c.execute('ALTER TABLE leads ADD COLUMN %s %s' % (col, kind))
        except sqlite3.OperationalError: pass
    return c

def import_snapshot():
    """First run without a database: imports leads embedded in dashboard.html."""
    try:
        html = open(os.path.join(FOLDER, 'dashboard.html'), encoding='utf-8').read()
        start = html.index('<script id="dados" type="application/json">') + len('<script id="dados" type="application/json">')
        end = html.index('</script>', start)
        data = json.loads(html[start:end])
        c = connection()
        for l in data.get('leads', []):
            c.execute('INSERT OR IGNORE INTO leads (%s) VALUES (%s)' % (','.join(FIELDS), ','.join('?'*len(FIELDS))),
                      [l.get(k) for k in FIELDS])
        c.commit(); c.close()
        print('Snapshot imported from dashboard.html into prospector.db')
    except Exception as e:
        print('(no snapshot to import: %s)' % e)

class App(SimpleHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def _body(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n).decode('utf-8')) if n else {}
    def do_GET(self):
        if self.path.split('?')[0] == '/api/config':
            cfg = read_config()
            hg = dict(cfg.get('hostgator', {}))
            hg['passwordSet'] = bool(hg.get('password'))
            hg.pop('password', None)  # the password NEVER leaves the file
            return self._json(200, {'provider': cfg.get('provider', {}), 'hostgator': hg})
        if self.path.split('?')[0] == '/api/leads':
            c = connection(); c.row_factory = sqlite3.Row
            rows = [dict(r) for r in c.execute('SELECT * FROM leads').fetchall()]; c.close()
            return self._json(200, rows)
        if self.path in ('/', ''):
            self.path = '/dashboard.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
        if self.path.split('?')[0] == '/api/leads':
            l = self._body(); c = connection()
            c.execute('INSERT OR REPLACE INTO leads (%s) VALUES (%s)' % (','.join(FIELDS), ','.join('?'*len(FIELDS))),
                      [l.get(k) for k in FIELDS])
            c.commit(); c.close(); return self._json(200, {'ok': True})
        return self._json(404, {'error': 'route'})
    def do_PUT(self):
        if self.path.split('?')[0] == '/api/config':
            cfg = read_config(); body = self._body()
            if 'provider' in body or 'hostgator' in body:
                if 'provider' in body:
                    prov = cfg.get('provider', {})
                    prov.update({k: v for k, v in body['provider'].items() if isinstance(v, str)})
                    cfg['provider'] = prov
                if 'hostgator' in body:
                    hg = cfg.get('hostgator', {})
                    for k, v in body['hostgator'].items():
                        if not isinstance(v, str): continue
                        if k == 'password' and v == '': continue  # blank = keep the current one
                        hg[k] = v
                    cfg['hostgator'] = hg
            else:  # compatibility: flat body = provider
                prov = cfg.get('provider', {})
                prov.update({k: v for k, v in body.items() if isinstance(v, str)})
                cfg['provider'] = prov
            json.dump(cfg, open(CONFIG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            return self._json(200, {'ok': True})
        parts = self.path.split('?')[0].split('/')
        if len(parts) == 4 and parts[1] == 'api' and parts[2] == 'leads':
            slug, changes = parts[3], self._body()
            sets = [k for k in changes if k in FIELDS and k != 'slug']
            if sets:
                c = connection()
                c.execute('UPDATE leads SET %s, updated=datetime("now","localtime") WHERE slug=?' %
                          ','.join('%s=?' % k for k in sets), [changes[k] for k in sets] + [slug])
                c.commit(); c.close()
            return self._json(200, {'ok': True})
        return self._json(404, {'error': 'route'})
    def do_DELETE(self):
        parts = self.path.split('?')[0].split('/')
        if len(parts) == 4 and parts[1] == 'api' and parts[2] == 'leads':
            c = connection(); c.execute('DELETE FROM leads WHERE slug=?', (parts[3],)); c.commit(); c.close()
            return self._json(200, {'ok': True})
        return self._json(404, {'error': 'route'})
    def log_message(self, *a): pass

if __name__ == '__main__':
    fresh = not os.path.exists(DB)
    connection().close()
    if fresh: import_snapshot()
    print('Prospector running at http://localhost:%d  (Ctrl+C to stop)' % PORT)
    try: webbrowser.open('http://localhost:%d' % PORT)
    except Exception: pass
    try: ThreadingHTTPServer(('127.0.0.1', PORT), App).serve_forever()
    except KeyboardInterrupt: print('\nStopped.')
