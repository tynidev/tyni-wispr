#!/usr/bin/env pwsh
# Installation script for Tyni-Wispr with CUDA support

Write-Host "🚀 Installing Tyni-Wispr with CUDA Support" -ForegroundColor Green
Write-Host "=" * 50

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.7+ first." -ForegroundColor Red
    exit 1
}

# Install the package
Write-Host "📦 Installing Tyni-Wispr package..." -ForegroundColor Yellow
pip install -e .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Package installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Package installation failed" -ForegroundColor Red
    exit 1
}

# Install PyTorch with CUDA support
Write-Host "🔥 Installing PyTorch with CUDA support..." -ForegroundColor Yellow
pip install --extra-index-url https://download.pytorch.org/whl/cu128 torch>=2.0.0 --force-reinstall

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ PyTorch with CUDA installed successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️  CUDA installation failed, falling back to CPU version..." -ForegroundColor Yellow
    pip install torch --force-reinstall
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PyTorch CPU version installed" -ForegroundColor Green
    } else {
        Write-Host "❌ PyTorch installation failed" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host "=" * 50
Write-Host "📝 Quick Start:"
Write-Host "   tyni-wispr --help                    # Show help"
Write-Host "   tyni-wispr                           # Start with default settings"
Write-Host "   tyni-wispr -m small.en -l            # Use small English model with logging"
Write-Host "   tyni-wispr --llm-enhance             # Enable LLM text enhancement"
Write-Host ""
Write-Host "🎯 Usage:"
Write-Host "   1. Run: tyni-wispr"
Write-Host "   2. Press RIGHT SHIFT to start/stop recording"
Write-Host "   3. Text will be typed automatically!"
Write-Host "=" * 50
