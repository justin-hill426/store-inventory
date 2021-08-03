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
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name, product_quantity=product_quantity,
                                      product_price=product_price, date_updated=date_updated)
                session.add(new_product)
        session.commit()


def clean_quantity(quantity_str):
    try:
        product_quantity = int(quantity_str)
    except ValueError:
        input('''
                                  \n****** Value ERROR ******
                                  \rThe product quantity should be a number.
                                  \rPress enter to try again.
                                  \r*************************''')
        return
    else:
        return product_quantity


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
    date_split = date_str.split('/')
    return datetime.datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))



if __name__ == '__main__':
    # add_csv()
