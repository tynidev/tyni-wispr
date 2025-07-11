"""Main entry point for Tyni-Wispr application."""

import time
import keyboard
import pyautogui
from enum import Enum
from threading import Lock
from .config import parse_arguments, DEFAULT_HOTKEY, DEFAULT_CANCEL_HOTKEY, DEFAULT_SAMPLERATE, DEFAULT_CHANNELS
from .models import load_enhancer_llm, load_whisper
from .audio import AudioRecorder
from .transcription import transcribe_audio
from .ui import RecordingOverlay
from .utils import log_performance, post_process_transcription

class RecordingState(Enum):
    """Enumeration for recording states."""
    IDLE = "idle"
    RECORDING = "recording"
    TRANSCRIBING = "transcribing"

class TyniWispr:
    """Main application class for Tyni-Wispr."""
    
    def __init__(self, args):
        self.args = args
        self.state = RecordingState.IDLE
        self.state_lock = Lock()
        
        # Initialize components
        self.enhancer = load_enhancer_llm(args)
        self.model, _ = load_whisper(args.model)
        self.audio_recorder = AudioRecorder(samplerate=DEFAULT_SAMPLERATE, channels=DEFAULT_CHANNELS)
        self.overlay = RecordingOverlay()
        
        # Key event handlers
        self.setup_key_handlers()
        
    def setup_key_handlers(self):
        """Set up keyboard event handlers."""
        keyboard.on_press_key(DEFAULT_HOTKEY, self._on_num_lock_press)
        keyboard.on_press_key(DEFAULT_CANCEL_HOTKEY, self._on_escape_press)
        
    def _on_num_lock_press(self, event):
        """Handle NUM Lock key press events."""
        with self.state_lock:
            if self.state == RecordingState.IDLE:
                self._start_recording()
            elif self.state == RecordingState.RECORDING:
                self._stop_recording_and_transcribe()
                
    def _on_escape_press(self, event):
        """Handle ESC key press events."""
        with self.state_lock:
            if self.state == RecordingState.RECORDING:
                self._cancel_recording()
                
    def _start_recording(self):
        """Start recording audio."""
        if not self.args.silent:
            print("🎙️  Recording...")
            
        self.state = RecordingState.RECORDING
        self.audio_recorder.start_recording()
        self.overlay.show(mode='recording')
        
    def _cancel_recording(self):
        """Cancel current recording."""
        if not self.args.silent:
            print("🚫 Recording canceled!")
            
        self.state = RecordingState.IDLE
        self.audio_recorder.stop_recording()
        self.overlay.hide()
        
    def _stop_recording_and_transcribe(self):
        """Stop recording and process transcription."""
        if not self.args.silent:
            print("🛑 Recording stopped. Processing...")
            
        self.state = RecordingState.TRANSCRIBING
        self.audio_recorder.stop_recording()
        
        # Process the audio in a separate method
        self._process_transcription()
        
    def _process_transcription(self):
        """Process the recorded audio and generate transcription."""
        # Show transcribing overlay
        self.overlay.show(mode='transcribing')
        
        # Process the audio
        audio_mono, audio_duration = self.audio_recorder.process_audio_buffer()
        
        # Early exit: No audio recorded
        if audio_mono is None:
            self.overlay.hide()
            if not self.args.silent:
                print("⚠️  No audio recorded!")
            self.state = RecordingState.IDLE
            return
        
        # Transcribe
        transcription_start_time = time.time()
        text = transcribe_audio(self.model, audio_mono)
        transcription_time = time.time() - transcription_start_time
        
        if not self.args.silent:
            print(f"📝 Transcription : {text} (⏱️ {transcription_time:.2f}s / {transcription_time*1000:.0f}ms)")

        # Early exit: No transcription result
        if not text:
            self.overlay.hide()
            self.state = RecordingState.IDLE
            return

        # Enhance the transcription with LLM if enabled
        enhancement_time = None
        if self.enhancer:
            enhancement_start_time = time.time()
            enhanced_text = self.enhancer.enhance(text)
            enhancement_time = time.time() - enhancement_start_time
            
            if not self.args.silent:
                print(f"🔍 LLM Enhanced  : {enhanced_text} (⏱️ {enhancement_time:.2f}s / {enhancement_time*1000:.0f}ms)")
            text = enhanced_text
        
        # Post-process the text
        post_process_start_time = time.time()
        text = post_process_transcription(text, self.args.corrections_config)
        post_process_time = time.time() - post_process_start_time
        
        if not self.args.silent:
            print(f"🔧 Post-processed: {text} (⏱️ {post_process_time:.2f}s / {post_process_time*1000:.0f}ms)")

        # Log performance if enabled
        if self.args.log_performance:
            log_performance(self.args.model, transcription_time, len(text), audio_duration, enhancement_time, post_process_time)

        # Hide transcribing overlay before typing
        self.overlay.hide()

        # Early exit: No text to type after processing
        if not text:
            self.state = RecordingState.IDLE
            return
            
        # Type the text
        pyautogui.write(text + ' ')
        
        # Return to idle state
        self.state = RecordingState.IDLE
        
    def run(self):
        """Main application loop."""
        # Start audio stream
        self.audio_recorder.start_stream()

        print("🎯 Ready! Press NUM Lock to start recording. Press NUM Lock again to stop & transcribe. Press ESC to cancel.")
        
        try:
            # Keep the application running and listening for key events
            keyboard.wait()  # This will wait indefinitely until interrupted
        except KeyboardInterrupt:
            print("\n👋 Exiting.")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources."""
        keyboard.unhook_all()
        self.overlay.hide()
        self.audio_recorder.stop_stream()

def main():
    """Main entry point for the Tyni-Wispr speech-to-text application.
    
    Initializes the Whisper model, sets up audio recording, and handles
    the toggle-based recording workflow for real-time transcription.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    print(f"🎤 Starting Tyni-Wispr with model: {args.model}")
    if args.log_performance:
        print("📊 Performance logging enabled - data will be saved to transcription_performance.csv")
    
    # Create and run the application
    app = TyniWispr(args)
    app.run()

if __name__ == "__main__":
    main()
