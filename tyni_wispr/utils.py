"""Utility functions for logging, text processing, and help display."""

import csv
import os
from datetime import datetime

def log_performance(model_name, transcription_time, text_length, audio_duration, enhancement_time=None):
    """Log performance metrics to a CSV file.
    
    Args:
        model_name (str): Name of the Whisper model used.
        transcription_time (float): Time taken to transcribe in seconds.
        text_length (int): Length of the transcribed text in characters.
        audio_duration (float): Duration of the audio in seconds.
        enhancement_time (float, optional): Time taken for LLM enhancement in seconds.
    """
    log_file = "transcription_performance.csv"
    file_exists = os.path.exists(log_file)
    
    with open(log_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'model', 'transcription_time_ms', 'text_length', 'audio_duration_ms', 'time_per_char_ms', 'realtime_factor', 'enhancement_time_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        time_per_char = transcription_time / text_length if text_length > 0 else 0
        realtime_factor = transcription_time / audio_duration if audio_duration > 0 else 0
        
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'transcription_time_ms': round(transcription_time * 1000, 2),
            'text_length': text_length,
            'audio_duration_ms': round(audio_duration * 1000, 2),
            'time_per_char_ms': round(time_per_char * 1000, 4),
            'realtime_factor': round(realtime_factor, 3),
            'enhancement_time_ms': round(enhancement_time * 1000, 2) if enhancement_time is not None else 'None'
        })

def post_process_transcription(text):
    """Post-process transcribed text by cleaning and formatting it.
    
    Args:
        text (str): Raw transcribed text from Whisper.
        
    Returns:
        str: Cleaned and formatted text, or empty string if no valid text.
    """
    # Strip whitespace
    text = text.strip()
    
    # Return empty string if no text
    if not text:
        return ""
    
    # Capitalize the first letter
    text = text[0].upper() + text[1:]
    
    return text

def show_help():
    """Display help information about available Whisper models and usage."""
    help_text = """
🎤 TYNI-WISPR: Real-time Speech-to-Text using Whisper
=====================================================

USAGE:
    python tyni-wispr.py [OPTIONS]

ARGUMENTS:
    --model, -m              Whisper model to use (default: turbo)
    --log-performance, -l    Enable performance logging to CSV file
    --silent, -s             Suppress startup and completion log messages
    --llm-enhance, -e        Enable LLM text enhancement via Ollama
    --ollama-model           Ollama model to use for enhancement (default: gemma3:12b)
    --ollama-url             Ollama server URL and port (default: http://localhost:11434)
    --help, -h               Show this help message and exit

HOW TO USE:
    1. Run the script: python tyni-wispr.py
    2. Press and hold the right shift key to start recording
    3. Release the right shift key to stop recording
    4. Audio is transcribed using Whisper model
    5. Text is optionally enhanced with LLM (if --llm-enhance is enabled)
    6. Final text is automatically typed in the active window

WORKFLOW:
    Recording → Whisper Transcription → [LLM Enhancement] → Text Output

AVAILABLE WHISPER MODELS:
==========================

🏃 TINY MODELS (39M parameters, ~150MB)
    • tiny     - Multilingual, fastest speed (10x vs large), lowest accuracy
    • tiny.en  - English-only variant, optimized for English content
    Best for: Quick transcriptions, limited resources, clear audio with minimal noise

⚡ BASE MODELS (74M parameters, ~300MB) 
    • base     - Multilingual, good balance for limited resources (7x vs large)
    • base.en  - English-only variant, better performance on English
    Best for: General purpose transcription with reasonable accuracy when resources are limited

🚀 SMALL MODELS (244M parameters, ~1GB)
    • small    - Multilingual, recommended for most use cases (4x vs large)
    • small.en - English-only variant, more efficient for English content
    Best for: Daily transcription needs with good accuracy and reasonable speed

🎯 MEDIUM MODELS (769M parameters, ~3GB)
    • medium   - Multilingual, high accuracy (2x vs large)
    • medium.en- English-only variant, optimized for English
    Best for: High-quality transcriptions where accuracy is important

🔥 LARGE MODELS (1.5B parameters, ~6GB)
    • large-v1 - Original large model
    • large-v2 - Improved large model  
    • large-v3 - Latest large model with best accuracy
    • large    - Alias for latest large model
    Best for: Professional transcription where maximum accuracy is essential

⚡ ADVANCED MODELS
    • turbo    - Optimized for speed while maintaining accuracy (RECOMMENDED)

SELECTION TIPS:
===============
    • For English-only: Use .en variants for better performance and efficiency
    • For multilingual: Use standard models (support 100+ languages)
    • CPU-only systems: Stick to tiny/base models
    • Consumer GPUs: small/medium models work well
    • High-end GPUs: can efficiently run large models
    • Clear audio: Smaller models may be sufficient
    • Challenging audio (noise/accents): Use larger models

EXAMPLES:
=========
    python tyni-wispr.py                         # Use default turbo model
    python tyni-wispr.py --model small.en        # Use small English-only model
    python tyni-wispr.py -m tiny                 # Use tiny multilingual model
    python tyni-wispr.py --log-performance       # Enable performance logging
    python tyni-wispr.py -m turbo -l             # Use turbo model with logging
    python tyni-wispr.py --llm-enhance           # Enable LLM text enhancement    python tyni-wispr.py -e --ollama-model llama3:8b  # Use different LLM model
    python tyni-wispr.py --ollama-url http://192.168.1.100:11434  # Use remote Ollama server
    python tyni-wispr.py -e --ollama-url http://localhost:8080 --ollama-model llama3:8b  # Custom URL and model
    python tyni-wispr.py -m small.en -l -e -s    # Compact mode with all features
    python tyni-wispr.py --silent                # Suppress console output
    python tyni-wispr.py --help                  # Show this help

LLM ENHANCEMENT:
================
    • Requires Ollama running locally (default: http://localhost:11434) or remotely
    • Use --ollama-url to specify custom Ollama server URL and port
    • Improves punctuation, grammar, and text clarity
    • Adds processing time but enhances accuracy
    • Use --ollama-model to specify different models
    • Install Ollama models with: ollama pull MODEL_NAME

REQUIREMENTS:
=============
    • Python 3.7+
    • PyTorch with CUDA support (optional, for GPU acceleration)
    • Microphone access
    • Required packages: whisper, torch, sounddevice, numpy, pyautogui, keyboard, requests
    • Ollama (optional, for LLM text enhancement)
"""
    print(help_text)
