import tkinter as tk
from tkinter import messagebox
import os

class Haushaltsbuch:
    def __init__(self):
        self.ausgaben_datei = "ausgaben.txt"
        self.einnahmen_datei = "einnahmen.txt"
        self.erstelle_dateien()

    def erstelle_dateien(self):
        if not os.path.exists(self.ausgaben_datei):
            with open(self.ausgaben_datei, "w") as file:
                pass
        if not os.path.exists(self.einnahmen_datei):
            with open(self.einnahmen_datei, "w") as file:
                pass

    def ausgabe_hinzufügen(self, kategorie, betrag):
        with open(self.ausgaben_datei, "a") as file:
            file.write(f"{kategorie}: {betrag}\n")

    def einnahme_hinzufügen(self, kategorie, betrag):
        with open(self.einnahmen_datei, "a") as file:
            file.write(f"{kategorie}: {betrag}\n")

    def gesamtausgaben_anzeigen(self):
        with open(self.ausgaben_datei, "r") as file:
            ausgaben_text = file.read()
        return ausgaben_text

    def gesamteinnahmen_anzeigen(self):
        with open(self.einnahmen_datei, "r") as file:
            einnahmen_text = file.read()
        return einnahmen_text

    def gesamtüberschuss_anzeigen(self):
        with open(self.einnahmen_datei, "r") as file:
            einnahmen = [float(line.split(":")[1]) for line in file.readlines()]
        with open(self.ausgaben_datei, "r") as file:
            ausgaben = [float(line.split(":")[1]) for line in file.readlines()]
        einnahmen_summe = sum(einnahmen)
        ausgaben_summe = sum(ausgaben)
        überschuss = einnahmen_summe - ausgaben_summe
        return f"Gesamtüberschuss: {überschuss}"

def ausgabe_eintragen():
    kategorie = kategorie_entry.get()
    betrag = float(betrag_entry.get())
    haushaltsbuch.ausgabe_hinzufügen(kategorie, betrag)
    messagebox.showinfo("Erfolg", "Ausgabe hinzugefügt!")
    kategorie_entry.delete(0, tk.END)
    betrag_entry.delete(0, tk.END)

def einnahme_eintragen():
    kategorie = kategorie_entry.get()
    betrag = float(betrag_entry.get())
    haushaltsbuch.einnahme_hinzufügen(kategorie, betrag)
    messagebox.showinfo("Erfolg", "Einnahme hinzugefügt!")
    kategorie_entry.delete(0, tk.END)
    betrag_entry.delete(0, tk.END)

def gesamtausgaben_anzeigen():
    ausgaben_text = haushaltsbuch.gesamtausgaben_anzeigen()
    messagebox.showinfo("Gesamtausgaben", ausgaben_text)

def gesamteinnahmen_anzeigen():
    einnahmen_text = haushaltsbuch.gesamteinnahmen_anzeigen()
    messagebox.showinfo("Gesamteinnahmen", einnahmen_text)

def gesamtüberschuss_anzeigen():
    überschuss_text = haushaltsbuch.gesamtüberschuss_anzeigen()
    messagebox.showinfo("Gesamtüberschuss", überschuss_text)

if __name__ == "__main__":
    haushaltsbuch = Haushaltsbuch()

    root = tk.Tk()
    root.title("Haushaltsbuch")

    label_kategorie = tk.Label(root, text="Kategorie:")
    label_kategorie.grid(row=0, column=0)

    kategorie_entry = tk.Entry(root)
    kategorie_entry.grid(row=0, column=1)

    label_betrag = tk.Label(root, text="Betrag:")
    label_betrag.grid(row=1, column=0)

    betrag_entry = tk.Entry(root)
    betrag_entry.grid(row=1, column=1)

    button_ausgabe = tk.Button(root, text="Ausgabe hinzufügen", command=ausgabe_eintragen)
    button_ausgabe.grid(row=2, column=0)

    button_einnahme = tk.Button(root, text="Einnahme hinzufügen", command=einnahme_eintragen)
    button_einnahme.grid(row=2, column=1)

    button_gesamtausgaben = tk.Button(root, text="Gesamtausgaben anzeigen", command=gesamtausgaben_anzeigen)
    button_gesamtausgaben.grid(row=3, column=0)

    button_gesamteinnahmen = tk.Button(root, text="Gesamteinnahmen anzeigen", command=gesamteinnahmen_anzeigen)
    button_gesamteinnahmen.grid(row=3, column=1)

    button_gesamtüberschuss = tk.Button(root, text="Gesamtüberschuss anzeigen", command=gesamtüberschuss_anzeigen)
    button_gesamtüberschuss.grid(row=4, column=0, columnspan=2)

    root.mainloop()
