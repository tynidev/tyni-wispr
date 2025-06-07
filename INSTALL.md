# Tyni-Wispr Installation Guide

## Quick Installation Options

### Option 1: Automatic Installation with CUDA Support (Recommended for GPU users)

**Windows PowerShell:**
```powershell
.\install_with_cuda.ps1
```

**Windows Command Prompt:**
```cmd
install_with_cuda.bat
```

### Option 2: Manual Installation with CUDA Support

```bash
# Install the package
pip install -e .

# Install PyTorch with CUDA support
pip install --extra-index-url https://download.pytorch.org/whl/cu128 torch>=2.0.0 --force-reinstall
```

### Option 3: CPU-Only Installation (No GPU acceleration)

```bash
# Install the package
pip install -e .

# Install CPU-only PyTorch
pip install torch --force-reinstall
```

### Option 4: Using pip with requirements.txt

```bash
# This will automatically handle CUDA installation
pip install -r requirements.txt
pip install -e .
```

## Verification

After installation, verify everything works:

```bash
# Show help (should work without errors)
tyni-wispr --help

# Test quick run (Ctrl+C to exit)
tyni-wispr -m tiny --silent
```

## Usage

Once installed, you can run Tyni-Wispr from anywhere:

```bash
tyni-wispr                           # Start with default settings
tyni-wispr -m small.en -l            # Use small English model with logging
tyni-wispr --llm-enhance             # Enable LLM text enhancement
```

## Troubleshooting

**CUDA Issues:**
- If you get CUDA errors, install CPU-only version: `pip install torch --force-reinstall`
- Check CUDA availability: `python -c "import torch; print(torch.cuda.is_available())"`

**Import Errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try reinstalling: `pip uninstall tyni-wispr && pip install -e .`
