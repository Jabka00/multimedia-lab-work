import vlc
import os
import time
from mutagen import File

class MediaPlayer:
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.current_file = None
        self.duration = 0
        self.volume = 70  
        self.playlist = []
        self.current_index = 0
        
        try:
            import platform
            if platform.system() == 'Windows':
                self.instance = vlc.Instance('--no-xlib')
            else:
                self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
            self.player.audio_set_volume(self.volume)
        except Exception as e:
            print(f"ПОМИЛКА: Не вдалося ініціалізувати VLC: {e}")
            print("Переконайтеся, що VLC Media Player встановлено в системі.")
            print("Завантажте VLC з https://www.videolan.org/vlc/")
            raise
        
    def load_file(self, file_path):
        if not os.path.exists(file_path):
            return False
            
        self.current_file = file_path
        
        try:
            media = self.instance.media_new(file_path)
            self.player.set_media(media)
            
            media.parse()
            self.duration = media.get_duration() / 1000.0  

            if self.duration <= 0:
                self.load_audio_info(file_path)
                
            return True
        except Exception as e:
            print(f"Помилка завантаження файлу: {e}")
            return False
            
    def is_video_file(self, file_path):
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        return any(file_path.lower().endswith(ext) for ext in video_extensions)
        
    def load_audio_info(self, file_path):
        try:
            audio_file = File(file_path)
            if audio_file is not None and audio_file.info.length:
                self.duration = audio_file.info.length
            else:
                self.duration = 0
        except:
            self.duration = 0
            
    def play(self):
        if not self.current_file:
            return False
            
        try:
            if self.is_paused:
                self.player.play()
                self.is_paused = False
            else:
                self.player.play()
                time.sleep(0.1)
                if self.duration <= 0:
                    media = self.player.get_media()
                    if media:
                        self.duration = media.get_duration() / 1000.0
                        
            self.is_playing = True
            return True
        except Exception as e:
            print(f"Помилка відтворення: {e}")
            return False
            
    def pause(self):
        if self.is_playing and not self.is_paused:
            self.player.pause()
            self.is_paused = True
            
    def resume(self):
        if self.is_paused:
            self.player.play()
            self.is_paused = False
            
    def stop(self):
        self.player.stop()
        self.is_playing = False
        self.is_paused = False
            
    def seek(self, position):
        if self.duration > 0:
            relative_position = position / self.duration
            relative_position = max(0.0, min(1.0, relative_position))
            self.player.set_position(relative_position)
                
    def set_volume(self, volume):
        self.volume = int(max(0.0, min(1.0, volume)) * 100)
        self.player.audio_set_volume(self.volume)
        
    def get_position(self):
        if not self.is_playing:
            return 0
            
        position = self.player.get_position()
        if position >= 0 and self.duration > 0:
            return position * self.duration
        return 0
            
    def get_duration(self):
        if self.player.get_length() > 0:
            self.duration = self.player.get_length() / 1000.0
        return self.duration
        
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def get_video_handle(self):
        return self.player
