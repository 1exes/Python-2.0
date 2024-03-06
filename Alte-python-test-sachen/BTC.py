BTC =float(19334.00)
ETH =float(1623.00)
Matic =float(1.80)




for x in [ "(1) BTC", "(2) ETH", "(3) Matic","(4) Benutzer"]:
    print(x)

coin = int(input("Bitte coin eingeben :"))

if 4:
    test1 = float(input("Bitte geben sie denn preis von dem coin an:"))
    test2 = float(input("Geben sie an wie viel coins sie haben :"))
    print(str(test1 * test2) + "€ ist es gerade wert ")
    exit("Programm ENDE")




menge = int(input("Bitte geben sie ihre menge ein :"))



match coin:

    case 1:
        ergebnis1 = BTC * menge
        print(str(ergebnis1)+"€")

    case 2:
        ergebnis2 = ETH * menge
        print(str(ergebnis2)+"€")

    case 3:
        ergbnis3 = Matic * menge
        print(str(ergbnis3)+"€")


















