import TikTokApi

api = (TikTokApi)

results = 10

# Da TikTok ihre API geändert hat, musst du die custom_verifyFp-Option verwenden.
# Du musst in deinem Webbrowser zu TikTok gehen, dich anmelden und den s_v_web_id-Wert erhalten.
trending = api.trending(count=results, custom_verifyFp="")

for tiktok in trending:
    # Gibt die ID des TikToks aus
    print(tiktok['id'])

print(len(trending))
