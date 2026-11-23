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
#Constants and Menu data
#------------------------------------------------------------------------------
# Constants are written in uppercase to represent fixed rules.
# This allows them to be changed in one place, instead of needing to find and
# change every section of code which uses the same constant.


BUSINESS_NAME = "Maraetai Kiwi Fish & Chips"
MAX_QUANTITY_PER_ITEM = 10
MIN_QUANTITY_PER_ITEM = 1
MIN_PHONE_NUMBER = 7 
MAX_PHONE_NUMBER = 15 
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
    ["E02", "Vinegar", "Extra", .50]
    ["D01", "L&P Can", "Drink", 3]
    ["D02", "Coca Cola Can", 3]
]