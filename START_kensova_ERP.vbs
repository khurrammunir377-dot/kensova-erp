Option Explicit
' START_KENSOVA_ERP.vbs
' Double-click this file to start Kensova ERP in a maximized Edge app window.

Dim WshShell, fso, scriptDir, edgePath, cmd, psCmd
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Start the ERP server hidden.
WshShell.Run """" & scriptDir & "\run_KENSOVA_erp_8009.bat""", 0, False

' Give the server a moment to start.
WScript.Sleep 3000

' Locate Microsoft Edge.
If fso.FileExists("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") Then
    edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ElseIf fso.FileExists("C:\Program Files\Microsoft\Edge\Application\msedge.exe") Then
    edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
Else
    edgePath = "msedge"
End If

' Open ERP as an Edge app window.
cmd = """" & edgePath & """ --new-window --start-maximized --app=http://127.0.0.1:8009"
WshShell.Run cmd, 1, False

' Use the supplied PowerShell-style Windows API maximizer.
' This is more reliable than Edge's --start-maximized alone.
WScript.Sleep 1500
psCmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & scriptDir & "\maximize_window.ps1"""
WshShell.Run psCmd, 0, False

Set fso = Nothing
Set WshShell = Nothing
