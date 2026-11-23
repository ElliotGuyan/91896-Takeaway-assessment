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
#While it may be a sauce, there is already a "Sides" category, and having s 
#conflict would be a problem.

MENU_ITEMS = [
    ["F01", "Battered Hoki Fillet", "Fish", 7.50],
    ["F02", "Battered Snapper Fillet", "Fish", 11.50],
    ["F03", "Battered Tarakihi", "Fish", 10.50],
    ["C01", "Scoop of Potato Chips", "Chips", 4.50],
    ["C02", "Kumara Chips", "Chips", 6.50],
    ["S01", "Battered Hot Dog", "Side", 4],
    ["S02", "Squid Rings", "Side", 7],
    ["E01", "Tomato Sauce", "Extra", .50],
    ["E02", "Extra Lemon", "Extra", .50]
    ["D01", "L&P Can", "Drink", 3]
    ["D02", "Coca Cola Can", 3]
]

#------------------------------------------------------------------------------
# Formatting and input validation functions.
#------------------------------------------------------------------------------

def format_currency(amount): #Formats numbers into currency with 2dp.
    return f"${amount:.2f}"


def verify_customer_name(prompt): #Prompts the user until a valid name is given.
    while True: 
        raw_name = input(prompt).strip() # Strips the raw name of spaces before and after
        if raw_name and any(char.isalpha() for char in raw_name): # Checks that there is at least one alphabetical letter in the name
            valid_name = " ".join(raw_name.split()).title() # Connects the name back together.
            return valid_name
        print("Invalid name. Please enter a name containing letters, (The name cannot be blank)")



def verify_customer_name_customer_phone_number(prompt): # Prompts the user until a valid number is given

    while True:
        raw_phone = input(prompt).strip() #Strips the raw number. removing any spaces 
        digits_only = "".join(char for char in raw_phone if char.isdigit()) # Checks if the input is digits only

        if (
            raw_phone
            and all(char.isdigit() or char in "-+()" for char in raw_phone) # Allows signs, -+() and spaces.
            and MIN_PHONE_NUMBER_LENGTH <= len(digits_only) <= MAX_PHONE_NUMBER_LENGTH # Checks that the phone number is within the valid length (7-15)
        ):
            return " ".join(raw_phone.split()) 
        
        print( 
            f"Invalid phone number. Please enter {MIN_PHONE_NUMBER_LENGTH} - {MAX_PHONE_NUMBER_LENGTH}" # Message to tell the user to correct an invalid input
            "digits (Spaces and hypens are allowed)"
        )


def get_valid_integer(prompt, min_value, max_value): 

    while True: 
        raw_input = input(prompt).strip()
        try:
            number = int(raw_input)
        except ValueError:
            print(f"Invalid input. Please enter a whole number ({min_value} - {max_value})")
            continue 

        if min_value <= number <= max_value:
            return number
        
        print(f"Out of range. Please enter a number between {min_value} and {max_value}")

def get_yes_or_no(prompt):
    while True: 
        choice = input(prompt).strip().upper()
        if choice in ("Y", "YES"):
            return True
        if choice in ("N", "NO"): 
            return False
        print("Invalid response. Please enter Y or N.")


def build_order_label(wants_salt_and_vinegar):

    if wants_salt_and_vinegar:
        return "Pickup (With Salt & Vinegar)"
    return "Pickup (Plain/No Salt)"



#------------------------------------------------------------------------------
# Menu display, search & order cost functions
#------------------------------------------------------------------------------

def display_menu(menu): #Prints the menu in neatly, evenly aligned columns along with order limits

    line_width = 58
    print("\n" + "=" * line_width)
    print(f"{BUSINESS_NAME.upper()} - MENU".center(line_width))
    print("=" * line_width)
    print(f"{'Code':<6} {'Item':<28} {'Category':<10} {'Price':>10}")
    print("-" * line_width)

    for item_code, item_name, category, price in menu: 
        print(f"{item_code:<6} {item_name:<28} {category:<10} {format_currency(price):>10}")

    print("-" * line_width)
    print(f"Note: {MAX_QUANTITY_PER_ITEM} of each item per order. All prices include GST")


def find_menu_item(menu, code_input): #Searches the 2D menu list for a match item code (case-insensitive) Returns the matching row [code, name, category, price] or none

    target_code = code_input.strip().upper()
    for item in menu:
        if item[0] == target_code:
            return item
        return None 
    

def calculate_order_totals(order_items): # Calculates and returns the total price of the order

    total_count = 0 #Items
    total_cost = 0.0 #Price 2dp

    for item_data in order_items.values():
        qty = item_data["quantity"] # qty is used inplace of quantity. As less confusing since quantity follows right after in the [] brackets
        total_count += qty
        total_cost += item_data["price"] * qty 

    included_gst = total_cost - (total_cost / (1 + GST_RATE))
    return total_count, total_cost, included_gst

def display_order_summary(customer_details, order_items, is_final=False): #Displays an itemised summary of customer details, items, GST and total cost

    line_width = 60 
    header_title = "TAX RECEIPT & ORDER SUMMARY" if is_final else "CURRENT ORDER SUMMARY"


    print("\n" + "=" * line_width)
    print(header_title.center(line_width))
    print("=" * line_width)
    print(f"Customer : {customer_details['name']}")
    print(f"Phone    : {customer_details['phone']}")
    print(f"Order    : {customer_details['order_type']}"  )
    print("-" * line_width)

    if not order_items:
        print("Your order is currently empty.")
        print("-" * line_width)      
        return
    
    print(f"{'Code':<6} {'Item':<25} {'Qty':>4} {'Unit':>10} {'Subtotal':>11}")
    print("-" * line_width)

    for code, details in order_items.items():
        subtotal = details["price"] * details["quantity"]
        print(
            f"{code:<6} {details['name']:<25} {details['quantity']:>4} "
            f"{format_currency(details['price']):>10}"
        )

    total_count, total_cost, included_gst = calculate_order_totals(order_items)
    print("-" * line_width)
    print(f"{'Total Items:':<47} {total_count:>11}")
    print(f"{'Includes GST (15%):':<47} {format_currency(included_gst):>11} ")
    print(f"{'TOTAL TO PAY:':<47} {format_currency(total_cost):>11}")
    print("-" * line_width)




















