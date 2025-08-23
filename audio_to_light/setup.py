#!/usr/bin/env python3
"""
Setup script for Audio to Light Visualizer
Handles installation and dependency checking
"""

import sys
import subprocess
import pkg_resources
import platform


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True


def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False


def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "numpy>=1.21.0",
        "pyaudio>=0.2.11", 
        "pygame>=2.1.0",
        "matplotlib>=3.5.0",
        "scipy>=1.7.0"
    ]
    
    print("Checking dependencies...")
    
    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.require(package)
            print(f"✓ {package} - already installed")
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            missing_packages.append(package)
            print(f"✗ {package} - missing or incompatible version")
    
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✓ {package} installed successfully")
            else:
                print(f"✗ Failed to install {package}")
                return False
        
        print("\nAll dependencies installed successfully!")
    else:
        print("\nAll dependencies are already satisfied!")
    
    return True


def check_audio_system():
    """Check if audio system is properly configured"""
    print("\nChecking audio system...")
    
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        audio.terminate()
        
        if input_devices:
            print(f"✓ Found {len(input_devices)} audio input device(s):")
            for device in input_devices[:3]:  # Show first 3 devices
                print(f"  - {device}")
            if len(input_devices) > 3:
                print(f"  ... and {len(input_devices) - 3} more")
        else:
            print("✗ No audio input devices found")
            print("  Please check your microphone connection and system audio settings")
            return False
            
    except Exception as e:
        print(f"✗ Audio system check failed: {e}")
        
        # Provide system-specific help
        system = platform.system().lower()
        if system == "linux":
            print("\nFor Linux users, try:")
            print("  sudo apt-get install python3-pyaudio portaudio19-dev")
            print("  or")
            print("  sudo dnf install python3-pyaudio portaudio-devel")
        elif system == "darwin":
            print("\nFor macOS users, try:")
            print("  brew install portaudio")
        elif system == "windows":
            print("\nFor Windows users:")
            print("  Audio drivers should be installed automatically")
            print("  If issues persist, try updating your audio drivers")
        
        return False
    
    return True


def run_test():
    """Run a quick test of the application"""
    print("\nRunning quick test...")
    
    try:
        # Test imports
        import numpy as np
        import pygame
        from audio_processor import AudioProcessor
        from light_effects import LightEffects
        
        print("✓ All modules imported successfully")
        
        # Test audio processor initialization
        audio_proc = AudioProcessor()
        print("✓ Audio processor created successfully")
        
        # Test light effects initialization (without display)
        pygame.init()
        pygame.display.set_mode((100, 100), pygame.NOFRAME)
        light_fx = LightEffects(100, 100)
        print("✓ Light effects system initialized successfully")
        
        # Cleanup
        light_fx.cleanup()
        audio_proc.stop_recording()
        
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("Audio to Light Visualizer - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not check_and_install_dependencies():
        print("\nSetup failed: Could not install required dependencies")
        return 1
    
    # Check audio system
    if not check_audio_system():
        print("\nWarning: Audio system issues detected")
        print("The application may not work properly without a working microphone")
    
    # Run test
    if not run_test():
        print("\nWarning: Initial test failed")
        print("The application may have issues running")
    
    print("\n" + "=" * 40)
    print("Setup complete!")
    print("\nTo run the application:")
    print("  python main.py")
    print("\nMake sure your microphone is connected and working!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())