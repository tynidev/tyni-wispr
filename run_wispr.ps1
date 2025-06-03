# Run Tyni-Wispr Script
# This script activates the Python virtual environment and runs the Tyni-Wispr audio transcription tool
# with the turbo model and performance logging enabled

# Get the script's directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($scriptDir)) {
    $scriptDir = Get-Location
}

# Define paths
$venvPath = Join-Path $scriptDir "venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
$pythonScript = Join-Path $scriptDir "tyni-wispr.py"

# Check if virtual environment exists
if (-not (Test-Path $venvPath)) {
    Write-Host "Error: Virtual environment not found at: $venvPath" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Cyan
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if the Python script exists
if (-not (Test-Path $pythonScript)) {
    Write-Host "Error: Python script not found at: $pythonScript" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Display startup information
Write-Host "🎤 Starting Tyni-Wispr Audio Transcription Tool" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Model: turbo (optimized for speed and accuracy)" -ForegroundColor White
Write-Host "Performance Logging: Enabled" -ForegroundColor White
Write-Host "Virtual Environment: $venvPath" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan

try {
    # Change to script directory
    Set-Location $scriptDir
    
    # Activate virtual environment and run the Python script
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Cyan
    
    # Use & operator to run the activation script in the current scope
    & $activateScript
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Virtual environment activated successfully" -ForegroundColor Green
        Write-Host "🚀 Starting Tyni-Wispr with turbo model in silent mode..." -ForegroundColor Cyan
        
        # Run the Python script with turbo model and performance logging
        python $pythonScript --model turbo --silent
    } else {
        Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
} catch {
    Write-Host "❌ Error occurred: $_" -ForegroundColor Red
    Write-Host "Please ensure:" -ForegroundColor Yellow
    Write-Host "  1. Python is installed and in PATH" -ForegroundColor White
    Write-Host "  2. Virtual environment is properly set up" -ForegroundColor White
    Write-Host "  3. All dependencies are installed (pip install -r requirements.txt)" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
} finally {
    # Return to original directory if needed
    Write-Host "`n👋 Tyni-Wispr session ended." -ForegroundColor Yellow
}
