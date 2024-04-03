import pandas as pd
import os
import re

# Pfad zur Excel-Datei und zum Ordner mit den Videos
excel_datei = r'Y:\video_info.xlsx'
video_ordner = r'Y:\Videos'

# DataFrame aus der Excel-Datei erstellen
df = pd.read_excel(excel_datei)

# Funktion zum Bereinigen des Dateinamens
def clean_filename(filename):
    return re.sub(r'[\\/:"*?<>|]', '', filename)

# Durch jede Zeile der Excel-Datei iterieren
for index, row in df.iterrows():
    link = str(row['Video-Link'])  # Spalte 'Video-Link' in der Excel-Datei
    beschreibung = str(row['Video-Beschreibung mit Hashtags'])  # Spalte 'Video-Beschreibung mit Hashtags' in der Excel-Datei
    
    # Den Dateinamen aus dem Link extrahieren
    video_id = link.split('/')[-1]
    alter_name = os.path.join(video_ordner, video_id + '.mp4')
    
    # Überprüfen, ob die Datei im Ordner existiert
    if os.path.exists(alter_name):
        # Neuen Dateinamen aus dem Ordner und der Beschreibung erstellen
        neuer_name = os.path.join(video_ordner, f"{clean_filename(beschreibung)}.mp4")
        
        # Überprüfen, ob die Datei mit dem neuen Namen bereits existiert
        if not os.path.exists(neuer_name):
            # Die Datei umbenennen
            os.rename(alter_name, neuer_name)
            print(f'Datei umbenannt: {alter_name} -> {neuer_name}')
            
            # Video-ID und neuen Dateinamen in die Excel-Datei schreiben
            df.at[index, 'Video-ID'] = video_id
            df.at[index, 'Neuer Dateiname'] = neuer_name
        else:
            print(f'Datei mit neuem Namen bereits vorhanden: {neuer_name}')
    else:
        print(f'Datei nicht gefunden: {alter_name}')

# DataFrame mit den aktualisierten Informationen in die Excel-Datei schreiben
df.to_excel(excel_datei, index=False)
