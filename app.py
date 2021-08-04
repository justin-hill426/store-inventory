from models import Base, session, Product, engine
import csv
import datetime
import time


def menu():
    """Prints out main menu of options"""
    while True:
        print('''\nMAIN MENU
                \r'v' - View a single product's inventory
                \r'a' - Add a new product to the database
                \r'b' - Make a backup of the entire inventory
                \r'q' - Quit''')
        choice = input("What would you like to do? ")
        if choice in ['v', 'a', 'b', 'q']:
            return choice
        else:
            input('''
              \rPlease choose one of the options above.
              \rThe options are 'v', 'a', 'b', and 'e'.
              \rPress enter to try again. ''')


def add_csv():
    """Adds the data from the csv file to the database"""
    with open('inventory.csv') as file:
        data = csv.reader(file)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db is None:
                product_name = row[0]
                product_price = clean_price(row[1], added_by_user=False)
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name, product_quantity=product_quantity,
                                      product_price=product_price, date_updated=date_updated)
                session.add(new_product)
        session.commit()


def make_backup():
    """Makes a backup CSV file from current database data"""
    with open('backup.csv', 'w', newline='') as csvfile:
        copywriter = csv.writer(csvfile, delimiter=',')
        fields = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        copywriter.writerow(fields)
        for curr_product in session.query(Product):
            copywriter.writerow([curr_product.product_name, price_output(curr_product.product_price),
                                 curr_product.product_quantity, date_output(curr_product.date_updated)])


def clean_quantity(quantity_str):
    """Cleans the quantity to make sure it is properly formatted"""
    try:
        product_quantity = int(quantity_str)
    except ValueError:
        input('''\n****** Value ERROR ******
                  \rThe product quantity should be a number.
                  \rPress enter to try again.
                  \r*************************''')
        return
    else:
        return product_quantity


def clean_price(price_str, added_by_user):
    """Cleans the price to make sure it is properly formatted"""
    if added_by_user:
        try:
            price_float = float(price_str)
        except ValueError:
            input('''\n****** PRICE ERROR ******
                      \rThe price should be entered as a number without a currency symbol
                      \rEx: 5.99
                      \rPress enter to try again.
                      \r*************************''')
            return
        else:
            return int(price_float * 100)
    else:
        try:
            price_str = price_str[1:]
            price_float = float(price_str)
        except ValueError:
            input('''\n****** PRICE ERROR ******
                      \rThe price should be entered as a number with a currency symbol
                      \rEx: $10.66
                      \rPress enter to try again.
                      \r*************************''')
            return
        else:
            return int(price_float * 100)


def clean_date(date_str):
    """Cleans the date to make sure it is properly formatted"""
    date_split = date_str.split('/')
    year = int(date_split[2])
    month = int(date_split[0])
    day = int(date_split[1])
    return datetime.datetime(year, month, day)


def price_output(price):
    return "$" + "{:.2f}".format(price / 100)


def date_output(date):
    """Returns the datetime object parsed to a properly formatted string"""
    return date.strftime("%m/%d/%Y")


def clean_id(id_string, id_options):
    """Cleans the ID to make sure it is valid"""
    try:
        book_id = int(id_string)
    except ValueError:
        input('''\n****** ID ERROR ******
                 \rThe id should be a number.
                 \rPress enter to try again.
                 \r*************************''')
        return
    else:
        if book_id in id_options:
            return book_id
        else:
            input(f'''\n****** ID ERROR ******
                      \r ID options: {id_options}
                      \rThe id should be a number in the range of options.
                      \rPress enter to try again.
                      \r*************************''')
            return


def view_product():
    """View a current product in the database"""
    id_options = []
    for curr_product in session.query(Product):
        id_options.append(curr_product.product_id)
    id_error = True
    while id_error:
        id_choice = input(f'''\nId Options: {id_options}
                        \rProduct id: ''')
        id_choice = clean_id(id_choice, id_options)
        if type(id_choice) == int:
            id_error = False
    product_choice = session.query(Product).filter(Product.product_id == id_choice).first()
    print(f'''\n Product Name: {product_choice.product_name}
                    \r Product Quantity: {product_choice.product_quantity}
                    \r Product Price: {price_output(product_choice.product_price)}
                    \r Product's Last Edit Date: {date_output(product_choice.date_updated)}''')
    time.sleep(1.5)


def create_new_product():
    """Create a new product in the product catalog"""
    product_name = input("Product Name: ")
    quantity_error = True
    while quantity_error:
        product_quantity = input("Product Quantity: ")
        product_quantity = clean_quantity(product_quantity)
        if type(product_quantity) == int:
            quantity_error = False
    price_error = True
    while price_error:
        product_price = input("Product Price: ")
        product_price = clean_price(product_price, added_by_user=True)
        if type(product_price) == int:
            price_error = False
    new_product = Product(product_name=product_name, product_quantity=product_quantity,
                          product_price=product_price, date_updated=datetime.datetime.now())
    old_product_in_db = session.query(Product).filter(Product.product_name == new_product.product_name).one_or_none()
    if old_product_in_db:
        old_product_in_db.product_name = new_product.product_name
        old_product_in_db.product_quantity = new_product.product_quantity
        old_product_in_db.product_price = new_product.product_price
        old_product_in_db.date_updated = new_product.date_updated
        print(f"Product {product_name} was updated in the Product Catalog")
    else:
        session.add(new_product)
        print(f"Product {product_name} was added to the Product Catalog")
    session.commit()
    time.sleep(1.5)


def app():
    """Maintains User Interaction"""
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            view_product()
        elif choice == 'b':
            make_backup()
        elif choice == 'a':
            create_new_product()
        else:
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
