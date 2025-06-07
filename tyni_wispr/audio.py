"""Audio recording and processing functionality."""

import numpy as np
import sounddevice as sd

class AudioRecorder:
    """Handles audio recording and buffering."""
    
    def __init__(self, samplerate=16000, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.audio_buffer = []
        self.recording = False
        self.stream = None
        
    def start_stream(self):
        """Initialize and start the audio input stream."""
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype='int16',
            callback=self._audio_callback
        )
        self.stream.start()
        
    def stop_stream(self):
        """Stop and close the audio stream."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            
    def start_recording(self):
        """Start recording audio to buffer."""
        self.audio_buffer = []
        self.recording = True
        
    def stop_recording(self):
        """Stop recording and return the audio data."""
        self.recording = False
        return self.audio_buffer
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback function for audio stream."""
        if self.recording:
            self.audio_buffer.append(indata.copy())
            
    def process_audio_buffer(self):
        """Convert audio buffer to normalized float32 mono audio data.
        
        Returns:
            tuple: A tuple containing (audio_mono, audio_duration) where audio_mono is
                   normalized float32 audio data and audio_duration is the duration in seconds.
        """
        if not self.audio_buffer:
            return None, 0
            
        audio_np = np.concatenate(self.audio_buffer, axis=0)
        # Convert audio to float32 and normalize for direct transcription
        audio_float = audio_np.astype(np.float32) / 32768.0  # Convert int16 to float32
        audio_mono = audio_float.flatten()  # Ensure mono
        # Calculate audio duration
        audio_duration = len(audio_mono) / self.samplerate
        return audio_mono, audio_duration
