import json
import random

# Define file paths for data persistence
menu_file = "menu.json"
orders_file = "orders.json"

# Initialize data dictionaries
menu = {}
orders = []

# Load menu and orders data from JSON files
def load_data():
    global menu, orders
    try:
        with open(menu_file, "r") as menu_data:
            loaded_menu = json.load(menu_data)
            # Convert keys from strings to integers
            menu = {int(key): value for key, value in loaded_menu.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        menu = {}

    try:
        with open(orders_file, "r") as orders_data:
            orders = json.load(orders_data)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []

# Save menu and orders data to JSON files
def save_data():
    with open(menu_file, "w") as menu_data, open(orders_file, "w") as orders_data:
        json.dump(menu, menu_data, indent=4)
        json.dump(orders, orders_data, indent=4)

# Initialize data
load_data()

# Function to add a new dish to the menu
def add_dish():
    dish_id = int(input("Enter dish ID: "))
    if dish_id in menu:
        print("Dish with the same ID already exists.")
        return

    name = input("Enter dish name: ")
    price = float(input("Enter dish price: "))
    availability = input("Is the dish available (yes/no): ").lower() == "yes"

    menu[dish_id] = {"name": name, "price": price, "availability": availability}
    save_data()
    print(f"Dish with ID {dish_id} has been added to the menu.")

# Function to remove a dish from the menu
def remove_dish():
    dish_id = int(input("Enter dish ID to remove: "))
    if dish_id in menu:
        del menu[dish_id]
        save_data()
        print(f"Dish with ID {dish_id} has been removed from the menu.")
    else:
        print(f"Dish with ID {dish_id} not found in the menu.")

# Function to update dish availability
def update_availability():
    dish_id = int(input("Enter dish ID to update availability: "))
    if dish_id in menu:
        availability = input("Is the dish available (yes/no): ").lower() == "yes"
        menu[dish_id]["availability"] = availability
        save_data()
        print(f"Availability of dish with ID {dish_id} has been updated.")
    else:
        print(f"Dish with ID {dish_id} not found in the menu.")

# Function to take a new customer order
def take_order():
    customer_name = input("Enter customer's name: ")
    order_items = []

    while True:
        dish_id = int(input("Enter dish ID (0 to finish): "))
        if dish_id == 0:
            break
        if dish_id in menu and menu[dish_id]["availability"]:
            order_items.append(dish_id)
        elif dish_id not in menu:
            print(f"Dish with ID {dish_id} not found in the menu.")
        elif not menu[dish_id]["availability"]:
            print(f"Dish with ID {dish_id} is not available.")

    if order_items:
        order_id = random.randint(1000, 9999)
        order = {"order_id": order_id, "customer_name": customer_name, "items": order_items, "status": "received"}
        orders.append(order)
        save_data()
        print(f"Order with ID {order_id} has been received.")


# Function to update order status
def update_order_status():
    order_id = int(input("Enter order ID to update status: "))
    for order in orders:
        if order["order_id"] == order_id:
            print("Current Status:", order["status"])
            new_status = input("Enter new status (preparing/ready for pickup/delivered): ")
            order["status"] = new_status
            save_data()
            print(f"Status of order with ID {order_id} has been updated.")
            break
    else:
        print(f"Order with ID {order_id} not found.")
# Function to calculate the total price of an order
def calculate_order_price(order):
    total_price = 0
    for item_id in order["items"]:
        dish = menu.get(item_id, {})
        total_price += dish.get("price", 0)
    return total_price

# Function to review orders with status filtering
def review_orders():
    print("Review Options:")
    print("1. Show all orders")
    print("2. Show 'preparing' orders")
    print("3. Show 'ready for pickup' orders")
    print("4. Show 'delivered' orders")
    choice = input("Enter your choice: ")

    if choice == '1':
        selected_orders = orders
    elif choice == '2':
        selected_orders = [order for order in orders if order["status"] == "preparing"]
    elif choice == '3':
        selected_orders = [order for order in orders if order["status"] == "ready for pickup"]
    elif choice == '4':
        selected_orders = [order for order in orders if order["status"] == "delivered"]
    else:
        print("Invalid choice. Showing all orders.")
        selected_orders = orders

    print("Selected Orders:")
    for order in selected_orders:
        print(f"Order ID: {order['order_id']}, Customer: {order['customer_name']}, Status: {order['status']}")
        print("Items:")
        for item_id in order["items"]:
            dish = menu.get(item_id, {})
            print(f"  - Dish ID: {item_id}, Dish Name: {dish.get('name', 'N/A')}, Price: {dish.get('price', 'N/A')}")
        total_price = calculate_order_price(order)
        print(f"Total Price: ${total_price:.2f}")

# Main menu and user interaction
while True:
    print("\nOptions:")
    print("1. Add a new dish to the menu")
    print("2. Remove a dish from the menu")
    print("3. Update dish availability")
    print("4. Take a new order")
    print("5. Update order status")
    print("6. Review all orders")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_dish()
    elif choice == '2':
        remove_dish()
    elif choice == '3':
        update_availability()
    elif choice == '4':
        take_order()
    elif choice == '5':
        update_order_status()
    elif choice == '6':
        review_orders()
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please try again.")
