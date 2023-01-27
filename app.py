import customtkinter
import sqlite3
import functions as cf
import time     

class Buttons(customtkinter.CTkFrame):
    def __init__(self, *args, command_add, total_func, itemlist_func, **kwargs):
        super().__init__(*args, **kwargs)

        self.command_add = command_add
        self.total = total_func
        self.itemlist_func = itemlist_func

        self.columnconfigure(0, weight=1)

        self.headlabel_font = customtkinter.CTkFont(family="sans-serif", size=20)
        self.btn_font = customtkinter.CTkFont(family="sans-serif", size=16)

        self.headlabel = customtkinter.CTkLabel(master=self, text="Kassen\nbuttons", font=self.headlabel_font)
        self.headlabel.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.addToCart = customtkinter.CTkButton(master=self, text="Produkt hinzufügen", command=self.command_add, font=self.btn_font)
        self.addToCart.grid(row=1, column=0, padx=0, pady=5, sticky="ew")

        self.totalbtn = customtkinter.CTkButton(master=self, text="Show Total", command=self.total, font=self.btn_font)
        self.totalbtn.grid(row=2, column=0, padx=0, pady=5, sticky="ew")

        self.itemlistbtn = customtkinter.CTkButton(master=self, text="Produktliste", command=self.itemlist_func, font=self.btn_font)
        self.itemlistbtn.grid(row=3, column=0, padx=0, pady=5, sticky="ew")


class VerwaltungsButtons(customtkinter.CTkFrame):
    def __init__(self, *args, addProducts_func, deleteProduct_func, editProduct_func, **kwargs):
        super().__init__(*args, **kwargs)

        self.editProduct_func = editProduct_func
        self.addProducts_func = addProducts_func
        self.deleteProduct_func = deleteProduct_func
        self.columnconfigure(0, weight=1)

        self.headlabel_font = customtkinter.CTkFont(family="sans-serif", size=20)
        self.btn_font = customtkinter.CTkFont(family="sans-serif", size=16)

        self.headlabel = customtkinter.CTkLabel(master=self, text="Verwaltungs\nbuttons", font=self.headlabel_font)
        self.headlabel.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.addNewProduct = customtkinter.CTkButton(master=self, text="Neues Produkt erstellen", command=self.addProducts_func, font=self.btn_font)
        self.addNewProduct.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.editProductbtn = customtkinter.CTkButton(master=self, text="Produkt bearbeiten", command=self.editProduct_func, font=self.btn_font)
        self.editProductbtn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.removeproductbtn = customtkinter.CTkButton(master=self, text="Produkt löschen", command=self.deleteProduct_func, font=self.btn_font)
        self.removeproductbtn.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    def nothing(self):
        pass

class AddToCart(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Produkt dem Warenkorb hinzufügen")
        self.geometry("50+20")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(10, self.startup)
        self.grab_set()

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.header_font = customtkinter.CTkFont("sans-serif", 20)
        self.normal_font = customtkinter.CTkFont("sans-serif", 12)

    def create_widgets(self):
        
        self.header_label = customtkinter.CTkLabel(master=self, text="Produkt hinzufügen", font=self.header_font)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

        self.selectproductlabel = customtkinter.CTkLabel(master=self, text="Produkt:", font=self.normal_font)
        self.selectproductlabel.grid(row=1, column=0, pady=20, padx=10, sticky="e")

        self.productselectbox = customtkinter.CTkOptionMenu(master=self, values=self.namelist, font=self.normal_font, command=self.handle_product)
        self.productselectbox.grid(row=1, column=1, pady=20, padx=10, sticky="w")

        self.stockmessage = customtkinter.CTkLabel(master=self, text="", font=self.normal_font, text_color="green")
        self.stockmessage.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        self.amountlabel = customtkinter.CTkLabel(master=self, text="Stückzahl", font=self.normal_font)
        self.amountlabel.grid(row=3, column=0, pady=20, padx=10, sticky="e")

        self.amountentry = customtkinter.CTkEntry(master=self, textvariable=self.amountvariable)
        self.amountentry.grid(row=3, column=1, pady=20, padx=10, sticky="e")

        pass

    def handle_product(self):
        pass

    def startup(self):
        self.amountvariable = customtkinter.StringVar(master=self, value="1")
        self.itemlist, self.namelist = cf.get_every_name(cur)
        self.create_widgets()
        pass

    def close(self):
        self.grab_release()
        self.destroy()


class TopLevelItemList(customtkinter.CTkToplevel):
    def __init__(self, *args, itemstr, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.itemstr = itemstr
        self.title("Produktliste")
        self.geometry("10+10")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.after(10, self.create_widges)
        self.after(20000, self.on_close)
        self.bind("<Button>", self.on_close)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.grab_set()
        self.update_idletasks()
        self.overrideredirect(1)

        self.configure(borderwidth=5, relief="solid")
        
        self.header_font = customtkinter.CTkFont(family="sans-serif", size=20)
        self.list_font = customtkinter.CTkFont(family="sans-serif", size=18)
    
    def create_widges(self):

        self.header_label = customtkinter.CTkLabel(master=self, text="Produktliste:", font=self.header_font)
        self.header_label.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        self.itemlist = customtkinter.CTkLabel(master=self, text=self.itemstr, font=self.list_font, justify="left")
        self.itemlist.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
    
    def on_close(self, *args):
        self.grab_release()
        self.destroy()

class AddProducts(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Neues Produkt erstellen")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(10, self.create_widgets)


        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1), weight=1)

        self.header_font = customtkinter.CTkFont(family="sans-serif", size=20)
        self.label_font = customtkinter.CTkFont(family="sans-serif", size=14)
        self.error_font = customtkinter.CTkFont(family="sans-serif", size=12)


    def create_widgets(self):
        
        self.headerlabel = customtkinter.CTkLabel(master=self, text="Neues Produkt erstellen", font=self.header_font)
        self.headerlabel.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.namelabel = customtkinter.CTkLabel(master=self, text="Produktname:", justify="right")
        self.namelabel.grid(row=1, column=0, sticky="e")

        self.nameentry = customtkinter.CTkEntry(master=self)
        self.nameentry.grid(row=1, column=1, sticky="w")

        self.pricelabel = customtkinter.CTkLabel(master=self, text="Preis:", justify="right")
        self.pricelabel.grid(row=2, column=0, sticky="e")

        self.priceentry = customtkinter.CTkEntry(master=self, font=self.label_font)
        self.priceentry.grid(row=2, column=1, sticky="w")

        self.stocklabel = customtkinter.CTkLabel(master=self, text="Lagereinheiten:", font=self.label_font, justify="right")
        self.stocklabel.grid(row=3, column=0, sticky="e")

        self.stockentry = customtkinter.CTkEntry(master=self, font=self.label_font)
        self.stockentry.grid(row=3, column=1, sticky="w")

        self.error_message = customtkinter.CTkLabel(master=self, font=self.error_font, text_color="yellow", text="")
        self.error_message.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.add_button = customtkinter.CTkButton(master=self, text="Produkt hinzufügen", font=self.label_font, command=self.add_product)
        self.add_button.grid(row=5, column=0, sticky="ew", pady=20, padx=20)

        self.cancel_button = customtkinter.CTkButton(master=self, text="Abbrechen", font=self.label_font, command=self.close)
        self.cancel_button.grid(row=5, column=1, sticky="ew", pady=20, padx=20)

        self.nameentry.focus_set()



    def add_product(self):
        name = self.nameentry.get()
        name = name.strip()
        if name == "":
            self.error_message.configure(text="Kein Name angegeben!")
            pass
        price = self.priceentry.get()
        price = price.strip()
        if price == "":
            self.error_message.configure(text="Kein Preis angegeben!")
            pass
        stock = self.stockentry.get()
        stock = stock.strip()
        if stock == "":
            stock == 0
        try:
            stock = int(stock)
        except:
            self.error_message.configure(text="Lagereinheiten ist keine gültige Zahl!")
            pass
        if price.endswith("€"):
            price = price.strip("€")
        if price.find(",") > 0:
            price = price.replace(",", ".")
        try:
            price = float(price)
        except:
             price=0.0
             self.error_message.configure(text="Preis ist keine gültige Zahl!")
             pass
        name = name.strip()
        name = str(name)
        price = str(price)
        stock = str(stock)
        try:
            cur.execute(f"INSERT INTO products (name, price, stock) VALUES ('{name}','{price}','{stock}')")
            conn.commit()
            self.error_message.configure(text="YAY! Produkt erstellt!", text_color = "green")
            self.close()
        except:
            self.error_message.configure(text="Nöööööööööööööööö")
            pass
        

    def close(self):
        self.grab_release()
        self.destroy()

class Remove_Product(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Product entfernen")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", func=self.close)
        self.after(10, self.startup)
        self.destructbutton_fg_color = "#FF2815"
        self.headerlabel_font = customtkinter.CTkFont(family="sans-serif", size=22)
        self.normal_font = customtkinter.CTkFont(family="sans-serif", size=14)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.startup()

    def startup(self):
        self.itemlist, self.namelist = cf.get_every_name(cur)
        self.create_widgets()

    def create_widgets(self):
        self.headerlabel = customtkinter.CTkLabel(master=self, text="Produkt löschen", font=self.headerlabel_font, text_color="red")
        self.headerlabel.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

        self.productselectlabel = customtkinter.CTkLabel(master=self, text="Produkt auswählen:", font=self.normal_font)
        self.productselectlabel.grid(row=1, column=0, sticky="e", pady=20, padx=20)

        self.productselect = customtkinter.CTkOptionMenu(master=self, values=self.namelist, font=self.normal_font, dropdown_font=self.normal_font, command=self.set_info)
        self.productselect.grid(row=1, column=1, sticky="ew", pady=20, padx=20)

        self.productselect.set("--Produkt wählen--")

        self.productinfolabel = customtkinter.CTkLabel(master=self, text="", font=self.normal_font)
        self.productinfolabel.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        
        self.removebtn = customtkinter.CTkButton(master=self, text="Produkt löschen", text_color="red", command=self.run_accept_choice, state="disabled")
        self.removebtn.grid(row=3, column=0, pady=20, padx=20, sticky="ew")

        self.quitbtn = customtkinter.CTkButton(master=self, text="Abbrechen", command=self.close)
        self.quitbtn.grid(row=3, column=1, pady=20, padx=20, sticky="ew")

    def run_accept_choice(self):
        self.grab_release()
        self.accept_choice()

    def accept_choice(self):

        self.warning_popup = customtkinter.CTkToplevel(fg_color="#8a0000")
        self.warning_popup.title("ALARM!!!")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.warninglabel = customtkinter.CTkLabel(master=self.warning_popup, text=f"Sie sind im Begriff \"{self.itemtodelete}\" entgültig zu löschen. Diese Aktion ist irreversibel!", font=self.headerlabel_font)
        self.warninglabel.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

        self.deletebtn = customtkinter.CTkButton(master=self.warning_popup, text="Entgültig löschen", fg_color="red", hover_color="#800000", text_color="white", font=self.normal_font, command=self.delete_forever)
        self.deletebtn.grid(row=1, column=0, pady=20, padx=20, sticky="ew")
        self.deletebtn.configure(state="disabled")

        self.cancelbtn = customtkinter.CTkButton(master=self.warning_popup, text="Abbrechen", command=self.accept_choice_close)
        self.cancelbtn.grid(row=1, column=1, pady=20, padx=20, sticky="ew")
        
    
    def accept_choice_close(self):
        self.warning_popup.grab_release()
        self.warning_popup.destroy()
        self.close()

    def delete_forever(self):
        cur.execute(f"DELETE FROM products WHERE name=\'{self.itemtodelete}\'")
        conn.commit()
        self.accept_choice_close()
        self.close()
        pass

    def set_info(self, choice):
        for i in range(len(self.itemlist)):
            name, price, stock = self.itemlist[i]
            if name == choice:
                self.productinfolabel.configure(text=f"Produktname: {name} / Preis: {price} / Lagereinheiten: {stock}")
                self.itemtodelete = name
            else:
                continue
        self.removebtn.configure(state="normal")


    def close(self):
        self.grab_release()
        self.destroy()

class Edit_Product(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Produkt bearbeiten")
        self.grab_set()
        self.protocol("WM_DELTE_WINDOW", func=self.close)
        self.after(10, self.startupp)

        self.header_font = customtkinter.CTkFont(family="sans-serif", size=22)
        self.normal_font = customtkinter.CTkFont(family="sans-serif", size=14)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1, weight=1)


    def create_widgets(self):
        self.header = customtkinter.CTkLabel(master=self, text="Produkt bearbeiten", font=self.header_font)
        self.header.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky="ew")

        self.productselectlabel = customtkinter.CTkLabel(master=self, text="Produkt auswählen:", font=self.normal_font)
        self.productselectlabel.grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        self.productselectmenu = customtkinter.CTkOptionMenu(master=self, values=self.namelist, font=self.normal_font, command=self.enable_modify)
        self.productselectmenu.grid(row=1, column=1, pady=20, padx=20, sticky="ew")
        self.productselectmenu.set("Produkt wählen!")

        self.productnamelabel = customtkinter.CTkLabel(master=self, text="Produktname:", font=self.normal_font, anchor="e")
        self.productnamelabel.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
        self.productnamelabel.grid_forget()

        self.productnameentry = customtkinter.CTkEntry(master=self, font=self.normal_font, text_color="#4d4d4d", state="disabled")
        self.productnameentry.grid(row=2, column=1, pady=20, padx=20, sticky="ew")
        self.productnameentry.grid_forget()

        self.tick_productname = customtkinter.CTkCheckBox(master=self, text="Bearbeiten", command=self.checkbox_handle, onvalue="on", offvalue="off")
        self.tick_productname.grid()
        self.tick_productname.grid_forget()

        self.productpricelabel = customtkinter.CTkLabel(master=self, text="Preis:", font=self.normal_font, anchor="e")
        self.productpricelabel.grid(row=3, column=0, pady=20, padx=20, sticky="ew")
        self.productpricelabel.grid_forget()

        self.productpriceeentry = customtkinter.CTkEntry(master=self, font=self.normal_font, state="disabled", text_color="#4d4d4d")
        self.productpriceeentry.grid(row=3, column=1, pady=20, padx=20, sticky="ew")
        self.productpriceeentry.grid_forget()

        self.tick_productprice = customtkinter.CTkCheckBox(master=self, text="Bearbeiten", command=self.checkbox_handle, onvalue="on", offvalue="off")
        self.tick_productprice.grid()
        self.tick_productprice.grid_forget()

        self.productstocklabel = customtkinter.CTkLabel(master=self, text="Lagereinheiten:", font=self.normal_font, anchor="e")
        self.productstocklabel.grid(row=4, column=0, pady=20, padx=20, sticky="ew")
        self.productstocklabel.grid_forget()

        self.productstockentry = customtkinter.CTkEntry(master=self, font=self.normal_font, state="disabled", text_color="#4d4d4d")
        self.productstockentry.grid(row=4, column=1, pady=20, padx=20, sticky="ew")
        self.productstockentry.grid_forget()

        self.tick_productstock = customtkinter.CTkCheckBox(master=self, text="Bearbeiten", command=self.checkbox_handle, onvalue="on", offvalue="off")
        self.tick_productstock.grid()
        self.tick_productstock.grid_forget()

        self.edit_button = customtkinter.CTkButton(master=self, text="Produkt bearbeiten", command=self.edit, state="disabled")
        self.edit_button.grid()
        self.edit_button.grid_forget()

        self.cancel_button = customtkinter.CTkButton(master=self, text="Abbrechen", command=self.close)
        self.cancel_button.grid(row=5, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    def edit(self):
        name = self.name
        price = self.price
        stock = self.stock
        if self.tick_productname.get() == "on" and self.productnameentry.get() != name:
            try:
                cur.execute(f"UPDATE products SET name=\"{self.productnameentry.get()}\" WHERE name='{name}'")
                conn.commit()
            except:
                pass
        if self.tick_productprice.get() == "on" and self.productpriceeentry.get() != price:
            try:
                nprice = self.productpriceeentry.get()
                nprice = nprice.strip()
                nprice = nprice.removesuffix("€")
                try: 
                    nprice.replace(",",".")
                except:
                    pass
                nprice = float(nprice)
                cur.execute(f"UPDATE products SET price=\"{nprice}\" WHERE name='{name}'")
                conn.commit()
            except:
                pass
        if self.tick_productstock.get() == "on" and self.productstockentry.get() != stock:
            try:
                nstock = self.productpriceeentry.get()
                nstock = int(nstock)
                cur.execute(f"UPDATE products SET stock=\"{nstock}\" WHERE name='{name}'")
                conn.commit()
            except:
                pass
        pass

    def checkbox_handle(self):
        if self.tick_productname.get() == "off" and self.tick_productprice.get() == "off" and self.tick_productstock.get() == "off":
            self.edit_button.configure(state="disabled")
        else:
            self.edit_button.configure(state="normal")
        if self.tick_productname.get() == "on":
            self.productnameentry.configure(state="normal", text_color="white")
        elif self.tick_productname.get() == "off":
            self.productnameentry.configure(state="disabled", text_color="#4d4d4d")
            #check
            if self.productnameentry.get() == self.name:
                pass
            else:
                self.productnameentry.configure(state="normal")
                self.productnameentry.delete("0","end")
                self.productnameentry.insert("0", self.name)
                self.productnameentry.configure(state="disabled")
                pass
            pass
        
        if self.tick_productprice.get() == "on":
            self.productpriceeentry.configure(state="normal", text_color="white")
            pass
        elif self.tick_productprice.get() == "off":
            self.productpriceeentry.configure(state="disabled", text_color="#4d4d4d")
            
            if self.productpriceeentry.get() == self.price:
                pass
            else:
                self.productpriceeentry.configure(state="normal")
                self.productpriceeentry.delete("0","end")
                self.productpriceeentry.insert("0",self.price)
                self.productpriceeentry.configure(state="disabled")
                pass
            pass
            
            if self.tick_productstock.get() == "on":
                self.productstockentry.configure(state="normal", text_color="white")
                pass
            elif self.tick_productstock.get() == "off":
                self.productpriceeentry.configure(state="disabled", text_color="#4d4d4d")
                if self.productpriceeentry.get() == self.stock:
                    self.productstockentry.configure(state="normal")
                    self.productstockentry.delete("0","end")
                    self.productstockentry.insert("0",self.stock)
                    self.productstockentry.configure(state="disabled")
                pass
            pass

    def enable_modify(self, choice):
        self.edit_button.grid(row=5, column=0, pady=20, padx=20, sticky="ew")
        self.cancel_button.grid(row=5, column=1, columnspan=1, pady=20, padx=20, sticky="ew")
        for i in range(len(self.itemslist)):
            name, price, stock = self.itemslist[i]
            if name == choice:
                self.name = name
                self.price = str(price)
                self.stock = str(stock)
                self.productnameentry.configure(state="normal")
                self.productnameentry.delete("0","end")
                self.productnameentry.insert("0",self.name)
                self.productnameentry.configure(state="disabled")
                
                self.productpriceeentry.configure(state="normal")
                self.productpriceeentry.delete("0","end")
                self.productpriceeentry.insert("0",self.price)
                self.productpriceeentry.configure(state="disabled")

                self.productstockentry.configure(state="normal")
                self.productstockentry.delete("0","end")
                self.productstockentry.insert("0",self.stock)
                self.productstockentry.configure(state="disabled")

                self.productnamelabel.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
                self.productnameentry.grid(row=2, column=1, pady=20, padx=20, sticky="ew")
                self.tick_productname.grid(row=2, column=2, pady=20, padx=20, sticky="ew")
                self.productpricelabel.grid(row=3, column=0, pady=20, padx=20, sticky="ew")
                self.productpriceeentry.grid(row=3, column=1, pady=20, padx=20, sticky="ew")
                self.tick_productprice.grid(row=3, column=2, pady=20, padx=20, sticky="ew")
                self.productstocklabel.grid(row=4, column=0, pady=20, padx=20, sticky="ew")
                self.productstockentry.grid(row=4, column=1, pady=20, padx=20, sticky="ew")
                self.tick_productstock.grid(row=4, column=2, pady=20, padx=20, sticky="ew")
            else:
                continue

    def startupp(self):
        self.itemslist, self.namelist = cf.get_every_name(cur)
        self.after(10, self.create_widgets)
        pass

    
    def close(self):
        self.grab_release()
        self.destroy()

class TopLevelTotalvalue(customtkinter.CTkToplevel):
    def __init__(self, *args, totalvalue, **kwargs):
        super().__init__(*args, **kwargs)

        self.total = str(totalvalue)

        self.title("Total")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.labelfont = customtkinter.CTkFont(family="Courir", size=25)

        self.labeltext = "Total:  " + self.total + " €"
        self.after(10, self.create_widgets) #Widges entstehen erst nach kurzer verzögerung, verhindert flackern
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.grab_set()

    def create_widgets(self):

        self.totalvaluelabel = customtkinter.CTkLabel(master=self, text=self.labeltext, font=self.labelfont)
        self.totalvaluelabel.grid(row=0, column=0, pady=50, padx=50, sticky="nsew")
    
    def kassenzettel(self):
        pass

    def on_close(self):
        self.grab_release()
        self.destroy()



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.attributes('-fullscreen', True)
        self.state('zoomed')
        self.title("Supermarktsystem")
        self.after(10, self.create_widgets)

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_columnconfigure((0,1), weight=1)



    def create_widgets(self):
        self.header_font = customtkinter.CTkFont(family="sans-serif", size=50)
        self.button_font = customtkinter.CTkFont(family="sans-serif", size=18)
        self.list_font = customtkinter.CTkFont(family="Cascadia Mono", size=14)
        self.error_font = customtkinter.CTkFont(family="sans-serif", size=12)

        self.headerlabel = customtkinter.CTkLabel(master=self, text="Supermarktsystem", font=self.header_font)
        self.headerlabel.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ns")

        self.listtitle = customtkinter.CTkLabel(master=self, text="Produktliste:", font=self.button_font)
        self.listtitle.grid(row=1,column=1)

        self.buttons = Buttons(self, command_add=self.addtocartreally, total_func=self.Total_popup, itemlist_func=self.Itemlist_popup, fg_color="transparent")
        self.buttons.grid(row=2, column=0, rowspan=2, padx=5, pady=10, sticky="nse")

        self.verwaltungsbnts = VerwaltungsButtons(self, addProducts_func=self.createproduct, deleteProduct_func=self.deleteproduct, editProduct_func=self.editproduct)
        self.verwaltungsbnts.grid(row=2, column=0, rowspan=2, padx=5, pady=10, sticky="nw")

        self.CartList = customtkinter.CTkTextbox(master=self, state="disabled", activate_scrollbars=False, font=self.list_font)
        self.CartList.grid(row=2, column=1, rowspan=2, padx=40, pady=40, sticky="nsew")

        self.errormessage = customtkinter.CTkLabel(master=self, text="", text_color="yellow", font=self.error_font)
        self.errormessage.grid(row=3, column=1, padx=40, pady=0, sticky="sew")

        self.totalvaluefield = customtkinter.CTkTextbox(master=self, state="normal", activate_scrollbars=False, font=self.list_font, height=20, cursor="arrow")
        self.totalvaluefield.grid(row=4, column=1, padx=40, pady=20, sticky="e")
        self.totalvaluefield.insert("0.0", "0.0 €")
        self.totalvaluefield.configure(state="disabled")

        self.totalvaluelabel = customtkinter.CTkLabel(master=self, text="Total:", font=self.list_font, justify="right")
        self.totalvaluelabel.grid(row=4, column=1, padx=40, pady=20, sticky="ns")

        self.exitbutton = customtkinter.CTkButton(master=self, text="Schließen", command=self.destroy)
        self.exitbutton.grid(row=4, column=0, padx=20, pady=20, sticky="sw")

        global itemlist
        itemlist = []
        global totalvalue
        totalvalue = 0.0
        global value
        value = 0

    def close(self):
        self.destroy()
        pass

    def createproduct(self):
        AddProducts()
    
    def deleteproduct(self):
        Remove_Product()

    def editproduct(self):
        Edit_Product()

    def Itemlist_popup(self):
        
        cur.execute("SELECT name FROM products")
        result = cur.fetchall()
        itemstr = "Produkte:\n\n"
        for i in range(len(result)):
            item = result[i][0]
            item = item + "\n"
            itemstr = itemstr + item
        TopLevelItemList(itemstr=itemstr)
    
    def kassenzettel_gen(self):
        pass
        
    def Total_popup(self):
        global itemlist
        global totalvalue
        TopLevelTotalvalue(totalvalue=totalvalue)
        totalvalue = 0.0
        self.errormessage.configure(text="")
        self.CartList.configure(state="normal")
        self.CartList.delete("0.0", "end")
        self.CartList.configure(state="disabled")
        self.totalvaluefield.configure(state="normal")
        self.totalvaluefield.delete("0.0", "end")
        self.totalvaluefield.insert("0.0", "0.0 €")
        self.totalvaluefield.configure(state="disabled")
        print(itemlist)
        itemlist = []

    def addtocartreally(self):
        AddToCart()

    def addtocart(self):
        self.errormessage.configure(text="")
        global totalvalue
        dialog = customtkinter.CTkInputDialog(text="Welches Produkt soll hinzugefügt werden?", title="Kassensystem")
        answer = dialog.get_input()
        if answer == None or answer == "":
            self.errormessage.configure(text="Kein Produkt eingegeben!")
            pass
        if "'" in answer or '"' in answer or "\\" in answer or "/" in answer:
            self.errormessage.configure(text="Verbotenes Symbol erkannt!")
        else:
            self.errormessage.configure(text="")
            answer = str(answer)
            if answer == "":
                self.errormessage.configure(text="Produkt nicht gefunden!")
            else:
                answer = answer.strip() ## Remove whitespaces
                name, price, stock = cf.get_properties_returned(cur, answer)
                if name == None or price == None or name=="":
                    self.errormessage.configure(text="Produkt nicht gefunden!")
                elif stock == None or stock == 0:
                    self.errormessage.configure(text="Produkt nicht im Lager vorhanden!")
                else:
                    itemlist.append((name, price))
                    string = cf.display(name, price)
                    print(string)
                    self.CartList.configure(state="normal")
                    self.CartList.insert("0.0", "\n")
                    self.CartList.insert("0.0", string)
                    self.CartList.configure(state="disabled")
                    value = totalvalue + price
                    totalvalue = value
                    totalvalue = round(totalvalue, 2)
                    inputvalue = totalvalue
                    self.totalvaluefield.configure(state="normal")
                    self.totalvaluefield.delete("0.0", "end")
                    self.totalvaluefield.insert("0.0", f"{inputvalue} €")
                    self.totalvaluefield.configure(state="disabled")


conn = sqlite3.connect("database.db")
cur = conn.cursor()

customtkinter.set_default_color_theme("dark-blue")

if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        exit(1)