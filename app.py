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

        self.addToCart = customtkinter.CTkButton(master=self, text="Produkt hinzufügen", command=self.command_add)
        self.addToCart.grid(row=0, column=0, padx=0, pady=5)

        self.totalbtn = customtkinter.CTkButton(master=self, text="Show Total", command=self.total)
        self.totalbtn.grid(row=1, column=0, padx=0, pady=5)

        self.itemlistbtn = customtkinter.CTkButton(master=self, text="Produktliste", command=itemlist_func)
        self.itemlistbtn.grid(row=2, column=0, padx=0, pady=5)

class TopLevelItemList(customtkinter.CTkToplevel):
    def __init__(self, *args, itemstr, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.itemstr = itemstr
        self.title("Produktliste")
        self.geometry("10+10")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.after(10, self.create_widges)
        self.after(5000, self.on_close)
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
        print("Holla!")
        self.grab_release()
        self.destroy()

class AddProducts(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)

        self.title("Neues Produkt erstellen")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(10, self.close)


        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1), weight=1)

        self.header_font = customtkinter.CTkFont(family="sans-serif", size=20)
        self.label_font = customtkinter.CTkFont(family="sans-serif", size=14)


    def create_widgets(self):
        
        self.headerlabel = customtkinter.CTkLabel(master=self, text="Neues Produkt erstellen", font=self.header_font)
        self.headerlabel.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.namelabel = customtkinter.CTkLabel(master=self, text="Produktname:" justify="right")
        self.namelabel.grid(row=1, column=0, sticky="e")

        self.nameentry = customtkinter.CTkEntry(master=self)

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

        self.buttons = Buttons(self, command_add=self.addtocart, total_func=self.Total_popup, itemlist_func=self.Itemlist_popup, fg_color="transparent")
        self.buttons.grid(row=2, column=0, rowspan=2, padx=5, pady=10, sticky="nse")

        self.CartList = customtkinter.CTkTextbox(master=self, state="disabled", activate_scrollbars=False, font=self.list_font)
        self.CartList.grid(row=2, column=1, rowspan=2, padx=40, pady=40, sticky="nsew")

        self.errormessage = customtkinter.CTkLabel(master=self, text="", text_color="yellow", font=self.error_font)
        self.errormessage.grid(row=3, column=1, padx=40, pady=0, sticky="sew")

        self.totalvaluefield = customtkinter.CTkTextbox(master=self, state="normal", activate_scrollbars=False, font=self.list_font, height=20)
        self.totalvaluefield.grid(row=4, column=1, padx=40, pady=20, sticky="e")
        self.totalvaluefield.insert("0.0", "0.0 €")
        self.totalvaluefield.configure(state="disabled")

        self.totalvaluelabel = customtkinter.CTkLabel(master=self, text="Total:", font=self.list_font, justify="right")
        self.totalvaluelabel.grid(row=4, column=1, padx=40, pady=20, sticky="w")

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

    def addtocart(self):
        self.errormessage.configure(text="")
        global totalvalue
        dialog = customtkinter.CTkInputDialog(text="Welches Produkt soll hinzugefügt werden?", title="Kassensystem")
        answer = dialog.get_input()
        if answer == None or answer == "":
            self.errormessage.configure(text="Kein Produkt eingegeben!")
            pass
        else:
            self.errormessage.configure(text="")
            answer = str(answer)
            if answer == "":
                self.errormessage.configure(text="Produkt nicht gefunden!")
            else:
                answer = answer.strip() ## Remove whitespaces
                name, price = cf.get_properties_returned(cur, answer)
                if name == None or price == None or name=="":
                    self.errormessage.configure(text="Produkt nicht gefunden!")
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


    def kassensystem(self):
        pass


    def lagerverwaltung(self):
        pass

conn = sqlite3.connect("database.db")
cur = conn.cursor()

if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        exit(1)