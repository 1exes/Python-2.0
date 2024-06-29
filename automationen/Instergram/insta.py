from instabot import Bot
import os

# Instagram Anmeldedaten
username = 'dein_username'
password = 'dein_passwort'

# Pfad zum Video und Beschreibung
video_path = 'pfad/zum/video.mp4'
caption = 'Deine Videobeschreibung'

# Instagram Bot initialisieren und einloggen
bot = Bot()
bot.login(username=username, password=password)

# Video hochladen
bot.upload_video(video_path, caption=caption)

# Logout nach dem Hochladen
bot.logout()
