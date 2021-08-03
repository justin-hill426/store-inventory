from models import Base, session, Product, engine
import csv
import datetime
import time


def menu():
    while True:
        print('''
                \nMAIN MENU
                \r'v' - View Details of Single Product
                \r'a' - Add new product to the database
                \r'b' - Make a backup of database
                \r'e' - Exit''')
        choice = input("What would you like to do? ")
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else:
            input('''
              \rPlease choose one of the options above.
              \rThe options are 'v', 'a', 'b', and 'e'.
              \rPress enter to try again. ''')


def add_csv():
    with open('inventory.csv') as file:
        data = csv.reader(file)
        for row in data:
            print(row)
            # product_quantity =
            # product_price
            # date_updated


def clean_quantity(quantity_str):
    pass


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
                          \n****** PRICE ERROR ******
                          \rThe price should be a number without a currency symbol
                          \rEx: 10.66
                          \rPress enter to try again.
                          \r*************************''')
        return
    else:
        return int(price_float * 100)


def clean_date(date_str):
    pass


if __name__ == '__main__':
    add_csv()
