import tkinter as tk
from tkinter import ttk, messagebox
from clicknium import clicknium as cc, locator
import time
import pyautogui
from random import shuffle
from datetime import datetime, timedelta
import threading
import requests
import json


class TikTokMultitool:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Multitool")
        
        self.tabControl = ttk.Notebook(self.root)
        
        self.bulkDownloaderTab = ttk.Frame(self.tabControl)
        self.uploadPlannerTab = ttk.Frame(self.tabControl)
        self.analyticsTab = ttk.Frame(self.tabControl)
        self.hashtagGeneratorTab = ttk.Frame(self.tabControl)
        self.autoActionsTab = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.bulkDownloaderTab, text="Bulk Downloader")
        self.tabControl.add(self.uploadPlannerTab, text="Upload Planner")
        self.tabControl.add(self.analyticsTab, text="Analytics")
        self.tabControl.add(self.hashtagGeneratorTab, text="Hashtag Generator")
        self.tabControl.add(self.autoActionsTab, text="Auto Actions")
        
        self.tabControl.pack(expand=1, fill="both")
        
        self.create_bulk_downloader_tab()
        self.create_upload_planner_tab()
        self.create_analytics_tab()
        self.create_hashtag_generator_tab()
        self.create_auto_actions_tab()
    
    def create_bulk_downloader_tab(self):
        frame = ttk.LabelFrame(self.bulkDownloaderTab, text="Bulk Downloader")
        frame.grid(row=0, column=0, padx=20, pady=20)
        
        ttk.Label(frame, text="TikTok URLs (comma separated):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.bulk_urls_entry = ttk.Entry(frame, width=50)
        self.bulk_urls_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(frame, text="Download", command=self.bulk_download).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
    def bulk_download(self):
        urls = self.bulk_urls_entry.get().split(',')
        for url in urls:
            video_data = requests.get(url.strip() + "/?type=video")
            video_json = json.loads(video_data.text)
            video_url = video_json['itemInfo']['itemStruct']['video']['playAddr']
            video_name = video_json['itemInfo']['itemStruct']['desc'] + ".mp4"
            
            with open(video_name, 'wb') as f:
                f.write(requests.get(video_url).content)
        
        messagebox.showinfo("Info", "Videos downloaded successfully!")
    
    def create_upload_planner_tab(self):
        frame = ttk.LabelFrame(self.uploadPlannerTab, text="Upload Planner")
        frame.grid(row=0, column=0, padx=20, pady=20)
        
        ttk.Label(frame, text="Start Number:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.start_number_entry = ttk.Entry(frame, width=10)
        self.start_number_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="End Number:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.end_number_entry = ttk.Entry(frame, width=10)
        self.end_number_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Button(frame, text="Plan Upload", command=self.plan_upload).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    def plan_upload(self):
        start_number = int(self.start_number_entry.get())
        end_number = int(self.end_number_entry.get())
        
        video_numbers = list(range(start_number, end_number + 1))
        shuffle(video_numbers)
        
        daily_posts = 2  # Minimum 2 videos per day
        best_upload_times = [(10, 10), (14, 0), (16, 53), (17, 16), (18, 45)][:daily_posts]
        
        threading.Thread(target=self.upload_videos, args=(video_numbers, best_upload_times)).start()
    
    def upload_videos(self, video_numbers, best_upload_times):
        tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")
        time.sleep(5)
        
        for num in video_numbers:
            current_time = datetime.now()
            
            while True:
                next_upload_time = None
                for hour, minute in best_upload_times:
                    if current_time.hour < hour or (current_time.hour == hour and current_time.minute < minute):
                        next_upload_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                        break
                
                if next_upload_time is None:
                    next_upload_time = current_time.replace(hour=best_upload_times[0][0], minute=best_upload_times[0][1], second=0, microsecond=0) + timedelta(days=1)
                
                wait_time = (next_upload_time - current_time).total_seconds()
                
                hours, remainder = divmod(wait_time, 3600)
                minutes, _ = divmod(remainder, 60)
                print(f"Video wird hochgeladen am {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}. Nächste Hochladezeit in {int(hours)} Stunden und {int(minutes)} Minuten.")
                
                if wait_time <= 600:
                    break
                
                time.sleep(600)
                current_time = datetime.now()
            
            time.sleep(wait_time)
            
            tab.find_element(locator.tiktok.one).click(by='mouse-emulation')
            time.sleep(5)

            file_path = fr"C:\Users\edgar\Videos\{num}.mp4"
            pyautogui.write(file_path)
            pyautogui.press('enter')

            tab.find_element(locator.tiktok.four).set_text("Funny", by='sendkey-after-click')
            time.sleep(60)

            tab.find_element(locator.tiktok.five).click(by='mouse-emulation')
            
            tab.find_element(locator.tiktok.div_noch_ein_video_hochladen).click(by='mouse-emulation')
            
            time.sleep(10)
        
        messagebox.showinfo("Info", "All videos uploaded successfully!")
        tab.close()
    
    def create_analytics_tab(self):
        frame = ttk.LabelFrame(self.analyticsTab, text="Analytics")
        frame.grid(row=0, column=0, padx=20, pady=20)
        
        ttk.Label(frame, text="TikTok Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.analytics_username_entry = ttk.Entry(frame, width=30)
        self.analytics_username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(frame, text="Get Analytics", command=self.get_analytics).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
    def get_analytics(self):
        username = self.analytics_username_entry.get()
        # Implement analytics logic (views, likes, comments, etc.)
        pass
    
    def create_hashtag_generator_tab(self):
        frame = ttk.LabelFrame(self.hashtagGeneratorTab, text="Hashtag Generator")
        frame.grid(row=0, column=0, padx=20, pady=20)
        
        ttk.Label(frame, text="Keyword:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.hashtag_keyword_entry = ttk.Entry(frame, width=30)
        self.hashtag_keyword_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(frame, text="Generate Hashtags", command=self.generate_hashtags).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
    def generate_hashtags(self):
        keyword = self.hashtag_keyword_entry.get()
        # Implement hashtag generation logic
        pass
    
    def create_auto_actions_tab(self):
        frame = ttk.LabelFrame(self.autoActionsTab, text="Auto Actions")
        frame.grid(row=0, column=0, padx=20, pady=20)
        
        ttk.Label(frame, text="TikTok URL:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.auto_url_entry = ttk.Entry(frame, width=50)
        self.auto_url_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(frame, text="Auto Actions", command=self.auto_actions).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
    def auto_actions(self):
        tiktok_url = self.auto_url_entry.get()
        # Implement auto actions logic (comments, likes, etc.)
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = TikTokMultitool(root)
    root.mainloop()
