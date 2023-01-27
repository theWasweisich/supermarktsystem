def display(name, price, amount="1x"):
    """ Beautifies the variables name, price, amount into one string for func. addtocart() """
    
    pricestr = str(price)
    pricelist = pricestr.split(".")
    if len(pricelist[0]) == 1:
        pricelist[0] = "0" + pricelist[0]
    if len(pricelist[1]) == 1:
        pricelist[1] = pricelist[1] + "0"
    pricestr = pricelist[0] + "." + pricelist[1]
    pricelen = len(pricestr)
    namelen = len(name)
    spaces = 20-(pricelen + namelen)
    strspaces = " "*spaces
    name = name.strip()
    amount = amount.strip()
    string = amount + " " + name + strspaces + pricestr + " €"
    return string

def beautify_result(result):
    print(33*" "+"\n"+"||"+" "*2+"Produkt"+" "*2+"||"+" "+"Preis"+" "+"||"+" "+"Lager"+" "+"||")
    print("||"+(" "*11)+"||"+(" "*7)+"||"+(" "*7)+"||")
    for i in range(len(result)):
        _, name, price, stock = result[i]
        abstand_name, abstand_price, abstand_stock = (11-len(name)), (7-len(str(price))), (7-len(str(stock)))
        print("||"+" "*abstand_name+f"{name}"+"||"+" "*abstand_price+f"{price}"+"||"+" "*abstand_stock+f"{stock}"+"||")
        print("||"+(" "*11)+"||"+(" "*7)+"||"+(" "*7)+"||")
    return

def auflisten(cursor):
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    beautify_result(result)
    return

def hinzufügen(cursor):
    name = input("Wie heißt das Produkt (<11 Zeichen): ")
    if len(name) >= 11:
        raise ValueError
    preis = input("Wie viel kostet das Produkt? ")
    preis = preis.strip()
    if preis.endswith("€"):
        preis = preis.strip("€")
    elif preis.find(",") > 0:
        preis = preis.replace(",", ".")
    try:
        preis = float(preis)
    except:
        print("Fehler!")
        preis = 0
        raise NameError("Hoppala!")
    stock = input(f'Wieviele Einheiten von "{name}" sind vorrätig? (Zahl) ')
    try:
        int(stock)
    except:
        print("Fehler: Eingabe keine natürliche Zahl!")
        stock = 0
        raise NameError("Hoppala!")
    answer = input(f"Möchten Sie Das Produkt \"{name}\" mit dem Preis von {preis}€ und dem Lagerbestand von {stock} hinzufügen? (Ja/Nein) ")
    if answer == "Ja" or answer == "JA":
        try:
            cursor.execute(f"INSERT INTO products (name, price, stock) VALUES ('{name}','{preis}','{stock}');")
        except:
            print("LÖL")
            pass
    else:
        print("\nDann halt nicht!")
        pass
    return

def get_property(cursor, type, answer=None):
    if answer == None:
        if type == "preis":
            answer = input("Von welchem Produkt möchten Sie den Preis wissen? ")
        elif type == "lager":
            answer = input("Von welchem Produkt möchten Sie den Lagerbestand wissen? ")
        else:
            pass
    print("\n"*3)
    answer = answer.strip() #Entfernt mögliche Leerzeichen am anfang / ende des Strings
    try:
        cursor.execute(f"SELECT * FROM products WHERE name='{answer}'")
        result = cursor.fetchall()
        if result == []:
            print("Produkt nicht gefunden!")
        for i in range(len(result)):
            _, name, preis, stock = result[i]
            preis = str(preis)
            preis = preis.replace(".",",")
            if type == "preis":
                print(f"Der aktuelle Preis für \"{name}\" ist {preis}€")
            elif type == "lager":
                print(f"Das Produkt \"{name}\" ist {stock}-mal vorhanden!")
            else:
                print("WTF IST HIER DENN LOS????????????")
                pass
    except:
        print("Da ist wohl etwas schiefgelaufen!")
        pass
    return


def update_property(cursor, type):
    if type == "preis":
        answer = input("Wessen Produkt möchten Sie den Preis ändern? ")
        product = answer.strip() #Entfernt mögliche Leerzeichen am anfang / ende des Strings
        get_property(cursor, "preis", product)
        try: #Testet, ob es dieses Produkt gibt.
            cursor.execute(f"SELECT id FROM products WHERE name=\"{product}\"")
            if cursor.fetchall() == []:
                print("Fehler! Product nicht gefunden. Bitte ernet versuchen!")
        except:
            print("Fehler! Produkt nicht gefunden. Bitte erneut versuchen!")
            pass
        preis = input(f"\nGeben Sie den neuen Preis für \"{product}\" an. ")
        preis = preis.strip() #Entfernt mögliche Leerzeichen am anfang / ende des Strings
        if preis.endswith("€"):
            preis = preis.strip("€")
        if preis.find(",") > 0:
            preis = preis.replace(",", ".")
        try:
            preis = float(preis)
            print(preis)
        except:
            print("Fehler!")
            preis = 0
            raise NameError("Hoppala!")
        sql = f"""UPDATE products SET price=\"{preis}\" WHERE name=\"{product}\""""
        try:
            cursor.execute(sql)
        except:
            print("Hoppala! Bitte erneut versuchen!")


    elif type == "lager":
        answer = input("Wessen Produkt möchten Sie den Lagerbestand ändern? ")
        product = answer.strip() #Entfernt mögliche Leerzeichen am anfang / ende des Strings
        get_property(cursor, "lager", product)
        try: #Testet, ob es dieses Produkt gibt.
            cursor.execute(f"SELECT id FROM products WHERE name=\"{product}\"")
            if cursor.fetchall() == []:
                print("Fehler! Product nicht gefunden. Bitte ernet versuchen!")
        except:
            print("Fehler! Produkt nicht gefunden. Bitte erneut versuchen!")
            pass
        stock = input(f"\nGeben Sie den neuen Lagerbestand für \"{product}\" an. ")
        stock = stock.strip() #Entfernt mögliche Leerzeichen am anfang / ende des Strings
        sql = f"""UPDATE products SET stock=\"{stock}\" WHERE name=\"{product}\""""
        try:
            cursor.execute(sql)
        except:
            print("Hoppala! Bitte erneut versuchen!")
    return

def get_properties_returned(cursor, product):
    cursor.execute(f"SELECT * FROM PRODUCTS WHERE name=\'{product}\'")
    response = cursor.fetchall()
    if response == []:
        return (None, None)
    for i in range(len(response)):
        _, name, price, stock = response[i]
        price = float(price)
        return (name, price, stock)

def get_every_name(cursor):
    """Returns
    
    1. A list with every item with its name, price and stock in a tupel
    2. A list with just every name of the products"""
    cursor.execute("SELECT * FROM products")
    response = cursor.fetchall()
    if response == []:
        return None
    list = []
    namelist = []
    for i in range(len(response)):
        _, name, price, stock = response[i]
        stock = int(stock)
        price = float(price)
        inputtupel = (name, price, stock)
        list.append(inputtupel)
        namelist.append(name)
    return list, namelist

def edit_stock(cursor, product, amount, operation):
    """

Edits the stock of a product with the name of "product" by the amount of "amount".

    """
    if operation == "-":
        try:
            cursor.execute(f"SELECT stock FROM products WHERE name='{product}'")
            old_stock = cursor.fetchall()
            if old_stock >= amount:
                stock = old_stock - amount
                cursor.execute(f"UPDATE products SET stock='{stock}' WHERE name='{product}'")
                return True
            else:
                return False
        except:
            return False

    if operation == "+":
        try:
            cursor.execute(f"SELECT * FROM products WHERE name='{product}'")
            old_stock = cursor.fetchall()
            stock = old_stock + amount
            cursor.execute(f"UPDATE products SET stock='{stock}' WHERE name='{product}'")
            return True
        except:
            return False