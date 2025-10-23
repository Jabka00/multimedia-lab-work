import pygame
import cv2
import threading
import time
import os
from mutagen import File
import numpy as np

class MediaPlayer:
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.current_file = None
        self.position = 0
        self.duration = 0
        self.volume = 0.7
        self.playlist = []
        self.current_index = 0
        
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.set_volume(self.volume)
        
    def load_file(self, file_path):
        if not os.path.exists(file_path):
            return False
            
        self.current_file = file_path
        self.position = 0
        
        try:
            if self.is_video_file(file_path):
                self.load_video_info(file_path)
            else:
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
            
    def load_video_info(self, file_path):
        try:
            cap = cv2.VideoCapture(file_path)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                self.duration = frame_count / fps if fps > 0 else 0
                cap.release()
            else:
                self.duration = 0
        except:
            self.duration = 0
            
    def play(self):
        if not self.current_file:
            return False
            
        try:
            if self.is_video_file(self.current_file):
                self.play_video()
            else:
                self.play_audio()
            self.is_playing = True
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Помилка відтворення: {e}")
            return False
            
    def play_audio(self):
        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play(start=self.position)
        
    def play_video(self):
        def video_thread():
            try:
                cap = cv2.VideoCapture(self.current_file)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_delay = 1.0 / fps if fps > 0 else 1.0 / 25.0
                
                if self.position > 0:
                    cap.set(cv2.CAP_PROP_POS_MSEC, self.position * 1000)
                    
                while self.is_playing and not self.is_paused:
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    cv2.imshow('Відео', frame)
                    if cv2.waitKey(int(frame_delay * 1000)) & 0xFF == ord('q'):
                        break
                        
                cap.release()
                cv2.destroyAllWindows()
            except Exception as e:
                print(f"Помилка відтворення відео: {e}")
            
        threading.Thread(target=video_thread, daemon=True).start()
        
    def pause(self):
        if self.is_playing:
            if self.is_video_file(self.current_file):
                self.is_paused = True
            else:
                pygame.mixer.music.pause()
            self.is_paused = True
            
    def resume(self):
        if self.is_paused:
            if self.is_video_file(self.current_file):
                self.is_paused = False
            else:
                pygame.mixer.music.unpause()
            self.is_paused = False
            
    def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.position = 0
        
        if self.is_video_file(self.current_file):
            cv2.destroyAllWindows()
        else:
            pygame.mixer.music.stop()
            
    def seek(self, position):
        self.position = max(0, min(position, self.duration))
        
        if self.is_video_file(self.current_file):
            pass
        else:
            if self.is_playing:
                pygame.mixer.music.stop()
                pygame.mixer.music.play(start=self.position)
                
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        
    def get_position(self):
        if self.is_video_file(self.current_file):
            return self.position
        else:
            return pygame.mixer.music.get_pos() / 1000.0
            
    def get_duration(self):
        return self.duration
        
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
