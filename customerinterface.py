import customtkinter
import sqlite3
import customerfunctions as cf
import cv2
from pyzbar.pyzbar import decode

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font_big = customtkinter.CTkFont("Roboto", 15)
        self.font_normal = customtkinter.CTkFont("Roboto", 12)
        self.create_widgets()

    def create_widgets(self):
        self.qr_button = customtkinter.CTkButton(master=self, text="Produkt scannen", font=self.font_normal, command=self.qr_func)
        self.qr_button.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        self.messagelabel = customtkinter.CTkLabel(master=self, text="", font=self.font_normal)
        self.messagelabel.grid(row=0, column=1, pady=20, padx=20, sticky="ew")

        self.cartlist = customtkinter.CTkTextbox(master=self, font=self.font_normal, state="disabled", activate_scrollbars=False)
        self.cartlist.grid(row=1, column=0, columnspan=2, sticky="nesw")
    
    def qr_func(self):
        result = cf.get_qr_code()
        if result == None:
            self.messagelabel.configure(text="Kein Produkt gefunden!")
        else:
            answer = self.qr_evaluate(result)
            if answer == None:
                return
            (name, price, stock) = answer
            self.messagelabel.configure(text=f"Produkt: {name}; Mit dem Preis: {price} und der Verfügbarkeit von {stock} Lagereinheiten")
        pass

    def qr_evaluate(self, code: int):
        try:
            code = int(code)
            result = cf.get_from_id(cur, code)
            if result == None:
                self.messagelabel.configure(text="Fehler! Produkt konnte nicht gefunden werden! Bitte konsultieren Sie einen Mitarbeiter")
            elif result == "Error":
                self.messagelabel.configure(text="Fehler! Bitte konsultieren Sie einen Mitarbeiter!")
                pass
            return result
        except ValueError:
            self.messagelabel.configure(text="Fehler! Bitte konsultiern Sie einen Mitarbeiter!")
        pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Customerinterface")
        self.attributes("-fullscreen", True)
        self.state("zoomed")

        self.font_header = customtkinter.CTkFont("Roboto", 24)
        self.font_label = customtkinter.CTkFont("Roboto", 12)

        self.rowconfigure(1, weight=1)
        self.columnconfigure((0,1), weight=1)

        self.after(100, self.create_widgets)

    def create_widgets(self):

        self.header_label = customtkinter.CTkLabel(master=self, text="Selbstbedienungskasse", font=self.font_header)
        self.header_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.itemcartframe = MainFrame(self)
        self.itemcartframe.grid(row=1, column=0, columnspan=2, sticky="nesw", pady=30, padx=30)

        self.closebtn = customtkinter.CTkButton(master=self, text="Schließen", font=self.font_label, command=self.close)
        self.closebtn.grid(row=5, column=0, pady=20, padx=20, sticky="sw")


    def close(self):
        self.destroy()

conn = sqlite3.connect("database.db")
cur = conn.cursor()

if __name__ == "__main__":
    app = App()
    app.mainloop()