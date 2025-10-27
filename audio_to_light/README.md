# Audio to Light Visualizer

A real-time audio visualization system that captures sound from your microphone and converts it into dynamic light effects.

## Features

- **Real-time Audio Processing**: Captures microphone input and analyzes frequency spectrum
- **Multiple Visual Effects**: 6 different visualization modes
- **Frequency Band Analysis**: Separates bass, mid, and treble frequencies
- **Interactive Controls**: GUI control panel and keyboard shortcuts
- **Smooth Animations**: Fluid visual transitions and particle effects

## Visual Effects

1. **Spectrum** - Real-time frequency spectrum display with color-coded bars
2. **Circles** - Concentric circles responding to bass, mid, and treble frequencies
3. **Bars** - Simplified frequency bars with rainbow colors
4. **Wave** - Waveform visualization with gradient colors
5. **Strobe** - Strobe light effect triggered by loud sounds
6. **Particles** - Dynamic particle system responding to different frequency bands

## Requirements

- Python 3.7+
- Microphone (built-in or external)
- Audio drivers compatible with PyAudio

## Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For Linux users, you may need to install additional packages:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-pyaudio portaudio19-dev

   # Fedora
   sudo dnf install python3-pyaudio portaudio-devel
   ```

4. **For macOS users:**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Control Panel:**
   - Click "Start Visualization" to begin
   - Select different effects using radio buttons
   - Monitor audio levels in real-time
   - Click "Stop Visualization" to end

3. **Keyboard Controls (in visualization window):**
   - `1-6`: Switch between different effects
   - `ESC`: Exit application
   - Close window: Exit application

## Troubleshooting

### Audio Issues
- **No microphone detected**: Check system audio settings and ensure microphone is enabled
- **Permission denied**: Grant microphone permissions to the application
- **Low audio levels**: Adjust microphone gain in system settings

### Installation Issues
- **PyAudio installation fails**: Install portaudio development headers first
- **Pygame display issues**: Ensure graphics drivers are properly installed
- **Module not found**: Verify all dependencies are installed in the correct Python environment

### Performance Issues
- **Choppy visualization**: Close other audio applications and reduce system load
- **High CPU usage**: Lower the frame rate or reduce particle count
- **Delayed response**: Check audio buffer settings and system latency

## Technical Details

### Audio Processing
- **Sample Rate**: 44.1 kHz
- **Chunk Size**: 1024 samples
- **FFT Analysis**: Real-time frequency domain analysis
- **Frequency Bands**:
  - Bass: 20-250 Hz
  - Mid: 250-4000 Hz
  - Treble: 4000-20000 Hz

### Visual Rendering
- **Framework**: Pygame for real-time graphics
- **Frame Rate**: 60 FPS target
- **Color System**: HSV color space for smooth transitions
- **Smoothing**: Exponential moving average for fluid animations

## File Structure

```
audio_to_light/
├── main.py              # Main application entry point
├── audio_processor.py   # Audio capture and analysis
├── light_effects.py     # Visual effects rendering
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## Customization

### Adding New Effects
1. Add a new method to the `LightEffects` class
2. Update the `update()` method to include your effect
3. Add the effect to the GUI controls

### Adjusting Audio Sensitivity
Modify the frequency band ranges in `audio_processor.py`:
```python
self.bass_range = (20, 250)     # Bass frequencies
self.mid_range = (250, 4000)    # Mid frequencies  
self.treble_range = (4000, 20000)  # Treble frequencies
```

### Visual Customization
- Adjust colors by modifying HSV values in `light_effects.py`
- Change particle behavior in the `_update_particles()` method
- Modify smoothing factors for different animation speeds

## Contributing

Feel free to contribute by:
- Adding new visual effects
- Improving audio processing algorithms
- Enhancing the user interface
- Optimizing performance
- Fixing bugs

## License

This project is open source. Feel free to use, modify, and distribute.

## Credits

Built using:
- **NumPy** - Numerical computing
- **PyAudio** - Audio I/O
- **Pygame** - Graphics and visualization
- **SciPy** - Signal processing
- **Tkinter** - GUI controls