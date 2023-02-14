import customtkinter
import sqlite3
import customerfunctions as cf
import cv2
from pyzbar.pyzbar import decode
from lang import translations

global itemslist
global totalvalue
itemslist = []
totalvalue = 0.0


class App(customtkinter.CTk):
    def __init__(self):
        global translations
        super().__init__()

        self.title("Customerinterface")
        self.attributes("-fullscreen", True)
        self.state("zoomed")

        self.font_header = customtkinter.CTkFont("Roboto", 24)
        self.font_label = customtkinter.CTkFont("Roboto", 12)

        self.rowconfigure(1, weight=1)
        self.columnconfigure((0,1), weight=1)

        self.after(100, self.create_widgets)

        self.translation = translations['de']

    def create_widgets(self):

        self.header_label = customtkinter.CTkLabel(master=self, text=self.translation['header'], font=self.font_header)
        self.header_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.language_select = customtkinter.CTkSegmentedButton(master=self, values=['Deutsch', 'English', 'Français'], command=self.language_select)
        self.language_select.set(value='Deutsch')
        self.language_select.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        self.welcomeframe = WelcomeFrame(self, translation=self.translation)
        self.welcomeframe.grid(row=1, column=0, columnspan=2, sticky="nes", pady=30, padx=30)

        self.closebtn = customtkinter.CTkButton(master=self, text=self.translation['exit'], font=self.font_label, command=self.close_func)
        self.closebtn.grid(row=2, column=0, pady=20, padx=20, sticky="sw")

    def language_select(self, value):
        print(f"Value: {value}")
        if value == 'Français':
            print("Switching to Français")
            self.translation = translations['fr']
        if value == 'Deutsch':
            print("Switching to German")
            self.translation = translations['de']
        if value == 'English':
            print("Switching to English")
            self.translation = translations['en']
            pass

        self.header_label.configure(text=self.translation['header'])
        self.itemcartframe.destroy()
        self.itemcartframe = MainFrame(self, translation=self.translation)
        self.itemcartframe.grid(row=1, column=0, columnspan=2, sticky="nes", pady=30, padx=30)
        #Update MainFrame somehow
        pass

    def close_func(self):
        self.destroy()

    def openmainframe(self):
        self.itemcartframe = MainFrame(self, translation=self.translation)
        self.itemcartframe.grid(row=1, column=0, columnspan=2, sticky="nes", pady=30, padx=30)
        self.itemcartframe.grid_forget()

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, *args, translation, **kwargs):
        super().__init__(*args, **kwargs)

        self.translation = translation

        self.font_big = customtkinter.CTkFont("Roboto", 15)
        self.font_normal = customtkinter.CTkFont("Roboto", 12)
        self.font_cartlist = customtkinter.CTkFont("Cascadia Mono", 12)
        self.font_instructions = customtkinter.CTkFont("Roboto", 13)
        #self.columnconfigure(1, weight=1)
        #self.columnconfigure(0, weight=0)
        self.create_widgets()

    def create_widgets(self):
        self.qr_button = customtkinter.CTkButton(master=self, text=self.translation['scan'], font=self.font_normal, command=self.qr_func)
        self.qr_button.grid(row=0, column=0, pady=20, padx=20, sticky="e")

        self.messagelabel = customtkinter.CTkLabel(master=self, text="", font=self.font_normal)
        self.messagelabel.grid(row=0, column=0, pady=20, padx=20, sticky="es")

        self.instructions = customtkinter.CTkLabel(master=self, font=self.font_instructions, text=self.translation['instructions'], anchor="w", justify="left", bg_color="#484848", corner_radius=200)
        self.instructions.grid(row=2, column=0, sticky="sw", pady=20, padx=20)

        self.cartlist = customtkinter.CTkTextbox(master=self, font=self.font_cartlist, state="disabled", activate_scrollbars=False, text_color="#ffffff", width=500)
        self.cartlist.tag_add("tag1", "0.0", "end")
        self.cartlist.tag_config("tag1", justify="right")
        self.cartlist.grid(row=0, column=1, columnspan=1, sticky="nes", pady=20, padx=20)

        self.totalvaluelabel = customtkinter.CTkLabel(master=self, font=self.font_cartlist, text=self.translation['total'])
        self.totalvaluelabel.grid(row=1, column=1, pady=20, padx=20)

        self.totalvaluefield = customtkinter.CTkTextbox(master=self, font=self.font_cartlist, state="normal", activate_scrollbars=False, text_color="#ffffff", height=13)
        self.totalvaluefield.insert("0.0", "0,00 €")
        self.totalvaluefield.tag_add("tag2", "0.0", "end")
        self.totalvaluefield.tag_config("tag2", justify="right")
        self.totalvaluefield.configure(state="disabled")
        self.totalvaluefield.grid(row=1, column=1, columnspan=1, sticky="e", pady=20, padx=20)

    def qr_func(self):
        global totalvalue
        global itemslist
        result = cf.get_qr_code()
        if result == None:
            self.messagelabel.configure(text=self.translation['no_product_found'], text_color="#ff0000")
        else:
            answer = self.qr_evaluate(result)
            if answer == None:
                return
            (name, price, stock) = answer
            string = cf.display(name, price)
            if string == None:
                self.messagelabel.configure(text=f"{self.translation['error']} #2153", text_color="#ff0000")
            itemslist.append("name")
            print(f"0:TotalValue: {totalvalue}")
            totalvalue = totalvalue + price
            self.cartlist.configure(state="normal")
            self.cartlist.tag_remove("tag1", "0.0", "end")
            self.cartlist.insert("0.0", "\n")
            self.cartlist.insert("0.0", string)
            self.cartlist.tag_add("tag1", "0.0", "end")
            self.cartlist.tag_config("tag1", justify="right")
            self.cartlist.configure(state="disabled")
            value = totalvalue
            value = round(value, 2)
            totalvalue = value
            totalvaluestring = str(totalvalue) + " €"
            self.totalvaluefield.configure(state="normal")
            self.totalvaluefield.delete("0.0", "end")
            self.totalvaluefield.insert("0.0", totalvaluestring)
            self.totalvaluefield.configure(state="disabled")
            self.totalvaluefield.tag_add('tag2', "0.0", "end")
            self.totalvaluefield.tag_config("tag2", justify="right")
            stock = stock - 1
            cur.execute(f"UPDATE products SET stock ='{stock}' WHERE name='{name}'")
            conn.commit()
        pass

    def qr_evaluate(self, code: int):
        try:
            code = int(code)
            result = cf.get_from_id(cur, code)
            if result == None:
                self.messagelabel.configure(text=f"{self.translation['error']} #1637", text_color="#ff0000")
            elif result == "Error":
                self.messagelabel.configure(text=f"{self.translation['error']} #1634", text_color="#ff0000")
                pass
            return result
        except ValueError:
            self.messagelabel.configure(text=f"{self.translation['error']} #9631", text_color="#ff0000")
        pass

class WelcomeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, translation, **kwargs):
        super().__init__(*args, **kwargs)

        self.translation = translation

        self.font_big = customtkinter.CTkFont("Roboto", 30)
        self.font_normal = customtkinter.CTkFont("Roboto", 12)

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2), weight=1)

        self.create_widgets()

    def create_widgets(self):

        self.header = customtkinter.CTkLabel(master=self, text=self.translation['welcome_header'])
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.scanlabel = customtkinter.CTkLabel(master=self, text=self.translation['scanlabel'])

        pass

conn = sqlite3.connect("database.db")
cur = conn.cursor()

if __name__ == "__main__":
    app = App()
    app.mainloop()