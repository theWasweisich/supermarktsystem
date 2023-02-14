import cv2
from pyzbar.pyzbar import decode
import sqlite3

def get_qr_code():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    _, frame = cap.read()
    gray_image = cv2.cvtColor(frame, 0)
    barcode = decode(gray_image)
    
    for obj in barcode:
        barcodeData = obj.data.decode("utf-8")
        return barcodeData

def get_from_id(cur: sqlite3.Cursor, id: int):
    """
    gets product information with the given id.
    returns a tupel of (name, price, stock) if available.
    If not, returns None
    """
    try:
        cur.execute(f"SELECT * FROM products WHERE id='{id}'")
        result = cur.fetchall()
        if len(result) > 0:
            answer = result[0]
            _, name, price, stock, _ = answer
            return name, price, stock
        else:
            return None
    except:
        return "Error"

def display(name, price, amount="1x"):
    """ Beautifies the variables name, price, amount into one string"""
    
    pricestr = str(price)
    if not pricestr.find(".") == -1:
        print("ja")
        pricelist = pricestr.split(".")
        if len(pricelist[0]) == 1:
            pricelist[0] = "0" + pricelist[0]
        elif len(pricelist[1]) == 1:
            pricelist[1] = pricelist[1] + "0"
        else:
            return None
        pricestr = pricelist[0] + "." + pricelist[1]
    pricelen = len(pricestr)
    namelen = len(name)
    spaces = 20-(pricelen + namelen)
    strspaces = " "*spaces
    name = name.strip()
    amount = amount.strip()
    string = amount + " " + name + strspaces + pricestr + " €"
    return string
