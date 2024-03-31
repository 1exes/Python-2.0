from clicknium import clicknium as cc, locator, ui
import time

# URL der Webseite öffnen
tab = cc.edge.open("https://www.tiktok.com/upload?lang=en")

# Datum im Format "TT.MM.JJJJ" eingeben
datum = "15.04.2024"
datum_input = tab.find_element(locator.tiktok.datum)
datum_input.set_text(datum, by='sendkey-after-click')

# Warten, um sicherzustellen, dass das Datum gesetzt wurde
time.sleep(2)

# Andere Aktionen auf der Webseite...
