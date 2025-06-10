"""Recording overlay UI components."""

import tkinter as tk
from tkinter import ttk
import threading
import time

class RecordingOverlay:
    """A transparent overlay window that displays recording and transcribing indicators."""
    
    def __init__(self):
        self.root = None
        self.is_showing = False
        self.thread = None
        self.current_mode = None
        
    def show(self, mode='recording'):
        """Show the overlay in a separate thread.
        
        Args:
            mode (str): Either 'recording' or 'transcribing'
        """
        if self.is_showing:  # If already showing or in the process of showing
            return
        
        self.is_showing = True
        self.current_mode = mode
        # Start the overlay thread
        # Daemon thread to ensure it exits when the main program does
        self.thread = threading.Thread(target=self._create_overlay, daemon=True)
        self.thread.start()
    
    def hide(self):
        """Signal the recording overlay to hide."""
        if self.is_showing:
            self.is_showing = False  # stop the overlay loop

            # Wait for the thread to finish cleaning up using a while loop
            while self.thread and self.thread.is_alive():
                time.sleep(0.01)  # Small delay to avoid busy waiting
    
    def _create_overlay(self):
        """Create and display the overlay window. This runs in a separate thread."""
        try:            
            self.root = tk.Tk()
            self.root.title("Recording")
            
            self.root.attributes('-alpha', 0.9)
            self.root.attributes('-topmost', True)
            self.root.overrideredirect(True)
            
            screen_width = self.root.winfo_screenwidth()
            
            frame = ttk.Frame(self.root, style='Recording.TFrame')
            frame.pack(fill='both', expand=True)
            
            # Configure display based on mode
            if self.current_mode == 'transcribing':
                # Transcribing mode: steady blue display
                flash_on_color = 'white'
                flash_off_color = '#0066CC'  # Blue background
                flash_interval = 0.5  # Faster update for steady display
                is_text_visible = True
                text_content = "TRANSCRIBING"
                should_flash = True
            else:
                # Recording mode: flashing red display
                flash_on_color = 'white'
                flash_off_color = '#FF0000'  # Red background
                flash_interval = 0.5  # seconds for each state (on/off)
                is_text_visible = True
                text_content = "REC"
                should_flash = True
            
            scale = 2

            style = ttk.Style()
            style.configure('Recording.TFrame', background=flash_off_color)
            style.configure('Recording.TLabel', background=flash_off_color, foreground=flash_on_color, font=('Arial Black', int(12 * scale), 'bold'))
            
            label = ttk.Label(frame, text=text_content, style='Recording.TLabel')
            label.pack(expand=True, padx=int(10 * scale), pady=int(8 * scale))
            
            # Position in top right corner
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            x_position = screen_width - window_width - 20
            y_position = 20
            self.root.geometry(f"+{x_position}+{y_position}")
            while self.is_showing:
                if self.root:
                    # Handle flashing for recording mode, steady display for transcribing
                    if should_flash:
                        # Flash the text by toggling visibility
                        if is_text_visible:
                            style.configure('Recording.TLabel', foreground=flash_on_color)
                            style.configure('Recording.TLabel', background=flash_off_color)
                            style.configure('Recording.TFrame', background=flash_off_color)
                        else:
                            style.configure('Recording.TLabel', foreground=flash_off_color)
                            style.configure('Recording.TLabel', background=flash_on_color) 
                            style.configure('Recording.TFrame', background=flash_on_color)
                        is_text_visible = not is_text_visible  # Toggle visibility for next flash
                    else:
                        # Steady display for transcribing mode
                        style.configure('Recording.TLabel', foreground=flash_on_color)
                        style.configure('Recording.TLabel', background=flash_off_color)
                        style.configure('Recording.TFrame', background=flash_off_color)
                    
                    self.root.update()  # Refresh the Tkinter window
                time.sleep(flash_interval)  # Control the flashing speed

        except Exception:
            pass  # Silently ignore, ensure finally block runs for cleanup
        finally:
            # Cleanup: hide and destroy the overlay window
            if self.root:
                try:
                    self.root.destroy()  # Destroy the Tkinter window from its own thread
                except tk.TclError:
                    pass  # Window might already be destroyed

            # Reset the root to None for future use
            self.root = None
            
            # Ensure the thread is marked as finished
            self.is_showing = False
