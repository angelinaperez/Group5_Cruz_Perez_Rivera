import csv
import re

from database import *


def read_csv(filename):
    gv.data.clear()
    tempList = list()
    with open(f'{filename}', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['IF PROCESSED'] != 'PROCESSED':
                total_qty = 0
                for order in str(row['orders']).split('\n'):
                    (qty, product_name) = int(re.findall("[0-9]+", order)[0]), re.split("[0-9]+ ", order)[1]

                    total_qty += qty

                    if str(product_name).lower() == "Solo Bouquet (Sunflowers, Mini)".lower():
                        product_name = 'Sunflowers Mini Bouquet'
                        price = 550
                    elif str(product_name).lower() == "Solo Bouquet (Sunflowers, Large)".lower():
                        product_name = 'Sunflowers Large Bouquet'
                        price = 950
                    elif str(product_name).lower() == "Solo Bouquet (Roses, Mini)".lower():
                        product_name = 'Roses Mini Bouquet'
                        price = 500
                    elif str(product_name).lower() == "Solo Bouquet (Roses, Large)".lower():
                        product_name = 'Roses Large Bouquet'
                        price = 800
                    elif str(product_name).lower() == "Solo Bouquet (Daisies, Mini)".lower():
                        product_name = 'Daisies Mini Bouquet'
                        price = 500
                    elif str(product_name).lower() == "Solo Bouquet (Daisies, Large)".lower():
                        product_name = 'Daisies Large Bouquet'
                        price = 800
                    elif str(product_name).lower() == "Solo Bouquet (Lavenders, Mini)".lower():
                        product_name = 'Lavender Mini Bouquet'
                        price = 500
                    elif str(product_name).lower() == "Solo Bouquet (Lavenders, Large)".lower():
                        product_name = 'Lavender Large Bouquet'
                        price = 800
                    elif str(product_name).lower() == "Solo Bouquet (Tulips, Mini)".lower():
                        product_name = 'Tulips Mini Bouquet'
                        price = 530
                    elif str(product_name).lower() == "Solo Bouquet (Tulips, Large)".lower():
                        product_name = 'Tulips Large Bouquet'
                        price = 750
                    elif str(product_name).lower() == "Extra Layer of Wrapping".lower() or str(
                            product_name).lower() == "Extra Wrapping".lower():
                        product_name = 'Extra Layer of Wrapping'
                        price = 50
                    elif str(product_name).lower() == "Extra Leaves".lower():
                        product_name = 'Extra Leaves'
                        price = 80
                    elif str(product_name).lower() == "Dedication Letter".lower():
                        product_name = 'Dedication Letter'
                        price = 30

                    (stock,) = get_data(table_name_='inventory', column_name_='stock',
                                        filter_='product_name', filter_value_=product_name)
                    stock -= qty
                    stock_value = f"stock = {stock}"

                    update(table_name_='inventory', set_value=stock_value,
                           filter_='product_name', filter_value_=product_name)

                    tempList.append((row['date'], row['name'], product_name, qty, price, row['total']))
                tempList.append((row['date'], "Total", '', total_qty, '', row['total']))

                gv.data = tempList


def write_csv(filename):
    tempList = list()
    with open(f'{filename}', 'r', encoding='utf-8') as read_file:
        reader = csv.reader(read_file)
        for row in reader:
            tempList.append(row)

    with open(f'{filename}', 'w', newline='', encoding='utf-8') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(tempList[0])

        for i in range(1, len(tempList)):
            if tempList[i][23] != "PROCESSED":
                tempList[i][23] = "PROCESSED"
            writer.writerow(tempList[i])
