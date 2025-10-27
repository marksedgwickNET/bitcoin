#!/usr/bin/env python3
"""
Audio to Light Visualizer
Real-time audio visualization using microphone input

Controls:
- Numbers 1-6: Switch between different visual effects
- ESC: Exit application
- Close window: Exit application

Effects:
1. Spectrum - Frequency spectrum bars
2. Circles - Concentric circles for bass/mid/treble
3. Bars - Simplified frequency bars
4. Wave - Waveform visualization
5. Strobe - Strobe light effect
6. Particles - Dynamic particle system
"""

import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from audio_processor import AudioProcessor
from light_effects import LightEffects


class AudioToLightApp:
    def __init__(self):
        self.audio_processor = None
        self.light_effects = None
        self.running = False
        self.main_thread = None
        
        # Create GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the control GUI"""
        self.root = tk.Tk()
        self.root.title("Audio to Light Visualizer - Controls")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio to Light Visualizer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Stopped")
        status_label = ttk.Label(main_frame, text="Status:")
        status_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.status_display = ttk.Label(main_frame, textvariable=self.status_var,
                                       foreground="red")
        self.status_display.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.start_button = ttk.Button(button_frame, text="Start Visualization",
                                      command=self.start_visualization)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Visualization",
                                     command=self.stop_visualization, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Effect selection
        effect_frame = ttk.LabelFrame(main_frame, text="Visual Effects", padding="10")
        effect_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.effect_var = tk.StringVar(value="spectrum")
        effects = [
            ("Spectrum", "spectrum"),
            ("Circles", "circles"),
            ("Bars", "bars"),
            ("Wave", "wave"),
            ("Strobe", "strobe"),
            ("Particles", "particles")
        ]
        
        for i, (text, value) in enumerate(effects):
            radio = ttk.Radiobutton(effect_frame, text=text, variable=self.effect_var,
                                   value=value, command=self.change_effect)
            radio.grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=5)
        
        # Audio info
        info_frame = ttk.LabelFrame(main_frame, text="Audio Information", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.volume_var = tk.StringVar(value="Volume: 0.0")
        self.bass_var = tk.StringVar(value="Bass: 0.0")
        self.mid_var = tk.StringVar(value="Mid: 0.0")
        self.treble_var = tk.StringVar(value="Treble: 0.0")
        
        ttk.Label(info_frame, textvariable=self.volume_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, textvariable=self.bass_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(info_frame, textvariable=self.mid_var).grid(row=2, column=0, sticky=tk.W)
        ttk.Label(info_frame, textvariable=self.treble_var).grid(row=3, column=0, sticky=tk.W)
        
        # Instructions
        instructions = """
Controls in Visualization Window:
• Press 1-6 to switch effects
• Press ESC to exit
• Close window to exit

Make sure your microphone is connected and working!
        """
        
        inst_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        inst_frame.grid(row=5, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        ttk.Label(inst_frame, text=instructions, justify=tk.LEFT).grid(row=0, column=0)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def start_visualization(self):
        """Start the audio visualization"""
        try:
            # Initialize audio processor
            self.audio_processor = AudioProcessor()
            self.audio_processor.start_recording()
            
            # Initialize light effects
            self.light_effects = LightEffects()
            
            # Update status
            self.status_var.set("Running")
            self.status_display.config(foreground="green")
            
            # Update button states
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start main loop in separate thread
            self.running = True
            self.main_thread = threading.Thread(target=self.main_loop)
            self.main_thread.daemon = True
            self.main_thread.start()
            
            # Start audio info update
            self.update_audio_info()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start visualization: {e}")
            self.stop_visualization()
    
    def stop_visualization(self):
        """Stop the audio visualization"""
        self.running = False
        
        if self.audio_processor:
            self.audio_processor.stop_recording()
            self.audio_processor = None
            
        if self.light_effects:
            self.light_effects.cleanup()
            self.light_effects = None
            
        # Update status
        self.status_var.set("Stopped")
        self.status_display.config(foreground="red")
        
        # Update button states
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        # Reset audio info
        self.volume_var.set("Volume: 0.0")
        self.bass_var.set("Bass: 0.0")
        self.mid_var.set("Mid: 0.0")
        self.treble_var.set("Treble: 0.0")
    
    def change_effect(self):
        """Change the visual effect"""
        if self.light_effects:
            self.light_effects.set_effect_mode(self.effect_var.get())
    
    def main_loop(self):
        """Main visualization loop"""
        clock = self.light_effects.clock
        
        while self.running and self.light_effects.running:
            # Handle pygame events
            if not self.light_effects.handle_events():
                self.running = False
                break
                
            # Get audio features
            audio_features = self.audio_processor.get_audio_features()
            
            # Update visual effects
            self.light_effects.update(audio_features)
            
            # Limit frame rate
            clock.tick(60)
        
        # Stop visualization when main loop ends
        self.root.after(0, self.stop_visualization)
    
    def update_audio_info(self):
        """Update audio information display"""
        if self.running and self.audio_processor:
            try:
                features = self.audio_processor.get_audio_features()
                
                self.volume_var.set(f"Volume: {features['volume']:.3f}")
                self.bass_var.set(f"Bass: {features['bass']:.3f}")
                self.mid_var.set(f"Mid: {features['mid']:.3f}")
                self.treble_var.set(f"Treble: {features['treble']:.3f}")
                
                # Schedule next update
                self.root.after(100, self.update_audio_info)
            except:
                pass  # Ignore errors during shutdown
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_visualization()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        print("Starting Audio to Light Visualizer...")
        print("Make sure your microphone is connected and working!")
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = AudioToLightApp()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())