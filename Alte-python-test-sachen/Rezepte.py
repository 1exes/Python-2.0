class Login:
    error = None
    def __init__(self, uid, passw):
        self.uid = "user"
        self.passw = "user"
        Login.error = "Enter a valid user id and password"

    def authenticate(self):
        if (self.uid == logid and self.passw == logpass):
            print ("Login successful")
        else:
            print (Login.error)
log = Login("", "")
logid = input("Enter your user ID: ")
logpass = input("Enter your password: ")


log.authenticate()




for x in ["(1) Pfannkuschen","(2) Waffeln","(3) Käsekuchen"]:
    print(x)

auswahl = int(input("Bitte wähle ein Rezept:"))
print()
if auswahl == 1:
    for g in ["200g Gramm Weizenmehl","400 mL Milch","3	Eier","2 Essloffel Zucker","50g Butter"]:
        print(g)
if auswahl == 2:
    for h in ["150g Butter","100g Zucker","4 Eier","250g Weizenmehl","50g Speisestarke","2 Teeloffel Backpulver","1	Prise Salz","300 mL	Milch "]:
        print(h)
elif auswahl == 3:
        for j in ["120 g weiße Schokolade","120 g Frischkäse","3 Eier"]:
            print(j)












