import numpy as np
import pyaudio
import threading
import time
from scipy.fft import fft, fftfreq


class AudioProcessor:
    def __init__(self, sample_rate=44100, chunk_size=1024, channels=1):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.format = pyaudio.paFloat32
        
        # Audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        
        # Audio data buffers
        self.audio_data = np.zeros(chunk_size)
        self.frequency_data = np.zeros(chunk_size // 2)
        self.frequency_bins = fftfreq(chunk_size, 1/sample_rate)[:chunk_size//2]
        
        # Threading
        self.lock = threading.Lock()
        self.thread = None
        
        # Audio analysis parameters
        self.volume = 0.0
        self.bass_level = 0.0
        self.mid_level = 0.0
        self.treble_level = 0.0
        
        # Frequency band ranges (Hz)
        self.bass_range = (20, 250)
        self.mid_range = (250, 4000)
        self.treble_range = (4000, 20000)
    
    def start_recording(self):
        """Start audio recording and processing"""
        if self.is_recording:
            return
            
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.is_recording = True
            self.stream.start_stream()
            
            # Start processing thread
            self.thread = threading.Thread(target=self._process_audio)
            self.thread.daemon = True
            self.thread.start()
            
            print("Audio recording started")
            
        except Exception as e:
            print(f"Error starting audio recording: {e}")
    
    def stop_recording(self):
        """Stop audio recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        if self.thread:
            self.thread.join(timeout=1.0)
            
        print("Audio recording stopped")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback function for audio stream"""
        audio_array = np.frombuffer(in_data, dtype=np.float32)
        
        with self.lock:
            self.audio_data = audio_array.copy()
            
        return (None, pyaudio.paContinue)
    
    def _process_audio(self):
        """Process audio data in separate thread"""
        while self.is_recording:
            with self.lock:
                data = self.audio_data.copy()
            
            # Calculate volume (RMS)
            self.volume = np.sqrt(np.mean(data**2))
            
            # Apply window function for better frequency analysis
            windowed_data = data * np.hanning(len(data))
            
            # Compute FFT
            fft_data = fft(windowed_data)
            magnitude = np.abs(fft_data[:len(fft_data)//2])
            
            # Normalize magnitude
            if np.max(magnitude) > 0:
                magnitude = magnitude / np.max(magnitude)
            
            self.frequency_data = magnitude
            
            # Calculate frequency band levels
            self._calculate_frequency_bands()
            
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage
    
    def _calculate_frequency_bands(self):
        """Calculate bass, mid, and treble levels"""
        # Find indices for frequency ranges
        bass_indices = np.where((self.frequency_bins >= self.bass_range[0]) & 
                               (self.frequency_bins <= self.bass_range[1]))[0]
        mid_indices = np.where((self.frequency_bins >= self.mid_range[0]) & 
                              (self.frequency_bins <= self.mid_range[1]))[0]
        treble_indices = np.where((self.frequency_bins >= self.treble_range[0]) & 
                                 (self.frequency_bins <= self.treble_range[1]))[0]
        
        # Calculate average levels for each band
        self.bass_level = np.mean(self.frequency_data[bass_indices]) if len(bass_indices) > 0 else 0
        self.mid_level = np.mean(self.frequency_data[mid_indices]) if len(mid_indices) > 0 else 0
        self.treble_level = np.mean(self.frequency_data[treble_indices]) if len(treble_indices) > 0 else 0
    
    def get_audio_features(self):
        """Get current audio features"""
        return {
            'volume': self.volume,
            'bass': self.bass_level,
            'mid': self.mid_level,
            'treble': self.treble_level,
            'frequency_data': self.frequency_data.copy(),
            'frequency_bins': self.frequency_bins.copy()
        }
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop_recording()
        if hasattr(self, 'audio'):
            self.audio.terminate()