import tkinter as tk
from tkinter import ttk
import threading
import os
import time
import platform

class MediaPlayerUI:
    def __init__(self, root, media_player):
        self.root = root
        self.media_player = media_player
        self.is_seeking = False
        self.video_frame = None
        
        self.create_widgets()
        self.update_ui()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_video_frame(main_frame)
        self.create_info_frame(main_frame)
        self.create_controls_frame(main_frame)
        self.create_progress_frame(main_frame)
        self.create_playlist_frame(main_frame)
        
    def create_video_frame(self, parent):
        video_container = ttk.LabelFrame(parent, text="Відео", padding=5)
        video_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.video_frame = tk.Frame(video_container, bg='black', width=640, height=360)
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        self.video_placeholder = tk.Label(
            self.video_frame, 
            text="Відкрийте відео або аудіо файл",
            bg='black',
            fg='white',
            font=('Arial', 14)
        )
        self.video_placeholder.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_info_frame(self, parent):
        info_frame = ttk.LabelFrame(parent, text="Інформація про файл", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_label = ttk.Label(info_frame, text="Файл не вибрано")
        self.file_label.pack(anchor=tk.W)
        
        self.time_label = ttk.Label(info_frame, text="00:00 / 00:00")
        self.time_label.pack(anchor=tk.W)
        
    def create_controls_frame(self, parent):
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.play_button = ttk.Button(controls_frame, text="▶", command=self.toggle_play_pause)
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(controls_frame, text="⏹", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.prev_button = ttk.Button(controls_frame, text="⏮", command=self.previous)
        self.prev_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.next_button = ttk.Button(controls_frame, text="⏭", command=self.next)
        self.next_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(controls_frame, text="Гучність:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.volume_var = tk.DoubleVar(value=0.7)
        self.volume_scale = ttk.Scale(controls_frame, from_=0, to=1, 
                                    variable=self.volume_var, 
                                    command=self.on_volume_change)
        self.volume_scale.pack(side=tk.LEFT, padx=(0, 10))
        
    def create_progress_frame(self, parent):
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_scale = ttk.Scale(progress_frame, from_=0, to=100,
                                      variable=self.progress_var,
                                      command=self.on_seek)
        self.progress_scale.pack(fill=tk.X)
        
    def create_playlist_frame(self, parent):
        playlist_frame = ttk.LabelFrame(parent, text="Плейлист", padding=10)
        playlist_frame.pack(fill=tk.BOTH, expand=True)
        
        self.playlist_listbox = tk.Listbox(playlist_frame, height=10)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.playlist_listbox.bind('<Double-1>', self.on_playlist_select)
        
    def toggle_play_pause(self):
        if not self.media_player.current_file:
            return
            
        if self.media_player.is_playing:
            if self.media_player.is_paused:
                self.media_player.resume()
                self.play_button.config(text="⏸")
            else:
                self.media_player.pause()
                self.play_button.config(text="▶")
        else:
            if self.media_player.play():
                self.play_button.config(text="⏸")
                
    def stop(self):
        self.media_player.stop()
        self.play_button.config(text="▶")
        self.progress_var.set(0)
        
    def previous(self):
        if self.media_player.current_index > 0:
            self.media_player.current_index -= 1
            self.load_current_playlist_item()
            
    def next(self):
        if self.media_player.current_index < len(self.media_player.playlist) - 1:
            self.media_player.current_index += 1
            self.load_current_playlist_item()
            
    def seek_forward(self):
        current_pos = self.media_player.get_position()
        new_pos = min(current_pos + 10, self.media_player.get_duration())
        self.media_player.seek(new_pos)
        
    def seek_backward(self):
        current_pos = self.media_player.get_position()
        new_pos = max(current_pos - 10, 0)
        self.media_player.seek(new_pos)
        
    def volume_up(self):
        new_volume = min(self.media_player.volume + 0.1, 1.0)
        self.media_player.set_volume(new_volume)
        self.volume_var.set(new_volume)
        
    def volume_down(self):
        new_volume = max(self.media_player.volume - 0.1, 0.0)
        self.media_player.set_volume(new_volume)
        self.volume_var.set(new_volume)
        
    def on_volume_change(self, value):
        self.media_player.set_volume(float(value))
        
    def on_seek(self, value):
        if not self.is_seeking and self.media_player.get_duration() > 0:
            position = (float(value) / 100.0) * self.media_player.get_duration()
            self.media_player.seek(position)
            
    def load_media(self, file_path):
        if self.media_player.load_file(file_path):
            self.file_label.config(text=os.path.basename(file_path))
            self.playlist_listbox.delete(0, tk.END)
            self.playlist_listbox.insert(tk.END, os.path.basename(file_path))
            self.media_player.playlist = [file_path]
            self.media_player.current_index = 0
            
            self.embed_video()
            
    def load_folder(self, folder_path):
        media_extensions = ['.mp3', '.mp4', '.avi', '.mkv', '.wav', '.flac', 
                          '.ogg', '.mov', '.wmv', '.flv']
        
        files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in media_extensions):
                files.append(os.path.join(folder_path, file))
                
        if files:
            self.media_player.playlist = sorted(files)
            self.media_player.current_index = 0
            self.load_current_playlist_item()
            
            self.playlist_listbox.delete(0, tk.END)
            for file in files:
                self.playlist_listbox.insert(tk.END, os.path.basename(file))
                
    def load_current_playlist_item(self):
        if (self.media_player.playlist and 
            0 <= self.media_player.current_index < len(self.media_player.playlist)):
            file_path = self.media_player.playlist[self.media_player.current_index]
            self.load_media(file_path)
            
    def on_playlist_select(self, event):
        selection = self.playlist_listbox.curselection()
        if selection:
            self.media_player.current_index = selection[0]
            self.load_current_playlist_item()
            
    def update_ui(self):
        if self.media_player.current_file:
            duration = self.media_player.get_duration()
            position = self.media_player.get_position()
            
            if duration > 0 and not self.is_seeking:
                progress = (position / duration) * 100
                self.progress_var.set(progress)
                
            time_text = f"{self.media_player.format_time(position)} / {self.media_player.format_time(duration)}"
            self.time_label.config(text=time_text)
            
        self.root.after(100, self.update_ui)  
        
    def embed_video(self):
        try:
            if self.video_placeholder:
                self.video_placeholder.place_forget()
            
            player = self.media_player.get_video_handle()
            
            self.root.update()
            
            if platform.system() == 'Windows':
                win_id = self.video_frame.winfo_id()
                player.set_hwnd(win_id)
            elif platform.system() == 'Linux':
                win_id = self.video_frame.winfo_id()
                player.set_xwindow(win_id)
            elif platform.system() == 'Darwin':
                win_id = self.video_frame.winfo_id()
                player.set_nsobject(win_id)
                
        except Exception as e:
            print(f"Помилка вбудовування відео: {e}")
