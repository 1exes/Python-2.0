from TikTokApi import TikTokApi

api = TikTokApi()

# Beispiel: Abrufen von TikTok-Videos eines bestimmten Benutzers
username = "username"
count = 5  # Anzahl der Videos, die abgerufen werden sollen

tiktoks = api.by_username(username, count=count)

for tiktok in tiktoks:
    print(tiktok['desc'])

sssss

s