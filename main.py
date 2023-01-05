# Notizen: README.md #

import sqlite3
import time
from time import localtime, strftime
import functions as f




hours = 0

zeitraw = strftime("%X", localtime())
hours, _, _ = zeitraw.split(":")

hours = int(hours)

if hours <= 12 and hours > 5:
    zeit = 1
elif hours > 12 and hours <= 18:
    zeit = 2
else:
    zeit = 3



conn = sqlite3.connect("database.db")

cur = conn.cursor()

option1 = ["1", "1)", "eins", "Eins", "EINS"]
option2 = ["2","2)","zwei","Zwei","ZWEI"]
option3 = ["3","3)","drei","Drei","DREI"]
option4 = ["4","4)","vier","Vier","VIER","fier","Fier","FIER"]
option5 = ["5","5)","fünf","Fünf","FÜNF"]
option6 = ["6","6)","sechs","Sechs","SECHS"]
option7 = ["7","7)","sieben","Sieben","SIEBEN"]
exitoption = ["exit","quit","close","abbrechen","schließen"]

print("Herzlich Wilkommen im Supermarktsystem! Wählen Sie eine der folgenden Aktionen aus:")
print(2*"\n")

try:
    while True:
        print("""
    Optionen:

    1) Alle Produkte auflisten.
    2) Ein neues Produkt hinzufügen.
    3) Den Preis eines Produktes herrausfinden
    4) Lagerbestand eines Produktes herrausfinden
    5) Preis eines Produktes ändern
    6) Lagerbestand eines Produktes ändern
        """)


        answer = input("Option auswählen: ")
        if answer in exitoption:
            raise KeyboardInterrupt
        elif answer in option1:
            #Alle Produkte auflisten
            f.auflisten(cur)
            time.sleep(1)
            print(3*"\n")
        elif answer in option2:
            #Neues Produkt hinzufügen
            f.hinzufügen(cur)
            print(3*"\n")
            conn.commit()
        elif answer in option3:
            #Preis herausfinden
            f.get_property(cur, "preis")
            print(3*"\n")
        elif answer in option4:
            #Lagerbestand herrausfinden
            f.get_property(cur, "lager")
            print(3*"\n")
        elif answer in option5:
            #Preis ändern
            f.update_property(cur, "preis")
            conn.commit()
        elif answer in option6:
            #Lagerbestand ändern
            f.update_property(cur, "lager")
            conn.commit()



        else:
            print("Bitte wählen Sie eine gültige Option aus!")


except KeyboardInterrupt:
    print("\n"*5)
    if zeit == 1:
        print("Haben Sie noch einen angenehmen Morgen!")
    elif zeit == 2:
        print("Haben Sie noch einen angenehmen Tag!")
    elif zeit == 3:
        print("Haben Sie noch eine ruhige Nacht!")


