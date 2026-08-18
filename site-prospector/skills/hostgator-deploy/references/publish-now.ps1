# Site Prospector - automatic HostGator publishing (Windows)
# Manual: double-click publish-now.bat (shows a window)
# Automatic: installed by install-publisher.bat, runs every minute hidden (-Auto)
param([switch]$Auto)
$ErrorActionPreference = "Stop"
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $folder
function Finish($code){ if(-not $Auto){ pause }; exit $code }
function Log($msg,$color="Gray"){
  if($Auto){ Add-Content "publisher-log.txt" ("[" + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + "] " + $msg) }
  else { Write-Host $msg -ForegroundColor $color }
}
if (-not (Test-Path "publish-queue.txt")) { if(-not $Auto){ Log "Nothing in the queue - ask your AI assistant to publish first." "Yellow" }; Finish 0 }
try { $cfg = Get-Content "prospector-config.json" -Raw -Encoding UTF8 | ConvertFrom-Json } catch { Log "ERROR: prospector-config.json not found/invalid." "Red"; Finish 1 }
$u = $cfg.hostgator.user; $p = $cfg.hostgator.password; $srv = $cfg.hostgator.server
if (-not $u -or -not $p -or -not $srv) { Log "ERROR: fill in the HostGator connection (dashboard > Settings) including the password." "Red"; Finish 1 }
$queue = Get-Content "publish-queue.txt" -Encoding UTF8 | Where-Object { $_ -match "\|" }
$ok = 0; $fail = 0
foreach ($line in $queue) {
  $parts = $line -split "\|", 2
  $local = $parts[0].Trim(); $remote = $parts[1].Trim()
  if (-not (Test-Path $local)) { Log ("SKIPPED (does not exist): " + $local) "Yellow"; $fail++; continue }
  Log ("Uploading " + $local + " -> " + $remote + " ...")
  & curl.exe -sS --connect-timeout 20 -T "$local" "ftp://$srv/$remote" --user "${u}:${p}" --ftp-create-dirs
  if ($LASTEXITCODE -eq 0) { Log "  OK" "Green"; $ok++ } else { Log ("  FAILED (code " + $LASTEXITCODE + ")") "Red"; $fail++ }
}
Log ("Finished: " + $ok + " uploaded, " + $fail + " failed.") "Cyan"
if ($fail -eq 0 -and $ok -gt 0) {
  Rename-Item "publish-queue.txt" ("publish-done-" + (Get-Date -Format "yyyyMMdd-HHmm") + ".txt") -Force
  Log "Queue done. Tell your AI assistant ('published') to verify the URLs." "Cyan"
}
Finish 0
