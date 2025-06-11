"""Main entry point for Tyni-Wispr application."""

import time
import keyboard
import pyautogui
from .config import parse_arguments, DEFAULT_HOTKEY, DEFAULT_CANCEL_HOTKEY, DEFAULT_SAMPLERATE, DEFAULT_CHANNELS
from .models import load_enhancer_llm, load_whisper
from .audio import AudioRecorder
from .transcription import transcribe_audio
from .ui import RecordingOverlay
from .utils import log_performance, post_process_transcription

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
    enhancer = load_enhancer_llm(args)

    # Initialize Whisper model
    model, _ = load_whisper(args.model)

    # Initialize audio recorder
    audio_recorder = AudioRecorder(samplerate=DEFAULT_SAMPLERATE, channels=DEFAULT_CHANNELS)

    # Initialize recording overlay
    overlay = RecordingOverlay()
    
    # Start audio stream
    audio_recorder.start_stream()

    print("🎯 Ready! Hold the hotkey to record. Press Escape to cancel recording.")
    try:
        # --- Main Loop ---
        # Wait for hotkey. Record audio. On release/cancel:
        #  - Transcribe speech
        #  - Enhance with LLM
        #  - Post-process text
        #  - Log performance
        #  - Type result into active window
        # Repeat until interrupted.
        while True:            
            keyboard.wait(DEFAULT_HOTKEY)
            if not args.silent:
                print("🎙️  Recording...")
                
            # Record audio
            audio_recorder.start_recording()
            overlay.show(mode='recording')
            
            # Wait for hotkey (Stop/Cancel)
            recording_canceled = False
            while True:
                if keyboard.is_pressed(DEFAULT_CANCEL_HOTKEY):
                    recording_canceled = True
                    if not args.silent:
                        print("🚫 Recording canceled!")
                    break
                elif not keyboard.is_pressed(DEFAULT_HOTKEY):
                    # Hotkey was released, stop recording normally
                    break
                time.sleep(0.01)  # Small delay to prevent high CPU usage

            # Stop recording (Cancel was pressed or hotkey released)
            audio_recorder.stop_recording()
            overlay.hide()
            
            # If recording was canceled, skip processing and go back to waiting
            if recording_canceled:
                continue
            
            if not args.silent:
                print("🛑 Recording stopped. Processing...")

            # Transcription
            overlay.show(mode='transcribing')

            # Process the audio
            audio_mono, audio_duration = audio_recorder.process_audio_buffer()
            
            # Early exit: No audio recorded
            if audio_mono is None:
                overlay.hide()
                print("⚠️  No audio recorded!")
                continue
            
            # Transcribe
            transcription_start_time = time.time()
            text = transcribe_audio(model, audio_mono)
            transcription_time = time.time() - transcription_start_time
            
            if not args.silent:
                print(f"📝 Transcription : {text} (⏱️ {transcription_time:.2f}s / {transcription_time*1000:.0f}ms)")

            # Early exit: No transcription result
            if not text:
                overlay.hide()
                continue

            # Enhance the transcription with LLM if enabled
            enhancement_time = None
            if enhancer:
                enhancement_start_time = time.time()
                enhanced_text = enhancer.enhance(text)
                enhancement_time = time.time() - enhancement_start_time
                
                if not args.silent:
                    print(f"🔍 LLM Enhanced  : {enhanced_text} (⏱️ {enhancement_time:.2f}s / {enhancement_time*1000:.0f}ms)")
                text = enhanced_text
            
            # Post-process the text
            post_process_start_time = time.time()
            text = post_process_transcription(text, args.corrections_config)
            post_process_time = time.time() - post_process_start_time
            
            if not args.silent:
                print(f"🔧 Post-processed: {text} (⏱️ {post_process_time:.2f}s / {post_process_time*1000:.0f}ms)")

            # Log performance if enabled
            if args.log_performance:
                log_performance(args.model, transcription_time, len(text), audio_duration, enhancement_time, post_process_time)

            # Hide transcribing overlay before typing
            overlay.hide()

            # Early exit: No text to type after processing
            if not text:
                continue
                
            # Type the text
            pyautogui.write(text + ' ')

    except KeyboardInterrupt:
        print("\n👋 Exiting.")
    finally:
        overlay.hide()
        audio_recorder.stop_stream()

if __name__ == "__main__":
    main()
