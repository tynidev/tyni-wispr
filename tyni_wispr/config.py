"""Configuration and command-line argument parsing for Tyni-Wispr."""

import argparse
import sys

# Default configuration
DEFAULT_MODEL = 'turbo'
DEFAULT_OLLAMA_MODEL = 'gemma3:12b'
DEFAULT_OLLAMA_URL = 'http://localhost:11434'
DEFAULT_HOTKEY = 'right shift'
DEFAULT_CANCEL_HOTKEY = 'escape'
DEFAULT_SAMPLERATE = 16000
DEFAULT_CHANNELS = 1

def parse_arguments():
    """Parse command-line arguments for the application.
    
    Returns:
        argparse.Namespace: Parsed arguments containing model, log_performance, silent, 
                           llm_enhance, ollama_model, ollama_url, and help flags.
    """
    parser = argparse.ArgumentParser(
        description="Real-time speech-to-text using Whisper",
        add_help=False
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        default=DEFAULT_MODEL,
        help=f'Whisper model to use (default: {DEFAULT_MODEL})'
    )
    
    parser.add_argument(
        '--log-performance', '-l',
        action='store_true',
        help='Enable performance logging to CSV file'
    )
    
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Show help message and exit'
    )
    parser.add_argument(
        '--silent', '-s',
        action='store_true',
        help='Suppress startup and completion log messages'
    )

    # Create mutually exclusive group for LLM enhancement options
    llm_group = parser.add_mutually_exclusive_group()
    
    # Ollama LLM enhancement options
    llm_group.add_argument(
        '--llm-enhance-ollama', '-e',
        action='store_true',
        help='Enable LLM text enhancement via Ollama'
    )
    parser.add_argument(
        '--ollama-model',
        type=str,
        default=DEFAULT_OLLAMA_MODEL,
        help=f'Ollama model to use for text enhancement (default: {DEFAULT_OLLAMA_MODEL})'
    )
    parser.add_argument(
        '--ollama-url',
        type=str,
        default=DEFAULT_OLLAMA_URL,
        help=f'Ollama server URL and port (default: {DEFAULT_OLLAMA_URL})'
    )
    
    # Azure OpenAI LLM enhancement options
    llm_group.add_argument(
        '--llm-enhance-azure-openai', '-a',
        action='store_true',
        help='Enable LLM text enhancement via Azure OpenAI'
    )

    parser.add_argument(
        '--corrections-config',
        type=str,
        default='corrections.json',
        help='Path to JSON file containing name corrections (default: corrections.json)'
    )
    
    args = parser.parse_args()
    
    if args.help:
        from .utils import show_help
        show_help()
        sys.exit(0)
    
    return args
