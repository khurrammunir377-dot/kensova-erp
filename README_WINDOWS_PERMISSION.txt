KENSOVA ERP - WINDOWS DOWNLOAD / PERMISSION SETUP

IMPORTANT: Unblock the downloaded ZIP BEFORE extracting it.
This is the most reliable way to prevent Windows from asking for permission
when START_KENSOVA_ERP.vbs or the BAT files are opened.

1. Download the Kensova ERP ZIP.
2. Right-click the ZIP -> Properties.
3. If an "Unblock" checkbox appears near the bottom, tick it.
4. Click Apply -> OK.
5. Extract the ZIP to a normal local folder, for example C:\KensovaERP.
6. Run setup_venv.bat once.
7. Start the ERP with START_kensova_ERP.vbs.

If the ZIP was already extracted before it was unblocked:
1. Close the ERP.
2. Run UNBLOCK_KENSOVA_FILES.bat from the extracted folder once.
3. Then run START_kensova_ERP.vbs again.

If Windows still shows an "Open File - Security Warning", the ZIP/folder is
still carrying a Windows download security mark. Unblock the original ZIP,
extract it again, and use the newly extracted copy.

NOTE:
- This is different from a UAC administrator prompt. Unblocking removes the
  downloaded-file security mark; it does not bypass Windows administrator
  permissions or company security policies.
- Do not run the ERP from inside the ZIP. Extract it first.
