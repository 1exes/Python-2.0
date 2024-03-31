from random2 import randint

# Anzahl der Videos, Start- und Endzahl abfragen
start_number = int(input("Startzahl: "))
end_number = int(input("Endzahl: "))

# Zufällige Zahl generieren und ausgeben
random_num = randint(start_number, end_number)
print(f"Zufällige Zahl zwischen {start_number} und {end_number}: {random_num}")
