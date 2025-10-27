#!/usr/bin/env python3
"""
Audio to Light Visualizer - Demo Mode
Simulates audio input for demonstration purposes
"""

import sys
import time
import math
import numpy as np
import threading
from light_effects import LightEffects

class SimulatedAudioProcessor:
    """Simulates audio processing with generated waveforms"""
    
    def __init__(self):
        self.running = False
        self.time = 0
        self.volume = 0.0
        self.bass_level = 0.0
        self.mid_level = 0.0
        self.treble_level = 0.0
        self.frequency_data = np.zeros(512)
        
    def start_recording(self):
        """Start simulated audio processing"""
        self.running = True
        self.thread = threading.Thread(target=self._simulate_audio)
        self.thread.daemon = True
        self.thread.start()
        print("Demo audio simulation started")
        
    def stop_recording(self):
        """Stop simulated audio processing"""
        self.running = False
        
    def _simulate_audio(self):
        """Generate simulated audio features"""
        while self.running:
            self.time += 0.05
            
            # Simulate dynamic audio with different patterns
            bass_freq = 0.5 + 0.3 * math.sin(self.time * 0.8)
            mid_freq = 0.4 + 0.4 * math.sin(self.time * 1.2)  
            treble_freq = 0.3 + 0.5 * math.sin(self.time * 1.8)
            
            # Add some randomness
            bass_noise = 0.1 * (np.random.random() - 0.5)
            mid_noise = 0.1 * (np.random.random() - 0.5)
            treble_noise = 0.1 * (np.random.random() - 0.5)
            
            self.bass_level = max(0, bass_freq + bass_noise)
            self.mid_level = max(0, mid_freq + mid_noise)
            self.treble_level = max(0, treble_freq + treble_noise)
            
            # Overall volume
            self.volume = (self.bass_level + self.mid_level + self.treble_level) / 3
            
            # Generate frequency spectrum
            for i in range(len(self.frequency_data)):
                freq_ratio = i / len(self.frequency_data)
                if freq_ratio < 0.2:  # Bass region
                    self.frequency_data[i] = self.bass_level * (1 - freq_ratio * 2)
                elif freq_ratio < 0.6:  # Mid region  
                    self.frequency_data[i] = self.mid_level * (1 - abs(freq_ratio - 0.4) * 2)
                else:  # Treble region
                    self.frequency_data[i] = self.treble_level * (freq_ratio - 0.6) * 2
                    
                # Add some noise
                self.frequency_data[i] += 0.05 * (np.random.random() - 0.5)
                self.frequency_data[i] = max(0, min(1, self.frequency_data[i]))
            
            time.sleep(0.05)
    
    def get_audio_features(self):
        """Get current simulated audio features"""
        return {
            'volume': self.volume,
            'bass': self.bass_level,
            'mid': self.mid_level,
            'treble': self.treble_level,
            'frequency_data': self.frequency_data.copy(),
            'frequency_bins': np.linspace(0, 22050, len(self.frequency_data))
        }

def main():
    """Main demo function"""
    print("Audio to Light Visualizer - Demo Mode")
    print("Simulating audio input for demonstration...")
    print("Press keys in the visualization window:")
    print("  1-6: Switch between effects")
    print("  ESC: Exit")
    print("=" * 50)
    
    try:
        # Initialize components
        audio_processor = SimulatedAudioProcessor()
        light_effects = LightEffects(800, 600)
        
        # Start simulation
        audio_processor.start_recording()
        
        # Set initial effect
        effect_names = ["spectrum", "circles", "bars", "wave", "strobe", "particles"]
        current_effect = 0
        light_effects.set_effect_mode(effect_names[current_effect])
        
        print(f"Starting with '{effect_names[current_effect]}' effect")
        
        clock = light_effects.clock
        frame_count = 0
        start_time = time.time()
        
        # Main loop
        while light_effects.running:
            # Handle events
            if not light_effects.handle_events():
                break
            
            # Get simulated audio features
            audio_features = audio_processor.get_audio_features()
            
            # Update visual effects
            light_effects.update(audio_features)
            
            # Auto-switch effects every 10 seconds for demo
            if frame_count % 600 == 0 and frame_count > 0:  # 10 seconds at 60fps
                current_effect = (current_effect + 1) % len(effect_names)
                light_effects.set_effect_mode(effect_names[current_effect])
                print(f"Auto-switched to '{effect_names[current_effect]}' effect")
            
            # Display info every 3 seconds
            if frame_count % 180 == 0:
                elapsed = time.time() - start_time
                fps = frame_count / elapsed if elapsed > 0 else 0
                print(f"Demo running: {elapsed:.1f}s, FPS: {fps:.1f}, "
                      f"Volume: {audio_features['volume']:.2f}, "
                      f"Effect: {effect_names[current_effect]}")
            
            frame_count += 1
            clock.tick(60)  # 60 FPS
        
        # Cleanup
        audio_processor.stop_recording()
        light_effects.cleanup()
        
        print("\nDemo completed!")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())