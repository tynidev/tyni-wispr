"""Main entry point for Tyni-Wispr application."""

import warnings
import time
import keyboard
import pyautogui
from .config import parse_arguments, DEFAULT_HOTKEY, DEFAULT_SAMPLERATE, DEFAULT_CHANNELS
from .models import load_model
from .audio import AudioRecorder
from .transcription import transcribe_audio
from .enhancement import LLMEnhancer
from .ui import RecordingOverlay
from .utils import log_performance

warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

def main():
    """Main entry point for the Tyni-Wispr speech-to-text application.
    
    Initializes the Whisper model, sets up audio recording, and handles
    the hotkey-based recording workflow for real-time transcription.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    print(f"🎤 Starting Tyni-Wispr with model: {args.model}")
    if args.log_performance:
        print("📊 Performance logging enabled - data will be saved to transcription_performance.csv")
    
    # Initialize LLM enhancer if enabled
    enhancer = None
    if args.llm_enhance:
        enhancer = LLMEnhancer(model=args.ollama_model)
        if not enhancer.check_availability():
            print("⚠️  LLM enhancement disabled - Ollama not available")
            enhancer = None

    # Load Whisper model
    model, device = load_model(args.model)

    print("🎯 Ready! Hold the hotkey to record.")

    # Initialize components
    audio_recorder = AudioRecorder(samplerate=DEFAULT_SAMPLERATE, channels=DEFAULT_CHANNELS)
    overlay = RecordingOverlay()
    
    # Start audio stream
    audio_recorder.start_stream()

    try:
        while True:
            keyboard.wait(DEFAULT_HOTKEY)
            if not args.silent:
                print("🎙️  Recording...")
                
            audio_recorder.start_recording()
            overlay.show()
            
            keyboard.wait(DEFAULT_HOTKEY)
            audio_recorder.stop_recording()
            overlay.hide()
            
            if not args.silent:
                print("🛑 Recording stopped. Processing...")

            # Process the audio
            audio_mono, audio_duration = audio_recorder.process_audio_buffer()
            
            if audio_mono is not None:
                # Transcribe
                transcription_start_time = time.time()
                text = transcribe_audio(model, audio_mono)
                transcription_time = time.time() - transcription_start_time
                
                if not args.silent:
                    print(f"📝 Transcription: {text} (⏱️ {transcription_time:.2f}s / {transcription_time*1000:.0f}ms)")

                # Enhance with LLM if available
                enhancement_time = None
                if enhancer and text:
                    enhancement_start_time = time.time()
                    enhanced_text = enhancer.enhance(text)
                    enhancement_time = time.time() - enhancement_start_time
                    
                    if not args.silent:
                        print(f"🔍 LLM Enhanced: {enhanced_text} (⏱️ {enhancement_time:.2f}s / {enhancement_time*1000:.0f}ms)")
                    text = enhanced_text

                # Log performance if enabled
                if args.log_performance:
                    log_performance(args.model, transcription_time, len(text), audio_duration, enhancement_time)

                # Type the text
                if text:
                    pyautogui.write(text + ' ')
            else:
                print("⚠️  No audio recorded!")

    except KeyboardInterrupt:
        print("\n👋 Exiting.")
    finally:
        overlay.hide()
        audio_recorder.stop_stream()

if __name__ == "__main__":
    main()
