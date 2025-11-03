import mysql.connector
from getpass import getpass
import os
import time

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pypro"
)
cursor = db.cursor()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")


def register():
    clear()
    print("=== Register ===")
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print("\nRegistration successful!")
    except mysql.connector.IntegrityError:
        print("\nUsername already exists!")
    pause()

def login():
    clear()
    print("=== Login ===")
    username = input("Username: ")
    password = getpass("Password: ")

    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"\nWelcome, {username}!")
        time.sleep(1)
        return user[0]
    else:
        print("\nInvalid credentials.")
        pause()
        return None


def home(user_id):
    while True:
        clear()
        print("=== HOME - Available Products ===\n")
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        for p in products:
            print(f"{p[0]}. {p[1]} - ${p[2]}")
        print("0. Return to Main Menu")

        try:
            choice = int(input("\nEnter product ID to add to cart (0 to exit): "))
            if choice == 0:
                break

            cursor.execute("SELECT * FROM products WHERE id=%s", (choice,))
            product = cursor.fetchone()
            if not product:
                print("\nInvalid product ID.")
                pause()
                continue

            qty = int(input(f"Enter quantity for {product[1]}: "))
            if qty <= 0:
                print("\nQuantity must be at least 1.")
                pause()
                continue

            cursor.execute("SELECT * FROM cart WHERE user_id=%s AND product_id=%s", (user_id, choice))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("UPDATE cart SET quantity = quantity + %s WHERE user_id=%s AND product_id=%s", (qty, user_id, choice))
            else:
                cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, choice, qty))
            db.commit()

            print(f"\nAdded {qty} x {product[1]} to cart.")
            pause()

        except ValueError:
            print("\nInvalid input! Please enter a number.")
            pause()


def view_cart(user_id):
    clear()
    cursor.execute("""
        SELECT products.name, products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()

    if not items:
        print("Your cart is empty.")
        pause()
        return

    print("=== Your Cart ===\n")
    total = 0
    for name, price, qty in items:
        subtotal = float(price) * qty
        total += subtotal
        print(f"{name}  x{qty}  =  ${subtotal:.2f}")
    print(f"\nTotal: ${total:.2f}")
    pause()


def checkout(user_id):
    clear()
    cursor.execute("""
        SELECT products.name, products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()

    if not items:
        print("Your cart is empty. Add items first.")
        pause()
        return

    print("=== Checkout ===\n")
    total = 0
    for name, price, qty in items:
        total += float(price) * qty
        print(f"{name} x{qty}")
    print(f"\nTotal amount: ${total:.2f}")

    confirm = input("\nConfirm checkout? (y/n): ").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
        db.commit()
        print("\nCheckout successful! Your order has been placed.")
    else:
        print("\nCheckout cancelled.")
    pause()


def main():
    clear()
    print("=== TERMINAL E-COMMERCE SYSTEM ===")
    user_id = None

    while True:
        clear()
        if not user_id:
            print("""
=== MAIN MENU ===
1. Register
2. Login
3. Exit
""")
            choice = input("Choose: ")

            if choice == '1':
                register()
            elif choice == '2':
                user_id = login()
            elif choice == '3':
                clear()
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
                pause()
        else:
            clear()
            print("""
=== USER MENU ===
1. Home (View + Add to Cart)
2. View Cart
3. Checkout
4. Logout
""")
            choice = input("Choose: ")

            if choice == '1':
                home(user_id)
            elif choice == '2':
                view_cart(user_id)
            elif choice == '3':
                checkout(user_id)
            elif choice == '4':
                user_id = None
                print("\nLogged out successfully.")
                time.sleep(1)
            else:
                print("Invalid choice.")
                pause()

main()
