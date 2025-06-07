# Tyni-Wispr

🎤 **Real-time speech-to-text transcription using OpenAI's Whisper model**

Tyni-Wispr is a powerful, modular speech-to-text tool that converts your voice to text in real-time. Simply press and hold a hotkey to record, release to transcribe, and watch as your words are automatically typed into any application.

## ✨ Features

- 🎯 **Real-time speech-to-text** using OpenAI's Whisper
- ⚡ **Hotkey activation** (Right Shift) - press to record, release to transcribe
- 🤖 **LLM text enhancement** (optional) - improve grammar and punctuation with Ollama
- 🚀 **GPU acceleration** with CUDA support for faster transcription
- 📊 **Performance logging** to CSV for optimization
- 🔧 **Modular architecture** - easy to extend and customize
- 📦 **Easy installation** with multiple options
- 🖥️ **Cross-platform** Python package
- 🎮 **Windows startup integration** for background use

## 🚀 Quick Installation

### Option 1: Automatic Installation (Recommended)

**Windows with GPU (CUDA) support:**
```powershell
.\install_with_cuda.ps1
```

### Option 2: Manual Installation

**With GPU acceleration:**
```bash
pip install -e .
pip install --extra-index-url https://download.pytorch.org/whl/cu128 torch>=2.0.0 --force-reinstall
```

**CPU-only (no GPU required):**
```bash
pip install -e .
pip install torch --force-reinstall
```

### Option 3: Virtual Environment Installation (Recommended for isolation)

**Create and activate virtual environment:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install with GPU support
pip install -r requirements.txt
pip install -e .

# OR install CPU-only version
# pip install -e .
# pip install torch --force-reinstall
```

### Option 4: From Requirements (handles CUDA automatically)
```bash
pip install -r requirements.txt
pip install -e .
```

## 🎯 Quick Start

After installation, you can run Tyni-Wispr from anywhere:

```bash
tyni-wispr --help                    # Show all options
tyni-wispr                           # Start with default settings
tyni-wispr -m small.en -l            # Use small English model with logging
tyni-wispr --llm-enhance             # Enable LLM text enhancement
```

### Basic Usage:
1. **Run**: `tyni-wispr`
2. **Record**: Press and hold **Right Shift**
3. **Transcribe**: Release **Right Shift**
4. **Result**: Text automatically typed in active window!

## 🏗️ Project Structure

```
tyni-wispr/
├── tyni_wispr/              # Main package
│   ├── main.py              # Entry point and main application loop
│   ├── config.py            # Configuration and argument parsing
│   ├── audio.py             # Audio recording and processing
│   ├── transcription.py     # Whisper transcription logic
│   ├── enhancement.py       # LLM text enhancement (Ollama)
│   ├── models.py            # Model loading and management
│   ├── ui.py               # Recording overlay interface
│   └── utils.py            # Logging and utility functions
├── setup.py                # Smart installation with CUDA handling
├── requirements.txt        # Dependencies with CUDA support
├── install_with_cuda.ps1   # Automated installation scripts
├── install_with_cuda.bat   
└── INSTALL.md              # Detailed installation guide
```

## 🔧 Configuration Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--model` | `-m` | Whisper model size | `turbo` |
| `--log-performance` | `-l` | Enable CSV performance logging | `False` |
| `--silent` | `-s` | Suppress console output | `False` |
| `--llm-enhance` | `-e` | Enable LLM text enhancement | `False` |
| `--ollama-model` | | Ollama model for enhancement | `gemma3:12b` |
| `--ollama-url` | | Ollama server URL and port | `http://localhost:11434` |
| `--help` | `-h` | Show help message | |

## 🎮 Available Models

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | 39M | 10x faster | Basic | Quick notes, clear audio |
| `small.en` | 244M | 4x faster | Good | English-only content |
| `turbo` | Optimized | Fast | High | **Recommended for most users** |
| `medium` | 769M | 2x faster | Very High | Professional transcription |
| `large` | 1.5B | Baseline | Highest | Maximum accuracy needed |

## 🤖 LLM Enhancement Setup

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Start Ollama**: `ollama serve` (default: http://localhost:11434)
3. **Install a model**: `ollama pull gemma3:12b`
4. **Enable in Tyni-Wispr**: `tyni-wispr --llm-enhance`
5. **Custom server**: `tyni-wispr --llm-enhance --ollama-url http://your-server:port`

## 🔍 Troubleshooting

### GPU/CUDA Issues
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Install CPU-only version if GPU issues persist
pip install torch --force-reinstall --index-url https://download.pytorch.org/whl/cpu
```

### Audio Issues
- **No microphone detected**: Check Windows audio settings
- **Poor transcription**: Try a larger model (`-m medium` or `-m large`)
- **Background noise**: Use headset microphone for better results

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clean reinstall
pip uninstall tyni-wispr
pip install -e .
```

### LLM Enhancement Not Working
- Ensure Ollama is running: `ollama serve`
- Ensure Ollama is accessible via default url: `http://localhost:11434`
- Check model availability: `ollama list`
- Install required model: `ollama pull gemma3:12b`

## 📈 Performance Tips

- **GPU users**: Use CUDA installation for 3-10x faster transcription
- **CPU users**: Stick to `tiny` or `small` models
- **English-only**: Use `.en` model variants for better performance
- **Background use**: Enable `--silent` mode to reduce console output
- **Accuracy**: Use `--llm-enhance` for grammar and punctuation improvement

## 📊 Performance Logging

Enable performance logging to track transcription metrics:

```bash
tyni-wispr --log-performance
```

This creates `transcription_performance.csv` with timing and accuracy data.

## 🔗 Related Projects

- [OpenAI Whisper](https://github.com/openai/whisper) - The underlying transcription model
- [Ollama](https://ollama.ai) - Local LLM inference for text enhancement

## 📄 License

See [LICENSE](LICENSE) for details.

---

**Made with ❤️ for seamless voice-to-text workflow**
