from tkinter import *
from tkinter import ttk

import csv_handler
from fonts import *
from utils import *
from csv_handler import *

#class function calls add product button in main, to run def function that contains buttons annd displays, applicationlayout its
#use self function to access class
#create list of product window
#for most buttons, it will only run and execute the code if there is no error. search button and clear button are the only exceptions
class ListOfProduct:
    # display buttons, textbox layout #creating app buttons and functionality
    def __init__(self):
        reset()
        self.window = Toplevel()
        self.window.geometry("589x600")
        Label(self.window, width=28, text="List of Products", font=times_new_roman, bg="pink").grid(row=0, columnspan=3)

        self.column_name1 = Entry(self.window, width=4, bg="light grey")
        self.column_name1.insert(0, "ID")
        self.column_name1.grid(row=1, column=0)

        self.column_name2 = Entry(self.window, width=50, bg="light grey")
        self.column_name2.insert(0, "PRODUCT NAME")
        self.column_name2.grid(row=1, column=1)

        self.column_name3 = Entry(self.window, width=9, bg="light grey")
        self.column_name3.insert(0, "PRICE")
        self.column_name3.grid(row=1, column=2)

        plus = 100

        self.prev_list = Button(self.window, text="< Prev", font=Sans_button, command=lambda: self.display('prev'))
        self.next_list = Button(self.window, text="Next >", font=Sans_button, command=lambda: self.display('next'))
        self.prev_list.place(x=54.5, y=250 + plus)
        self.next_list.place(x=104.5, y=250 + plus)

        self.search_box = Entry(self.window, width=20)
        self.search_box.place(x=180.5, y=250 + plus)

        self.search_button = Button(self.window, text="SEARCH", font=Sans_button, width=7,
                                    command=lambda: self.display('search'))
        self.search_button.place(x=389.5, y=250 + plus)

        self.clear_button = Button(self.window, text="CLEAR", font=Sans_button, width=7,
                                   command=lambda: self.display('clear'))
        self.clear_button.place(x=389.5, y=280 + plus)

        Label(self.window, text="Product Name", bg="pink", font=verdana).place(x=44.5, y=310 + plus)
        self.product_name = Entry(self.window, width=50)
        self.product_name.place(x=44.5, y=330 + plus)

        self.price_default = IntVar(self.window)
        Label(self.window, text="Price", bg="pink", font=verdana).place(x=44.5, y=360 + plus)
        self.price = Spinbox(self.window, from_=0, to=1000, width=9, textvariable=self.price_default)
        self.price.place(x=89.5, y=360 + plus)

        self.add_button = Button(self.window, text="ADD", font=Sans_button, width=7, command=self.add)
        self.add_button.place(x=289.5, y=360 + plus)

        self.edit_button = Button(self.window, text="EDIT", font=Sans_button, width=7, command=self.edit)
        self.edit_button.place(x=289.5, y=390 + plus)

        self.delete_button = Button(self.window, text="DELETE", font=Sans_button, width=7, command=self.delete)
        self.delete_button.place(x=289.5, y=420 + plus)

        self.display()

        self.window.resizable(False, False)
        self.window.configure(bg="pink")
        self.window.mainloop()

    #to display table in list of products
    def display(self, command=''):
        get_data(table_name_='product')
        #if conditions are to call self. functions in def init self
        #if user clicks on next button,it checks length of data and if there is a next page
        if command == 'next':
            if not gv.search and len(gv.data) - 1 >= gv.maximum:
                next_()
            if gv.search and len(gv.search_data) - 1 >= gv.maximum:
                next_()
        elif command == 'prev' and gv.minimum > 0:
            prev_()
        elif command == 'search':
            reset()
            if self.search_box.get() != '':
                search(self.search_box.get(), 'product')
                gv.search = True
        elif command == 'clear':
            self.search_box.delete(0, 'end')
            gv.search = False
        #if there is no search filter, all data from gvdata is appended to display data
        #if search is true, data appended will be dependent on search filter
        #if range of appended data is less than the maximum, other rows will be kept empty
        display_data = []
        if len(gv.data) != 0:
            if gv.search is True:
                if len(gv.search_data) != 0:
                    for i in range(gv.minimum, gv.maximum):
                        display_data.append(gv.search_data[i])
                        if i == len(gv.search_data) - 1:
                            for j in range(gv.maximum - len(display_data)):
                                display_data.append(('', '', ''))
                            break
            else:
                for i in range(gv.minimum, gv.maximum):
                    display_data.append(gv.data[i])
                    if i == len(gv.data) - 1:
                        for j in range(gv.maximum - len(display_data)):
                            display_data.append(('', '', ''))
                        break

        #displays appended data
        for i in range(2, 12):
            color = "pink" if i % 2 == 0 else "light grey"

            (product_id, product_name, price) = display_data[i - 2] if len(display_data) != 0 else ('', '', '')

            column_1 = Entry(self.window, width=4, bg=color)
            column_1.grid(row=i, column=0)
            column_1.insert(0, product_id)

            column_2 = Entry(self.window, width=50, bg=color)
            column_2.grid(row=i, column=1)
            column_2.insert(0, product_name)

            column_3 = Entry(self.window, width=9, bg=color)
            column_3.grid(row=i, column=2)
            column_3.insert(0, price)

    #def function to delete what was typed in textbox
    def input_delete(self):
        self.product_name.delete(0, 'end')
        self.price_default.set(0)

    #def function to add input data in database if no error(calling add product in database.py)
    #after input data is added in database, inventory system is also updated
    def add(self):
        product = (self.product_name.get(), int(self.price.get()))
        get_error(input_=product, window_='ListOfProduct', command_='add')

        if gv.input_error is False:
            self.input_delete()
            add_product(product)
            self.display()

    #def function when using edit button, data will be extracted from database which will allow the data in the inventory system to be editable
    #can correct spelling and price, changes will be saved using def save_edit function
    def edit(self):
        prev_data = tuple()
        get_error(input_=(self.product_name.get(),), window_='ListOfProduct', command_='edit')
        if gv.input_error is False:
            prev_data = get_data(table_name_='product', column_name_='product_name, price',
                                 filter_='product_name', filter_value_=self.product_name.get())
            get_error(input_=prev_data, window_='ListOfProduct', command_='edit')

        if gv.input_error is False:
            self.add_button.config(state=DISABLED)
            self.edit_button.config(state=DISABLED)
            self.delete_button.config(state=DISABLED)

            self.price_default.set(prev_data[1])

            save_button = Button(self.window, text="SAVE", font=Sans_button, width=7, command=lambda: save_edit())
            save_button.place(x=289.5, y=450)

        def save_edit():
            self.add_button.config(state=NORMAL)
            self.edit_button.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)
            product_name, price = (self.product_name.get(), int(self.price.get()))
            print(product_name, price)

            product_value = f"product_name = '{product_name}', price = {price}"
            update(table_name_='product', set_value=product_value,
                   filter_='product_name', filter_value_=prev_data[0])

            save_button.destroy()

            self.input_delete()
            self.display()

    #def function when using delete button, data will be deleted from the database and the inventory system
    def delete(self):
        prev_data = tuple()
        get_error(input_=(self.product_name.get(),), window_='ListOfProduct', command_='delete')

        if gv.input_error is False:
            prev_data = get_data(table_name_='product', column_name_='product_name',
                                 filter_='product_name', filter_value_=self.product_name.get())
            print(prev_data)
            get_error(input_=prev_data, window_='ListOfProduct', command_='delete')

        if gv.input_error is False:
            delete(table_name_='product', filter_='product_name', filter_value_=prev_data[0])
            delete(table_name_='inventory', filter_='product_name', filter_value_=prev_data[0])
            self.input_delete()
            self.display()

#second window with layout buttons functionality
class AddStock:
    def __init__(self):
        reset()
        self.window = Toplevel()
        self.window.geometry('630x700')

        self.month, self.day, self.year = get_date()
        print(self.month, self.day, self.year)
        create_table(self.month, self.year, 'PurchaseHistory')

        self.month_label = StringVar(self.window)
        self.month_label.set(f"{self.month} Stock")
        Label(self.window, textvariable=self.month_label,
              font=times_new_roman, bg="pink").grid(row=0, columnspan=5)

        self.column_name1 = Entry(self.window, width=4, bg="light grey")
        self.column_name1.insert(0, "ID")
        self.column_name1.grid(row=1, column=0)

        self.column_name2 = Entry(self.window, width=10, bg="light grey")
        self.column_name2.insert(0, "DATE")
        self.column_name2.grid(row=1, column=1)

        self.column_name3 = Entry(self.window, width=5, bg="light grey")
        self.column_name3.insert(0, "QTY")
        self.column_name3.grid(row=1, column=2)

        self.column_name4 = Entry(self.window, width=50, bg="light grey")
        self.column_name4.insert(0, "PRODUCT NAME")
        self.column_name4.grid(row=1, column=3)

        plus = 100

        self.prev_list = Button(self.window, text="< Prev", font=Sans_button, command=lambda: self.display('prev'))
        self.next_list = Button(self.window, text="Next >", font=Sans_button, command=lambda: self.display('next'))
        self.prev_list.place(x=82.25, y=250 +plus)
        self.next_list.place(x=132.25, y=250 +plus)

        self.search_box = Entry(self.window, width=20)
        self.search_box.place(x=230, y=250 +plus)

        self.search_button = Button(self.window, text="SEARCH", font=Sans_button, width=7,
                                    command=lambda: self.display('search'))
        self.search_button.place(x=460, y=250 +plus)

        self.clear_button = Button(self.window, text="CLEAR", font=Sans_button, width=7,
                                   command=lambda: self.display('clear'))
        self.clear_button.place(x=460, y=280 +plus)

        Label(self.window, text="Product Name", bg="pink", font=verdana).place(x=14.5, y=310)
        self.product_name = ttk.Combobox(self.window, width=50, textvariable=StringVar())
        product_list = ['No Product Yet']
        for i in get_data(table_name_='product', column_name_='product_name'):
            product_list.append(i[0])
            if 'No Product Yet' in product_list:
                product_list.remove('No Product Yet')
        self.product_name['values'] = product_list
        self.product_name.place(x=14.5, y=330 +plus)
        self.product_name.current(0)

        self.qty_default = IntVar(self.window)
        Label(self.window, text="QTY", bg="pink", font=verdana).place(x=354.5, y=310 +plus)
        self.qty = Spinbox(self.window, from_=0, to=1000, width=8, textvariable=self.qty_default)
        self.qty.place(x=500.5, y=330 +plus)

        self.id_default = IntVar(self.window)
        Label(self.window, text="ID", bg="pink", font=verdana).place(x=14.5, y=360 +plus)
        self.purchase_id = Spinbox(self.window, from_=0, to=1000, width=8, textvariable=self.id_default)
        self.purchase_id.place(x=44.5, y=360 +plus)

        self.add_button = Button(self.window, text="ADD", font=Sans_button, width=7, command=self.add)
        self.add_button.place(x=360, y=360 +plus)

        self.edit_button = Button(self.window, text="EDIT", font=Sans_button, width=7, command=self.edit)
        self.edit_button.place(x=360, y=390 +plus)

        self.delete_button = Button(self.window, text="DELETE", font=Sans_button, width=7, command=self.delete)
        self.delete_button.place(x=360, y=420 +plus)

        self.month_cb = ttk.Combobox(self.window, width=11, textvariable=StringVar())
        month_list = []
        for i in calendar.month_name:
            if '' in month_list:
                month_list.remove('')
            month_list.append(i)
        self.month_cb['values'] = month_list
        self.month_cb.place(x=14.5, y=420 +plus)
        self.month_cb.current(0)

        self.year_default = IntVar(self.window)
        self.year_sp = Spinbox(self.window, width=5, from_=2000, to_=3000, textvariable=self.year_default)
        self.year_sp.place(x=135.5, y=420 +plus)
        self.year_default.set(self.year)

        self.date_button = Button(self.window, text="GO", font=Sans_button, width=3, command=self.set_date)
        self.date_button.place(x=230.5, y=420 +plus)

        if 'No Product Yet' in product_list:
            self.add_button.config(state=DISABLED)

        self.display()

        self.window.resizable(False, False)
        self.window.configure(bg="pink")
        self.window.mainloop()

    #to display table in add stock
    def display(self, command=''):
        get_data(table_name_=f'"{self.month} {self.year} purchase"')

        if not len(gv.data):
            self.edit_button.config(state=DISABLED)
            self.delete_button.config(state=DISABLED)
        else:
            self.edit_button.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)

        if self.month != calendar.month_name[int(date.today().month)]:
            self.add_button.config(state=DISABLED)
        else:
            self.add_button.config(state=NORMAL)

        if command == 'next':
            if not gv.search and len(gv.data) - 1 >= gv.maximum:
                next_()
            if gv.search and len(gv.search_data) - 1 >= gv.maximum:
                next_()
        elif command == 'prev' and gv.minimum > 0:
            prev_()
        elif command == 'search':
            reset()
            if self.search_box.get() != '':
                search(self.search_box.get(), 'purchase')
                gv.search = True
        elif command == 'clear':
            self.search_box.delete(0, 'end')
            gv.search = False

        display_data = []
        if len(gv.data) != 0:
            if gv.search is True:
                if len(gv.search_data) != 0:
                    for i in range(gv.minimum, gv.maximum):
                        display_data.append(gv.search_data[i])
                        if i == len(gv.search_data) - 1:
                            for j in range(gv.maximum - len(display_data)):
                                display_data.append(('', '', '', ''))
                            break
            else:
                for i in range(gv.minimum, gv.maximum):
                    display_data.append(gv.data[i])
                    if i == len(gv.data) - 1:
                        for j in range(gv.maximum - len(display_data)):
                            display_data.append(('', '', '', ''))
                        break

        for i in range(2, 12):
            color = "pink" if i % 2 == 0 else "light grey"

            (purchase_id, date_purchased, qty, product_name) = \
                display_data[i - 2] if len(display_data) != 0 else ('', '', '', '')

            column_1 = Entry(self.window, width=4, bg=color)
            column_1.grid(row=i, column=0)
            column_1.insert(0, purchase_id)

            column_2 = Entry(self.window, width=10, bg=color)
            column_2.grid(row=i, column=1)
            column_2.insert(0, date_purchased)

            column_3 = Entry(self.window, width=5, bg=color)
            column_3.grid(row=i, column=2)
            column_3.insert(0, qty)

            column_4 = Entry(self.window, width=50, bg=color)
            column_4.grid(row=i, column=3)
            column_4.insert(0, product_name)

    #def function to delete what was typed in textbox
    def input_delete(self):
        self.qty_default.set(0)
        self.id_default.set(0)

    #def function to add input data in database if no error(calling add product in database.py)
    #after input data is added in database, inventory system is also updated
    def add(self):
        get_error(input_=int(self.qty.get()), window_='PurchaseHistory', command_='add')

        if gv.input_error is False:
            product = (date.today(), int(self.qty.get()), self.product_name.get())

            purchase(self.month, self.year, product)

            self.input_delete()
            self.display()

    #def function when using edit button, data will be extracted from database which will allow the data in the inventory system to be editable
    #can correct spelling and price, changes will be saved using def save_edit function
    def edit(self):
        get_error(input_=int(self.purchase_id.get()), window_='PurchaseHistory', command_='edit')

        if gv.input_error is False:
            prev_data = get_data(table_name_=f'"{self.month} {self.year} purchase"',
                                 column_name_='id, date, QTY, product_name',
                                 filter_='id', filter_value_=f'{self.purchase_id.get()}')
            get_error(input_=prev_data, window_='PurchaseHistory', command_='edit')

            if gv.input_error is False:
                self.add_button.config(state=DISABLED)
                self.edit_button.config(state=DISABLED)
                self.delete_button.config(state=DISABLED)

                self.id_default.set(prev_data[0])
                self.qty_default.set(prev_data[2])
                self.product_name.set(prev_data[3])

                save_button = Button(self.window, text="SAVE", font=Sans_button, width=7, command=lambda: save_edit())
                save_button.place(x=390, y=450)

        def save_edit():
            self.add_button.config(state=NORMAL)
            self.edit_button.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)

            if int(self.qty.get()) != prev_data[2]:
                qty = int(self.qty.get())
                inventory_qty, rsp = get_data(table_name_='inventory', column_name_='QTY, RSP',
                                              filter_='product_name', filter_value_=f'{prev_data[3]}')
                new_amount = qty * rsp

                update(table_name_=f"'{self.month} {self.year} purchase'",
                       set_value=f"QTY = {qty}, amount = {new_amount}",
                       filter_='id', filter_value_=prev_data[0])

                purchase_total = 0
                for i, in get_data(table_name_=f"'{self.month} {self.year} purchase'", column_name_='amount',
                                   filter_='date', filter_value_=prev_data[1], fetch='all'):
                    purchase_total += i

                update(table_name_=f"'{self.month} {self.year} purchase_total'",
                       set_value=f"total = {purchase_total}",
                       filter_='date', filter_value_=prev_data[1])

                if qty > prev_data[2]:
                    inventory_qty += (qty - prev_data[2])
                else:
                    inventory_qty -= (prev_data[2] - qty)

                update(table_name_='inventory', set_value=f'QTY = {inventory_qty}',
                       filter_='product_name', filter_value_=prev_data[3])
            elif self.product_name.get() != prev_data[3]:
                product_name = self.product_name.get()
                rsp, = get_data(table_name_='inventory', column_name_='RSP',
                                filter_='product_name', filter_value_=f'{product_name}')
                new_amount = prev_data[2] * rsp

                update(table_name_=f"'{self.month} {self.year} purchase'",
                       set_value=f"product_name = '{product_name}', amount = {new_amount}",
                       filter_='id', filter_value_=prev_data[0])

                purchase_total = 0
                for i, in get_data(table_name_=f"'{self.month} {self.year} purchase'", column_name_='amount',
                                   filter_='date', filter_value_=prev_data[1], fetch='all'):
                    purchase_total += i

                update(table_name_=f"'{self.month} {self.year} purchase_total'",
                       set_value=f"total = {purchase_total}",
                       filter_='date', filter_value_=prev_data[1])

                inventory_qty, = get_data(table_name_='inventory', column_name_='QTY',
                                          filter_='product_name', filter_value_=f'{prev_data[3]}')
                inventory_qty -= prev_data[2]
                update(table_name_='inventory', set_value=f'QTY = {inventory_qty}',
                       filter_='product_name', filter_value_=prev_data[3])

                inventory_qty, = get_data(table_name_='inventory', column_name_='QTY',
                                          filter_='product_name', filter_value_=f'{product_name}')
                inventory_qty += prev_data[2]
                update(table_name_='inventory', set_value=f'QTY = {inventory_qty}',
                       filter_='product_name', filter_value_=product_name)

            self.input_delete()
            save_button.destroy()
            self.display()

    #def function when using delete button, data will be deleted from the database and the inventory system
    def delete(self):
        get_error(input_=int(self.purchase_id.get()), window_='PurchaseHistory', command_='delete')

        if gv.input_error is False:
            prev_data = get_data(table_name_=f'"{self.month} {self.year} purchase"',
                                 column_name_='id, date, QTY, product_name',
                                 filter_='id', filter_value_=f'{self.purchase_id.get()}')
            get_error(input_=prev_data, window_='PurchaseHistory', command_='delete')

            if gv.input_error is False:
                delete(table_name_=f'"{self.month} {self.year} purchase"', filter_='id', filter_value_=prev_data[0])

                inventory_qty, = get_data(table_name_='inventory', column_name_='QTY',
                                          filter_='product_name', filter_value_=f'{prev_data[3]}')

                purchase_total = 0
                for i, in get_data(table_name_=f"'{self.month} {self.year} purchase'", column_name_='amount',
                                   filter_='date', filter_value_=prev_data[1], fetch='all'):
                    purchase_total += i

                update(table_name_=f"'{self.month} {self.year} purchase_total'",
                       set_value=f"total = {purchase_total}",
                       filter_='date', filter_value_=prev_data[1])

                inventory_qty -= prev_data[2]

                update(table_name_='inventory', set_value=f'QTY = {inventory_qty}',
                       filter_='product_name', filter_value_=prev_data[3])

                self.input_delete()
                self.display()

    #if user wants to check previous data, this def functions allows to view past months and years
    def set_date(self):
        get_error(input_=f'"{self.month_cb.get()} {self.year_sp.get()} purchase"',
                  window_="PurchaseHistory", command_="set_date")
        if gv.input_error is False:
            self.month = self.month_cb.get()
            self.year = self.year_sp.get()
            self.month_label.set(f"{self.month} Purchase History")
            print(self.month, self.year)
            reset()
            self.display()

#third window setup/layout/buttons/functionality
class Sales:
    def __init__(self):
        reset()
        self.window = Toplevel()
        self.window.geometry("722x700")

        self.month, self.day, self.year = get_date()
        print(self.month, self.day, self.year)
        create_table(self.month, self.year, 'Sales')

        self.month_label = StringVar(self.window)
        self.month_label.set(f"{self.month} Sales")
        Label(self.window, width=28, textvariable=self.month_label,
              font=times_new_roman, bg="pink").grid(row=0, columnspan=7)

        self.column_name1 = Entry(self.window, width=4, bg="#FF3399")
        self.column_name1.insert(0, "ID")
        self.column_name1.grid(row=1, column=0)

        self.column_name2 = Entry(self.window, width=12, bg="#FF3399")
        self.column_name2.insert(0, "DATE")
        self.column_name2.grid(row=1, column=1)

        self.column_name3 = Entry(self.window, width=20, bg="#FF3399")
        self.column_name3.insert(0, "CUSTOMER NAME")
        self.column_name3.grid(row=1, column=2)

        self.column_name4 = Entry(self.window, width=50, bg="#FF3399")
        self.column_name4.insert(0, "PRODUCT NAME")
        self.column_name4.grid(row=1, column=3)

        self.column_name5 = Entry(self.window, width=5, bg="#FF3399")
        self.column_name5.insert(0, "QTY")
        self.column_name5.grid(row=1, column=4)

        self.column_name6 = Entry(self.window, width=7, bg="#FF3399")
        self.column_name6.insert(0, "PRICE")
        self.column_name6.grid(row=1, column=5)

        self.column_name8 = Entry(self.window, width=9, bg="#FF3399")
        self.column_name8.insert(0, "AMOUNT")
        self.column_name8.grid(row=1, column=6)

        plus = 100

        self.prev_list = Button(self.window, text="< Prev", font=Sans_button, command=lambda: self.display('prev'))
        self.next_list = Button(self.window, text="Next >", font=Sans_button, command=lambda: self.display('next'))
        self.prev_list.place(x=208.5, y=250 +plus)
        self.next_list.place(x=258.5, y=250 +plus)

        self.search_box = Entry(self.window, width=20)
        self.search_box.place(x=332.375, y=250 +plus)

        self.search_button = Button(self.window, text="SEARCH", font=Sans_button, width=7,
                                    command=lambda: self.display('search'))
        self.search_button.place(x=550.375, y=250 +plus)

        self.clear_button = Button(self.window, text="CLEAR", font=Sans_button, width=7,
                                   command=lambda: self.display('clear'))
        self.clear_button.place(x=550.375, y=280 +plus)

        minus = 75

        Label(self.window, text="CSV Filename", bg="pink", font=verdana).place(x=163.375 - minus, y=310 +plus)
        self.csv_filename = Entry(self.window, width=59)
        self.csv_filename.place(x=163.375 - minus, y=330 +plus)

        self.import_button = Button(self.window, text="IMPORT", font=Sans_button, width=7,
                                    command=lambda: self.import_())
        self.import_button.place(x=630.375, y=330 +plus)

        self.id_default = IntVar(self.window)
        Label(self.window, text="ID", bg="pink", font=verdana).place(x=163.375 - 75, y=360 +plus)
        self.purchase_id = Spinbox(self.window, from_=0, to=1000, width=8, textvariable=self.id_default)
        self.purchase_id.place(x=163.375 - 45, y=360 +plus)

        self.month_cb = ttk.Combobox(self.window, width=11, textvariable=StringVar())
        month_list = []
        for i in calendar.month_name:
            if '' in month_list:
                month_list.remove('')
            month_list.append(i)
        self.month_cb['values'] = month_list
        self.month_cb.place(x=163.375 - minus, y=420 +plus)
        self.month_cb.current(0)

        self.year_default = IntVar(self.window)
        self.year_sp = Spinbox(self.window, width=5, from_=2000, to_=3000, textvariable=self.year_default)
        self.year_sp.place(x=254.375 - minus, y=420 +plus)
        self.year_default.set(self.year)

        self.date_button = Button(self.window, text="GO", font=Sans_button, width=3, command=self.set_date)
        self.date_button.place(x=308.375 - minus, y=420 +plus)

        self.display()

        self.window.resizable(False, False)
        self.window.configure(bg="pink")
        self.window.mainloop()

    #to display table in sales
    def display(self, command=''):
        get_data(table_name_=f'"{self.month} {self.year} sales"')

        if command == 'next':
            if not gv.search and len(gv.data) - 1 >= gv.maximum:
                next_()
            if gv.search and len(gv.search_data) - 1 >= gv.maximum:
                next_()
        elif command == 'prev' and gv.minimum > 0:
            prev_()
        elif command == 'search':
            reset()
            if self.search_box.get() != '':
                search(self.search_box.get(), f'sales')
                gv.search = True
        elif command == 'clear':
            self.search_box.delete(0, 'end')
            gv.search = False

        display_data = []
        if len(gv.data) != 0:
            if gv.search is True:
                if len(gv.search_data) != 0:
                    for i in range(gv.minimum, gv.maximum):
                        display_data.append(gv.search_data[i])
                        if i == len(gv.search_data) - 1:
                            for j in range(gv.maximum - len(display_data)):
                                display_data.append(('', '', '', '', '', '', ''))
                            break
            else:
                for i in range(gv.minimum, gv.maximum):
                    display_data.append(gv.data[i])
                    if i == len(gv.data) - 1:
                        for j in range(gv.maximum - len(display_data)):
                            display_data.append(('', '', '', '', '', '', ''))
                        break

        for i in range(2, 12):
            color = "light grey"
            if len(display_data) != 0 and display_data[i - 2][2].find('Total') != -1:
                color = "#FF99CC"

            (sales_id, date_sold, customer_name, product_name, qty, price, amount) = \
                display_data[i - 2] if len(display_data) != 0 else ('', '', '', '', '', '', '')

            if customer_name.find('Total') != -1:
                product_name = ''

            column_1 = Entry(self.window, width=4, bg=color)
            column_1.grid(row=i, column=0)
            column_1.insert(0, sales_id)

            column_2 = Entry(self.window, width=12, bg=color)
            column_2.grid(row=i, column=1)
            column_2.insert(0, date_sold)

            column_3 = Entry(self.window, width=20, bg=color)
            column_3.grid(row=i, column=2)
            column_3.insert(0, customer_name)

            column_4 = Entry(self.window, width=50, bg=color)
            column_4.grid(row=i, column=3)
            column_4.insert(0, product_name)

            column_5 = Entry(self.window, width=5, bg=color)
            column_5.grid(row=i, column=4)
            column_5.insert(0, qty)

            column_6 = Entry(self.window, width=7, bg=color)
            column_6.grid(row=i, column=5)
            column_6.insert(0, price)

            column_8 = Entry(self.window, width=9, bg=color)
            column_8.grid(row=i, column=6)
            column_8.insert(0, amount)

    #if user wants to check previous data, this def functions allows to view past months and years
    def set_date(self):
        get_error(input_=f'"{self.month_cb.get()} {self.year_sp.get()} sales"',
                  window_="Sales", command_="set_date")
        if gv.input_error is False:
            self.month = self.month_cb.get()
            self.year = self.year_sp.get()
            self.month_label.set(f"{self.month} Sales")
            print(self.month, self.year)
            reset()
            self.display()

    #to import csv file to be processed (where data will come from) and writes into the csvfile
    def import_(self):
        filename = self.csv_filename.get()
        get_error(input_=f'{filename}', window_="Sales", command_="import")
        if gv.input_error is False:
            (month, year) = str(filename).split(' - ')[0].split(' ')
            create_table(month, year, 'Sales')
            csv_handler.read_csv(filename)
            sell(month, year)
            csv_handler.write_csv(filename=filename)
            self.display()

#fourth winndow layout/buttons/functionality
class Inventory:
    def __init__(self):
        reset()
        self.window = Toplevel()
        self.window.geometry("448x600")
        Label(self.window, width=28, text="INVENTORY", font=times_new_roman, bg="pink").grid(row=0, columnspan=4)

        self.column_name1 = Entry(self.window, width=4, bg="light grey")
        self.column_name1.insert(0, "ID")
        self.column_name1.grid(row=1, column=0)

        self.column_name3 = Entry(self.window, width=9, bg="light grey")
        self.column_name3.insert(0, "STOCK")
        self.column_name3.grid(row=1, column=1)

        self.column_name2 = Entry(self.window, width=50, bg="light grey")
        self.column_name2.insert(0, "PRODUCT NAME")
        self.column_name2.grid(row=1, column=2)

        self.column_name3 = Entry(self.window, width=9, bg="light grey")
        self.column_name3.insert(0, "PRICE")
        self.column_name3.grid(row=1, column=3)

        plus = 100

        self.prev_list = Button(self.window, text="< Prev", font=Sans_button, command=lambda: self.display('prev'))
        self.next_list = Button(self.window, text="Next >", font=Sans_button, command=lambda: self.display('next'))
        self.prev_list.place(x=44, y=250 +plus)
        self.next_list.place(x=94, y=250 +plus)

        self.search_box = Entry(self.window, width=20)
        self.search_box.place(x=169, y=250 +plus)

        self.search_button = Button(self.window, text="SEARCH", font=Sans_button, width=7,
                                    command=lambda: self.display('search'))
        self.search_button.place(x=369, y=250 +plus)

        self.clear_button = Button(self.window, text="CLEAR", font=Sans_button, width=7,
                                   command=lambda: self.display('clear'))
        self.clear_button.place(x=369, y=280 +plus)

        self.display()

        self.window.resizable(False, False)
        self.window.configure(bg="pink")
        self.window.mainloop()

    #to display table for current inventory list stock
    def display(self, command=''):
        get_data(table_name_='inventory')
        if command == 'next':
            if not gv.search and len(gv.data) - 1 >= gv.maximum:
                next_()
            if gv.search and len(gv.search_data) - 1 >= gv.maximum:
                next_()
        elif command == 'prev' and gv.minimum > 0:
            prev_()
        elif command == 'search':
            reset()
            if self.search_box.get() != '':
                search(self.search_box.get(), 'inventory')
                gv.search = True
        elif command == 'clear':
            self.search_box.delete(0, 'end')
            gv.search = False

        display_data = []
        if len(gv.data) != 0:
            if gv.search is True:
                if len(gv.search_data) != 0:
                    for i in range(gv.minimum, gv.maximum):
                        display_data.append(gv.search_data[i])
                        if i == len(gv.search_data) - 1:
                            for j in range(gv.maximum - len(display_data)):
                                display_data.append(('', '', '', ''))
                            break
            else:
                for i in range(gv.minimum, gv.maximum):
                    display_data.append(gv.data[i])
                    if i == len(gv.data) - 1:
                        for j in range(gv.maximum - len(display_data)):
                            display_data.append(('', '', '', ''))
                        break

        for i in range(2, 12):
            color = "pink" if i % 2 == 0 else "light grey"

            (product_id, stock, product_name, price) = display_data[i - 2] if len(display_data) != 0 else ('', '', '', '')

            column_1 = Entry(self.window, width=4, bg=color)
            column_1.grid(row=i, column=0)
            column_1.insert(0, product_id)

            stock_color = "#E92A5C" if str(stock).find('-') != -1 else color

            column_2 = Entry(self.window, width=9, bg=stock_color)
            column_2.grid(row=i, column=1)
            column_2.insert(0, stock)

            column_3 = Entry(self.window, width=50, bg=color)
            column_3.grid(row=i, column=2)
            column_3.insert(0, product_name)

            column_4 = Entry(self.window, width=9, bg=color)
            column_4.grid(row=i, column=3)
            column_4.insert(0, price)
