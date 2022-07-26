import calendar
import csv
from tkinter import messagebox
from database import *
from datetime import date


def next_():
    gv.minimum += 10
    gv.maximum += 10


def prev_():
    gv.minimum -= 10
    gv.maximum -= 10


def reset():
    gv.minimum = 0
    gv.maximum = 10
    gv.search = False


def search(filter_, table):
    gv.search_data.clear()
    for data in gv.data: # gv.data = list
        try:
            if int(filter_) in data:
                gv.search_data.append(data)
        except ValueError:
            if table == 'product':
                if data[1].find(filter_) != -1:
                    gv.search_data.append(data)
            elif table == 'purchase':
                if data[3].find(filter_) != -1:
                    gv.search_data.append(data)
            elif table == 'sales':
                if data[2].find(filter_) != -1 or data[3].find(filter_) != -1 or data[6] == filter_:
                    gv.search_data.append(data)
            elif table == 'inventory':
                if data[2].find(filter_) != -1:
                    gv.search_data.append(data)
    for i in range(len(gv.search_data)):
        print(gv.search_data[i])


def get_error(input_, window_, command_):
    gv.input_error = False
    gv.error_msg = ''

    if window_ == 'ListOfProduct':
        if command_ == 'add':
            for i in range(2):
                if input_[i] == '' or input_[i] == 0:
                    gv.input_error = True
                    if i == 0:
                        gv.error_msg += 'Please input product name\n'
                    elif i == 1:
                        gv.error_msg += 'Please input valid price\n'
                elif input_[0] != '':
                    product_name = get_data(table_name_='product', column_name_='product_name',
                                            filter_='product_name', filter_value_=f'{input_[0]}')
                    if product_name is not None:
                        gv.input_error = True
                        gv.error_msg = 'This Product Already Exist'
                        break
        elif command_ == 'edit' or command_ == 'delete':
            if input_ is None:
                gv.input_error = True
                if command_ == 'edit':
                    gv.error_msg = 'Cannot find the product name in database'
                else:
                    gv.error_msg = 'This product name doesnt exist'
            elif input_[0] == '':
                gv.input_error = True
                if command_ == 'edit':
                    gv.error_msg = 'Please input product name to edit'
                else:
                    gv.error_msg = 'Please input product name to delete'
    elif window_ == 'PurchaseHistory':
        if command_ == 'add':
            if input_ == 0:
                gv.input_error = True
                gv.error_msg += 'Please input valid QTY\n'

        elif command_ == 'edit' or command_ == 'delete':
            if input_ == 0 or input_ is None:
                gv.input_error = True
                if input_ == 0:
                    gv.error_msg += 'Please input valid ID\n'
                elif input_ is None:
                    gv.error_msg += 'ID not found\n'
        elif command_ == 'set_date':
            try:
                get_data(table_name_=input_)
            except sqlite3.OperationalError:
                gv.input_error = True
                gv.error_msg += 'No Data Found\n'
    elif window_ == 'Sales':
        if command_ == 'set_date':
            try:
                get_data(table_name_=input_)
            except sqlite3.OperationalError:
                gv.input_error = True
                gv.error_msg += 'No Data Found\n'
        elif command_ == 'import':
            try:
                with open(f'{input_}', 'r', encoding='utf-8') as file:
                    csv.reader(file)
            except FileNotFoundError:
                gv.input_error = True
                gv.error_msg += 'File Not Found\n'

    if gv.input_error is True:
        messagebox.showwarning(message=gv.error_msg)


def get_date():
    year, month, day = str(date.today()).split('-')
    return calendar.month_name[int(month)], int(day), int(year)
