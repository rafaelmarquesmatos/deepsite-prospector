#!/bin/bash
# Site Prospector - publishes the queue to HostGator (macOS).
# Manual: double-click. Automatic (launchd): called with --auto (log in publisher-log.txt, no pause).
cd "$(dirname "$0")"
AUTO=0; [ "$1" = "--auto" ] && AUTO=1
log(){ if [ $AUTO -eq 1 ]; then echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> publisher-log.txt; else echo "$1"; fi; }
finish(){ [ $AUTO -eq 0 ] && read -p "Press Enter to close..."; exit $1; }
[ -f publish-queue.txt ] || { [ $AUTO -eq 0 ] && log "Nothing in the queue - ask your AI assistant to publish first."; finish 0; }
CFG=prospector-config.json
[ -f $CFG ] || { log "ERROR: prospector-config.json not found."; finish 1; }
U=$(python3 -c "import json;print(json.load(open('$CFG'))['hostgator'].get('user',''))")
P=$(python3 -c "import json;print(json.load(open('$CFG'))['hostgator'].get('password',''))")
SRV=$(python3 -c "import json;print(json.load(open('$CFG'))['hostgator'].get('server',''))")
[ -n "$U" ] && [ -n "$P" ] && [ -n "$SRV" ] || { log "ERROR: fill in the HostGator connection in the dashboard (Settings), including the password."; finish 1; }
OK=0; FAIL=0
while IFS='|' read -r LOCAL REMOTE; do
  LOCAL=$(echo "$LOCAL" | xargs); REMOTE=$(echo "$REMOTE" | xargs)
  [ -z "$LOCAL" ] && continue
  if [ ! -f "$LOCAL" ]; then log "SKIPPED (does not exist): $LOCAL"; FAIL=$((FAIL+1)); continue; fi
  log "Uploading $LOCAL -> $REMOTE ..."
  if curl -sS --connect-timeout 20 -T "$LOCAL" "ftp://$SRV/$REMOTE" --user "$U:$P" --ftp-create-dirs; then
    log "  OK"; OK=$((OK+1))
  else
    log "  FAILED"; FAIL=$((FAIL+1))
  fi
done < publish-queue.txt
log "Finished: $OK uploaded, $FAIL failed."
if [ $FAIL -eq 0 ] && [ $OK -gt 0 ]; then
  mv publish-queue.txt "publish-done-$(date '+%Y%m%d-%H%M').txt"
  log "Queue done. Tell your AI assistant ('published') to verify the URLs."
fi
finish 0
