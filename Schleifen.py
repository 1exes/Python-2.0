berchnung_zu_stunden = 24
name_of_unit = "Stunden"



def tage_zu_units(anzhal_von_Tagen,eigene_nachricht):
    if anzhal_von_Tagen > 0:
        return f"{anzhal_von_Tagen} Tage sind {anzhal_von_Tagen * berchnung_zu_stunden} {name_of_unit}"
    else:
        return "die zahl ist negativ und kann nicht verarbeite werden"



user_input = input("Gebe deine anzahl an tagen an die in stunden umgerechnet erden sollen")
user_input_number = int(user_input)

calculated_value = tage_zu_units(user_input_number)
print(calculated_value)
