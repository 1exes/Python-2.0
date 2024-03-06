import tkinter as tk
from tkinter import messagebox

import mysqlx-connetor




class Haushaltsbuch:
    def __init__(self):
        self.verbindung = mysqlx.connector.connect(
            host="localhost",
            user="benutzername",
            password="passwort",
            database="haushaltsbuch_db"
        )
        self.cursor = self.verbindung.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS ausgaben (id INT AUTO_INCREMENT PRIMARY KEY, kategorie VARCHAR(255), betrag FLOAT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS einnahmen (id INT AUTO_INCREMENT PRIMARY KEY, kategorie VARCHAR(255), betrag FLOAT)")
        self.verbindung.commit()

    def ausgabe_hinzufügen(self, kategorie, betrag):
        self.cursor.execute("INSERT INTO ausgaben (kategorie, betrag) VALUES (%s, %s)", (kategorie, betrag))
        self.verbindung.commit()

    def einnahme_hinzufügen(self, kategorie, betrag):
        self.cursor.execute("INSERT INTO einnahmen (kategorie, betrag) VALUES (%s, %s)", (kategorie, betrag))
        self.verbindung.commit()

    def gesamtausgaben_anzeigen(self):
        self.cursor.execute("SELECT * FROM ausgaben")
        ausgaben = self.cursor.fetchall()
        ausgaben_text = "Gesamtausgaben:\n"
        for ausgabe in ausgaben:
            ausgaben_text += f"{ausgabe[1]}: {ausgabe[2]}\n"
        return ausgaben_text

    def gesamteinnahmen_anzeigen(self):
        self.cursor.execute("SELECT * FROM einnahmen")
        einnahmen = self.cursor.fetchall()
        einnahmen_text = "Gesamteinnahmen:\n"
        for einnahme in einnahmen:
            einnahmen_text += f"{einnahme[1]}: {einnahme[2]}\n"
        return einnahmen_text

    def gesamtüberschuss_anzeigen(self):
        self.cursor.execute("SELECT SUM(betrag) FROM einnahmen")
        einnahmen_summe = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT SUM(betrag) FROM ausgaben")
        ausgaben_summe = self.cursor.fetchone()[0]
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

