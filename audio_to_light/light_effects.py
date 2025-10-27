import pygame
import numpy as np
import colorsys
import math
import time


class LightEffects:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Audio to Light Visualizer")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Color and effect parameters
        self.hue_offset = 0
        self.brightness_multiplier = 1.0
        self.effect_mode = "spectrum"  # spectrum, circles, bars, wave, strobe
        
        # Effect-specific parameters
        self.circle_radius = 50
        self.bar_count = 32
        self.wave_amplitude = 100
        self.strobe_intensity = 0
        
        # Smoothing for visual effects
        self.smoothed_volume = 0
        self.smoothed_bass = 0
        self.smoothed_mid = 0
        self.smoothed_treble = 0
        self.smoothing_factor = 0.1
        
        # Background and particle effects
        self.particles = []
        self.max_particles = 50
        
    def update(self, audio_features):
        """Update visual effects based on audio features"""
        volume = audio_features['volume']
        bass = audio_features['bass']
        mid = audio_features['mid']
        treble = audio_features['treble']
        frequency_data = audio_features['frequency_data']
        
        # Smooth the audio features for more fluid animation
        self.smoothed_volume = self._smooth(self.smoothed_volume, volume)
        self.smoothed_bass = self._smooth(self.smoothed_bass, bass)
        self.smoothed_mid = self._smooth(self.smoothed_mid, mid)
        self.smoothed_treble = self._smooth(self.smoothed_treble, treble)
        
        # Update hue based on audio
        self.hue_offset = (self.hue_offset + self.smoothed_treble * 2) % 360
        
        # Update brightness
        self.brightness_multiplier = 0.3 + self.smoothed_volume * 2
        
        # Clear screen with dark background
        bg_intensity = int(self.smoothed_volume * 30)
        self.screen.fill((bg_intensity, bg_intensity // 2, bg_intensity // 4))
        
        # Render current effect
        if self.effect_mode == "spectrum":
            self._draw_spectrum(frequency_data)
        elif self.effect_mode == "circles":
            self._draw_circles(bass, mid, treble)
        elif self.effect_mode == "bars":
            self._draw_bars(frequency_data)
        elif self.effect_mode == "wave":
            self._draw_wave(frequency_data)
        elif self.effect_mode == "strobe":
            self._draw_strobe(volume)
        elif self.effect_mode == "particles":
            self._draw_particles(bass, mid, treble)
        
        # Update particles
        self._update_particles()
        
        pygame.display.flip()
        
    def _smooth(self, current, target):
        """Smooth value transitions"""
        return current + (target - current) * self.smoothing_factor
        
    def _draw_spectrum(self, frequency_data):
        """Draw frequency spectrum visualization"""
        bar_width = self.width // len(frequency_data)
        
        for i, magnitude in enumerate(frequency_data):
            if magnitude > 0.01:  # Threshold to reduce noise
                height = int(magnitude * self.height * self.brightness_multiplier)
                x = i * bar_width
                
                # Color based on frequency (red=bass, green=mid, blue=treble)
                hue = (i / len(frequency_data) * 360 + self.hue_offset) % 360
                rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, magnitude)
                color = tuple(int(c * 255) for c in rgb)
                
                pygame.draw.rect(self.screen, color, 
                               (x, self.height - height, bar_width - 1, height))
    
    def _draw_circles(self, bass, mid, treble):
        """Draw concentric circles based on frequency bands"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Bass circle (red)
        bass_radius = int(bass * 200 * self.brightness_multiplier)
        if bass_radius > 5:
            bass_color = (255, int(bass * 255), 0)
            pygame.draw.circle(self.screen, bass_color, (center_x, center_y), bass_radius, 3)
        
        # Mid circle (green)
        mid_radius = int(mid * 150 * self.brightness_multiplier)
        if mid_radius > 5:
            mid_color = (0, 255, int(mid * 255))
            pygame.draw.circle(self.screen, mid_color, (center_x, center_y), mid_radius, 3)
        
        # Treble circle (blue)
        treble_radius = int(treble * 100 * self.brightness_multiplier)
        if treble_radius > 5:
            treble_color = (int(treble * 255), 0, 255)
            pygame.draw.circle(self.screen, treble_color, (center_x, center_y), treble_radius, 3)
    
    def _draw_bars(self, frequency_data):
        """Draw vertical bars visualization"""
        # Downsample frequency data for better visualization
        samples = 32
        step = len(frequency_data) // samples
        bar_width = self.width // samples
        
        for i in range(samples):
            start_idx = i * step
            end_idx = min((i + 1) * step, len(frequency_data))
            magnitude = np.mean(frequency_data[start_idx:end_idx])
            
            if magnitude > 0.01:
                height = int(magnitude * self.height * self.brightness_multiplier)
                x = i * bar_width
                
                hue = (i / samples * 240 + self.hue_offset) % 360
                rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, magnitude)
                color = tuple(int(c * 255) for c in rgb)
                
                pygame.draw.rect(self.screen, color,
                               (x + 2, self.height - height, bar_width - 4, height))
    
    def _draw_wave(self, frequency_data):
        """Draw wave visualization"""
        if len(frequency_data) < 2:
            return
            
        points = []
        samples = min(len(frequency_data), self.width // 4)
        
        for i in range(samples):
            x = int(i * self.width / samples)
            magnitude = frequency_data[i] if i < len(frequency_data) else 0
            y = int(self.height / 2 - magnitude * self.wave_amplitude * self.brightness_multiplier)
            points.append((x, y))
        
        if len(points) > 1:
            # Draw wave with gradient colors
            for i in range(len(points) - 1):
                hue = (i / len(points) * 360 + self.hue_offset) % 360
                rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, 0.8)
                color = tuple(int(c * 255) for c in rgb)
                
                pygame.draw.line(self.screen, color, points[i], points[i + 1], 3)
    
    def _draw_strobe(self, volume):
        """Draw strobe effect"""
        if volume > 0.5:  # Threshold for strobe activation
            intensity = int(volume * 255 * self.brightness_multiplier)
            hue = (self.hue_offset + time.time() * 100) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, volume)
            color = tuple(int(c * intensity) for c in rgb)
            self.screen.fill(color)
    
    def _draw_particles(self, bass, mid, treble):
        """Draw particle effect"""
        # Add new particles based on audio
        if bass > 0.3 and len(self.particles) < self.max_particles:
            for _ in range(int(bass * 5)):
                self._add_particle("bass")
        
        if mid > 0.3 and len(self.particles) < self.max_particles:
            for _ in range(int(mid * 3)):
                self._add_particle("mid")
        
        if treble > 0.3 and len(self.particles) < self.max_particles:
            for _ in range(int(treble * 2)):
                self._add_particle("treble")
    
    def _add_particle(self, freq_type):
        """Add a new particle"""
        particle = {
            'x': np.random.randint(0, self.width),
            'y': np.random.randint(0, self.height),
            'vx': np.random.uniform(-5, 5),
            'vy': np.random.uniform(-5, 5),
            'life': 1.0,
            'decay': np.random.uniform(0.01, 0.03),
            'size': np.random.randint(2, 8),
            'type': freq_type
        }
        self.particles.append(particle)
    
    def _update_particles(self):
        """Update and draw particles"""
        to_remove = []
        
        for i, particle in enumerate(self.particles):
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Update life
            particle['life'] -= particle['decay']
            
            # Remove if dead or out of bounds
            if (particle['life'] <= 0 or 
                particle['x'] < 0 or particle['x'] > self.width or
                particle['y'] < 0 or particle['y'] > self.height):
                to_remove.append(i)
                continue
            
            # Draw particle
            alpha = particle['life']
            if particle['type'] == 'bass':
                color = (255, int(100 * alpha), int(100 * alpha))
            elif particle['type'] == 'mid':
                color = (int(100 * alpha), 255, int(100 * alpha))
            else:  # treble
                color = (int(100 * alpha), int(100 * alpha), 255)
            
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size'] * alpha))
        
        # Remove dead particles
        for i in reversed(to_remove):
            del self.particles[i]
    
    def set_effect_mode(self, mode):
        """Change the current effect mode"""
        valid_modes = ["spectrum", "circles", "bars", "wave", "strobe", "particles"]
        if mode in valid_modes:
            self.effect_mode = mode
            print(f"Effect mode changed to: {mode}")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.set_effect_mode("spectrum")
                elif event.key == pygame.K_2:
                    self.set_effect_mode("circles")
                elif event.key == pygame.K_3:
                    self.set_effect_mode("bars")
                elif event.key == pygame.K_4:
                    self.set_effect_mode("wave")
                elif event.key == pygame.K_5:
                    self.set_effect_mode("strobe")
                elif event.key == pygame.K_6:
                    self.set_effect_mode("particles")
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
        
        return self.running
    
    def cleanup(self):
        """Cleanup pygame resources"""
        pygame.quit()