for x in ("(1) Gruppe","(2) Gruppe","(3) Gruppe","(49 Beutzerdefinirt"):
    print(x)



gruppe1 = input("Bitte Gruppe Wählen :")


match gruppe1:
    case "1":
        print()
        print("Beine","Brust","Ausführung")
        übung1 = input("welche Übung?:")

        match übung1:
            case "Brust":
                print("50m brust","....")

            case "Beine":
                print("50m Rücken")

            case "Ausführung":
                print("50m mit Bret")
    case "2":
        print()
        print("Beine", "Brust", "Ausführung")
        übung2 = input("welche Übung?:")

        match übung2:
            case "Brust":
                print("150m brust", "....")

            case "Beine":
                print("150m Rücken")

            case "Ausführung":
                print("150m mit Bret")

    case "3":
        print()
        print("Beine", "Brust", "Ausführung")
        übung3 = input("welche Übung?:")

        match übung3:
            case "Brust":
                print("300m brust", "....")

            case "Beine":
                print("300m Rücken")

            case "Ausführung":
                print("300m mit Bret")

    case "4":
        print()
        print("150m","300m","600m","1500m")
        übung4 =input("Wie viele meter :")

        match übung4:
            case "150m":
                print("150m...")


            case "300m":
                print("300m,,,")

            case "600m":
                print("600m..")

            case "1500m":
                print("1500m...")
