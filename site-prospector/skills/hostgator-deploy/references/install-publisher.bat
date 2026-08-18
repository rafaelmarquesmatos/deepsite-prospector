@echo off
title Site Prospector - install automatic publisher
echo.
echo  This installer creates a Windows task that checks every 1 minute
echo  for sites in the queue and publishes them on HostGator by itself. No windows, no clicks.
echo.
schtasks /Create /F /TN "ProspectorPublisher" /SC MINUTE /MO 1 /TR "wscript.exe \"%~dp0hidden-publisher.vbs\""
if %errorlevel%==0 (
  echo.
  echo  [OK] Automatic publisher installed! You can close this window.
  echo  To uninstall someday: schtasks /Delete /TN ProspectorPublisher /F
) else (
  echo.
  echo  [ERROR] Could not create the task. Close and run this file with
  echo  right-click ^> "Run as administrator".
)
echo.
pause
