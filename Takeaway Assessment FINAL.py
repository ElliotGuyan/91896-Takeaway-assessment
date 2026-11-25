'''
Takeaway programme assessment.

The purpose of this programme is to increase the productivity of online orders, while introducing the ease of not needing to manually answer.
This should increase the sales of the company, as they can focus more on cooking, rather then having to take down orders inbetween cooking other meals.

This programme should collect any relevant information to ordering the food from the user. e.g. Name and phone number. (Payment in person) 
The user should be able to order a maximum quantity of 10 of each item (may vary on the item) as well as order multiple items on the menu (Up to all of the items)
The user must be able to confirm and/or edit their order.
The programme must display the users order, including the cost and item list.

- Elliot Guyan
- 23/11/2026

'''

''' 
Ideas/creation path:

- Welcoming the user
- User information collection and storage as well as a relation to the person making an order (order number)
- Programme interface
- Functions 
- 

To do:

- Testing
- Trialing


'''
#------------------------------------------------------------------------------
# Constants and Menu data
#------------------------------------------------------------------------------
# Constants are written in uppercase to represent fixed rules.
# This allows them to be changed in one place, instead of needing to find and
# change every section of code which uses the same constant.


BUSINESS_NAME = "Maraetai Kiwi Fish & Chips"
MAX_QUANTITY_PER_ITEM = 10
MIN_QUANTITY_PER_ITEM = 1
MIN_PHONE_NUMBER_LENGTH = 7 
MAX_PHONE_NUMBER_LENGTH = 15 
GST_RATE = 0.15 

# 2D list storing menu items. [Item_code, item_name, category, unit_price]
#The first character of the code is the first letter corresponding to its menu
#category. For example, Tomato sauce is E01, because it is an extra.
#While it may be a sauce, there is already a "Sides" category, and having another s 
#conflict would be a problem.

MENU_ITEMS = [
    ["F01", "Battered Hoki Fillet", "Fish", 7.50],
    ["F02", "Battered Snapper Fillet", "Fish", 11.50],
    ["F03", "Battered Tarakihi", "Fish", 10.50],
    ["C01", "Scoop of Potato Chips", "Chips", 4.50],
    ["C02", "Kumara Chips", "Chips", 6.50],
    ["S01", "Battered Hot Dog", "Side", 4],
    ["S02", "Squid Rings", "Side", 7],
    ["E01", "Tomato Sauce", "Extra", 1.50],
    ["E02", "Extra Lemon", "Extra", 1.50],
    ["D01", "L&P Can", "Drink", 3],
    ["D02", "Coca Cola Can", "Drink", 3],
]

#------------------------------------------------------------------------------
# Formatting and input validation functions.
#------------------------------------------------------------------------------

def format_currency(amount): 
    '''Formats numbers into currency with 2dp.'''
    return f"${amount:.2f}"


def verify_customer_name(prompt): 
    '''Prompts the user until a valid name is given.'''
    while True: 
        raw_name = input(prompt).strip() # Strips the raw name of spaces before and after
        if raw_name and any(char.isalpha() for char in raw_name): # Checks that there is at least one alphabetical letter in the name
            valid_name = " ".join(raw_name.split()).title() # Connects the name back together.
            return valid_name
        print("\nInvalid name. Please enter a name containing letters, (The name cannot be blank)")



def verify_customer_customer_phone_number(prompt): 
    ''' Prompts the user until a valid number is given'''

    while True:
        raw_phone = input(prompt).strip() #Strips the raw number. removing any spaces 
        digits_only = "".join(char for char in raw_phone if char.isdigit()) # Checks if the input is digits only

        if (
            raw_phone
            and all(char.isdigit() or char in " -+()" for char in raw_phone) # Allows signs, -+() and spaces.
            and MIN_PHONE_NUMBER_LENGTH <= len(digits_only) <= MAX_PHONE_NUMBER_LENGTH # Checks that the phone number is within the valid length (7-15)
        ):
            return " ".join(raw_phone.split()) # Connects the phone number back together
        
        print( 
            f"Invalid phone number. Please enter {MIN_PHONE_NUMBER_LENGTH} - {MAX_PHONE_NUMBER_LENGTH}" # Message to tell the user to correct an invalid input
            " digits (Spaces and hypens are allowed)"
        )


def get_valid_integer(prompt, min_value, max_value): 
    '''Returns until the user gives a valid integer'''
    while True: 
        raw_input = input(prompt).strip() #Strips the inputted number of whitespace at the beginning and the end
        try:
            number = int(raw_input) # If the number is valid, then it equals the number and continues on with the code.
        except ValueError: # Rejects decimal numbers
            print(f"Invalid input. Please enter a whole number ({min_value} - {max_value})") #Prints a message to tell the user to write a valid number
            continue # If the number which has been input is invalid, it will redo the question until it gets a valid integer.

        if min_value <= number <= max_value: #Checks if the number given is between the boundaries. 
            return number # Confirms number is within the range and continues on with the code
        
        print(f"Out of range. Please enter a number between {min_value} and {max_value}") #Informs the user they have entered an invalid number (outside of the range) and asks for a new number.

def get_yes_or_no(prompt): 
    '''Function to get answers from yes or no questions'''
    while True: 
        choice = input(prompt).strip().upper() #This segment makes the input case-insensitive. As it forces it to be uppercase
        if choice in ("Y", "YES", "YEAH", "YEA"):
            return True #Answers the question with True
        if choice in ("N", "NO", "NAH", "NAY"):
            return False # Answers the question with False
        print("Invalid response. Please enter Y or N.(Yes, Yeah, Yea, No, Nah, Nay)") #The inputted answer is invalid due to a space inbetween the characters, [" ye s "] or the input is not in the answers


def build_order_label(wants_salt_and_vinegar): 
    '''Function for whether the user wants salt and vinegar '''

    if wants_salt_and_vinegar: #This function is small, and seperated between the request and the actual function, therefore it is really short.
        return "Pickup (With Salt & Vinegar)"
    return "Pickup (Plain/No Salt)"



#------------------------------------------------------------------------------
# Menu display, search & order cost functions
#------------------------------------------------------------------------------

def display_menu(menu): 
    '''Prints the menu in neatly, evenly aligned columns along with order limits'''

    line_width = 58 # Basis for how wide the line surrounding the menu will be
    print("\n" + "=" * line_width) # Multiplies the line width number (58) by the character which will be the border (=), and drops it down one line.
    print(f"{BUSINESS_NAME.upper()} - MENU".center(line_width)) #Writes the business name, all capitals and centers it
    print("=" * line_width) 
    print(f"{'Code':<6} {'Item':<28} {'Category':<10} {'Price':>10}") # The information about the food and the spacing it has.
    print("-" * line_width)

    for item_code, item_name, category, price in menu: 
        print(f"{item_code:<6} {item_name:<28} {category:<10} {format_currency(price):>10}")

    print("-" * line_width)
    print(f"Note: A maximum of {MAX_QUANTITY_PER_ITEM} of each item per order. All prices include GST")


def find_menu_item(menu, code_input): #Searches the 2D menu list for a match item code (case-insensitive) Returns the matching row [code, name, category, price] or none

    target_code = code_input.strip().upper()
    for item in menu:
        if item[0] == target_code:
            return item
    return None 
    

def calculate_order_totals(order_items): 
    '''Calculates and returns the total price of the order'''

    total_count = 0         #Starting total amount of items
    total_cost = 0.0        #Starting total price 

    for item_data in order_items.values():
        qty = item_data["quantity"] # qty is used inplace of quantity. As less confusing since quantity follows right after in the [] brackets
        total_count += qty
        total_cost += item_data["price"] * qty 

    included_gst = total_cost - (total_cost / (1 + GST_RATE))
    return total_count, total_cost, included_gst

def display_order_summary(customer_details, order_items, is_final=False): 
    '''Displays an itemised summary of customer details, items, GST and total cost'''

    line_width = 60 
    header_title = "TAX RECEIPT & ORDER SUMMARY" if is_final else "CURRENT ORDER SUMMARY"

    print("\n" + "=" * line_width)
    print(header_title.center(line_width)) #Centres the header
    print("=" * line_width)
    print("Please check your details are accurate.".center(line_width))
    print(f"Customer : {customer_details['name']}") #All customer information
    print(f"Phone    : {customer_details['phone']}")
    print(f"Order    : {customer_details['order_type']}")
    print("-" * line_width)

    if not order_items: 
        '''Checks if there are no items in the order, and rejects the user going to finalisation/checkout'''
        print("Your order is currently empty.") # Message for the user that they have nothing in their order
        print("-" * line_width)      
        return
    
    print(f"{'Code':<6} {'Item':<25} {'Qty':>4} {'Unit':>10} {'Subtotal':>11}") #Sizing of display
    print("-" * line_width)

    for code, details in order_items.items():
        subtotal = details["price"] * details["quantity"] 
        print(
            f"{code:<6} {details['name']:<25} {details['quantity']:>4} "
            f"{format_currency(details['price']):>10} {format_currency(subtotal):>11}"############################
        )

    total_count, total_cost, included_gst = calculate_order_totals(order_items) # Calling involved variables. 
    print("-" * line_width)
    print(f"{'Total Items:':<47} {total_count:>11}")
    print(f"{'Includes GST (15%):':<47} {format_currency(included_gst):>11} ")
    print(f"{'TOTAL TO PAY:':<47} {format_currency(total_cost):>11}")
    print("-" * line_width)


#------------------------------------------------------------------------------
# Customer details & order workflow functions.
#------------------------------------------------------------------------------

def collect_customer_details():
    '''Collection of customer details in a dictionary in the correct storage system [Name = str] [Phone = str] [order_type = str]'''

    print("=" * 58)
    print(f"Welcome to {BUSINESS_NAME}!".center(58))
    print("=" * 58)


    customer_name = verify_customer_name("\nPlease enter your name for the order: ")
    phone_number = verify_customer_customer_phone_number("\nPlease enter your contact phone number: ")
    wants_salt_and_vinegar = get_yes_or_no(
        "\nWould you like salt and vinegar on your order? (Y/N): "
    )

    return {
        "name": customer_name,
        "phone": phone_number,
        "order_type": build_order_label(wants_salt_and_vinegar)
    }

def edit_customer_details(customer_details):
    '''Allows the user to update their name, phone number, salt and vinegar preference, or all details at once.'''

    while True:
        print("\n" + "-" * 50)
        print("EDIT CUSTOMER DETAILS".center(50))
        print("-"* 50)
        print(f" Current Name  : {customer_details['name']}") #Current customer information print, allows the customer to see if they made a mistake anywhere.
        print(f" Current Phone : {customer_details['phone']}")
        print(f" Current Order : {customer_details['order_type']}")
        print("-"* 50)
        print("  [1] Change customer name") #Selection for what you want to change, or to go back to ordering.
        print("  [2] Change phone number")
        print("  [3] Change salt and vinegar preference")
        print("  [4] Update all customer details")
        print("  [B] Back to order review")
        choice = input("Select an option (1-4 or B): ").strip().upper() 
    
    #Updates information based on the customers need to change, changes the customer information in the dictionary and repeats it back to user.
        if choice =="B":
            return
        
        if choice == "1":
            customer_details["name"] = verify_customer_name("Enter a new customer name: ") 
            print(f"Customer name updated to '{customer_details['name']}'.")

        elif choice == "2":
            customer_details["phone"] = verify_customer_customer_phone_number("Enter a new contact phone number: ")
            print(f"Customer phone number updated to '{customer_details['phone']}'.")

        elif choice == "3":

            wants_salt_and_vinegar = get_yes_or_no(
                "Would you like salt and vinegar on your order? (Y/N): "
            )

            customer_details["order_type"] = build_order_label(wants_salt_and_vinegar)
            print(f"Order preference updated to '{customer_details['order_type']}'.")

        elif choice == "4":
            customer_details["name"] = verify_customer_name("Enter a new customer name: ")
            customer_details["phone"] = verify_customer_customer_phone_number("Enter a new contact phone number: ")
            wants_salt_and_vinegar = get_yes_or_no(
                "Would you like salt and vinegar on your order? (Y/N): "
            )
        else:
            print("Please enter a valid option: 1, 2, 3, 4, or B.")


def add_items_to_order(menu, order_items):
    '''Adds items to the customers order. Selection of multiple items and valid quantities.'''

    while True: 
        display_menu(menu)
        code_input = input("Enter item code to add (or 'DONE' to review order): ").strip()

        if code_input.upper() == "DONE": #Checks if the user has finished their order
            if not order_items: #Checks if there is any item inside of the users order and rejects if the order is empty
                print("Your order is empty. Please add at least one item before finalising your order.")
                continue
            break

        matched_item = find_menu_item(menu, code_input)
        if matched_item is None: #Checks if there is an item responding to the code input by the user
            print(f"'{code_input}' is not a valid item code. Please check the menu and try again.")
            continue

        item_code, item_name, category, unit_price = matched_item #Creates new variable to keep track of the items which the user has on their order
        existing_qty = order_items[item_code]["quantity"] if item_code in order_items else 0 #Makes it so that there are no items in the order at the start, and all items must be added
        remaining_limit = MAX_QUANTITY_PER_ITEM - existing_qty #Limit for how many items you can order

        if remaining_limit <= 0:  #Rejects over-ordering causing problems in the kitchen
            print(
                f"Limit reached: you already have {MAX_QUANTITY_PER_ITEM} x {item_name}" 
                "in your order."
            )
            continue

        qty_to_add = get_valid_integer( #Checking the valid input from the user, seeing if it is a valid integer or a decimal
            f"How many '{item_name}' would you like? ({MIN_QUANTITY_PER_ITEM} - {remaining_limit}): ",
            MIN_QUANTITY_PER_ITEM,
            remaining_limit,
        )

        if item_code in order_items: #Adding the requested number of items into the order
            order_items[item_code]["quantity"] += qty_to_add
        else:
            order_items[item_code] = {
                "name": item_name,
                "price": unit_price,
                "quantity": qty_to_add,
            }

        updated_qty = order_items[item_code]["quantity"] #The number of items in the order 
        print(f"Added {qty_to_add} x {item_name} (total in order: {updated_qty}).")


def edit_order_items(customer_details, order_items):
    '''Allows the customer to update item quantities or remove items from the order'''

    while True:
        if not order_items: 
            print("All items have been removed from your order")
            return
        
        display_order_summary(customer_details, order_items, is_final=False) #Displays the order summary, along with the choices for the user to edit their order
        print("Edit Order Options:")
        print(" [C] Change quantity of an item")
        print(" [R] Remove an item completely")
        print(" [B] Back to order review")
        choice = input("Select an option (C/R/B): ").strip().upper() #Option controls for editing the order options 

        if choice == "B":
            return
        
        if choice == "C": 
            code = input("Please enter the item code whose quantity you want to change: ").strip().upper()
            if code not in order_items: #Checking if the input is in the customers order.
                print(f"'{code}' is not currently in your order")
                continue

            item_name = order_items[code]["name"] #Updating quantity
            new_qty = get_valid_integer(
                f"Enter new quantity for {item_name} ({MIN_QUANTITY_PER_ITEM} - {MAX_QUANTITY_PER_ITEM}): ",
                MIN_QUANTITY_PER_ITEM,
                MAX_QUANTITY_PER_ITEM,
            )
            order_items[code]["quantity"] = new_qty
            print(f"Updated {item_name} quantity to {new_qty}.")


        elif choice == "R": #Removing items from the list
            code = input("Please enter the item code you want to remove: ").strip().upper()
            if code not in order_items:
                print(f"'{code}' is not currently in your order.")
                continue 

            removed_item = order_items.pop(code)
            print(f"removed {removed_item['name']} from your order.")

        else: #Rejection of 
            print("Invalid option. Please enter C, R or B.")

def review_and_confirm_order(menu, customer_details, order_items):
    '''Present the order review for customers to confirm, edit their order, change their details or cancel the order.'''

    while True: 
        display_order_summary(customer_details, order_items, is_final=False)
        print("Order Review Options")
        print("  [1] Confirm and place order")
        print("  [2] Edit order (Change quantities or remove items)")
        print("  [3] Add items")
        print("  [4] Edit customer details (Name, phone number, salt & vinegar)")
        print("  [5] Cancel order")
        action = input("Enter your choice (1-5): ").strip()

        if action == "1":
            if not order_items:
                print("Cannot confirm an empty order. Please add items or cancel the order.")
                continue
            return "CONFIRMED"

        elif action == "2":
            edit_order_items(customer_details, order_items)

        elif action == "3":
            add_items_to_order(menu, order_items)

        elif action == "4":
            edit_customer_details(customer_details)

        elif action == "5":
            if get_yes_or_no("Are you sure you want to cancel your entire order? (Y/N): "):
                order_items.clear()
                return "CANCELLED"

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

def main():
    '''Starting and ending function. Prints messages for when the order is cancelled, or when the order is placed'''

    customer_details = collect_customer_details()

    order_items = {}

    add_items_to_order(MENU_ITEMS, order_items)
    order_status = review_and_confirm_order(MENU_ITEMS, customer_details, order_items)

    if order_status == "CANCELLED":
        print(f"Order cancelled. No worries, {customer_details['name']}-see you next time!")
    else:
        display_order_summary(customer_details, order_items, is_final=True)
        print(
            f"\nHello {customer_details['name']}! Your order is in the fryer."
            f" We will text {customer_details['phone']} when it is ready for pickup"
        )



if __name__ == "__main__":
    main()













