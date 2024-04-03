import pandas as pd
import os

# Pfad zur Excel-Datei und zum Ordner mit den Videos
excel_datei = r'Y:\video_info.xlsx'
video_ordner = r'Y:\Videos'

# DataFrame aus der Excel-Datei erstellen
df = pd.read_excel(excel_datei)

# Durch jede Zeile der Excel-Datei iterieren
for index, row in df.iterrows():
    link = str(row['Video-Link'])  # Spalte 'Video-Link' in der Excel-Datei
    
    # Den Dateinamen aus dem Link extrahieren
    video_id = link.split('/')[-1]
    alter_name = os.path.join(video_ordner, video_id + '.mp4')
    
    # Überprüfen, ob die Datei im Ordner existiert
    if os.path.exists(alter_name):
        print(f'Datei gefunden: {alter_name}')
    else:
        print(f'Datei nicht gefunden: {alter_name}')
