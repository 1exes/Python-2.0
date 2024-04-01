from re import S
import ssl
import tkinter as tk
from tkinter import messagebox
from clicknium import clicknium as cc, locator
import time
import pyautogui
from random import shuffle
from datetime import datetime, timedelta
import threading
import subprocess

class TikTokUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Uploader")
        self.root.geometry("600x400")
        
        self.video_path = tk.StringVar()
        self.description_file = tk.StringVar()
        self.daily_posts = tk.IntVar(value=3)
        self.upload_times = tk.StringVar(value="9:00,13:00,16:00")
        
        # Video Path Entry
        tk.Label(root, text="Video Path:").place(x=20, y=20)
        self.video_path_entry = tk.Entry(root, textvariable=self.video_path, width=50)
        self.video_path_entry.place(x=150, y=20)
        
        # Description File Entry
        tk.Label(root, text="Description File:").place(x=20, y=60)
        self.description_file_entry = tk.Entry(root, textvariable=self.description_file, width=50)
        self.description_file_entry.place(x=150, y=60)

        # Daily Posts Entry
        tk.Label(root, text="Daily Posts (1-10):").place(x=20, y=100)
        self.daily_posts_entry = tk.Entry(root, textvariable=self.daily_posts, width=10)
        self.daily_posts_entry.place(x=150, y=100)

        # Upload Times Entry
        tk.Label(root, text="Upload Times (HH:MM separated by commas):").place(x=20, y=140)
        self.upload_times_entry = tk.Entry(root, textvariable=self.upload_times, width=50)
        self.upload_times_entry.place(x=250, y=140)

        # Start Button
        tk.Button(root, text="Start Upload", command=self.start_upload).place(x=250, y=180)

    def load_video_description(self, filename):
        try:
            with open(filename, "r") as f:
                description = f.read().strip()
            return description
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Video-Beschreibung: {e}")
            return None

    def start_upload(self):
        video_path = self.video_path.get()
        description_file = self.description_file.get()
        daily_posts = self.daily_posts.get()
        upload_times = [tuple(map(int, t.split(':'))) for t in self.upload_times.get().split(',')]
        
        start_number = 1
        end_number = 10
        
        video_numbers = list(range(start_number, end_number + 1))
        shuffle(video_numbers)
        
        best_upload_times = [(hour, minute) for hour, minute in upload_times][:daily_posts]
        
        threading.Thread(target=self.upload_videos, args=(video_path, description_file, video_numbers, best_upload_times)).start()
        self.root.destroy()
        
    def update_progress(self, progress_text):
        print(progress_text)
    
    def upload_videos(self, video_path, description_file, video_numbers, best_upload_times):
        try:
            tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
            time.sleep(5)
            
            for num in video_numbers:
                current_time = datetime.now()
                
                while True:
                    next_upload_time = None
                    for hour, minute in best_upload_times:
                        potential_upload_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                        if current_time < potential_upload_time:
                            next_upload_time = potential_upload_time
                            break
                    
                    if next_upload_time is None:
                        next_upload_time = current_time.replace(hour=best_upload_times[0][0], minute=best_upload_times[0][1], second=0, microsecond=0) + timedelta(days=1)
                    
                    wait_time = (next_upload_time - current_time).total_seconds()
                    
                    hours, remainder = divmod(wait_time, 3600)
                    minutes, _ = divmod(remainder, 60)
                    progress_text = f"Nächstes Video wird hochgeladen am {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten."
                    self.update_progress(progress_text)
                    
                    if wait_time <= 600:
                        break
                    
                    time.sleep(600)
                    current_time = datetime.now()
                
                time.sleep(wait_time)
                
                tab.find_element(locator.tiktok.one).click(by='mouse-emulation')
                time.sleep(5)
                
                file_path = f"{video_path}\\{num}.mp4"
                pyautogui.write(file_path)
                pyautogui.press('enter')
                
                description = self.load_video_description(description_file)
                tab.find_element(locator.tiktok.four).set_text(description, by='sendkey-after-click')
                time.sleep(60)
                
                time.sleep(10)
                progress_text = f"Video {num}.mp4 hochgeladen und beschrieben."
                self.update_progress(progress_text)
            
            progress_text = "Alle Videos wurden hochgeladen."
            self.update_progress(progress_text)
            
        except Exception as e:
            subprocess.run(["cmd.exe", "/c", "cls"])
            print(f"Ein Fehler ist aufgetreten: {e}")
            
        finally:
            try:
                tab.close()
            except:
                pass

root = tk.Tk()
app = TikTokUploaderApp(root)
root.mainloop()

