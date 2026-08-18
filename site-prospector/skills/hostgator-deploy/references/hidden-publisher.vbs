' Site Prospector - runs the publisher without a window (scheduled task)
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & folder & "\publish-now.ps1"" -Auto"
CreateObject("Wscript.Shell").Run cmd, 0, False
