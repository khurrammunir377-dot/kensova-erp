Add-Type -Namespace Win32Functions -Name Win32ShowWindowAsync -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
'@

# Wait briefly for the Edge app window to appear, then maximize it.
for ($i = 0; $i -lt 20; $i++) {
    $p = Get-Process | Where-Object {
        $_.MainWindowTitle -ne '' -and $_.ProcessName -match '^msedge$'
    } | Sort-Object StartTime -Descending | Select-Object -First 1

    if ($p -and $p.MainWindowHandle -ne [IntPtr]::Zero) {
        # 3 = SW_MAXIMIZE
        [Win32Functions.Win32ShowWindowAsync]::ShowWindowAsync($p.MainWindowHandle, 3) | Out-Null
        Start-Sleep -Milliseconds 250

        # Apply once more because Edge can restore its app window after launch.
        [Win32Functions.Win32ShowWindowAsync]::ShowWindowAsync($p.MainWindowHandle, 3) | Out-Null
        exit 0
    }

    Start-Sleep -Milliseconds 300
}
