# Taschenrechner von Us0R
# -*- coding: cp1252 -*-

def wahl():
    print('1. = " + ", 2. = " - ", 3. = " * ", 4. = " : "')


while True:
    print("Whählen sie aus :")
    wahl()
    d = input()
    if (d == 1):
        print("Geben sie die erste Zahl ein")
        a = input()
        ...

    print("Wollen sie das Program beenden?(Y/N)")
    a = input()
    if a.upper() == "Y":
        break
