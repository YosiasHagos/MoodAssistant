import pygame
import os

class AudioController:
    def __init__(self, audio_folder="audio"):
        """
        Initialize audio controller.
        
        Args:
            audio_folder (str): Folder containing audio files
        """
        pygame.mixer.init()
        self.audio_folder = audio_folder
        self.current_sound = None
        self.is_playing = False
        

        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)
            print(f"[AUDIO] Created audio folder: {audio_folder}")
        

        self.sound_map = {
            "happy": "happy.mp3",     
            "sad": "sad.mp3",       
            "stressed": "stressed.mp3",   
            "focused": "rain.mp3",    
            
        }
        
        print("[AUDIO] Audio controller initialized")
    
    def play_sound(self, sound_name):
        """
        Play a sound by name (e.g. 'happy', 'sad', 'stressed', 'focused', 'none').
        """
        
        self.stop_audio()
        
        
        if sound_name in ("none", "neutral") or sound_name not in self.sound_map:
            print(f"[AUDIO] No audio to play (sound: {sound_name})")
            return
        
        filename = self.sound_map[sound_name]
        filepath = os.path.join(self.audio_folder, filename)
        
        
        if not os.path.exists(filepath):
            print(f"[AUDIO WARNING] Audio file not found: {filepath}")
            print(f"[AUDIO] Please add '{filename}' to the '{self.audio_folder}' folder")
            return
        
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(-1)  
            self.current_sound = sound_name
            self.is_playing = True
            print(f"[AUDIO] Playing: {sound_name} ({filename})")
        except Exception as e:
            print(f"[AUDIO ERROR] Failed to play {sound_name}: {e}")
    
    def stop_audio(self):
        """Stop any currently playing audio."""
        if self.is_playing:
            try:
                pygame.mixer.music.stop()
                print(f"[AUDIO] Stopped: {self.current_sound}")
                self.current_sound = None
                self.is_playing = False
            except Exception as e:
                print(f"[AUDIO ERROR] Failed to stop audio: {e}")
    
    def set_volume(self, volume):
        """
        Set playback volume.
        
        Args:
            volume (float): Volume level 0.0 to 1.0
        """
        try:
            pygame.mixer.music.set_volume(volume)
            print(f"[AUDIO] Volume set to {int(volume * 100)}%")
        except Exception as e:
            print(f"[AUDIO ERROR] Failed to set volume: {e}")
    
    def cleanup(self):
        """Clean up audio resources."""
        self.stop_audio()
        pygame.mixer.quit()
        print("[AUDIO] Audio controller cleaned up")
