#!/bin/bash
# Site Prospector - installs the automatic publisher on macOS (launchd, once in a lifetime).
cd "$(dirname "$0")"
FOLDER="$(pwd)"
PLIST="$HOME/Library/LaunchAgents/com.prospector.publisher.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.prospector.publisher</string>
  <key>ProgramArguments</key><array>
    <string>/bin/bash</string>
    <string>$FOLDER/publish-now.command</string>
    <string>--auto</string>
  </array>
  <key>StartInterval</key><integer>60</integer>
  <key>RunAtLoad</key><true/>
</dict></plist>
PLISTEOF
launchctl unload "$PLIST" 2>/dev/null
if launchctl load "$PLIST"; then
  echo "[OK] Automatic publisher installed! Every 1 minute it checks the queue and publishes by itself."
  echo "To uninstall someday: launchctl unload \"$PLIST\" && rm \"$PLIST\""
else
  echo "[ERROR] Could not register. Run this file again or send me the error above."
fi
read -p "Press Enter to close..."
