import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from media_player import MediaPlayer
from ui_components import MediaPlayerUI
from config import Config

class MediaPlayerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Медіаплеєр")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        self.config = Config()
        self.media_player = MediaPlayer()
        self.ui = MediaPlayerUI(self.root, self.media_player)
        
        self.setup_menus()
        self.setup_keyboard_shortcuts()
        
    def setup_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Відкрити файл...", command=self.open_file)
        file_menu.add_command(label="Відкрити папку...", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.quit_app)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Повний екран", command=self.toggle_fullscreen)
        
    def setup_keyboard_shortcuts(self):
        self.root.bind('<space>', lambda e: self.ui.toggle_play_pause())
        self.root.bind('<Left>', lambda e: self.ui.seek_backward())
        self.root.bind('<Right>', lambda e: self.ui.seek_forward())
        self.root.bind('<Up>', lambda e: self.ui.volume_up())
        self.root.bind('<Down>', lambda e: self.ui.volume_down())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        
    def open_file(self):
        filetypes = [
            ("Медіа файли", "*.mp3 *.mp4 *.avi *.mkv *.wav *.flac *.ogg *.mov *.wmv"),
            ("Аудіо файли", "*.mp3 *.wav *.flac *.ogg"),
            ("Відео файли", "*.mp4 *.avi *.mkv *.mov *.wmv"),
            ("Всі файли", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Виберіть медіа файл",
            filetypes=filetypes
        )
        
        if filename:
            self.ui.load_media(filename)
            
    def open_folder(self):
        folder = filedialog.askdirectory(title="Виберіть папку з медіа файлами")
        if folder:
            self.ui.load_folder(folder)
            
    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        
    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)
        
    def quit_app(self):
        self.media_player.stop()
        self.root.quit()
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.mainloop()

if __name__ == "__main__":
    app = MediaPlayerApp()
    app.run()
