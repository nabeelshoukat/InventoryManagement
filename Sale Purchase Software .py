from tkinter import *
import tkinter.messagebox
import sqlite3
import datetime
import tkinter.ttk
import time
from datetime import datetime
import datetime
import os

# from PIL import ImageTk, Image

root = Tk()
root.iconbitmap("icon.ico")
heightwin = root.winfo_screenheight()
widthwin = root.winfo_screenwidth()
# date and time
today = datetime.datetime.today().date().strftime("%d-%m-%y")
time = time.strftime("%I:%M-%p")

products = []
quantity = []
price = []
counterlist = []
product_id=[]
discount=[]
with sqlite3.connect("AbdulRazaq.db") as db:
    cursor = db.cursor()
    db.commit()
class GasAgency:
    def __init__(self, master):


        self.master = master
        self.date = datetime.datetime.today().date()

        bg_color=cursor.execute( "SELECT back_color ,text_color,font from bgcolor")
        for i in bg_color:
            self.bgcol=i[0]
            self.fgcol=i[1]
            self.font=i[2]

            root.config(bg=self.bgcol)

           # ====================================Main menu================================

        self.main_menu = Menu()
        self.master.config(menu=self.main_menu)
        #  purchasse
        self.purchase_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Purchase", menu=self.purchase_menu, )
        self.purchase_menu.add_command(label="Purchase Product", command=self.purchase, font=("arial", 12,"bold"))
        self.purchase_menu.add_command(label="Purchase return",command=self.purchase_return_byinvoice,  font=("arial", 12,"bold"))
        self.purchase_menu.add_command(label="Purchase Existing", command=self.purchase_existing, font=("arial", 12,"bold"))
        # cash=========================================================cash menu===========

        self.cash_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Cash", menu=self.cash_menu)
        self.cash_menu.add_command(label="Cash in Hand", command=self.cash, font=("arial", 12, "bold"))
        # self.cash_menu.add_command(label="Sale Debit", command=self.cash_debt)
        # self.cash_menu.add_command(label="Purchase Debit", command=self.cash_debt)

        # sales return
        self.sales_return = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Sales Return", menu=self.sales_return)
        self.sales_return.add_command(label="Return By Invoice", command=self.sale_return_byinvoice, font=("arial", 12,"bold"))
        # self.sales_return.add_command(label="return By Product", command=self.sales_return_fun)
        # self.sales_return.add_cascade(label="Return By invoice",menu=self.sales_return)

        #seller menu

        self.seller = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Seller", menu=self.seller,font=(self.font,12))
        self.seller.add_command(label="Sales Man", command=self.seller_fun,font=(self.font,12,"bold"))

    # search product
        self.search_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Search Records", menu=self.search_menu)
        self.search_menu.add_command(label="Search by Record", command=self.search_by_record, font=("arial", 12,"bold"))
        self.search_menu.add_command(label="Search By Date", command=self.search_by_date,font=("arial", 12,"bold"))
        self.search_menu.add_separator()
        self.search_menu.add_command(label="Sale Return", command=self.search_sale_return, font=("arial", 12, "bold"))
        self.search_menu.add_command(label="Purchase Return", command=self.search_purchase_turn, font=("arial", 12, "bold"))
    # settings
        self.setting_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="Settings", menu=self.setting_menu)
        self.setting_menu.add_command(label="Background Color", command=self.background_color, font=("arial", 12,"bold"))
        # self.setting_menu.add_command(label="Foreground Color", command=self.foreground_color, font=("arial", 12,))


        # ==========================================================================Product searching and selling section====
        self.SerchProductBy = Label(root, text="Search product By:", bg=self.bgcol,font=(self.font, 12, "bold"), fg=self.fgcol)
        self.SerchProductBy.place(x=widthwin - 1350, y=heightwin - 700)
        #radio buttons
        self.radiovar = 2
        self.radioname = Radiobutton(root, text="Name", bg=self.bgcol,fg=self.fgcol,font=(self.font, 11, "bold"), value=1, variable=self.radiovar)
        self.radioname.place(x=widthwin - 1130, y=heightwin - 700)
        self.radioid = Radiobutton(root, text="ID", font=(self.font, 11, "bold"), bg=self.bgcol,fg=self.fgcol,value=2, variable=self.radiovar)
        self.radioid.place(x=widthwin - 1050, y=heightwin - 700)
        self.invoice_no=Label(root,text="Customer NO",bg=self.bgcol,fg=self.fgcol,font=(self.font,12))
        self.invoice_no.place(x=widthwin - 1250,y=heightwin-800)
        self.invoice = Entry(root, font=(self.font, 13),)
        self.invoice.place(x=widthwin - 1100, y=heightwin - 800)
        abc=cursor.execute("SELECT SUM(pur_price) from purchase ")
        for self.i in abc:
            label=Label(root,text=str(self.i[0]),font=(self.font,15),bg=self.bgcol,fg=self.fgcol)


        self.sale_count = cursor.execute("SELECT  count(*) FROM sale_detail ")
        for j in self.sale_count:
            k = int(j[0])
            if k <= 0:
                self.invoice.insert(END, 0)
            else:
                self.invoice_res = cursor.execute("SELECT MAX(invoice_no) from sale_detail")

                for r in self.invoice_res:
                    self.maxval= r[0]
                    self.maxval += 1
                    self.invoice.insert(END, self.maxval)

        self.Enterdata = Entry(root, width=20, font=(self.font, 12, "bold"))
        self.Enterdata.place(x=widthwin - 1150, y=heightwin - 650)

        self.Enterdata.focus()
        self.Enterdata.bind("<Return>",self.serchresult)

        self.search = Button(root, text="Search", font=(self.font, 12, "bold"),bg=self.bgcol,command=self.serchresult)
        self.search.place(x=widthwin - 1075, y=heightwin - 600)
        # self.search.bind("<Button-1>",self.serchresult)
        # ============================================= right tree view====
        self.right_frame=Frame(root,height=850,width=900)
        self.right_frame.place(x=widthwin - 380, y=heightwin - 800)
        self.my_right_tree_view = tkinter.ttk.Treeview(self.right_frame, height=30)
        self.my_right_tree_view.pack(side=LEFT)

        self.my_right_tree_view_scrollbar=Scrollbar(self.right_frame,orient="vertical",command=self.my_right_tree_view.yview)
        self.my_right_tree_view_scrollbar.pack(fill=Y,side=RIGHT)
        self.my_right_tree_view_scrollbar.config(command=self.my_right_tree_view.yview)


        self.cartlabel = Label(root, text="Available Stock", bg=self.bgcol,font=(self.font, 30))
        self.cartlabel.place(x=widthwin - 320, y=heightwin - 850)
        # defing a scrollbar
        self.my_right_tree_view['columns'] = ("ID", "Name", "Quantity")
        self.my_right_tree_view.column("#0", width=0, stretch=NO)
        self.my_right_tree_view.column("ID", width=120, anchor=W)
        self.my_right_tree_view.column("Name", width=120, anchor=W)
        self.my_right_tree_view.column("Quantity", width=120, anchor=W)

        # headinds

        self.my_right_tree_view.heading("#0", text="")
        self.my_right_tree_view.heading("ID", text="ID")
        self.my_right_tree_view.heading("Name", text="Name")
        self.my_right_tree_view.heading("Quantity", text="Quantity")
        # ============================================= right tree view====
        self.cartlabel = Label(root, text="Available Stock", bg=self.bgcol,font=(self.font, 30))
        self.cartlabel.place(x=widthwin - 320, y=heightwin - 850)

        self.my_right_tree_view['columns'] = ("ID", "Name", "Quantity")
        self.my_right_tree_view.column("#0", width=0, stretch=NO)
        self.my_right_tree_view.column("ID", width=120, anchor=W)
        self.my_right_tree_view.column("Name", width=120, anchor=W)
        self.my_right_tree_view.column("Quantity", width=120, anchor=W)

        # headinds
        self.my_right_tree_view.heading("#0", text="")
        self.my_right_tree_view.heading("ID", text="ID")
        self.my_right_tree_view.heading("Name", text="Name")
        self.my_right_tree_view.heading("Quantity", text="Quantity")

        result = cursor.execute("SELECT  product_id,name , quantity FROM purchase")
        for self.rr in result:
            self.my_right_tree_view.insert(parent="", index="end", iid=self.rr, text="",
            values=(self.rr[0], self.rr[1], self.rr[2]))

    def cart(self,event,*args,**kwargs):
            if len(self.Enterqty.get())<=0:
                tkinter.messagebox.showerror("Error","Please provide a quantity to process further")
            else:

                self.frame = Frame(root, width=350, height=630, bg=self.bgcol)
                self.frame.place(x=widthwin - 780, y=heightwin - 800)
                self.mycanvas = Canvas(self.frame)
                self.mycanvas.place(x=widthwin - 400, y=heightwin - 100, )

                self.scrollable_frame = Frame(self.mycanvas)
                self.scrollable_frame.bind("<Configure>",lambda event: self.mycanvas.configure(scrollregion=self.mycanvas.bbox("all")))
                self.mycanvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
                # self.mycanvas.configure(yscrollcommand=self.scrollbar.set)

                self.Productnameres.place_forget()
                self.Productnameprice.place_forget()
                self.Productname.place_forget()
                self.Productprice.place_forget()
                self.enterqty.place_forget()
                self.Enterqty.place_forget()
                self.addtocart.place_forget()
                self.discountentery.place_forget()
                self.discountlable.place_forget()
                self.Enterdata.focus()

                self.linelabel = Label(root, text="|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n"
                                                  "|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n"
                                                  "|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n"
                                                  "|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n""|\n" ,bg=self.bgcol)

                self.linelabel.place(x=widthwin - 800, y=heightwin - 900)

                self.labelproduct = Label(root, text="Product   |",bg=self.bgcol,fg=self.fgcol, font=(self.font, 12, "bold"))
                self.labelproduct.place(x=widthwin - 780, y=heightwin - 830)

                self.labelquantity = Label(root, text="Quantity    |",bg=self.bgcol,fg=self.fgcol, font=(self.font, 12, "bold"))
                self.labelquantity.place(x=widthwin - 670, y=heightwin - 830)

                self.labelprice = Label(root, text="Price",bg=self.bgcol,fg=self.fgcol, font=(self.font, 12, "bold"))
                self.labelprice.place(x=widthwin - 550, y=heightwin - 830)

                self.totalprice = Label(root, text="", bg=self.bgcol,fg=self.fgcol,font=(self.font, 12, "bold"))
                self.totalprice.place(x=widthwin - 780, y=heightwin - 150)

                self.finishbutton = Button(root, text="Finish",  width=14,font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol,command=self.customer_attributes)
                self.finishbutton.place(x=widthwin - 600,y=heightwin-155)
                if self.radiovar==2:

                    self.cartquery = "SELECT name ,quantity,sale_price  FROM purchase WHERE product_id=?"
                    self.result = cursor.execute(self.cartquery, (self.Enterdata.get(),))
                    for self.r in self.result:
                        self.product = self.r[0]
                        self.quantity_temp = self.r[1]
                        self.totprice=self.r[2]
                        self.id= self.Enterdata.get()
                        self.quantity = self.Enterqty.get()
                        self.abc = ((int(self.Enterqty.get()) * int(self.totprice)) - int(self.discountentery.get()))


                        if int(self.Enterqty.get())>int(self.quantity_temp):
                            tkinter.messagebox.showinfo("ALERT","Not Enough stock")
                        else:
                            products.append(self.product)
                            price.append(self.abc)
                            quantity.append(self.quantity)
                            product_id.append(self.id)
                            discount.append(int(self.discountentery.get()))
                            self.x_index = 0
                            self.y_index = 10
                            self.counter = 0

                            for self.p in products:
                                self.labelproductvalue = Label(self.frame, text=str(products[self.counter]), bg=self.bgcol,fg=self.fgcol,font=(self.font, 12, "bold"),)
                                self.labelproductvalue.place(x=0, y=self.y_index)

                                self.labelquantityvalue = Label(self.frame, text=str(quantity[self.counter]),font=(self.font, 12, "bold"),bg=self.bgcol,fg=self.fgcol)
                                self.labelquantityvalue.place(x=150, y=self.y_index)

                                self.labelpricevalue = Label(self.frame, text=str(price[self.counter]),bg=self.bgcol,fg=self.fgcol, font=(self.font, 12, "bold"),)
                                self.labelpricevalue.place(x=230, y=self.y_index)

                                self.y_index += 30
                                self.totalprice.configure(text=str(f"Total Bill: {int(sum(price))}"))
                                sal_and_pur_price_query=("SELECT * from purchase WHERE product_id=?")
                                sale_and_pur_price=cursor.execute(sal_and_pur_price_query,(self.Enterdata.get(),))
                                for s_and_p in sale_and_pur_price:
                                    self.profit=((int(self.Enterqty.get())*(s_and_p[5]))-(int(self.Enterqty.get())*(s_and_p[4])))-int(self.discountentery.get())

                                cursor.execute(
                                    "CREATE TABLE IF NOT EXISTS sale_detail(invoice_no INTEGER ,product TEXT ,quantity INTEGER,price INTEGER,discount INTEGER,date TEXT,time TEXT,profit INTEGER)")
                                self.salequery = (
                                    "INSERT INTO sale_detail(invoice_no,product,quantity,price,discount,date,time,profit)VALUES(?,?,?,?,?,?,?,?)")
                                cursor.execute((self.salequery),(self.invoice.get(),products[self.counter], quantity[self.counter], price[self.counter],discount[self.counter],today,time,self.profit))
                                self.counter += 1
                    self.x = 0
                    self.initial = "SELECT * FROM purchase WHERE  product_id=?"
                    self.initial_res = cursor.execute(self.initial, (self.Enterdata.get(),))
                    for r in self.initial_res:
                        self.old_stock = r[3]
                    for i in products:
                        self.new_stock = int(self.old_stock) - int(self.Enterqty.get())
                        update_query = "UPDATE purchase SET quantity=? where product_id=?"
                        cursor.execute(update_query, (self.new_stock, product_id[0]))
                        db.commit()
                        self.x += 1
                    product_id.clear()
                    total_discount=sum(discount)
                    self.Enterdata.delete(0,END)


    def change_money(self,event,*args,**kwargs):
        self.price_total=int(sum(price))
        self.returned_amount =int(self.changeentery.get()) - int(self.price_total)
        if int(self.changeentery.get()) < self.price_total:
            tkinter.messagebox.showerror("ERROR","Amount is not Enough")
        else:
            aa =int(self.changeentery.get())  - int(self.price_total)
            self.returnamount = Label(root, text=f"Return Amount =  {aa}", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.returnamount.place(x=widthwin - 1500, y=heightwin - 600)


            self.cus_name = Label(root, text="Customer Name", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.cus_name.place(x=widthwin - 1500, y=heightwin - 550)
            self.cus_phone1 = Label(root, text="Phone No", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.cus_phone1.place(x=widthwin - 1500, y=heightwin - 500)
            self.cus_Address = Label(root, text="Address", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.cus_Address.place(x=widthwin - 1500, y=heightwin - 450)
            # entries

            self.cus_name_entery = Entry(root, font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.cus_name_entery.place(x=widthwin - 1300, y=heightwin - 550)
            self.cus_name_entery.focus()
            self.cus_name_entery.bind("<Return>",lambda event :self.cus_phone_entery.focus())
            self.cus_phone_entery = Entry(root, font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.cus_phone_entery.place(x=widthwin - 1300, y=heightwin - 500)
            self.cus_phone_entery.bind("<Return>", lambda event: self.cus_Address_entery.focus())
            self.cus_Address_entery = Entry(root, font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
            self.cus_Address_entery.place(x=widthwin - 1300, y=heightwin - 450)


            self.genrate_billbtn = Button(root, text="Generate  Bill ", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol,
                                       width=20,
                                     command=self.genrate_bill_fun)
            self.cus_Address_entery.bind("<Return>",  self.genrate_bill_fun)
            self.genrate_billbtn.place(x=widthwin - 1300, y=heightwin - 400)
            self.genrate_billbtn.bind("<Button-1>", self.genrate_bill_fun)



    def sales_record(self,*args):
        self.counter=0
        self.c_name = self.cus_name_entery.get()
        self.cus_phone = self.cus_phone_entery.get()
        self.cus_add = self.cus_Address_entery.get()
        self.given_money=self.changeentery.get()
        self.invoice=self.invoice.get()
        for self.counter in range(0,1):
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS cus_detail(invoice_no INTEGER ,given_money INTEGER,returned_money INTEGER,name TEXT ,phone TEXT, address TEXT)")
            self.salequery = ("INSERT INTO cus_detail(invoice_no,given_money,returned_money,name,phone,address)VALUES(?,?,?,?,?,?)")
            cursor.execute((self.salequery),(self.invoice,self.given_money,self.returned_amount,self.cus_name_entery.get(),self.cus_phone_entery.get(), self.cus_Address_entery.get()))
            db.commit()
            self.counter+=1


    def customer_attributes(self,*args,**kwargs):
        self.forget_main_widgets()
        self.cus_attribute = Label(root, text="Customer Attributes ", font=(self.font, 20, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.cus_attribute.place(x=widthwin - 1550, y=heightwin - 800)
        self.changelale = Label(root, text="Give Amount", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.changelale.place(x=widthwin - 1500, y=heightwin - 700)
        self.changeentery = Entry(root, font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.changeentery.place(x=widthwin - 1250, y=heightwin - 700)
        self.changeentery.focus()

        self.changebutton=Button(root,text="Received",font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.changebutton.place(x=widthwin-1150,y=heightwin-650)
        self.changeentery.bind("<Return>",self.change_money)
        self.changebutton.bind("<Button-1>",self.change_money)

    def serchresult(self,*args,**kwargs):
        query = "SELECT name ,sale_price FROM purchase WHERE product_id=?"
        self.res = cursor.execute(query, (self.Enterdata.get(),))

        cc = 0
        for self.r in self.res:
            cc+=1
            if len(self.r)>=1:

                self.Productname = Label(root, text="Product Name:", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol, )
                self.Productname.place(x=widthwin - 1200, y=heightwin - 500)

                self.Productprice = Label(root, text="Product Price:", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol )
                self.Productprice.place(x=widthwin - 1200, y=heightwin - 450)

                self.Productnameres = Label(root, text=str(self.r[0]), font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol )
                self.Productnameres.place(x=widthwin - 1000, y=heightwin - 500)

                self.Productnameprice = Label(root, text=str(self.r[1]), font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol )
                self.Productnameprice.place(x=widthwin - 1000, y=heightwin - 450)

                self.enterqty = Label(root, text="Enter QTY:", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol )
                self.enterqty.place(x=widthwin - 1200, y=heightwin - 400)

                self.Enterqty = Entry(root, width=20, font=(self.font, 13, "bold"))
                self.Enterqty.place(x=widthwin - 1050, y=heightwin - 400)
                self.Enterqty.focus()
                self.discountlable=Label(root,text="Discount",bg=self.bgcol,fg=self.fgcol,font=(self.font,12,"bold"))
                self.discountlable.place(x=widthwin - 1200, y=heightwin - 350)
                self.discountentery=Entry(root,font=(self.font,12))
                self.discountentery.place(x=widthwin - 1050, y=heightwin - 350)
                self.Enterqty.bind("<Return>",lambda event:self.discountentery.focus())
                self.discountentery.bind("<Return>",self.cart)
                self.discountentery.insert(END,0)
                self.addtocart = Button(root, text="Add to Cart", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol, width=32, command=self.cart)
                self.addtocart.place(x=widthwin - 1200, y=heightwin - 300)
                self.addtocart.bind("<Button-1>",self.cart)
                self.main_menu.entryconfig("Purchase", state="disable")
                self.main_menu.entryconfig("Cash", state='disable')
                self.main_menu.entryconfig("Sales Return", state='disable')
                self.main_menu.entryconfig("Seller", state="disable")
                self.main_menu.entryconfig("Search Records", state="disable")
                self.main_menu.entryconfig("Settings", state="disable")

        # ===========================================================================================================forget main widgets===============================

    def forget_main_widgets(self):
        # self.name_of_store.place_forget()
        self.SerchProductBy.place_forget()
        self.radioid.place_forget()
        self.radioname.place_forget()
        self.Enterdata.place_forget()
        self.search.place_forget()
        try:
            self.discountlable.place_forget()
            self.discountentery.place_forget()
            self.Productname.place_forget()
            self.Productprice.place_forget()
            self.Productnameprice.place_forget()
            self.Productnameres.place_forget()
            self.enterqty.place_forget()
            self.addtocart.place_forget()
            self.Enterqty.place_forget()
        except:
            pass


    def purchase(self,*args,**kwargs):
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.purchase_menu.entryconfig("Purchase return", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state="disable")
        self.main_menu.entryconfig("Search Records", state="disable")
        self.main_menu.entryconfig("Settings", state="disable")
        self.forget_main_widgets()
        # entries for purchase==========================================================================================


        self.productlabel = Label(root, text="Product purchase ", font=(self.font, 20, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.productlabel.place(x=widthwin - 1300, y=heightwin - 900)
        self.productidlabel = Label(root, text="Product ID ", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.productidlabel.place(x=widthwin - 1400, y=heightwin - 850)
        self.productidentery = Entry(root, font=(self.font, 13, "bold"), width=10)
        self.productidentery.place(x=widthwin - 1250, y=heightwin - 850)

        self.search_product_button1=Button(root,text="search",font=('arial',12,),command=self.search_purchase)
        self.search_product_button1.place(x=widthwin - 1150, y=heightwin - 850)
        self.productcompanylable = Label(root, text=" Company ", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.productcompanylable.place(x=widthwin - 1400, y=heightwin - 800)

        self.prodctcompanyentery = Entry(root, font=(self.font, 13, "bold"), width=20)
        self.prodctcompanyentery.place(x=widthwin - 1250, y=heightwin - 800)
        self.prodctcompanyentery.focus()
        self.productcompanylable.bind("<Return>", lambda event: self.prodctcompanyentery.focus())

        self.namepurchaselabel = Label(root, text=" Name", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.namepurchaselabel.place(x=widthwin - 1400, y=heightwin - 750)

        self.prodctcompanyentery.bind("<Return>", lambda event: self.namepurchaseentery.focus())


        self.namepurchaseentery = Entry(root, font=(self.font, 13, "bold"), width=20)
        self.namepurchaseentery.place(x=widthwin - 1250, y=heightwin - 750)

        self.howmuchpurchaselabel = Label(root, text="Quantity", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.howmuchpurchaselabel.place(x=widthwin - 1400, y=heightwin - 700)

        self.namepurchaseentery.bind("<Return>", lambda event: self.howmuchpurchaseentery.focus())

        self.howmuchpurchaseentery = Entry(root, font=(self.font, 13, "bold"), width=20)
        self.howmuchpurchaseentery.place(x=widthwin - 1250, y=heightwin - 700)

        self.howmuchpurchaseentery.bind("<Return>", lambda event: self.productpurpriceentery.focus())

        self.productpurpricelabel = Label(root, text="Purchase Price", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.productpurpricelabel.place(x=widthwin - 1400, y=heightwin - 650)


        self.productpurpriceentery = Entry(root, font=(self.font, 13, "bold"), width=20)
        self.productpurpriceentery.place(x=widthwin - 1250, y=heightwin - 650)
        self.howmuchpurchaseentery.bind("<Return>", lambda event: self.productpurpriceentery.focus())

        self.productsalepricelabel = Label(root, text="Sale Price", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.productsalepricelabel.place(x=widthwin - 1400, y=heightwin - 600)

        self.productsalepriceentery = Entry(root, font=(self.font, 13, "bold"), width=20)
        self.productsalepriceentery.place(x=widthwin - 1250, y=heightwin - 600)
        self.productpurpriceentery.bind("<Return>", lambda event: self.productsalepriceentery.focus())
        self.reciverNamelabel = Label(root, text="Receiver Name ", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.reciverNamelabel.place(x=widthwin - 1400, y=heightwin - 550)
        self.reciverNameentery = Entry(root, font=(self.font, 13, "bold"), width=20)
        self.reciverNameentery.place(x=widthwin - 1250, y=heightwin - 550)
        self.productsalepriceentery.bind("<Return>", lambda event: self.reciverNameentery.focus())


        self.selleridcopylabel = Label(root, text="Seller ID:", font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.selleridcopylabel.place(x=widthwin - 1400, y=heightwin - 500)
        self.selleridcopyentery = Entry(root, font=("arial", 13, "bold"), width=20)
        self.selleridcopyentery.place(x=widthwin - 1250, y=heightwin - 500)
        self.reciverNameentery.bind("<Return>", lambda event: self.selleridcopyentery.focus())

       # self.time=time.strftime("%H :%M")

        self.datelable = Label(root, text="Date                                " + str(today )+str((" | "+time)), font=(self.font, 13, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.datelable.place(x=widthwin - 1400, y=heightwin - 450)

        self.InsertIntoDatbase = Button(root, text="Add product", font=("arial", 13,), bg="green", fg='white',
                                        command=self.purchase_insert)
        self.InsertIntoDatbase.place(x=widthwin - 1400, y=heightwin - 400)

        self.updateDatbase1 = Button(root, text="UPDATE", font=("arial", 13,),width=12, bg="yellow", fg='black',
                                    command=self.update_purchase)
        self.updateDatbase1.place(x=widthwin - 1290, y=heightwin - 400)

        self.deletepurchase = Button(root, text="DELETE", font=("arial", 13,),width=15, bg="red", fg='white',
                                    command=self.delete_purchase)
        self.deletepurchase.place(x=widthwin - 1170, y=heightwin - 400)

        self.exitpurchase1 = Button(root, text="Exit", font=("arial", 13,), width=12,bg="yellow", fg='black',command=self.purchase_exit)
        self.exitpurchase1.place(x=widthwin - 1050, y=heightwin - 400)

        self.seller_tree_view_frame=Frame(root,width=200,height=300)
        self.seller_tree_view_frame.place(x=widthwin - 900, y=heightwin - 850)
        self.sellerinfotree = tkinter.ttk.Treeview(self.seller_tree_view_frame, height=20)
        self.sellerinfotree.pack(side=LEFT)
        self.sellerinfotree['columns'] = ("ID", "Name",)
        self.sellerinfotree.column("#0", width=0, stretch=NO)
        self.sellerinfotree.column("ID", width=50, anchor=W)
        self.sellerinfotree.column("Name", width=120, anchor=W)
        self.sellerinfotree.heading("#0", text="")
        self.sellerinfotree.heading("ID", text="ID")
        self.sellerinfotree.heading("Name", text="Name")
        self.seller_scrollbar=Scrollbar(self.seller_tree_view_frame,orient="vertical",command=self.sellerinfotree.yview)
        self.seller_scrollbar.pack(side=RIGHT,fill=Y)
        self.seller_scrollbar.config(command=self.sellerinfotree.yview)

        result1 = cursor.execute("SELECT  * FROM seller")
        for self.sel in result1:
            self.sellerinfotree.insert(parent="", index="end", iid=self.sel, text="", values=(self.sel[0], self.sel[1]))
        try:
            result = cursor.execute("SELECT  product_id,name , quantity FROM purchase")
            for self.rr in result:
                self.my_right_tree_view.insert(parent="", index="end", iid=self.rr, text="",values=(self.rr[0], self.rr[1], self.rr[2]))
        except:
            pass
    def purchase_existing(self):
        self.invoice.place_forget()
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state="disable")
        self.main_menu.entryconfig("Search Records", state="disable")
        self.main_menu.entryconfig("Settings", state="disable")
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.forget_main_widgets()
        self.searchidlale = Label(root, text="Product ID", font=(self.font, 13, "bold"), bg=self.bgcol,
                                       fg=self.fgcol)
        self.searchidlale.place(x=widthwin - 1400, y=heightwin - 700)
        self.searchidentery = Entry(root, font=("arial", 13, "bold"), width=15)
        self.searchidentery.place(x=widthwin - 1250, y=heightwin - 700)
        self.searchidentery.focus()
        self.search_product_existing = Button(root, text="search", font=("arial", 13,), width=12, bg="red", fg='white',
                                     command=self.purchase_existing_query)
        self.search_product_existing.place(x=widthwin - 1100, y=heightwin - 700)

    def purchase_existing_query(self):
        query = "SELECT * FROM purchase WHERE product_id=?"
        query_res = cursor.execute(query, (self.searchidentery.get()))
        for res in query_res:
            self.old_stock_existing = res[2]

        self.prodname = Label(root, text="Product Name :", font=(self.font, 13, "bold"), bg=self.bgcol,
                                   fg=self.fgcol)
        self.prodname.place(x=widthwin - 1400, y=heightwin - 600)
        self.prodname1 = Label(root, text=str(self.old_stock_existing), font=(self.font, 13, "bold"), bg=self.bgcol,
                                   fg=self.fgcol)
        self.prodname1.place(x=widthwin - 1100, y=heightwin - 600)
        self.searchidlale1 = Label(root, text="Enter Quantity", font=(self.font, 13, "bold"), bg=self.bgcol,
                                  fg=self.fgcol)
        self.searchidlale1.place(x=widthwin - 1400, y=heightwin - 500)
        self.searchidentery1 = Entry(root, font=("arial", 13, "bold"), width=15)
        self.searchidentery1.place(x=widthwin - 1250, y=heightwin - 500)
        self.searchidentery1.focus()
        self.purchase_product_new = Button(root, text="Add to stock", font=("arial", 13,), width=12, bg="red", fg='white',
                                              command=self.purchase_new_final)
        self.purchase_product_new.place(x=widthwin - 1100, y=heightwin - 500)

        self.purchase_product_exit = Button(root, text="EXIT", font=("arial", 13,), width=30, bg="red",
                                           fg='white',
                                           command=self.exit_new_purchase)
        self.purchase_product_exit.place(x=widthwin - 1260, y=heightwin - 450)

    def purchase_new_final(self):
        query = "SELECT * FROM purchase WHERE product_id=?"
        query_res = cursor.execute(query, (self.searchidentery.get()))
        for res in query_res:
            self.old_stock_existing = res[3]

            self.new_stock1 = int(self.old_stock_existing) + int(self.searchidentery1.get())
            update_query = "UPDATE purchase SET quantity=? where product_id=?"
            cursor.execute(update_query, (self.new_stock1,self.searchidentery.get()))
            db.commit()
        tkinter.messagebox.showinfo("Congrsts","The operation is successfull")
        aaa=tkinter.messagebox.askyesno("Alert","Do you want to work further in this dialog box")
        if aaa>=1:
            self.searchidlale1.place_forget()
            self.searchidentery1.place_forget()
            self.purchase_product_new.place_forget()
            self.purchase_product_exit.place_forget()
            self.searchidentery.focus()
            self.prodname.place_forget()
            self.prodname1.place_forget()
        else:
            self.searchidentery.place_forget()
            self.searchidlale.place_forget()
            self.searchidlale1.place_forget()
            self.searchidentery1.place_forget()
            self.purchase_product_new.place_forget()
            self.search_product_existing.place_forget()
            self.purchase_product_exit.place_forget()
            self.prodname.place_forget()
            self.prodname1.place_forget()
            GasAgency(root)
            self.main_menu.entryconfig("Purchase", state="normal")
            self.main_menu.entryconfig("Cash", state='normal')
            self.main_menu.entryconfig("Sales Return", state='normal')
            self.main_menu.entryconfig("Seller", state="normal")
            self.main_menu.entryconfig("Search Records", state="normal")
            self.main_menu.entryconfig("Settings", state="normal")
    def exit_new_purchase(self):
        self.searchidentery.place_forget()
        self.searchidlale.place_forget()
        self.searchidlale1.place_forget()
        self.searchidentery1.place_forget()
        self.purchase_product_new.destroy()
        self.search_product_existing.place_forget()
        self.prodname.place_forget()
        self.prodname1.place_forget()
        self.purchase_product_exit.place_forget()
        GasAgency(root)
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state="normal")
        self.main_menu.entryconfig("Search Records", state="normal")
        self.main_menu.entryconfig("Settings", state="normal")
    def search_purchase(self):
        search_purchse="SELECT * FROM purchase WHERE product_id=?"
        search_purchase_res=cursor.execute(search_purchse,(self.productidentery.get()))
        for i in search_purchase_res:


            self.prodctcompanyentery.  insert(0,i[1])
            self.namepurchaseentery.   insert(0,i[2])
            self.howmuchpurchaseentery.insert(0,i[3])
            self.productpurpriceentery.insert(0,i[4])
            self.productsalepriceentery.insert(0,i[5])
            self.reciverNameentery.     insert(0,i[6])
            self.selleridcopyentery.    insert(0,i[7])
            self.nowdate=i[8]
            self.nowtime=i[9]
    def update_purchase(self):
        pur_update_que="UPDATE purchase SET  company=? ,name=? ,quantity=? ,pur_price=? , sale_price=? ,rec_name=? ,seller_id=?,date=?,time=?WHERE product_id=?"
        cursor.execute(pur_update_que,(self.prodctcompanyentery.get(), self.namepurchaseentery.get(),  self.howmuchpurchaseentery.get(),self.productpurpriceentery.get(),self.productsalepriceentery.get(), self.reciverNameentery.get(),self.selleridcopyentery.get(),self.nowdate,self.nowtime,self.productidentery.get()))
        db.commit()
        pur=tkinter.messagebox.askyesno("Alert","Do you want to work further in this working area")
        if pur>=1:
            self.prodctcompanyentery.delete(0, END)
            self.namepurchaseentery.delete(0, END)
            self.howmuchpurchaseentery.delete(0, END)
            self.productpurpriceentery.delete(0, END)
            self.productsalepriceentery.delete(0, END)
            self.reciverNameentery.delete(0, END)
            self.selleridcopyentery.delete(0, END)
            self.prodctcompanyentery.focus()
        else:
            self.purchase_exit()
    def delete_purchase(self):
        delete_pur_query="DELETE FROM purchase WHERE product_id=?"
        cursor.execute(delete_pur_query,(self.productidentery.get()))
        ask=tkinter.messagebox.askyesno("Alert",f"Do you really want to delete the following product with id=  {self.productidentery.get()}")
        if ask>=1:
            db.commit()
            self.prodctcompanyentery.delete(0, END)
            self.namepurchaseentery.delete(0, END)
            self.howmuchpurchaseentery.delete(0, END)
            self.productpurpriceentery.delete(0, END)
            self.productsalepriceentery.delete(0, END)
            self.reciverNameentery.delete(0, END)
            self.selleridcopyentery.delete(0, END)
            self.prodctcompanyentery.focus()
        else:
            tkinter.messagebox.showinfo("Alert",f"You have not removed the product with the following id ={self.productidentery.get()}")
    def   seller_fun(self,*args):
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Search Records", state="disable")
        self.main_menu.entryconfig("Settings", state="disable")
        self.forget_main_widgets()
        self.forget_main_widgets()
        self.invoice.place_forget()
        self.invoice_no.place_forget()

        self.attributesofsellerlabel = Label(root, text="Seller", font=(self.font, 20, "bold"),bg=self.bgcol,fg=self.fgcol)
        self.attributesofsellerlabel.place(x=widthwin - 1400, y=heightwin - 800)
# creating id for search purpose only
        self.selleridlable = Label(root, text="ID To Modify", font=(self.font, 14), bg=self.bgcol, fg=self.fgcol)
        self.selleridlable.place(x=widthwin - 1400, y=heightwin - 750)
        self.selleridentrey  = Entry(root, font=(self.font, 15, "bold"), width=10)
        self.selleridentrey.place(x=widthwin - 1250, y=heightwin - 750)

        self.search_saler = Button(root, text="search", font=("arial", 13,), bg="red", fg="white", width=10,
                                command=self.update_seller)
        self.search_saler.place(x=widthwin - 1130, y=heightwin - 750)

        self.nameofsellerlabel = Label(root, text="Name", font=(self.font, 14),bg=self.bgcol,fg=self.fgcol)
        self.nameofsellerlabel.place(x=widthwin - 1400, y=heightwin - 700)
        self.nameofsellerentery = Entry(root, font=(self.font, 15, "bold"), width=20)
        self.nameofsellerentery.place(x=widthwin - 1250, y=heightwin - 700)
        self.nameofsellerentery.focus()
        self.phoneofsalesmanlabel = Label(root, text="Phone Number", font=(self.font, 14),bg=self.bgcol,fg=self.fgcol)
        self.phoneofsalesmanlabel.place(x=widthwin - 1400, y=heightwin - 650)
        self.phoneofsalesmanentery = Entry(root, font=(self.font, 15, "bold"), width=20)
        self.phoneofsalesmanentery.place(x=widthwin - 1250, y=heightwin - 650)
        self.nameofsellerentery.bind("<Return>",lambda event:self.phoneofsalesmanentery.focus())
        self.addressofsalesmanlabel = Label(root, text=" Address", font=(self.font, 14),fg=self.fgcol,bg=self.bgcol,)
        self.addressofsalesmanlabel.place(x=widthwin - 1400, y=heightwin - 600)
        self.addressofsalesmanentery = Entry(root, font=(self.font, 15, "bold"), width=20)
        self.addressofsalesmanentery.place(x=widthwin - 1250, y=heightwin - 600)
        self.phoneofsalesmanentery.bind("<Return>", lambda event: self.addressofsalesmanentery.focus())

        self.InsertIntoDatbase = Button(root, text="Insert", font=(self.font, 13,), bg="green", fg='white',width=13,command=self.seller_insert)
        self.InsertIntoDatbase.place(x=widthwin - 1400, y=heightwin - 520)

        self.exit_sale = Button(root, text="EXIT", font=("arial", 13,), bg="pink", fg="black",width=15,command=self.exit_sale_man)
        self.exit_sale.place(x=widthwin - 950, y=heightwin - 520)
        self.update_sale_finalbutton = Button(root, text="UPDATE", font=("arial", 13,), bg="yellow", fg="black", width=15,
                                command=self.update_seller_final)
        self.update_sale_finalbutton.place(x=widthwin - 1250, y=heightwin - 520)
        self.delete_sale_finalbutton = Button(root, text="DELETE", font=("arial", 13,), bg="red", fg="white", width=15,
                                              command=self.delete_seller)
        self.delete_sale_finalbutton.place(x=widthwin - 1100, y=heightwin - 520)
    # update seller
    def update_seller(self):
        seler_search="SELECT * FROM seller WHERE seller_id=?"
        seler_res=cursor.execute(seler_search,(self.selleridentrey.get()))
        for res in seler_res:
            name=res[1]
            phone=res[2]
            address=res[3]
            self.nameofsellerentery.insert(0,name)
            self.phoneofsalesmanentery.insert(0,phone)
            self.addressofsalesmanentery.insert(0,address)
    def update_seller_final(self):
        update_seller_query="UPDATE seller SET name=?,phone=?,address=?"
        cursor.execute(update_seller_query,(self.nameofsellerentery.get(),self.phoneofsalesmanentery.get(),self.addressofsalesmanentery.get()))
        tkinter.messagebox.showinfo("Congrats",f"Seller has been successfully updated with id={self.selleridentrey.get()}")
        self.exit_sale_man()
    def exit_sale_man(self):

        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Search Records", state="normal")
        self.main_menu.entryconfig("Settings", state="normal")
        self.exit_sale.place_forget()
        self.InsertIntoDatbase.place_forget()
        self.addressofsalesmanentery.place_forget()
        self.addressofsalesmanlabel.place_forget()
        self.phoneofsalesmanentery.place_forget()
        self.phoneofsalesmanlabel.place_forget()
        self.nameofsellerentery.place_forget()
        self.nameofsellerlabel.place_forget()
        self.attributesofsellerlabel.place_forget()
        self.selleridlable.place_forget()
        self.selleridentrey.place_forget()
        self.update_sale_finalbutton.place_forget()
        self.delete_sale_finalbutton.place_forget()
        self.search_saler.place_forget()

        GasAgency(root)
    def delete_seller(self):
        delete_query="delete  FROM seller WHERE seller_id=?"
        cursor.execute(delete_query,(self.selleridentrey.get()))
        db.commit()
        tkinter.messagebox.showinfo("oops!",f"One seller has been removed from your list with id= {self.selleridentrey.get()}")
        self.exit_sale_man()
    def seller_insert(self):

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS seller(seller_id  INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,phone TEXT ,address TEXT)")
        query = "INSERT INTO seller(name,phone,address)VALUES(?,?,?)"
        cursor.execute(query, (self.nameofsellerentery.get(),self.phoneofsalesmanentery.get(),self.addressofsalesmanentery.get()))
        db.commit()
        tkinter.messagebox.showinfo("Congrats", f"'{self.nameofsellerentery.get()}' has been successfully added in database as seller.")
        aa=tkinter.messagebox.askyesno("Alert","Do you want to Add more more persons")
        if aa>=1:
            self.nameofsellerentery.delete(0,END)
            self.phoneofsalesmanentery.delete(0,END)
            self.addressofsalesmanentery.delete(0,END)
            self.nameofsellerentery.focus()
        else:
            self.exit_sale_man()
            GasAgency(root)

    def genrate_bill_fun(self,*args):
        db.commit()
        self.sales_record()
        asktoprint=tkinter.messagebox.askyesno("Alert!","Do you want to print this Bill?")
        if asktoprint>=1:
            self.print_hard()
            self.cus_attribute.place_forget()
            self.changelale.place_forget()
            self.changeentery.place_forget()
            self.changebutton.place_forget()
            self.returnamount.place_forget()
            self.cus_name.destroy()
            self.cus_phone1.place_forget()
            self.cus_Address.place_forget()
            self.cus_name_entery.place_forget()
            self.cus_phone_entery.place_forget()
            self.cus_Address_entery.place_forget()
            self.genrate_billbtn.place_forget()
            self.finishbutton.destroy()
            self.frame.destroy()

            self.labelproduct.place_forget()
            self.labelquantity.place_forget()
            self.labelprice.place_forget()
            self.totalprice.place_forget()
            self.linelabel.place_forget()
        else:

            self.cus_attribute.place_forget()
            self.changelale.place_forget()
            self.changeentery.place_forget()
            self.changebutton.place_forget()
            self.returnamount.place_forget()
            self.cus_name.destroy()
            self.cus_phone1.place_forget()
            self.cus_Address.place_forget()
            self.cus_name_entery.place_forget()
            self.cus_phone_entery.place_forget()
            self.cus_Address_entery.place_forget()
            self.genrate_billbtn.place_forget()
            self.finishbutton.destroy()
            self.frame.destroy()
            self.main_menu.entryconfig("Purchase", state="normal")
            self.main_menu.entryconfig("Cash", state='normal')
            self.main_menu.entryconfig("Sales Return", state='normal')
            self.main_menu.entryconfig("Seller", state="normal")
            self.main_menu.entryconfig("Search Records", state="normal")
            self.main_menu.entryconfig("Settings", state="normal")
            GasAgency(root)

        self.labelproduct.place_forget()
        self.labelquantity.place_forget()
        self.labelprice.place_forget()
        self.totalprice.place_forget()
        self.linelabel.place_forget()
        products.clear()
        quantity.clear()
        price.clear()
        discount.clear()
        GasAgency(root)
    def purchase_insert(self,*args,**kwargs,):
        self.id = self.productidentery.get()
        self.company = self.prodctcompanyentery.get()
        self.name_of_prod = self.namepurchaseentery.get()
        self.qty = self.howmuchpurchaseentery.get()
        self.pur_price = self.productpurpriceentery.get()
        self.sale_price = self.productsalepriceentery.get()
        self.rec_name = self.reciverNameentery.get()
        if  self.prodctcompanyentery.get()=="" or  self.namepurchaseentery.get()=="" or self.howmuchpurchaseentery.get()=="" or self.productpurpriceentery.get()=="" or self.productsalepriceentery.get()=="" or self.reciverNameentery.get()=="" =="":
            tkinter.messagebox.showinfo("Alert","You forget something to insert")
        else:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS purchase(product_id INTEGER PRIMARY KEY,company TEXT,name TEXT ,quantity INTEGER,pur_price INTEGER, sale_price INTEGER,rec_name ,seller_id,date TEXT,time TEXT)")
            query = "INSERT INTO purchase(company ,name ,quantity ,pur_price , sale_price ,rec_name ,seller_id,date,time)VALUES(?,?,?,?,?,?,?,?,?)"
            cursor.execute(query, (self.company, self.name_of_prod, self.qty, self.pur_price, self.sale_price,self.rec_name,self.selleridcopyentery.get(),today,time))
            tkinter.messagebox.showinfo("Congrats ", "Data has been successfully added")
            db.commit()
            self.purchase_menu.entryconfig("Purchase return", state="normal")
            self.main_menu.entryconfig("Cash", state='normal')

            self.main_menu.entryconfig("Sales Return", state='normal')
            self.main_menu.entryconfig("Seller",state="normal")
            self.main_menu.entryconfig("Search Records", state="normal")
            self.main_menu.entryconfig("Settings", state="normal")
            self.productlabel.place_forget()
            self.productidlabel.place_forget()
            self.productidentery.place_forget()
            self.productcompanylable.place_forget()
            self.prodctcompanyentery.place_forget()
            self.namepurchaselabel.place_forget()
            self.namepurchaseentery.place_forget()
            self.howmuchpurchaselabel.place_forget()
            self.productpurpricelabel.place_forget()
            self.productpurpriceentery.place_forget()
            self.productsalepricelabel.place_forget()
            self.productsalepriceentery.place_forget()
            self.reciverNamelabel.place_forget()
            self.reciverNameentery.place_forget()
            self.selleridcopylabel.place_forget()
            self.selleridcopyentery.place_forget()
            self.datelable.place_forget()
            self.InsertIntoDatbase.place_forget()
            self.updateDatbase1.place_forget()
            self.howmuchpurchaseentery.place_forget()
            self.sellerinfotree.place_forget()
            self.exitpurchase1.place_forget()
            self.deletepurchase.place_forget()
            self.search_product_button1.place_forget()
            self.seller_tree_view_frame.place_forget()
            GasAgency(root)

    def purchase_exit(self):
        self.purchase_menu.entryconfig("Purchase return", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')

        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state="normal")
        self.main_menu.entryconfig("Search Records", state="normal")
        self.main_menu.entryconfig("Settings", state="normal")

        self.productlabel.place_forget()
        self.productidlabel.place_forget()
        self.productidentery.place_forget()
        self.productcompanylable.place_forget()
        self.prodctcompanyentery.place_forget()
        self.namepurchaselabel.place_forget()
        self.namepurchaseentery.place_forget()
        self.howmuchpurchaselabel.place_forget()
        self.productpurpricelabel.place_forget()
        self.productpurpriceentery.place_forget()
        self.productsalepricelabel.place_forget()
        self.productsalepriceentery.place_forget()
        self.reciverNamelabel.place_forget()
        self.reciverNameentery.place_forget()
        self.selleridcopylabel.place_forget()
        self.selleridcopyentery.place_forget()
        self.datelable.place_forget()
        self.InsertIntoDatbase.place_forget()

        self.howmuchpurchaseentery.place_forget()
        self.sellerinfotree.place_forget()
        self.sellerinfotree.destroy()
        self.seller_scrollbar.destroy()
        self.seller_tree_view_frame.destroy()

        self.deletepurchase.place_forget()
        self.search_product_button1.place_forget()
        self.updateDatbase1.place_forget()
        self.exitpurchase1.place_forget()
        GasAgency(root)

    def sale_return_byinvoice(self):

        self.purchase_menu.entryconfig("Purchase Product", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')

        self.main_menu.entryconfig("Sales Return", state='disable')
        self.forget_main_widgets()

        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.purchase_menu.entryconfig("Purchase return", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')

        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state="disable")
        self.main_menu.entryconfig("Search Records", state="disable")
        self.main_menu.entryconfig("Settings", state="disable")
        self.forget_main_widgets()

        # entries for sale return==========================================================================================

        self.productlabel = Label(root, text="Sales Return ", bg=self.bgcol,fg=self.fgcol,font=(self.font, 25, "bold"))
        self.productlabel.place(x=widthwin - 1250, y=heightwin - 900)
        self.productidlabel = Label(root, text="Product ID ", bg=self.bgcol,fg=self.fgcol,font=(self.font, 14))
        self.productidlabel.place(x=widthwin - 1400, y=heightwin - 800)
        self.productidentery1 = Entry(root, font=("arial", 15, "bold"),width=10)
        self.productidentery1.place(x=widthwin - 1250, y=heightwin - 800)
        self.productidentery1.bind("<Return>",self.sale_return_query)
        self.searxh_prod_return1 = Button(root, text="search", font=(self.font, 12),)
        self.searxh_prod_return1.place(x=widthwin - 1130, y=heightwin - 800)
        self.searxh_prod_return1.bind("<Button-1>",self.sale_return_query)
        self.productnamelabe = Label(root, text="Product Name ", font=(self.font, 14),fg=self.fgcol,bg=self.bgcol)
        self.productnamelabe.place(x=widthwin - 1400, y=heightwin - 750)
        self.productnameentery1 = Entry(root, font=(self.font, 15, "bold"), width=20)
        self.productnameentery1.place(x=widthwin - 1250, y=heightwin - 750)

        self.productpricelable = Label(root, text="Product Price ",bg=self.bgcol,fg=self.fgcol, font=(self.font, 14))
        self.productpricelable.place(x=widthwin - 1400, y=heightwin - 700)
        self.productpriceenteryentery1 = Entry(root, font=(self.font, 15, "bold"), width=20)
        self.productpriceenteryentery1.place(x=widthwin - 1250, y=heightwin - 700)
        self.productidentery1.focus()

    # sale return ======================================================================================================
    def sale_return_query(self,event,*args,**kwargs):
        self.pur_ret_query="SELECT name ,sale_price FROM purchase where product_id=?"
        self.res1=cursor.execute( self.pur_ret_query,(self.productidentery1.get(),))
        for i in self.res1:
            self.productnameentery1.delete(0,END)
            self.productnameentery1.insert(0,i[0])
            self.productpriceenteryentery1.insert(0,i[1])
        self.enterrinvoicelable = Label(root, text="Enter Invoice ", font=(self.font, 14),bg=self.bgcol,fg=self.fgcol)
        self.enterrinvoicelable.place(x=widthwin - 1400, y=heightwin - 650)
        self.enterrinvoiceentery = Entry(root, width=10,font=("arial", 15, "bold"),)
        self.enterrinvoiceentery.place(x=widthwin - 1250, y=heightwin - 650)
        self.enterrinvoiceentery.focus()
        self.enterrinvoiceentery.bind("<Return>",self.cus_identiy)
        self.searxh_prod_return2 = Button(root, text="SEARCH", font=("arial", 10),)
        self.searxh_prod_return2.place(x=widthwin - 1130, y=heightwin - 650)
        self.searxh_prod_return2.bind("<Button-1>",self.cus_identiy)

    def cus_identiy(self,event,*args,**kwargs):

        self.cus_name_identity_lable = Label(root, text="Customer Name ", bg=self.bgcol,fg=self.fgcol,font=(self.font, 14))
        self.cus_name_identity_lable.place(x=widthwin - 1400, y=heightwin - 550)
        self.cus_name_identity_entery = Entry(root, width=20, font=("arial", 15, "bold"))

        self.cus_name_identity_entery.place(x=widthwin - 1250, y=heightwin - 550)

        df=self.enterrinvoiceentery.get()

        query="SELECT name FROM cus_detail WHERE  invoice_no=?"
        res=cursor.execute(query,(self.enterrinvoiceentery.get(),))

        for r in res:

            if len(r)>=1:
                self.cus_name_identity_entery.delete(0,END)
                self.cus_name_identity_entery.insert(0,r[0])
        self.returnquantitylabel=Label(root, text="Entery Quantity ",bg=self.bgcol,fg=self.fgcol, font=("arial", 14))
        self.returnquantitylabel.place(x=widthwin - 1400, y=heightwin - 500)
        self.returnquantityentery=Entry(root, width=10, font=("arial", 14) )
        self.returnquantityentery.place(x=widthwin - 1250, y=heightwin - 500)
        self.returnquantityentery.focus()

        self.returnquantityentery.bind("<Return>",self.final_sale_return)
        self.salereturn = Button(root, text="Return Sale", font=("arial", 13,), bg="green", fg='white',)
        self.salereturn.place(x=widthwin - 1400, y=heightwin - 400)
        self.salereturn.bind("<Button-1>",self.final_sale_return)
        self.exit_sale_return_btn = Button(root, text="EXIT", font=("arial", 13,), bg="red", fg='white',
                                 command=self.exit_sale_return_fun)
        self.exit_sale_return_btn.place(x=widthwin - 1200, y=heightwin - 400)
    def exit_sale_return_fun(self):
        self.productlabel.place_forget()
        self.productidlabel.place_forget()
        self.productidentery1.place_forget()
        self.searxh_prod_return1.place_forget()
        self.productnamelabe.place_forget()
        self.productnameentery1.place_forget()
        self.enterrinvoicelable.place_forget()
        self.enterrinvoiceentery.place_forget()
        self.searxh_prod_return2.place_forget()
        self.cus_name_identity_lable.place_forget()
        self.cus_name_identity_entery.place_forget()
        self.returnquantitylabel.place_forget()
        self.returnquantityentery.place_forget()
        self.salereturn.place_forget()
        self.exit_sale_return_btn.place_forget()
        self.productlabel.place_forget()
        self.productidlabel.place_forget()
        self.productidentery1.place_forget()

        self.productnamelabe.place_forget()
        self.productnameentery1.place_forget()
        self.productpricelable.place_forget()
        self.productpriceenteryentery1.place_forget()
        GasAgency(root)
    def final_sale_return(self,event,*args,**kwargs):
        self.a=self.productidentery1.get()
        self.b=self.productnameentery1.get()
        self.c=self.productpriceenteryentery1.get()

        self.d=self.enterrinvoiceentery.get()
        self.e=self.cus_name_identity_entery.get()
        self.f=self.returnquantityentery.get()

        cursor.execute("CREATE TABLE IF NOT EXISTS sale_return(product_id INTEGAR,prod_name TEXT,prod_price INTGER,invioce_no INTEGAR,customer_name TEXT,quantity_return INTEGER,date TEXT ,time TEXT )")
        self.query="INSERT INTO sale_return (product_id ,prod_name ,prod_price ,invioce_no ,customer_name ,quantity_return,date,time )VALUES(?,?,?,?,?,?,?,?)"
        cursor.execute(self.query,(self.a,self.b,self.c,self.d,self.e,self.f,today,time))
        db.commit()
        self.initial1 = "SELECT * FROM purchase WHERE  product_id=?"
        self.initial_res1 = cursor.execute(self.initial1, (self.productidentery1.get(),))
        for r in self.initial_res1:
            self.old_stock1 = r[3]
            self.new_stock1 = int(self.old_stock1) + int(self.returnquantityentery.get())
            update_query1 = "UPDATE purchase SET quantity=? where product_id=?"
            cursor.execute(update_query1, (self.new_stock1, self.productidentery1.get()))
            db.commit()
            tkinter.messagebox.showinfo("Alert!", "the product has been successfully returned back")
            db.commit()
        self.exit_sale_return_fun()


# purchase return=================================================================
    def purchase_return_byinvoice(self):

        self.purchase_menu.entryconfig("Purchase Product", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.forget_main_widgets()

        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.purchase_menu.entryconfig("Purchase return", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')

        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.main_menu.entryconfig("Search Records", state='disable')
        self.main_menu.entryconfig("Settings", state='disable')
        self.forget_main_widgets()
        # entries for purchase==========================================================================================
        self.productlabel = Label(root, text="Purchase Return ", font=(self.font, 25,"bold"),bg=self.bgcol,fg=self.fgcol)
        self.productlabel.place(x=widthwin - 1250, y=heightwin - 900)
        self.searxh_prod_return1 = Button(root, text="search", font=("arial", 10),)
        self.searxh_prod_return1.place(x=widthwin - 1100, y=heightwin - 800)
        self.productidlabel = Label(root, text="Product ID ", font=(self.font, 14),bg=self.bgcol,fg=self.fgcol)
        self.productidlabel.place(x=widthwin - 1400, y=heightwin - 800)
        self.productidentery2 = Entry(root, font=("arial", 15, "bold"), width=10)
        self.productidentery2.place(x=widthwin - 1250, y=heightwin - 800)
        self.productidentery2.bind("<Return>",self.purchse_return_query)
        self.searxh_prod_return1.bind("<Button-1>",self.purchse_return_query)
        self.productnamelabe = Label(root, text="Product Name ", font=(self.font, 14),bg=self.bgcol,fg=self.fgcol)
        self.productnamelabe.place(x=widthwin - 1400, y=heightwin - 750)
        self.productnameentery2 = Entry(root, font=(self.font, 15, "bold"), width=20)
        self.productnameentery2.place(x=widthwin - 1250, y=heightwin - 750)

        self.productpricelable = Label(root, text="Product Price ", font=(self.font, 14),bg=self.bgcol,fg=self.fgcol)
        self.productpricelable.place(x=widthwin - 1400, y=heightwin - 700)
        self.productpriceenteryentery2 = Entry(root, font=("arial", 15, "bold"), width=20)
        self.productpriceenteryentery2.place(x=widthwin - 1250, y=heightwin - 700)
        self.productidentery2.focus()

    def purchse_return_query(self,event,*args,**kwargs):

        self.pur_ret_query2="SELECT name ,sale_price,seller_id FROM purchase where product_id=?"
        self.res1=cursor.execute( self.pur_ret_query2,(self.productidentery2.get(),))
        for i in self.res1:
            self.productnameentery2.delete(0,END)
            self.productnameentery2.insert(0,i[0])
            self.productpriceenteryentery2.delete(0,END)
            self.productpriceenteryentery2.insert(0,i[1])
            self.s=i[2]
        self.enterrinvoicelable = Label(root, text="seller ID ",bg=self.bgcol,fg=self.fgcol, font=(self.font, 14))
        self.enterrinvoicelable.place(x=widthwin - 1400, y=heightwin - 650)
        self.sellerid2 = Entry(root, width=10,font=(self.font, 15, "bold"),)
        self.sellerid2.place(x=widthwin - 1250, y=heightwin - 650)
        self.sellerid2.focus()
        self.sellerid2.insert(0,self.s)
        self.sellerid2.bind("<Return>",self.purchase_man_identiy)
        self.searxh_prod_return = Button(root, text="search", font=("arial", 10),)
        self.searxh_prod_return.place(x=widthwin - 1100, y=heightwin - 650)
        self.searxh_prod_return.bind("<Button-1>", self.purchase_man_identiy)
    def purchase_man_identiy(self,event,*args,**kwargs):
        self.cus_name_identity_lable2 = Label(root, text="seller Name ", bg=self.bgcol,fg=self.fgcol,font=(self.font, 14))
        self.cus_name_identity_lable2.place(x=widthwin - 1400, y=heightwin - 550)
        self.cus_name_identity_entery22 = Entry(root, width=20, font=("arial", 15, "bold"), )
        self.cus_name_identity_entery22.place(x=widthwin - 1250, y=heightwin - 550)
        self.query_cus2="SELECT name  from seller WHERE seller_id=?"
        self.res=cursor.execute(self.query_cus2,(self.sellerid2.get()))
        for r in self.res:
            self.cus_name_identity_entery22.delete(0,END)
            self.cus_name_identity_entery22.insert(0,r[0])
        self.returnquantitylabel2=Label(root, text="Enter Quantity ",bg=self.bgcol,fg=self.fgcol, font=("arial", 14))
        self.returnquantitylabel2.place(x=widthwin - 1400, y=heightwin - 500)
        self.returnquantityentery22=Entry(root, width=20, font=("arial", 15, "bold"), )
        self.returnquantityentery22.focus()
        self.returnquantityentery22.bind("<Return>",self.final_purchase_return)
        self.returnquantityentery22.place(x=widthwin - 1250, y=heightwin - 500)
        self.purchasereturn2 = Button(root, text="Purchase Return", font=("arial", 13,), bg="green", fg='white',)
        self.purchasereturn2.place(x=widthwin - 1400, y=heightwin - 400)
        self.purchasereturn2.bind("<Button-1>",self.final_purchase_return)
        self.purchaseexit2 = Button(root, text="EXIT", font=("arial", 13,), bg="green", fg='white',
                                   command=self.purchase_return_exit)
        self.purchaseexit2.place(x=widthwin - 1200, y=heightwin - 400)
    def final_purchase_return(self,event,*args,**kwargs):
        self.aa=self.productidentery2.get()
        self.bb=self.productnameentery2.get()
        self.cc=self.productpriceenteryentery2.get()
        self.dd=self.sellerid2.get()
        self.ee=self.cus_name_identity_entery22.get()
        self.ff=self.returnquantityentery22.get()

        cursor.execute("CREATE TABLE IF NOT EXISTS purchase_return(product_id INTEGAR,prod_name TEXT,prod_price INTGER,seller_id INTEGAR,seller_name TEXT,quantity_return INTEGER,date TEXT time TEXT )")
        self.query="INSERT INTO purchase_return (product_id ,prod_name ,prod_price ,seller_id ,seller_name ,quantity_return ,date,time )VALUES(?,?,?,?,?,?,?,?)"
        cursor.execute(self.query,(self.aa,self.bb,self.cc,self.dd,self.ee,self.ff,today,time))

        self.initial1 = "SELECT * FROM purchase WHERE  product_id=?"
        self.initial_res2 = cursor.execute(self.initial1, (self.productidentery2.get(),))
        for r in self.initial_res2:
            self.old_stock2 = r[3]
            self.new_stock2 = int(self.old_stock2) - int(self.returnquantityentery22.get())
            update_query2 = "UPDATE purchase SET quantity=? where product_id=?"
            cursor.execute(update_query2, (self.new_stock2, self.productidentery2.get(),))
            db.commit()
            tkinter.messagebox.showinfo("Alert!", "the product has been successfully returned back")
        db.commit()
        self.productlabel.place_forget()
        self.searxh_prod_return1.place_forget()
        self.productidlabel.place_forget()
        self.productidentery2.place_forget()
        self.productnamelabe.place_forget()
        self.productnameentery2.place_forget()
        self.productpricelable.place_forget()
        self.productpriceenteryentery2.place_forget()
        self.enterrinvoicelable.place_forget()
        self.sellerid2.place_forget()
        self.searxh_prod_return.place_forget()
        self.cus_name_identity_lable2.place_forget()
        self.cus_name_identity_entery22.place_forget()
        self.returnquantitylabel2.place_forget()
        self.returnquantityentery22.place_forget()
        self.purchasereturn2.place_forget()
        self.purchaseexit2.place_forget()

        GasAgency(root)

    def purchase_return_exit(self):
        self.productlabel.place_forget()
        self.searxh_prod_return1.place_forget()
        self.productidlabel.place_forget()
        self.productidentery2.place_forget()
        self.productnamelabe.place_forget()
        self.productnameentery2.place_forget()
        self.productpricelable.place_forget()
        self.productpriceenteryentery2.place_forget()
        self.enterrinvoicelable.place_forget()
        self.sellerid2.place_forget()
        self.searxh_prod_return.place_forget()
        self.cus_name_identity_lable2.place_forget()
        self.cus_name_identity_entery22.place_forget()
        self.returnquantitylabel2.place_forget()
        self.returnquantityentery22.place_forget()
        self.purchasereturn2.place_forget()
        self.purchaseexit2.place_forget()
        GasAgency(root)

#End sale return =============================================================

    def insert_purchase_return(self):
        self.id = self.productidentery.get()
        self.company = self.prodctcompanyentery.get()
        self.name_of_prod = self.namepurchaseentery.get()
        self.qty = self.howmuchpurchaseentery.get()
        self.pur_price = self.productpurpriceentery.get()
        self.sale_price = self.productsalepriceentery.get()
        self.rec_name = self.reciverNameentery.get()
        self.todaydate = today
# ======== cash menu================================================================================
    def search_by_date_res(self):
        self.exit_cash_button = Button(root, text="EXIT", font=(self.font, 12), width=15, bg="red",
                                      command=self.exit_cash)
        self.exit_cash_button.place(x=widthwin - 1220, y=heightwin - 750)
        self.print_cash_button = Button(root, text=" PRINT ", font=(self.font, 12), width=15, bg="red",
                                       command=self.print_cash_hardcopy)
        self.print_cash_button.place(x=widthwin - 1350, y=heightwin - 750)
        self.cash_frame=Frame(root,width=500,height=450)
        self.cash_frame.place(x=widthwin - 1500, y=heightwin - 700)
        self.search_tree_view = tkinter.ttk.Treeview(self.cash_frame, height=20)
        self.search_tree_view.pack(side=LEFT)
        self.cash_scroll=Scrollbar(self.cash_frame,orient="vertical",command=self.search_tree_view.yview)
        self.cash_scroll.pack(side=RIGHT,fill=Y)
        self.cash_scroll.config(command=self.search_tree_view.yview)
        self.search_tree_view['columns'] = ("INVOICE", "Cus Name", "Product", "Quantity", "Amount", "Phone", "Address","profit")
        self.search_tree_view.column("#0", width=0, stretch=NO)
        self.search_tree_view.column("INVOICE", width=120, anchor=W)
        self.search_tree_view.column("Cus Name", width=120, anchor=W)
        self.search_tree_view.column("Product", width=120, anchor=W)
        self.search_tree_view.column("Quantity", width=120, anchor=W)
        self.search_tree_view.column("Amount", width=120, anchor=W)
        self.search_tree_view.column("Phone", width=120, anchor=W)
        self.search_tree_view.column("Address", width=120, anchor=W)
        self.search_tree_view.column("profit", width=120, anchor=W)

        # headinds
        self.search_tree_view.heading("#0", text="")
        self.search_tree_view.heading("INVOICE", text="INVOICE")
        self.search_tree_view.heading("Cus Name", text="Cus Name")
        self.search_tree_view.heading("Product", text="Product")
        self.search_tree_view.heading("Quantity", text="Quantity")
        self.search_tree_view.heading("Amount", text="Amount")
        self.search_tree_view.heading("Phone", text="Phone")
        self.search_tree_view.heading("Address", text="Address")
        self.search_tree_view.heading("profit", text="profit")
        self.total_amount_today=0
        self.total_profit_today=0
        self.query = (
            f"SELECT DISTINCT cus_detail.invoice_no, cus_detail.name,sale_detail.product,sale_detail.quantity,sale_detail.price,cus_detail.phone,cus_detail.address ,sale_detail.date,sale_detail.profit FROM cus_detail,sale_detail  WHERE cus_detail.invoice_no =sale_detail.invoice_no AND sale_detail.date  BETWEEN '{self.search_data_entery_from1.get()}' AND '{self.search_data_entery_to1.get()}'")
        self.dateres = cursor.execute(self.query)
        self.count = 0

        for self.i in self.dateres:
            self.search_tree_view.insert(parent="", index="end", iid=self.count, text="",
                                         values=(self.i[0], self.i[1], self.i[2], self.i[3], self.i[4], self.i[5],
                                                 self.i[6],self.i[8]))
            self.count += 1
            self.total_amount_today += int(self.i[4])
            self.total_profit_today += int(self.i[8])

        self.total_amount_lable=Label(root,text=f"Total Sale From : {self.search_data_entery_from1.get()} To {self.search_data_entery_to1.get()}  is =  {self.total_amount_today}",font=(self.font,14,"bold"),bg=self.bgcol,fg=self.fgcol)
        self.total_amount_lable.place(x=widthwin-1300,y=heightwin-250)
        self.total_profit_lable = Label(root,
                                        text=f"Total Profit From : {self.search_data_entery_from1.get()} To {self.search_data_entery_to1.get()}  is =  {self.total_profit_today}",
                                        font=(self.font, 14,"bold"), bg=self.bgcol, fg=self.fgcol)
        self.total_profit_lable.place(x=widthwin - 1300, y=heightwin - 200)
    def cash(self,*args):
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Search Records", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.main_menu.entryconfig("Settings", state='disable')
        self.forget_main_widgets()
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.fromlabel=Label(root,text="FROM",font=(self.font,12,"bold",),bg=self.bgcol,fg=self.fgcol)
        self.fromlabel.place(x=widthwin-1500,y=heightwin-800)
        self.search_data_entery_from1 = Entry(root, font=(self.font, 12))
        self.search_data_entery_from1.place(x=widthwin - 1400, y=heightwin - 800)
        self.tolabel = Label(root, text="TO", font=(self.font, 12, "bold",),bg=self.bgcol,fg=self.fgcol)
        self.tolabel.place(x=widthwin - 1150, y=heightwin - 800)
        self.search_data_entery_to1= Entry(root, font=(self.font, 12))
        self.search_data_entery_to1.place(x=widthwin - 1100, y=heightwin - 800)
        self.search_data_entery_from1.insert(END,today)
        self.search_data_entery_to1.insert(END,today)
        self.search_record_button = Button(root, text="SEARCH", font=(self.font, 12), width=15,
                                           command=self.search_by_date_res)
        self.search_record_button.place(x=widthwin - 1080, y=heightwin - 750)

    def exit_cash(self):
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Search Records", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')
        self.tolabel.place_forget()
        self.fromlabel.place_forget()
        self.search_data_entery_to1.place_forget()
        self.search_data_entery_from1.place_forget()
        self.search_record_button.place_forget()
        self.exit_cash_button.place_forget()
        self.total_profit_lable.place_forget()
        self.cash_scroll.place_forget()
        self.search_tree_view.destroy()
        self.total_amount_lable.place_forget()
        self.cash_frame.destroy()
        self.print_cash_button.place_forget()
        GasAgency(root)
    def print_cash_hardcopy(self):
        self.directory1 = "E:/" + str("Print Records")
        if not os.path.exists(self.directory1):
            os.mkdir(self.directory1)

        if not os.path.exists(self.directory1 + "/" + str(today)):
            os.mkdir(self.directory1 + "/" + str(today))
        query = "SELECT * FROM security"
        res = cursor.execute(query)
        for r in res:
            self.com = r[2]
            self.add = r[4]
            self.phn = r[3]

        company = self.com
        address = f"{self.add}"
        phone = f"{self.phn}"
        date = "" + str(today) + "|" + str(time)

        bill_header = "\n\n---------------------------------------------------------------------------------------------------------------------\nSr.No:\tinvoice\tCus-Name\tProduct\t\tQTY\tAmount\t\tprofit\n------------------------------------------------------------------------------------------------------------------------"

        final = "Company:" + company + "\t\t\tPhone:" + phone + "\nAddress:" + address + "\t\tdate & time:" + date + "\n" + bill_header
        import random
        for i in range(0, 1):
            self.randomnum = random.randint(0, 1000)

        self.filename1 = str(self.directory1 + "/" + str(today) + "/"+str(self.randomnum)+".txt")
        if self.filename1:
            self.file = open(self.filename1, 'w')
            self.file.write(final)
        else:
            self.file = open(self.filename1, 'w')
            self.file.write(final)
        i = 0
        var = 1
        self.discount1=0
        self.totalsale=0
        self.print_cash_query = (
            f"SELECT DISTINCT cus_detail.invoice_no, cus_detail.name,sale_detail.product,sale_detail.quantity,sale_detail.price,cus_detail.phone,cus_detail.address ,sale_detail.date,sale_detail.profit FROM cus_detail,sale_detail  WHERE cus_detail.invoice_no =sale_detail.invoice_no AND sale_detail.date  BETWEEN '{self.search_data_entery_from1.get()}' AND '{self.search_data_entery_to1.get()}'")
        self.printcash_res = cursor.execute(self.print_cash_query)
        for self.csh in self.printcash_res:

            self.discount1+=self.csh[8]
            self.totalsale+=self.csh[4]
            self.file.write(
                "\n" + str(var) + "\t" + str(self.csh[0]) + "\t" + str(self.csh[1]) + "\t\t" + str(self.csh[2][:7])+"\t\t"+str(self.csh[3])+"\t"+str(self.csh[4])+"\t\t"+str(self.csh[8]))
            i += 1
            var += 1

        self.file.write(
            f"\n\n\t---------------------------------------------------------------------------------------------------------------------\n\n\tDiscount= {self.discount1}\t\tTotal Payment={self.totalsale}")
        os.startfile(self.filename1, 'print')
        self.file.close()
        self.exit_cash()
    def search_record(self):
        self.search_by_record_frame=Frame(root,width=600,height=400)
        self.search_by_record_frame.place(x=widthwin - 1500, y=heightwin - 700)
        self.search_tree_view2 = tkinter.ttk.Treeview(self.search_by_record_frame, height=25)
        self.search_tree_view2.pack(side=LEFT)
        self.search_by_record_scrollbar=Scrollbar(self.search_by_record_frame,orient="vertical",command=self.search_tree_view2.yview)
        self.search_by_record_scrollbar.pack(side=RIGHT,fill=Y)
        self.search_by_record_scrollbar.config(command=self.search_tree_view2.yview)
        self.search_tree_view2['columns'] = ("INVOICE", "Cus Name", "Product","Quantity","Amount","Phone","Address")
        self.search_tree_view2.column("#0", width=0, stretch=NO)
        self.search_tree_view2.column("INVOICE", width=120, anchor=W)
        self.search_tree_view2.column("Cus Name", width=120, anchor=W)
        self.search_tree_view2.column("Product", width=120, anchor=W)
        self.search_tree_view2.column("Quantity", width=120, anchor=W)
        self.search_tree_view2.column("Amount", width=120, anchor=W)
        self.search_tree_view2.column("Phone", width=120, anchor=W)
        self.search_tree_view2.column("Address", width=120, anchor=W)

        # headinds
        self.search_tree_view2.heading("#0", text="")
        self.search_tree_view2.heading("INVOICE",text="INVOICE" )
        self.search_tree_view2.heading("Cus Name", text="Cus Name")
        self.search_tree_view2.heading("Product", text="Product")
        self.search_tree_view2.heading("Quantity", text="Quantity")
        self.search_tree_view2.heading("Amount", text="Amount")
        self.search_tree_view2.heading("Phone", text="Phone")
        self.search_tree_view2.heading("Address", text="Address")

        self.radval=self.radiovar1.get()
        if self.radval ==1:
            self.search_data_entery.focus()
            self.query="SELECT DISTINCT cus_detail.invoice_no, cus_detail.name,sale_detail.product,sale_detail.quantity,sale_detail.price,cus_detail.phone,cus_detail.address FROM cus_detail,sale_detail WHERE cus_detail.invoice_no =sale_detail.invoice_no AND cus_detail.name=?"
            res = cursor.execute(self.query,(self.search_data_entery.get(),))
            self.count=0
            for self.i in res:

                self.search_tree_view2.insert(parent="", index="end", iid=self.count, text="",
                                    values=(self.i[0], self.i[1], self.i[2],self.i[3],self.i[4],self.i[5],self.i[6]))
                self.count+=1
            self.search_by_invoice.configure(state="disable")
            self.search_by_phone.configure(state='disable')
        elif self.radval==2:
            self.search_data_entery.focus()
            self.search_data_entery.focus()
            self.query = "SELECT DISTINCT cus_detail.invoice_no, cus_detail.name,sale_detail.product,sale_detail.quantity,sale_detail.price,cus_detail.phone,cus_detail.address FROM cus_detail,sale_detail WHERE cus_detail.invoice_no =sale_detail.invoice_no AND cus_detail.invoice_no=?"
            res = cursor.execute(self.query, (self.search_data_entery.get(),))
            self.count = 0
            for self.i in res:
                self.search_tree_view2.insert(parent="", index="end", iid=self.count, text="",
                                             values=(self.i[0], self.i[1], self.i[2], self.i[3], self.i[4], self.i[5],
                                                     self.i[6]))
                self.count += 1
            self.search_by_name.configure(state="disable")
            self.search_by_phone.configure(state="disable")
        elif self.radval==3:
            self.search_data_entery.focus()
            self.search_data_entery.focus()
            self.query = "SELECT DISTINCT cus_detail.invoice_no, cus_detail.name,sale_detail.product,sale_detail.quantity,sale_detail.price,cus_detail.phone,cus_detail.address FROM cus_detail,sale_detail WHERE cus_detail.invoice_no =sale_detail.invoice_no AND cus_detail.phone=?"
            res = cursor.execute(self.query, (self.search_data_entery.get(),))
            self.count = 0
            for self.i in res:
                self.search_tree_view2.insert(parent="", index="end", iid=self.count, text="",
                                             values=(self.i[0], self.i[1], self.i[2], self.i[3], self.i[4], self.i[5],
                                                     self.i[6]))
                self.count += 1
            self.search_by_name.configure(state="disable")
            self.search_by_invoice.configure(state="disable")
        else:
            tkinter.messagebox.showinfo("","Please Provide an input")
    def search_by_record(self,*args):
        self.forget_main_widgets()
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.radiovar1 = IntVar()
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.main_menu.entryconfig("Settings", state='disable')
        self.search_menu.entryconfig("Search By Date", state='disable')

        self.search_by_name = Radiobutton(root, text="Name", font=(self.font, 11, "bold"), value=1, variable=self.radiovar1,bg=self.bgcol,fg=self.fgcol)
        self.search_by_name.place(x=widthwin - 1500, y=heightwin - 850)

        self.search_by_invoice = Radiobutton(root, text="INVOICE", font=(self.font, 11, "bold"), value=2, variable=self.radiovar1,bg=self.bgcol,fg=self.fgcol)
        self.search_by_invoice.place(x=widthwin - 1400, y=heightwin - 850)

        self.search_by_phone = Radiobutton(root, text="Phone.No:", font=(self.font, 11, "bold"), value=3, variable=self.radiovar1,bg=self.bgcol,fg=self.fgcol)
        self.search_by_phone.place(x=widthwin - 1300, y=heightwin - 850)
        self.search_data_entery=Entry(root,font=("arial",12))
        self.search_data_entery.place(x=widthwin-1250,y=heightwin-800)
        self.search_data_entery.focus()
        self.search_record_button=Button(root,text="SEARCH",font=("arial",12),width=15,command=self.search_record)
        self.search_record_button.place(x=widthwin-1100,y=heightwin-750)
        self.exit_button = Button(root, text="EXIT", font=(self.font, 12), width=15,bg="red",
                                           command=self.exit_search)
        self.exit_button.place(x=widthwin -1300, y=heightwin - 750)

    def exit_search(self):
        self.search_by_name.place_forget()
        self.search_by_invoice.place_forget()
        self.search_by_phone.place_forget()
        self.search_data_entery.place_forget()
        self.search_record_button.place_forget()
        self.exit_button.place_forget()
        GasAgency(root)
        try:
            self.search_tree_view2.place_forget()
            self.search_by_record_scrollbar.destroy()
            self.search_by_record_frame.destroy()
        except:
            pass
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')
        self.search_menu.entryconfig("Search by Record", state='normal')

    def search_by_date_res1(self):
        self.search_tree_frame1=Frame(root,height=350,width=800)
        self.search_tree_frame1.place(x=widthwin - 1500, y=heightwin - 700)
        self.search_tree_view1 = tkinter.ttk.Treeview(self.search_tree_frame1, height=20)
        self.search_tree_view1.pack(side=LEFT)
        #adding a scrollbar
        self.tree_scroll_bar1=tkinter.Scrollbar(self.search_tree_frame1,orient="vertical",command=self.search_tree_view1.yview)
        self.tree_scroll_bar1.pack(fill=Y,side=RIGHT)
        self.tree_scroll_bar1.config(command=self.search_tree_view1.yview)
        self.search_tree_view1['columns'] = ("INVOICE", "Cus Name", "Product", "Quantity", "Amount", "Phone", "Address")
        self.search_tree_view1.column("#0", width=0, stretch=NO)
        self.search_tree_view1.column("INVOICE", width=120, anchor=W)
        self.search_tree_view1.column("Cus Name", width=120, anchor=W)
        self.search_tree_view1.column("Product", width=120, anchor=W)
        self.search_tree_view1.column("Quantity", width=120, anchor=W)
        self.search_tree_view1.column("Amount", width=120, anchor=W)
        self.search_tree_view1.column("Phone", width=120, anchor=W)
        self.search_tree_view1.column("Address", width=120, anchor=W)

        # headinds
        self.search_tree_view1.heading("#0", text="")
        self.search_tree_view1.heading("INVOICE", text="INVOICE")
        self.search_tree_view1.heading("Cus Name", text="Cus Name")
        self.search_tree_view1.heading("Product", text="Product")
        self.search_tree_view1.heading("Quantity", text="Quantity")
        self.search_tree_view1.heading("Amount", text="Amount")
        self.search_tree_view1.heading("Phone", text="Phone")
        self.search_tree_view1.heading("Address", text="Address")

        self.query = (
            f"SELECT DISTINCT cus_detail.invoice_no, cus_detail.name,sale_detail.product,sale_detail.quantity,sale_detail.price,cus_detail.phone,cus_detail.address ,sale_detail.date FROM cus_detail,sale_detail  WHERE cus_detail.invoice_no =sale_detail.invoice_no AND sale_detail.date  BETWEEN '{self.search_data_entery_from.get()}' AND '{self.search_data_entery_to.get()}'")
        self.dateres = cursor.execute(self.query)
        self.count = 0
        for self.i in self.dateres:

            self.search_tree_view1.insert(parent="", index="end", iid=self.count, text="",
                                         values=(self.i[0], self.i[1], self.i[2], self.i[3], self.i[4], self.i[5],
                                                 self.i[6]))

            self.count += 1
    def search_by_date(self,*args):
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.main_menu.entryconfig("Settings", state='disable')
        self.search_menu.entryconfig("Search by Record", state='disable')

        self.forget_main_widgets()
        self.invoice_no.place_forget()
        self.fromlabel=Label(root,text="FROM",font=(self.font,12,"bold",),bg=self.bgcol,fg=self.fgcol)
        self.fromlabel.place(x=widthwin-1500,y=heightwin-800)
        self.search_data_entery_from = Entry(root, font=("arial", 12))
        self.search_data_entery_from.place(x=widthwin - 1400, y=heightwin - 800)
        self.tolabel = Label(root, text="TO", bg=self.bgcol,fg=self.fgcol,font=(self.font, 12, "bold",))
        self.tolabel.place(x=widthwin - 1150, y=heightwin - 800)
        self.search_data_entery_to= Entry(root, font=("arial", 12))
        self.search_data_entery_to.place(x=widthwin - 1100, y=heightwin - 800)
        self.search_data_entery_from.insert(END,today)
        self.search_record_button = Button(root, text="SEARCH", bg=self.bgcol,fg=self.fgcol,font=(self.font, 12), width=15,
                                           command=self.search_by_date_res1)
        self.search_record_button.place(x=widthwin - 1100, y=heightwin - 750)
        self.searchdate_exit_button = Button(root, text="EXIT", font=("arial", 12), width=15,bg='red',command=self.exit_search_by_date)
        self.searchdate_exit_button.place(x=widthwin - 1300, y=heightwin - 750)

    def exit_search_by_date(self):
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.fromlabel.place_forget()
        self.search_data_entery_from.place_forget()
        self.tolabel.place_forget()
        self.search_data_entery_to.place_forget()
        self.search_record_button.place_forget()
        self.searchdate_exit_button.place_forget()
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')
        self.search_menu.entryconfig("Search by Record", state='normal')
        GasAgency(root)
        # self.search_tree_view1.destroy()
        # self.tree_scroll_bar1.destroy()
        try:
            self.search_tree_frame1.destroy()
            self.search_tree_view1.destroy()
            self.tree_scroll_bar1.destroy()
        except:
            pass
    def background_color(self,*kwargs):

        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.main_menu.entryconfig("Search Records", state='disable')
        self.forget_main_widgets()
        self.invoice.place_forget()
        self.invoice_no.place_forget()

        self.backgroundlabel=Label(root,text="Back Ground Color",font=(self.font,12),bg=self.bgcol,fg=self.fgcol)
        self.backgroundlabel.place(x=widthwin-1500,y=heightwin-800)
        self.bgvar=StringVar()
        self.optionmenubgcolor=OptionMenu(root,self.bgvar,"white", "black", "gray", "green", "blue", "pink","orange","light blue","cyan")
        self.optionmenubgcolor.place(x=widthwin-1350,y=heightwin-800)
        # self.bgvar.set("red")

        self.textlabel = Label(root, text="Text Color", font=(self.font, 12),bg=self.bgcol,fg=self.fgcol)
        self.textlabel.place(x=widthwin - 1200, y=heightwin - 800)
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.fgvar = StringVar()
        self.optionmenufgcolor = OptionMenu(root, self.fgvar, "white", "black", "gray", "green", "blue", "pink","orange","light blue","cyan")
        self.optionmenufgcolor.place(x=widthwin - 1100, y=heightwin - 800)
        # self.fgvar.set("black")
        self.fontlabel = Label(root, text="Font", font=(self.font, 12),bg=self.bgcol,fg=self.fgcol)
        self.fontlabel.place(x=widthwin - 950, y=heightwin - 800)
        self.fontvar = StringVar()
        self.fontlist = OptionMenu(root, self.fontvar ,'Terminal', 'System', 'Fixedsys', 'Modern', 'Roman', 'Script', 'Courier','Marlett', 'Arial','Calibri','Candara', 'Consolas', 'Constantia' ,'Corbel','Ebrima','Gabriola','Gadugi', 'Georgia', 'Impact', 'Javanese')
        self.fontlist.place(x=widthwin - 900, y=heightwin - 800)
        # self.fontvar.set("Arial")
        self.applybtn = Button(root, text="Apply Changes", bg="red", font=("arial", 12, "bold"), command=self.applybg)
        self.applybtn.place(x=widthwin - 1100, y=heightwin - 400)
        cursor.execute("CREATE TABLE IF NOT EXISTS bgcolor(back_color TEXT,text_color TEXT,font TEXT )")
        self.res2 = cursor.execute("SELECT  count(*) FROM bgcolor ")
        for j in self.res2:
            k=int(j[0])
            if k<=0:
                query = "INSERT INTO  bgcolor (back_color,text_color,font) VALUES(?,?,?)"
                cursor.execute(query, (self.bgvar.get(), self.fgvar.get(), self.fontvar.get()), )
                db.commit()
        quer = cursor.execute("SELECT * FROM bgcolor")
        for qr in quer:
            self.a = qr[0]
            self.b = qr[1]
            self.c = qr[2]
        self.bgvar.set(self.a)
        self.fgvar.set(self.b)
        self.fontvar.set(self.c)
    def applybg(self):

        self.res2 = cursor.execute("SELECT  count(*) FROM bgcolor ")
        for i in self.res2:
            if len(i)>0:
                queryupdate = "UPDATE  bgcolor SET  back_color=?,text_color=?,font=?"
                cursor.execute(queryupdate,(self.bgvar.get(),self.fgvar.get(),self.fontvar.get()))
                db.commit()
                tkinter.messagebox.showinfo("Congrats", "System Updated !!!")
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.main_menu.entryconfig("Search Records", state='normal')

        self.backgroundlabel.place_forget()
        self.optionmenubgcolor.place_forget()
        self.backgroundlabel.place_forget()
        self.optionmenufgcolor.place_forget()
        self.textlabel.place_forget()
        self.fontlabel.place_forget()
        self.fontlist.place_forget()
        self.applybtn.place_forget()
        GasAgency(root)
    #===============---------------=============---------------=============================----- searching record of sale and purchase return
    def search_sale_return(self):
        self.forget_main_widgets()
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.invoice_var=IntVar()
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.search_menu.entryconfig("Search by Record", state='disable')
        self.search_menu.entryconfig("Search By Date", state='disable')
        self.search_menu.entryconfig("Purchase Return", state='disable')
        self.main_menu.entryconfig("Settings", state='disable')
        self.radioinvoice=Radiobutton(root,text="By Invioce",variable=self.invoice_var,value=1,command=self.search_by_invoice_no,font=(self.font,12),bg=self.bgcol,fg=self.fgcol)
        self.radioinvoice.place(x=widthwin-1200,y=heightwin-800)
        self.radiobydate=Radiobutton(root,text="By Date",variable=self.invoice_var,value=2,command=self.search_by_date_of,font=(self.font,12),bg=self.bgcol,fg=self.fgcol)
        self.radiobydate.place(x=widthwin-1000,y=heightwin-800)
        self.search_invoice_button=Button(root,text="OK",fg=self.fgcol,bg=self.bgcol,font=(self.font,12),width=25,activebackground="red",command=self.search_sale_return_result)
        self.search_invoice_button.place(x=widthwin-1200,y=heightwin-750)
    def search_sale_return_result_(self):

        self.search_sale_return_frame = Frame(root, height=350, width=800)
        self.search_sale_return_frame.place(x=widthwin - 1500, y=heightwin - 500)
        self.search_sale_return_tree = tkinter.ttk.Treeview(self.search_sale_return_frame, height=15)
        self.search_sale_return_tree.pack(side=LEFT)
        # adding a scrollbar
        self.search_sale_return_scrollbar = tkinter.Scrollbar(self.search_sale_return_frame, orient="vertical",
                                                  command=self.search_sale_return_tree.yview)
        self.search_sale_return_scrollbar.pack(fill=Y, side=RIGHT)
        self.search_sale_return_scrollbar.config(command=self.search_sale_return_tree.yview)
        self.search_sale_return_tree['columns'] = ("prod id", "prod Name", "Price", "invoice", "cus name", "QTY Return", "date","time")
        self.search_sale_return_tree.column("#0", width=0, stretch=NO)
        self.search_sale_return_tree.column("prod id", width=80, anchor=W)
        self.search_sale_return_tree.column("prod Name", width=120, anchor=W)
        self.search_sale_return_tree.column("Price", width=120, anchor=W)
        self.search_sale_return_tree.column("invoice", width=120, anchor=W)
        self.search_sale_return_tree.column("cus name", width=120, anchor=W)
        self.search_sale_return_tree.column("QTY Return", width=120, anchor=W)
        self.search_sale_return_tree.column("date", width=120, anchor=W)
        self.search_sale_return_tree.column("time", width=120, anchor=W)


        # headinds
        self.search_sale_return_tree.heading("#0", text="")
        self.search_sale_return_tree.heading("prod id", text="prod id")
        self.search_sale_return_tree.heading("prod Name", text="prod Name")
        self.search_sale_return_tree.heading("Price", text="Price")
        self.search_sale_return_tree.heading("invoice", text="invoice")
        self.search_sale_return_tree.heading("cus name", text="cus name")
        self.search_sale_return_tree.heading("QTY Return", text="QTY Return")
        self.search_sale_return_tree.heading("date", text="date")
        self.search_sale_return_tree.heading("time", text="time")
#======================================================================== sale return by invoice===============
    def invice_result_(self):
        self.radiobydate.config(state="disable")
        self.entrinvoicelable = Label(root, text="Enter Invoice", font=(self.font, 12), bg=self.bgcol, fg=self.fgcol)
        self.entrinvoicelable.place(x=widthwin - 1250, y=heightwin - 650)
        self.entrinvoiceentery = Entry(root, font=(self.font, 12), width=12)
        self.entrinvoiceentery.place(x=widthwin - 1100, y=heightwin - 650)
        self.entrinvoiceentery.focus()
        self.search_invoice_button1 = Button(root, text="search", fg=self.fgcol, bg=self.bgcol, font=(self.font, 12),
                                             width=10, activebackground="red", command=self.insert_final_results)
        self.search_invoice_button1.place(x=widthwin - 950, y=heightwin - 650)

    def insert_final_results(self):
        self.search_sale_return_result_()
        self.exit_by_invoice = Button(root, text="EXIT", fg="white", bg="red", font=(self.font, 12),
                                   width=10, activebackground="red", command=self.exit_invoice_search_by_invoice)
        self.exit_by_invoice.place(x=widthwin - 1100, y=heightwin - 600)
        self.search_sale_return_query_ = ("SELECT * FROM sale_return WHERE invioce_no=?")
        self.search_sale_return_query_result = cursor.execute(self.search_sale_return_query_,
                                                              (self.entrinvoiceentery.get()))
        var = 0
        for self.z in self.search_sale_return_query_result:
            self.search_sale_return_tree.insert(parent="", index="end", iid=self.z, text="",
                                                values=(
                                                    self.z[0], self.z[1], self.z[2], self.z[3], self.z[4], self.z[5],
                                                    self.z[6], self.z[7]))

            var += 1

    def inset_data_sale_return_by_invoice(self):
        self.search_invoice_button1.place(x=widthwin - 950, y=heightwin - 650)
        self.search_sale_return_query_ = ("SELECT * FROM sale_return WHERE invioce_no=?")
        self.search_sale_return_query_result = cursor.execute(self.search_sale_return_query_,
                                                              (self.entrinvoiceentery.get()))
        var = 0
        for self.z in self.search_sale_return_query_result:
            self.search_sale_return_tree.insert(parent="", index="end", iid=self.z, text="",
                                                values=(
                                                    self.z[0], self.z[1], self.z[2], self.z[3], self.z[4], self.z[5],
                                                    self.z[6], self.z[7]))

            var += 1
#====================================================search purchase return by date======================================
    def sale_return_by_date_entries(self):
        self.radioinvoice.config(state="disable")
        self.search_sale_return_from_lable_from = Label(root, text="FROM", font=(self.font, 12), bg=self.bgcol, fg=self.fgcol)
        self.search_sale_return_from_lable_from.place(x=widthwin - 1300, y=heightwin - 650)
        self.search_sale_return_from_entery_from = Entry(root, font=(self.font, 12), width=12)
        self.search_sale_return_from_entery_from.place(x=widthwin - 1150, y=heightwin - 650)

        self.search_sale_return_from_lable_to = Label(root, text="TO", font=(self.font, 12), bg=self.bgcol, fg=self.fgcol)
        self.search_sale_return_from_lable_to.place(x=widthwin - 1000, y=heightwin - 650)
        self.search_sale_return_from_entery_to = Entry(root, font=(self.font, 12), width=12)
        self.search_sale_return_from_entery_to.place(x=widthwin - 850, y=heightwin - 650)
        self.search_invoice_button1 = Button(root, text="search", fg=self.fgcol, bg=self.bgcol, font=(self.font, 12),
                                             width=10, activebackground="red", command=self.search_sale_return_bydate)
        self.search_invoice_button1.place(x=widthwin - 900, y=heightwin - 600)
        self.search_sale_return_from_entery_to.insert(0,today)
        self.search_sale_return_from_entery_from.insert(0, today)

    def search_sale_return_bydate(self):

        self.exit_by_date = Button(root, text="EXIT", fg="white", bg="red", font=(self.font, 12),
                                   width=10, activebackground="red", command=self.exit_invoice_search_by_date)
        self.exit_by_date.place(x=widthwin - 1100, y=heightwin - 600)

        self.search_sale_return_query_result1 = cursor.execute(f"SELECT * FROM sale_return WHERE date BETWEEN '{self.search_sale_return_from_entery_from.get()}' AND '{self.search_sale_return_from_entery_to.get()}'")
        var = 0
        self.search_sale_return_result_()
        for self.y in self.search_sale_return_query_result1:

            self.search_sale_return_tree.insert(parent="", index="end", iid=self.y, text="",
                                                values=(
                                                    self.y[0], self.y[1], self.y[2], self.y[3], self.y[4], self.y[5],
                                                    self.y[6], self.y[7]))
            var += 1
    def search_sale_return_result(self):
        if self.invoice_var.get()==1:
            self.invice_result_()

        if self.invoice_var.get()==2:
            self.sale_return_by_date_entries()
    def exit_invoice_search_by_date(self):
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.search_menu.entryconfig("Search by Record", state='normal')
        self.search_menu.entryconfig("Search By Date", state='normal')
        self.search_menu.entryconfig("Purchase Return", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')

        self.radioinvoice.place_forget()
        self.radiobydate.place_forget()
        self.search_invoice_button.place_forget()
        self.exit_by_date.place_forget()
        self.search_sale_return_from_lable_from.place_forget()
        self.search_sale_return_from_entery_from.place_forget()
        self.search_sale_return_from_lable_to.place_forget()
        self.search_sale_return_from_entery_to.place_forget()
        self.search_invoice_button1.place_forget()
        self.search_sale_return_tree.destroy()
        self.search_sale_return_scrollbar.destroy()
        self.search_sale_return_frame.destroy()
        GasAgency(root)
    def exit_invoice_search_by_invoice(self):
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.search_menu.entryconfig("Search by Record", state='normal')
        self.search_menu.entryconfig("Search By Date", state='normal')
        self.search_menu.entryconfig("Purchase Return", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')
        self.entrinvoicelable.place_forget()
        self.entrinvoiceentery.place_forget()
        self.search_invoice_button1.place_forget()
        self.radioinvoice.place_forget()
        self.search_invoice_button.place_forget()
        self.search_invoice_button1.place_forget()
        self.search_sale_return_tree.destroy()
        self.search_sale_return_scrollbar.destroy()
        self.search_sale_return_frame.destroy()
        self.exit_by_invoice.place_forget()
        GasAgency(root)

    def search_by_invoice_no(self):
        pass
    def search_by_date_of(self):
        pass
    def search_purchase_return(self):
        pass
#============================ purchase return search====================================================================
    def search_purchase_turn(self):
        self.forget_main_widgets()
        self.invoice.place_forget()
        self.invoice_no.place_forget()
        self.invoice_var1=IntVar()
        self.main_menu.entryconfig("Purchase", state="disable")
        self.main_menu.entryconfig("Cash", state='disable')
        self.main_menu.entryconfig("Sales Return", state='disable')
        self.main_menu.entryconfig("Seller", state='disable')
        self.search_menu.entryconfig("Search by Record", state='disable')
        self.search_menu.entryconfig("Search By Date", state='disable')
        self.search_menu.entryconfig("Purchase Return", state='disable')
        self.main_menu.entryconfig("Settings", state='disable')
        self.radioinvoice1=Radiobutton(root,text="By Invioce",variable=self.invoice_var1,value=1,font=(self.font,12),bg=self.bgcol,fg=self.fgcol)
        self.radioinvoice1.place(x=widthwin-1200,y=heightwin-800)
        self.radiobydate1=Radiobutton(root,text="By Date",variable=self.invoice_var1,value=2,font=(self.font,12),bg=self.bgcol,fg=self.fgcol)
        self.radiobydate1.place(x=widthwin-1000,y=heightwin-800)
        self.search_invoice_button1=Button(root,text="OK",fg=self.fgcol,bg=self.bgcol,font=(self.font,12),width=25,activebackground="red",command=self.search_purchase_return_result)
        self.search_invoice_button1.place(x=widthwin-1200,y=heightwin-750)

    def search_purchase_return_result_(self):

        self.search_sale_return_frame1 = Frame(root, height=350, width=800)
        self.search_sale_return_frame1.place(x=widthwin - 1500, y=heightwin - 500)
        self.search_sale_return_tree1 = tkinter.ttk.Treeview(self.search_sale_return_frame1, height=15)
        self.search_sale_return_tree1.pack(side=LEFT)
        # adding a scrollbar
        self.search_sale_return_scrollbar1 = tkinter.Scrollbar(self.search_sale_return_frame1, orient="vertical",
                                                  command=self.search_sale_return_tree1.yview)
        self.search_sale_return_scrollbar1.pack(fill=Y, side=RIGHT)
        self.search_sale_return_scrollbar1.config(command=self.search_sale_return_tree1.yview)
        self.search_sale_return_tree1['columns'] = ("prod id", "prod Name", "Price", "seller id", "QTY", "date","time")
        self.search_sale_return_tree1.column("#0", width=0, stretch=NO)
        self.search_sale_return_tree1.column("prod id", width=80, anchor=W)
        self.search_sale_return_tree1.column("prod Name", width=120, anchor=W)
        self.search_sale_return_tree1.column("Price", width=120, anchor=W)
        self.search_sale_return_tree1.column("seller id", width=120, anchor=W)
        self.search_sale_return_tree1.column("QTY", width=120, anchor=W)
        self.search_sale_return_tree1.column("date", width=120, anchor=W)
        self.search_sale_return_tree1.column("time", width=120, anchor=W)


        # headinds
        self.search_sale_return_tree1.heading("#0", text="")
        self.search_sale_return_tree1.heading("prod id", text="prod id")
        self.search_sale_return_tree1.heading("prod Name", text="prod Name")
        self.search_sale_return_tree1.heading("Price", text="Price")
        self.search_sale_return_tree1.heading("seller id", text="invoice")
        self.search_sale_return_tree1.heading("QTY", text="QTY")
        self.search_sale_return_tree1.heading("date", text="date")
        self.search_sale_return_tree1.heading("time", text="time")
    def purchase_invice_result_(self):
        self.radiobydate1.config(state="disable")
        self.entrinvoicelable1 = Label(root, text="Enter Invoice", font=(self.font, 12), bg=self.bgcol, fg=self.fgcol)
        self.entrinvoicelable1.place(x=widthwin - 1250, y=heightwin - 650)
        self.entrinvoiceentery1 = Entry(root, font=(self.font, 12), width=12)
        self.entrinvoiceentery1.place(x=widthwin - 1100, y=heightwin - 650)
        self.entrinvoiceentery1.focus()
        self.search_invoice_button11 = Button(root, text="search", fg=self.fgcol, bg=self.bgcol, font=(self.font, 12),
                                             width=10, activebackground="red", command=self.purchase_insert_final_results_invoice)
        self.search_invoice_button11.place(x=widthwin - 950, y=heightwin - 650)
    def purchase_return_by_date_entries(self):
        self.radioinvoice1.config(state="disable")
        self.search_sale_return_from_lable_from1 = Label(root, text="FROM", font=(self.font, 12), bg=self.bgcol, fg=self.fgcol)
        self.search_sale_return_from_lable_from1.place(x=widthwin - 1300, y=heightwin - 650)
        self.search_sale_return_from_entery_from1 = Entry(root, font=(self.font, 12), width=12)
        self.search_sale_return_from_entery_from1.place(x=widthwin - 1150, y=heightwin - 650)

        self.search_sale_return_from_lable_to1 = Label(root, text="TO", font=(self.font, 12), bg=self.bgcol, fg=self.fgcol)
        self.search_sale_return_from_lable_to1.place(x=widthwin - 1000, y=heightwin - 650)
        self.search_sale_return_from_entery_to1 = Entry(root, font=(self.font, 12), width=12)
        self.search_sale_return_from_entery_to1.place(x=widthwin - 850, y=heightwin - 650)
        self.search_invoice_button11 = Button(root, text="search", fg=self.fgcol, bg=self.bgcol, font=(self.font, 12),
                                             width=10, activebackground="red", command=self.search_purchase_return_bydate)
        self.search_invoice_button11.place(x=widthwin - 900, y=heightwin - 600)
        self.search_sale_return_from_entery_to1.insert(0,today)
        self.search_sale_return_from_entery_from1.insert(0, today)

    def search_purchase_return_bydate(self):
        self.exit_by_date1 = Button(root, text="EXIT", fg="white", bg="red", font=(self.font, 12),
                                   width=10, activebackground="red", command=self.exit_invoice_search_by_date_purchase)
        self.exit_by_date1.place(x=widthwin - 1100, y=heightwin - 600)

        self.search_sale_return_query_result1 = cursor.execute(
            f"SELECT * FROM purchase_return WHERE date BETWEEN '{self.search_sale_return_from_entery_from1.get()}' AND '{self.search_sale_return_from_entery_to1.get()}'")
        var = 0
        self.search_purchase_return_result_()
        for self.y in self.search_sale_return_query_result1:
            self.search_sale_return_tree1.insert(parent="", index="end", iid=self.y, text="",
                                                values=(
                                                    self.y[0], self.y[1], self.y[2], self.y[3], self.y[4],
                                                    self.y[5],
                                                    self.y[6]))
            var += 1
    def purchase_insert_final_results_invoice(self):
        self.search_purchase_return_result_()
        self.exit_by_invoice1 = Button(root, text="EXIT", fg="white", bg="red", font=(self.font, 12),
                                   width=10, activebackground="red", command=self.exit_invoice_search_by_invoice_purchase)
        self.exit_by_invoice1.place(x=widthwin - 1100, y=heightwin - 600)
        self.search_purchase_return_query_ = ("SELECT * FROM purchase_return WHERE product_id=?")
        self.search_purchase_return_query_result = cursor.execute(self.search_purchase_return_query_,
                                                              (self.entrinvoiceentery1.get()))
        var = 0
        for self.z in self.search_purchase_return_query_result:
            self.search_sale_return_tree1.insert(parent="", index="end", iid=self.z, text="",
                                                values=(
                                                    self.z[0], self.z[1], self.z[2], self.z[3], self.z[4], self.z[5],
                                                    self.z[6],))

            var += 1
    def search_purchase_return_result(self):
        if self.invoice_var1.get()==1:
            self.purchase_invice_result_()

        if self.invoice_var1.get()==2:
            self.purchase_return_by_date_entries()
    def exit_invoice_search_by_date_purchase(self):
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.search_menu.entryconfig("Search by Record", state='normal')
        self.search_menu.entryconfig("Search By Date", state='normal')
        self.search_menu.entryconfig("Purchase Return", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')

        self.radioinvoice1.place_forget()
        self.radiobydate1.place_forget()
        self.search_invoice_button1.place_forget()
        self.exit_by_date1.place_forget()
        self.search_sale_return_from_lable_from1.place_forget()
        self.search_sale_return_from_entery_from1.place_forget()
        self.search_sale_return_from_lable_to1.place_forget()
        self.search_sale_return_from_entery_to1.place_forget()
        self.search_invoice_button11.place_forget()
        self.search_sale_return_tree1.destroy()
        self.search_sale_return_scrollbar1.destroy()
        self.search_sale_return_frame1.destroy()

        GasAgency(root)
    def exit_invoice_search_by_invoice_purchase(self):
        self.main_menu.entryconfig("Purchase", state="normal")
        self.main_menu.entryconfig("Cash", state='normal')
        self.main_menu.entryconfig("Sales Return", state='normal')
        self.main_menu.entryconfig("Seller", state='normal')
        self.search_menu.entryconfig("Search by Record", state='normal')
        self.search_menu.entryconfig("Search By Date", state='normal')
        self.search_menu.entryconfig("Purchase Return", state='normal')
        self.main_menu.entryconfig("Settings", state='normal')
        self.entrinvoicelable1.place_forget()
        self.entrinvoiceentery1.place_forget()
        self.search_invoice_button11.place_forget()
        self.radioinvoice1.place_forget()
        self.search_invoice_button1.place_forget()
        self.search_invoice_button11.place_forget()
        self.search_sale_return_tree1.destroy()
        self.search_sale_return_scrollbar1.destroy()
        self.search_sale_return_frame1.destroy()
        self.exit_by_invoice1.place_forget()
        GasAgency(root)

    def print_hard(self):

        self.directory="E:/"+str("Agency Records")
        if not os.path.exists(self.directory):
                os.mkdir(self.directory)
        # directory1=os.mkdir(directory+"/"+str(today))
        if not os.path.exists(self.directory+"/"+str(today)):
            os.mkdir(self.directory+"/"+str(today))
        query="SELECT * FROM security"
        res=cursor.execute(query)
        for r in res:
            self.com=r[2]
            self.add=r[4]
            self.phn=r[3]

        company=self.com
        address=f"{self.add}"
        phone=f"{self.phn}"
        date=""+str(today)+"|"+ str(time)

        bill_header="\n\n--------------------------------------------------------------------------------------------\nSr. No: \t\tproducts\t\tQuantity\t\tPrice\n\t\t--------------------------------------------------------------------------------------------"

        bill_footer=f"\n\n\t\t--------------------------------------------------------------------------------------------\n\t\tDiscount:\t\t\t\tPayment:"
        final="Company:"+company+"\t\t\tPhone:"+phone+"\nAddress:"+address+"\t\tdate & time:"+date+"\n"+bill_header



        self.filename=str(self.directory+"/"+str(today)+"/"+str(self.invoice)+".txt")
        if self.filename:
            self.file=open(self.filename,'w')
            self.file.write(final)
        else:
            self.file = open(self.filename, 'w')
            self.file.write(final)
        i=0
        var=1
        for r in products:
            self.file.write("\n"+str(var)+"\t\t"+str(products[i]+".....")[:7]+"\t\t"+str(quantity[i])+"\t\t"+str(price[i]))
            i+=1
            var+=1


        self.file.write(f"\n\n\t\t---------------------------------------------------------------------------------------------\n\n\tDiscount= {sum(discount)}\t\tTotal Payment={sum(price)}")
        os.startfile(self.filename,'print')
        self.file.close()

def check():

    global labelusername1
    global enteryusername1
    global labelpassword1
    global enterypassword1
    global enteryusername
    global labelconfirmpassword
    global enteryconfirmpassword
    global labelcompanyname
    global enterycomapnyname
    global enteryphone
    global enteryaddress
    global emailentery
    global secretwordentrey
    global buttonOKandproceed
    global emaillable
    global secretwordlable
    global Lableaddress
    global lablephoneNo
    global labelusername
    global enteryusername
    global labelpassword
    global enterypassword
    if enteryusername1.get() == "":
        tkinter.messagebox.showerror("Error", "User Name is not filled successfully")
    elif enterypassword1.get() == "":
        tkinter.messagebox.showerror("Error", "Password is not filled successfully")
    elif enteryconfirmpassword.get() == "":
        tkinter.messagebox.showerror("Error", "Confirm Password filled successfully")
    elif enterypassword1.get() != enteryconfirmpassword.get():
        tkinter.messagebox.showerror("Error", "password did not matched")

    elif enterycomapnyname.get() == "":
        tkinter.messagebox.showerror("Error", "Company Name is not filled successfully")
    elif len(enterypassword1.get()) <=3:
        tkinter.messagebox.showerror("Error", "Password too short,Minimum 4 Letters")
    elif enteryphone.get() == "" or len(enteryphone.get())<=10 :
        tkinter.messagebox.showerror("Error", "Phone Number is not correct")
    elif enterycomapnyname.get() == "":
        tkinter.messagebox.showerror("Error", "please Provide an address")
    elif secretwordentrey.get()=="" or len(secretwordentrey.get())<=3:
        tkinter.messagebox.showerror("Error", "please provide a concise word")

    else:
        cursor.execute("CREATE TABLE IF NOT EXISTS security(user_name TEXT ,password INTEGER,company TEXT,phone TEXT,address TEXT,fav_word TEXT,email TEXT)")
        query = "INSERT INTO  security(user_name ,password,company,phone,address,fav_word,email)VALUES(?,?,?,?,?,?,?)"
        cursor.execute(query, (enteryusername1.get(), enterypassword1.get(), enterycomapnyname.get(),enteryphone.get(),enteryaddress.get(),secretwordentrey.get(),emailentery.get()))
        db.commit()
        var = tkinter.messagebox.askyesno("Congratulation ",
                                          f"user '{enteryusername1.get()} 'has been registered Successfuly ,Do you want to proceed further.  ")
        if var >= 1:

            labelusername1.place_forget()
            labelcompanyname.place_forget()
            labelpassword1.place_forget()
            enterycomapnyname.place_forget()
            enterypassword1.place_forget()
            enteryusername1.place_forget()
            buttonOK.place_forget()
            labelconfirmpassword.place_forget()
            enteryconfirmpassword.place_forget()
            didnothaveacc.place_forget()

            buttonOK.place_forget()
            buttonOKandproceed.place_forget()
            enteryphone.place_forget()
            secretwordentrey.place_forget()
            enteryaddress.place_forget()
            emailentery.place_forget()
            emaillable.place_forget()
            secretwordlable.place_forget()
            Lableaddress.place_forget()
            lablephoneNo.place_forget()
            labelusername.place_forget()
            enteryusername.place_forget()
            enterypassword.place_forget()
            labelpassword.place_forget()
            try:
                signubtn.place_forget()
            except:
                pass
            GasAgency(root)
        else:
            root.destroy()
def check_update():

    global labelusername1
    global enteryusername1
    global labelpassword1
    global enterypassword1
    global enteryusername
    global labelconfirmpassword
    global enteryconfirmpassword
    global labelcompanyname
    global enterycomapnyname
    global enteryphone
    global enteryaddress
    global emailentery
    global secretwordentrey
    global buttonOKandproceed
    global emaillable
    global secretwordlable
    global Lableaddress
    global lablephoneNo
    global labelusername
    global enteryusername
    global labelpassword
    global enterypassword
    if enteryusername1.get() == "":
        tkinter.messagebox.showerror("Error", "User Name is not filled successfully")
    elif enterypassword1.get() == "":
        tkinter.messagebox.showerror("Error", "Password is not filled successfully")
    elif enteryconfirmpassword.get() == "":
        tkinter.messagebox.showerror("Error", "Confirm Password filled successfully")
    elif enterypassword1.get() != enteryconfirmpassword.get():
        tkinter.messagebox.showerror("Error", "password did not matched")

    elif enterycomapnyname.get() == "":
        tkinter.messagebox.showerror("Error", "Company Name is not filled successfully")
    elif len(enterypassword1.get()) <=3:
        tkinter.messagebox.showerror("Error", "Password too short,Minimum 4 Letters")
    elif enteryphone.get() == "" or len(enteryphone.get())<=10 :
        tkinter.messagebox.showerror("Error", "Phone Number is not correct")
    elif enterycomapnyname.get() == "":
        tkinter.messagebox.showerror("Error", "please Provide an address")
    elif secretwordentrey.get()=="" or len(secretwordentrey.get())<=3:
        tkinter.messagebox.showerror("Error", "please provide a concise word")

    else:
        # cursor.execute("CREATE TABLE IF NOT EXISTS security(user_name TEXT ,password INTEGER,company TEXT,phone TEXT,address TEXT,fav_word TEXT,email TEXT)")
        query = "UPDATE   security SET user_name=? ,password=?,company=?,phone=?,address=?,fav_word=?,email=?"
        cursor.execute(query, (enteryusername1.get(), enterypassword1.get(), enterycomapnyname.get(),enteryphone.get(),enteryaddress.get(),secretwordentrey.get(),emailentery.get()))
        db.commit()
        var = tkinter.messagebox.askyesno("Congratulation ","Your password has been updated successfully\nDo you want to proceed for further?")
        if var >= 1:

            labelusername1.place_forget()
            labelcompanyname.place_forget()
            labelpassword1.place_forget()
            enterycomapnyname.place_forget()
            enterypassword1.place_forget()
            enteryusername1.place_forget()
            buttonOK.place_forget()
            labelconfirmpassword.place_forget()
            enteryconfirmpassword.place_forget()
            didnothaveacc.place_forget()

            buttonOK.place_forget()
            buttonOKandproceed.place_forget()
            enteryphone.place_forget()
            secretwordentrey.place_forget()
            enteryaddress.place_forget()
            emailentery.place_forget()
            emaillable.place_forget()
            secretwordlable.place_forget()
            Lableaddress.place_forget()
            lablephoneNo.place_forget()
            labelusername.place_forget()
            enteryusername.place_forget()
            enterypassword.place_forget()
            labelpassword.place_forget()
            try:
                signubtn.place_forget()
            except:
                pass
            GasAgency(root)
        else:
            root.destroy()

def signup():
    global labelusername1
    global enteryusername1
    global enteryusername
    global labelpassword1
    global enterypassword1
    global labelconfirmpassword
    global enteryconfirmpassword
    global labelcompanyname
    global enterycomapnyname
    global buttonOKandproceed
    global enteryphone
    global enteryaddress
    global emailentery
    global secretwordentrey
    global emaillable
    global secretwordlable
    global Lableaddress
    global lablephoneNo
    global signubtn
    global reset_password
    didnothaveacc.place_forget()
    buttonOK.place_forget()
    try:
        signubtn.place_forget()
    except:
        pass

    labelusername1 = Label(root, text="Enter User Name:", font=("arial", 13, "bold"), fg='blue')
    labelusername1.place(x=300, y=200)
    enteryusername1 = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryusername1.place(x=550, y=200)
    enteryusername1.focus()
    labelpassword1 = Label(root, text="Enter Password", font=("arial", 13, "bold"), fg='blue')
    labelpassword1.place(x=300, y=250)
    enterypassword1 = Entry(root, width=20, font=("arial", 13, "bold"))
    enterypassword1.place(x=550, y=250)
    enteryusername1.bind("<Return>", lambda event: enterypassword1.focus())
    labelconfirmpassword = Label(root, text="Confirm Password", font=("arial", 13, "bold"), fg='blue')
    labelconfirmpassword.place(x=300, y=300)
    enteryconfirmpassword = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryconfirmpassword.place(x=550, y=300)
    enterypassword1.bind("<Return>", lambda event: enteryconfirmpassword.focus())
    labelcompanyname = Label(root, text="Company Name", font=("arial", 13, "bold"), fg='blue')
    labelcompanyname.place(x=300, y=350)
    enteryconfirmpassword.bind("<Return>", lambda event: enterycomapnyname.focus())
    enterycomapnyname = Entry(root, width=20, font=("arial", 13, "bold"))
    enterycomapnyname.place(x=550, y=350)
    lablephoneNo=Label(root, text="Phone Number", font=("arial", 13, "bold"), fg='blue')
    lablephoneNo.place(x=300, y=400)
    enteryphone = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryphone.place(x=550, y=400)
    enterycomapnyname.bind("<Return>", lambda event: enteryphone.focus())
    Lableaddress = Label(root, text="Address", font=("arial", 13, "bold"), fg='blue')
    Lableaddress.place(x=300, y=450)
    enteryaddress = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryaddress.place(x=550, y=450)
    enteryphone.bind("<Return>", lambda event: enteryaddress.focus())
    # enterycomapnyname.bind("<Return>",lambda event:buttonOK.focus())
    secretwordlable=Label(root, text="favourite word", font=("arial", 13, "bold"), fg='blue')
    secretwordlable.place(x=300, y=500)
    secretwordentrey=Entry(root, width=20, font=("arial", 13, "bold"))
    secretwordentrey.place(x=550, y=500)
    enteryaddress.bind("<Return>", lambda event: secretwordentrey.focus())
    emaillable = Label(root, text="E-mail", font=("arial", 13, "bold"), fg='blue')
    emaillable.place(x=300, y=550)
    emailentery = Entry(root, width=20, font=("arial", 13, "bold"))
    emailentery.place(x=550, y=550)
    secretwordentrey.bind("<Return>", lambda event: emailentery.focus())
    buttonOKandproceed = Button(root, text="Ok and Proceed", command=check, font=("cooper black", 13), width=15,
                                bg="yellow")
    buttonOKandproceed.place(x=500, y=600)
    # secretwordentrey.bind("<Return>", lambda event: buttonOKandproceed.focus())
    # buttonOKandproceed.bind("<Return>",lambda event:signup().foucus())
def signup_update():
    global labelusername1
    global enteryusername1
    global enteryusername
    global labelpassword1
    global enterypassword1
    global labelconfirmpassword
    global enteryconfirmpassword
    global labelcompanyname
    global enterycomapnyname
    global buttonOKandproceed
    global enteryphone
    global enteryaddress
    global emailentery
    global secretwordentrey
    global emaillable
    global secretwordlable
    global Lableaddress
    global lablephoneNo
    global signubtn
    global reset_password
    didnothaveacc.place_forget()
    buttonOK.place_forget()
    try:
        signubtn.place_forget()
    except:
        pass

    labelusername1 = Label(root, text="Enter User Name:", font=("arial", 13, "bold"), fg='blue')
    labelusername1.place(x=300, y=200)
    enteryusername1 = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryusername1.place(x=550, y=200)
    enteryusername1.focus()
    labelpassword1 = Label(root, text="Enter Password", font=("arial", 13, "bold"), fg='blue')
    labelpassword1.place(x=300, y=250)
    enterypassword1 = Entry(root, width=20, font=("arial", 13, "bold"))
    enterypassword1.place(x=550, y=250)
    enteryusername1.bind("<Return>", lambda event: enterypassword1.focus())
    labelconfirmpassword = Label(root, text="Confirm Password", font=("arial", 13, "bold"), fg='blue')
    labelconfirmpassword.place(x=300, y=300)
    enteryconfirmpassword = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryconfirmpassword.place(x=550, y=300)
    enterypassword1.bind("<Return>", lambda event: enteryconfirmpassword.focus())
    labelcompanyname = Label(root, text="Company Name", font=("arial", 13, "bold"), fg='blue')
    labelcompanyname.place(x=300, y=350)
    enteryconfirmpassword.bind("<Return>", lambda event: enterycomapnyname.focus())
    enterycomapnyname = Entry(root, width=20, font=("arial", 13, "bold"))
    enterycomapnyname.place(x=550, y=350)
    lablephoneNo=Label(root, text="Phone Number", font=("arial", 13, "bold"), fg='blue')
    lablephoneNo.place(x=300, y=400)
    enteryphone = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryphone.place(x=550, y=400)
    enterycomapnyname.bind("<Return>", lambda event: enteryphone.focus())
    Lableaddress = Label(root, text="Address", font=("arial", 13, "bold"), fg='blue')
    Lableaddress.place(x=300, y=450)
    enteryaddress = Entry(root, width=20, font=("arial", 13, "bold"))
    enteryaddress.place(x=550, y=450)
    enteryphone.bind("<Return>", lambda event: enteryaddress.focus())
    # enterycomapnyname.bind("<Return>",lambda event:buttonOK.focus())
    secretwordlable=Label(root, text="favourite word", font=("arial", 13, "bold"), fg='blue')
    secretwordlable.place(x=300, y=500)
    secretwordentrey=Entry(root, width=20, font=("arial", 13, "bold"))
    secretwordentrey.place(x=550, y=500)
    enteryaddress.bind("<Return>", lambda event: secretwordentrey.focus())
    emaillable = Label(root, text="E-mail", font=("arial", 13, "bold"), fg='blue')
    emaillable.place(x=300, y=550)
    emailentery = Entry(root, width=20, font=("arial", 13, "bold"))
    emailentery.place(x=550, y=550)
    secretwordentrey.bind("<Return>", lambda event: emailentery.focus())
    buttonOKandproceed = Button(root, text="Ok and Proceed", command=check_update, font=("cooper black", 13), width=15,
                                bg="yellow")
    buttonOKandproceed.place(x=500, y=600)


def forget_password():
    global favwordentery
    global reset_password
    labelusername.place_forget()
    enteryusername.place_forget()
    labelpassword.place_forget()
    enterypassword.place_forget()
    buttonOK.place_forget()
    didnothaveacc.place_forget()
    didforget.place_forget()
    reset_password.place_forget()
    global favwordlabel
    global favwordentery
    global forget_pass_btn
    favwordlabel = Label(root, text="Enter Fav.word", font=("arial", 13, "bold"), fg='blue')
    favwordlabel.place(x=300, y=300)
    favwordentery = Entry(root, width=20, font=("arial", 13, "bold"))
    favwordentery.place(x=550, y=300)
    favwordentery.focus()
    favwordentery.bind("<Return>",match_word)
    forget_pass_btn = Button(root, text="FORGET", command=match_word, font=("cooper black", 13), width=15,
                                bg="yellow")
    forget_pass_btn.place(x=500, y=400)

def match_word(event):
    gap=cursor.execute('SELECT fav_word FROM security')
    for i in gap:
        if i[0]==favwordentery.get():
            signup_update()
            favwordlabel.place_forget()
            favwordentery.place_forget()
            forget_pass_btn.place_forget()
        else:
            tkinter.messagebox.showinfo("SORRY;","Your favourite word did not matched")

    # passcheckquery='SELECT password or fav_word FROM security'
    # cursor.execute(passcheckquery,(forgetpasswordentery.get(),favwordentery.get()))
    # for j in passcheck:


def login(*args,**kwargs):
    password = enterypassword.get()
    username = enteryusername.get()
    res = ("SELECT * FROM security WHERE user_name=? and password=?")
    cursor.execute(res, [(username), (password)])
    result = cursor.fetchall()
    if result:

        labelusername.place_forget()
        enteryusername.place_forget()
        labelpassword.place_forget()
        enterypassword.place_forget()
        buttonOK.place_forget()
        didforget.place_forget()
        reset_password.place_forget()

        didnothaveacc.place_forget()
        try:
            signubtn.place_forget()
        except:
            pass
        GasAgency(root)
    else:
        tkinter.messagebox.showerror("ERROR", "Access denied ")

global labelusername
global enteryusername
global labelpassword
global enterypassword

labelusername = Label(root, text="Enter User Name:", font=("arial", 13, "bold"), fg='blue')
labelusername.place(x=300, y=200)
enteryusername = Entry(root, width=20, font=("arial", 13, "bold"))
enteryusername.place(x=550, y=200)
try:
    selct_name=cursor.execute("SELECT user_name from security")
    for name in selct_name:
        selected_name=name[0]
        enteryusername.insert(0,selected_name)
except:
    pass
labelpassword = Label(root, text="Enter Password:", font=("arial", 13, "bold"), fg='blue')
labelpassword.place(x=300, y=250)
loginbtn=PhotoImage(file="login.png")

buttonOK = Button(root, text="Login",image=loginbtn, command=login,borderwidth=0)
buttonOK.place(x=600, y=290)


didnothaveacc = Label(root, text="did not have an account? sign-up ", font=("arial", 13, "bold"), fg='blue')
didnothaveacc.place(x=300, y=350)

enterypassword = Entry(root,  show="⚫", font=( "arial",12,))
enterypassword.place(x=550, y=250)

enterypassword.focus()

enterypassword.bind("<Return>",login)



cursor.execute("CREATE TABLE IF NOT EXISTS security(user_name TEXT ,password INTEGER,company TEXT,phone TEXT,address TEXT,fav_word TEXT,email TEXT)")
db.commit()
check_password=cursor.execute('SELECT COUNT(*) FROM security')

for i in check_password:
    if i[0]<=0:

        global reset_password
        signubtn = Button(root, text="sign-up", font=("cooper black", 13), width=12,  command=signup )
        signubtn.place(x=580, y=400)
    else:
        global didforget
        didforget = Label(root, text=" Forgot password? Please insert your favourite word to reset ", font=("arial", 13, "bold"), fg='blue')
        didforget.place(x=300, y=350)
        reset_password = Button(root, text="Reset Password", font=("cooper black", 13), width=12, command=forget_password)
        reset_password.place(x=580, y=400)

name_of_store=cursor.execute("SELECT company from security")
for name in name_of_store:
    root.title(f"                                                                                                                                                                                                  "
           f"{name[0]} ")

root.geometry(str(widthwin) + "x" + str(heightwin))
root.mainloop()

