#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Site Prospector - CRM MCP server (STDIO).
Works with any agent that supports MCP servers, reading and writing the SAME
prospector.db used by the dashboard.

Installation:  pip install "mcp[cli]"
Run:           python prospector_mcp.py                     (uses the current folder)
               python prospector_mcp.py --folder "C:\\Users\\you\\Desktop\\Clients"
Self-test:     python prospector_mcp.py --test
"""
import argparse, json, os, sqlite3, sys, datetime

parser = argparse.ArgumentParser()
parser.add_argument('--folder', default=os.environ.get('PROSPECTOR_DIR', '.'),
                    help='Project folder (where prospector.db and dashboard.html live)')
parser.add_argument('--test', action='store_true', help='Run the self-test and exit')
ARGS, _ = parser.parse_known_args()
FOLDER = os.path.abspath(ARGS.folder)
DB = os.path.join(FOLDER, 'prospector.db')

FIELDS = ['slug','name','niche','city','rating','reviews','email','phone','whatsapp',
          'oldSite','reason','status','newUrl','proposalDate','value','notes',
          'contractStatus','contractDate','maintenance','paid','clientDoc','clientAddress']
VALID_STATUSES = ['new','redesigned','published','proposed','replied','closed','discarded']

def connection():
    c = sqlite3.connect(DB)
    c.execute('''CREATE TABLE IF NOT EXISTS leads(
        slug TEXT PRIMARY KEY, name TEXT, niche TEXT, city TEXT, rating REAL,
        reviews INTEGER, email TEXT, phone TEXT, whatsapp TEXT, oldSite TEXT,
        reason TEXT, status TEXT DEFAULT 'new', newUrl TEXT, proposalDate TEXT,
        value REAL, notes TEXT, contractStatus TEXT DEFAULT 'pending', contractDate TEXT,
        maintenance REAL, paid INTEGER DEFAULT 0, clientDoc TEXT, clientAddress TEXT,
        updated TEXT)''')
    c.commit()
    return c

def _rows(rows, cols):
    return [dict(zip(cols, r)) for r in rows]

def _now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# ---------- Logic (shared between MCP and self-test) ----------

def list_leads(status=None):
    c = connection(); cur = c.cursor()
    if status:
        cur.execute('SELECT %s FROM leads WHERE status=? ORDER BY name' % ','.join(FIELDS), (status,))
    else:
        cur.execute('SELECT %s FROM leads ORDER BY status, name' % ','.join(FIELDS))
    r = _rows(cur.fetchall(), FIELDS); c.close(); return r

def get_lead(slug):
    c = connection(); cur = c.cursor()
    cur.execute('SELECT %s FROM leads WHERE slug=?' % ','.join(FIELDS), (slug,))
    row = cur.fetchone(); c.close()
    return dict(zip(FIELDS, row)) if row else None

def save_lead(data):
    if not data.get('slug'):
        return {'error': 'slug is required (e.g. maria-silva)'}
    if data.get('status') and data['status'] not in VALID_STATUSES:
        return {'error': 'invalid status. Use: %s' % ', '.join(VALID_STATUSES)}
    current = get_lead(data['slug']) or {}
    current.update({k: v for k, v in data.items() if k in FIELDS and v is not None})
    current.setdefault('status', 'new'); current.setdefault('contractStatus', 'pending'); current.setdefault('paid', 0)
    c = connection()
    c.execute('INSERT OR REPLACE INTO leads (%s,updated) VALUES (%s,?)' % (','.join(FIELDS), ','.join('?'*len(FIELDS))),
              [current.get(k) for k in FIELDS] + [_now()])
    c.commit(); c.close()
    return {'ok': True, 'lead': current['slug'], 'status': current['status']}

def set_status(slug, status, extra_note=None):
    if status not in VALID_STATUSES:
        return {'error': 'invalid status. Use: %s' % ', '.join(VALID_STATUSES)}
    lead = get_lead(slug)
    if not lead: return {'error': 'lead not found: %s' % slug}
    c = connection()
    if status == 'proposed' and not lead.get('proposalDate'):
        c.execute('UPDATE leads SET proposalDate=? WHERE slug=?', (datetime.date.today().isoformat(), slug))
    if extra_note:
        new_notes = ((lead.get('notes') or '') + ' | ' + extra_note).strip(' |')
        c.execute('UPDATE leads SET notes=? WHERE slug=?', (new_notes, slug))
    c.execute('UPDATE leads SET status=?, updated=? WHERE slug=?', (status, _now(), slug))
    c.commit(); c.close()
    return {'ok': True, 'lead': slug, 'new_status': status}

def close_lead(slug, value, maintenance=None):
    lead = get_lead(slug)
    if not lead: return {'error': 'lead not found: %s' % slug}
    c = connection()
    c.execute('UPDATE leads SET status=?, value=?, maintenance=?, updated=? WHERE slug=?',
              ('closed', value, maintenance, _now(), slug))
    c.commit(); c.close()
    return {'ok': True, 'lead': slug, 'value': value, 'maintenance': maintenance}

def pending_followups(days=3):
    limit = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    c = connection(); cur = c.cursor()
    cur.execute("SELECT slug,name,email,proposalDate,notes FROM leads WHERE status='proposed' AND proposalDate<=? ", (limit,))
    r = _rows(cur.fetchall(), ['slug','name','email','proposalDate','notes']); c.close()
    return [x for x in r if 'follow-up' not in (x.get('notes') or '').lower()]

def financial_summary():
    c = connection(); cur = c.cursor()
    cur.execute("SELECT COALESCE(SUM(value),0), COALESCE(SUM(CASE WHEN paid=1 THEN value ELSE 0 END),0), COALESCE(SUM(maintenance),0), COUNT(*) FROM leads WHERE status='closed'")
    total, received, mrr, n = cur.fetchone(); c.close()
    return {'closed': n, 'total_closed': total, 'received': received,
            'to_receive': total - received, 'mrr_maintenance': mrr, 'projection_12m': total + mrr*12}

def regenerate_dashboard():
    """Rebuilds dashboard.html (snapshot) from the database, if a template exists in the folder."""
    tpl_path = None
    for candidate in ['dashboard-template.html', 'dashboard.html']:
        p = os.path.join(FOLDER, candidate)
        if os.path.exists(p): tpl_path = p; break
    if not tpl_path: return {'error': 'dashboard.html/template not found in folder %s' % FOLDER}
    import re
    t = open(tpl_path, encoding='utf-8').read()
    data = json.dumps({'updated': _now(), 'leads': list_leads()}, ensure_ascii=False)
    if '__DATA__' in t:
        new = t.replace('__DATA__', data)
    else:
        new = re.sub(r'(<script id="dados"[^>]*>).*?(</script>)', lambda m: m.group(1)+data+m.group(2), t, flags=re.S)
    open(os.path.join(FOLDER, 'dashboard.html'), 'w', encoding='utf-8').write(new)
    return {'ok': True, 'leads': len(list_leads())}

# ---------- Self-test ----------
if ARGS.test:
    import tempfile
    FOLDER = tempfile.mkdtemp(); DB = os.path.join(FOLDER, 'prospector.db')
    print('1 save:', save_lead({'slug':'test-mcp','name':'Test MCP','email':'t@t.com','niche':'nutritionist','city':'SP'}))
    print('2 list:', len(list_leads()), 'lead(s)')
    print('3 status:', set_status('test-mcp','proposed'))
    import sqlite3 as s3
    c=s3.connect(DB); c.execute("UPDATE leads SET proposalDate=date('now','-5 day') WHERE slug='test-mcp'"); c.commit(); c.close()
    print('4 pending followups:', pending_followups())
    print('5 close:', close_lead('test-mcp', 700, 100))
    print('6 financial:', financial_summary())
    print('7 invalid status (should error):', set_status('test-mcp','banana'))
    print('SELF-TEST OK')
    sys.exit(0)

# ---------- MCP server ----------
from mcp.server.fastmcp import FastMCP
mcp = FastMCP('prospector-crm')

@mcp.tool()
def list_leads(status: str = '') -> str:
    """List CRM leads. Optional: filter by status (new, redesigned, published, proposed, replied, closed, discarded)."""
    return json.dumps(list_leads(status or None), ensure_ascii=False)

@mcp.tool()
def get_lead(slug: str) -> str:
    """Return all data for a lead by slug (e.g. maria-silva)."""
    return json.dumps(get_lead(slug) or {'error': 'not found'}, ensure_ascii=False)

@mcp.tool()
def save_lead(slug: str, name: str = '', niche: str = '', city: str = '', rating: float = 0,
              reviews: int = 0, email: str = '', phone: str = '', whatsapp: str = '',
              oldSite: str = '', reason: str = '', newUrl: str = '', notes: str = '') -> str:
    """Create or update a lead in the CRM (use after prospecting or when fixing data). Slug in firstname-lastname format."""
    d = {k: v for k, v in locals().items() if v not in ('', 0)}
    return json.dumps(save_lead(d), ensure_ascii=False)

@mcp.tool()
def update_status(slug: str, status: str, note: str = '') -> str:
    """Move the lead through the funnel: new -> redesigned -> published -> proposed -> replied -> closed/discarded. NEVER use 'closed' without explicit user confirmation (to close with a value, use record_close)."""
    return json.dumps(set_status(slug, status, note or None), ensure_ascii=False)

@mcp.tool()
def record_close(slug: str, value: float, monthly_maintenance: float = 0) -> str:
    """Record a CLOSED client with the agreed value (and monthly maintenance, if any). Use only when the user confirms the deal and the value."""
    return json.dumps(close_lead(slug, value, monthly_maintenance or None), ensure_ascii=False)

@mcp.tool()
def pending_followups(days: int = 3) -> str:
    """List leads with a proposal sent N+ days ago, no reply and no follow-up registered - the ones needing a follow-up now."""
    return json.dumps(pending_followups(days), ensure_ascii=False)

@mcp.tool()
def record_followup(slug: str) -> str:
    """Record that the follow-up was sent today for the lead (1 per lead, never repeat)."""
    return json.dumps(set_status(slug, 'proposed', 'Follow-up sent on %s' % datetime.date.today().isoformat()), ensure_ascii=False)

@mcp.tool()
def financial_summary() -> str:
    """Financial dashboard: total closed, received, to receive, MRR from maintenance and 12-month projection."""
    return json.dumps(financial_summary(), ensure_ascii=False)

@mcp.tool()
def regenerate_dashboard() -> str:
    """Regenerate dashboard.html (visual panel) with current database data. Use at the end of any sequence of changes."""
    return json.dumps(regenerate_dashboard(), ensure_ascii=False)

if __name__ == '__main__':
    mcp.run()
