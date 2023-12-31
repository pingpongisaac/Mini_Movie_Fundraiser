import pandas
import random
from datetime import date

# functions


# checks if input is text
def text_check(question):

    while True:

        error = "Please only enter text"

        response = input(question)
        valid = response.isalpha()

        if valid:
            return response
        else:
            print(error)


# checks if input is on consisting of numbers
def num_check(question):

    while True:

        error = "Please only enter numbers"

        response = input(question)
        valid = response.isnumeric()

        if valid:
            return response
        else:
            print(error)


# show instructions
def show_instructions():
    print('''\n********** Instructions **********

To order a pizza, type in the pizza you would like from the menu.
Only the first word is necessary when entering the pizza 
eg: Cheese Pizza would simply require "cheese".

To order a topping, you would similarly enter the topping from the menu you desire.
eg: If you wanted Ham as an extra topping, you would enter "ham"

After you choose the desired pizzas with any extra toppings,
your order will be organised into a summary presented at the end of your order.

This information will also be automatically written to a text file, as a receipt.

**************************************

Here is the menu:''')


# shows menu of pizzas
def show_menu():
    print('''\n********** Menu **********
 * Hawaiian Pizza: $7.00
-------------------------- 
 * Cheese Pizza: $6.50
-------------------------- 
 * Meatlovers: $8.00
--------------------------     
 * Pepperoni: $7.50
**************************''')


# shows menu of toppings
def show_toppings():
    print('''\n******* Toppings *******
 * Ham: $2.50
------------------------
 * Mushroom: $3.50
------------------------
 * Onion: $1.50
 ----------------------- 
 * Olives: $2.00
------------------------
 * Tomatoes: $2.50
************************''')


# calc pizza price function
def calc_pizza_price(var_pizza):

    # Hawaiian Pizza is $7.00
    if var_pizza == "hawaiian":
        price = 7

    # Plain Cheese Pizza is $6.50
    elif var_pizza == "cheese":
        price = 6.5

    # Meatlovers Pizza is $8.00
    elif var_pizza == "meatlovers":
        price = 8

    # Pepperoni Pizza is $7.50
    else:
        price = 7.5

    return price


# calc toppings price function
def calc_topping_price(var_toppings):

    # Ham is $1.50
    if var_toppings == "ham":
        price = 2.5

    # Mushroom is $2.00
    elif var_toppings == "mushroom":
        price = 2

    # Olives are $1.50
    elif var_toppings == "olives":
        price = 1.5

    # Tomatoes are $2.00
    else:
        price = 2

    return price


# validates string based on list of options
def string_checker(question, num_letters, valid_responses):

    error = "Please choose a valid input"

    while True:
        response = input(question).lower()

        for item in valid_responses:
            if response == item[:num_letters] or response == item:
                return item

        print(error)


# currency format
def currency(x):
    return "${:.2f}".format(x)


# random winner
def random_number():
    number = random.randint(1, 10)
    return number


# main routine goes here

# lists for string checker referencing
yes_no_list = ["yes", "no"]
pizza_list = ["hawaiian", "cheese", "meatlovers", "pepperoni"]
toppings_list = ["ham", "mushroom", "olives", "tomatoes"]

# dictionaries to hold pizza details
all_pizzas = []
all_pizza_costs = []
all_toppings = []
all_toppings_cost = []
temp_toppings = []

pizza_parlour_dict = {
    "[Pizza]": all_pizzas,
    "[Pizza Price]": all_pizza_costs,
    "[Extra Toppings]": all_toppings,
    "[Toppings Price]": all_toppings_cost
}


more_pizza = "yes"
want_toppings = "no"
toppings_price = 0

print("Welcome to Isaac's Pizza Parlour!")
print()
name = text_check("Please enter your name for your order: ")
print()
phone = num_check("Hello {}, can we please have your phone number for if we need to contact you: ".format(name))
print()
address = input("And finally, can we please have your address for the delivery: ")
print()
want_instructions = string_checker("Thank you! Would you like to read the "
                                   "instructions for how to use our system? "
                                   "(yes/no): ", 1,
                                   yes_no_list)

while more_pizza == "yes":
    if want_instructions == "yes":
        show_instructions()
        show_menu()
    else:
        print("Okay, here is the menu:")
        show_menu()

    print()

    # initial pizza selection
    which_pizza = string_checker("Please select which pizza you would like: ", 0, pizza_list)

    print("You chose {} for ${}".format(which_pizza, calc_pizza_price(which_pizza)))
    all_pizzas.append(which_pizza)
    all_pizza_costs.append(calc_pizza_price(which_pizza))

    want_toppings = string_checker("Would you like any extra toppings?", 1, yes_no_list)
    toppings_price = 0
    temp_toppings = []

# runs through toppings order loop to determine toppings
    if want_toppings == "yes":
        while want_toppings == "yes":

            show_toppings()

            which_topping = string_checker("What toppings would you like?", 1, toppings_list)
            print("You chose {} for ${:.2f}".format(which_topping, calc_topping_price(which_topping)))

            toppings_price = toppings_price + calc_topping_price(which_topping)
            temp_toppings.append(which_topping)

            want_toppings = string_checker("Would you like any more extra toppings?", 1, yes_no_list)

            if want_toppings == "yes":
                continue
            elif want_toppings == "no":
                break
    else:
        temp_toppings.append("None")

    all_toppings.append(temp_toppings)
    all_toppings_cost.append(toppings_price)

    more_pizza = string_checker("Do you want any more pizzas?", 1, yes_no_list)

    if more_pizza == "yes":
        want_instructions = "no"
        continue
    elif more_pizza == "no":
        break


pizza_parlour_frame = pandas.DataFrame(pizza_parlour_dict)
# pizza_parlour_frame = mini_movie_frame.set_index('Name')

# calculate total ticket cost (ticket + surcharge)
pizza_parlour_frame['[Total]'] = pizza_parlour_frame['[Pizza Price]'] \
                            + pizza_parlour_frame['[Toppings Price]']

order_total = pizza_parlour_frame['[Total]'].sum()
winner = random_number()

# Currency Formatting (uses currency function)
add_dollars = ['[Pizza Price]', '[Topping Price]', '[Total]']
for var_item in add_dollars:
    pizza_parlour_frame[var_item] = pizza_parlour_frame[var_item].apply(currency)

print(pizza_parlour_frame)
print()
print("Your order total comes to ${:.2f}".format(order_total))
print()
if winner == 5:
    print("Congratulations, you are one our lucky %10 "
          "of customers. You have won a $20 Countdown gift card")

# **** Get current date for heading and filename ****
# get today's date
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

heading = "--------------- Isaac's Pizza Parlour Receipt ({}/{}/{}) --------------\n".format(day, month, year)
filename = "{}_pizza_order_{}_{}_{}".format(name, year, month, day)

# address the user
address_customer = "Order for {}\n" \
                   "Ph: {}\n" \
                   "{}/{}/{}\n".format(name, phone, year, month, day)

items_ordered_heading = "----------------------------- Items Ordered -----------------------------\n"
# Change frame to a string so that we can export it to file
pizza_parlour_string = pandas.DataFrame.to_string(pizza_parlour_frame)

# create strings for printing....
total_order_heading = "\n------------------------------ Order Total ------------------------------\n"
total_order_price = "Your total order price is: ${:.2f}\n".format(order_total)

# closing statement
thank_you = "Thank you for ordering from Isaac's Pizza Parlour, enjoy your meal!"

# list holding content to print \ write to file
to_write = [heading, address_customer, items_ordered_heading,
            pizza_parlour_string, total_order_heading, total_order_price,
            thank_you]


# write output to file
# create file to hold data (add .txt extension)
write_to = "{}.txt".format(filename)
text_file = open(write_to, "w+")

for item in to_write:
    text_file.write(item)
    text_file.write("\n")

# close file
text_file.close()
# program ends
