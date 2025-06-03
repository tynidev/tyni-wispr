# Tyni-Wispr Startup Shortcut Installer
# This script creates a Windows startup shortcut for the Tyni-Wispr audio transcription tool

# Get the script's directory (where run_wispr.ps1 is located)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($scriptDir)) {
    $scriptDir = Get-Location
}

# Define paths
$targetPath = Join-Path $scriptDir "run_wispr.ps1"
$startupFolder = [Environment]::GetFolderPath("Startup")
$shortcutName = "Tyni-Wispr Audio Transcription.lnk"
$shortcutPath = Join-Path $startupFolder $shortcutName

# Verify that run_wispr.ps1 exists
if (-not (Test-Path $targetPath)) {
    Write-Host "Error: run_wispr.ps1 not found at: $targetPath" -ForegroundColor Red
    Write-Host "Please ensure this script is in the same directory as run_wispr.ps1" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if shortcut already exists
if (Test-Path $shortcutPath) {
    Write-Host "A startup shortcut already exists at:" -ForegroundColor Yellow
    Write-Host "  $shortcutPath" -ForegroundColor Cyan
    $response = Read-Host "Do you want to replace it? (Y/N)"
    
    if ($response -ne 'Y' -and $response -ne 'y') {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 0
    }
    
    # Try to remove existing shortcut
    try {
        Remove-Item $shortcutPath -Force
        Write-Host "Existing shortcut removed." -ForegroundColor Green
    } catch {
        Write-Host "Error: Failed to remove existing shortcut: $_" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create the shortcut
try {
    Write-Host "`nCreating startup shortcut..." -ForegroundColor Cyan
    
    # Create WScript.Shell COM object
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    # Create the shortcut
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    
    # Set shortcut properties
    $pwshPath = Join-Path $env:ProgramFiles 'PowerShell/7/pwsh.exe'
    $shortcut.TargetPath = $pwshPath
    $shortcut.Arguments = '"' + $targetPath + '"'
    $shortcut.WorkingDirectory = $scriptDir
    $shortcut.Description = "GPU-accelerated Whisper audio transcription tool - Automatically transcribes audio from your microphone"
    $shortcut.IconLocation = "C:\Windows\System32\mmsys.cpl,0"  # Microphone icon
    
    # Save the shortcut
    $shortcut.Save()
    
    # Release COM object
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WScriptShell) | Out-Null
    
    Write-Host "`nSuccess! Startup shortcut created." -ForegroundColor Green
    Write-Host "`nShortcut details:" -ForegroundColor Cyan
    Write-Host "  Name: $shortcutName" -ForegroundColor White
    Write-Host "  Location: $startupFolder" -ForegroundColor White
    Write-Host "  Target: $targetPath" -ForegroundColor White
    Write-Host "  Working Directory: $scriptDir" -ForegroundColor White
    Write-Host "`nTyni-Wispr will now start automatically when Windows starts." -ForegroundColor Green
    Write-Host "To remove it, delete the shortcut from your startup folder or run this script again." -ForegroundColor Yellow
    
} catch {
    Write-Host "`nError: Failed to create shortcut: $_" -ForegroundColor Red
    Write-Host "Please ensure you have the necessary permissions." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Final message
Write-Host "`nPress Enter to exit..."
Read-Host