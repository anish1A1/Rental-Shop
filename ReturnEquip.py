



import datetime
from tabulate import tabulate
import Equipment

FINE_RATE = 3
RANGE_DAYS = [(1, 5), (6, 10), (11, 15), (16, 20)]  # Define the day ranges and their corresponding multipliers

def return_equipment():
    print("Available Equipment:")
    rented_equipment = Equipment.load_equipment_data("data.txt")
    display_rented_equipment(rented_equipment)
    
    while True:
        try:
            user_name = input("Enter your name: ").strip()
            if not user_name:
                print("\nPlease enter a valid name.")
            else:
                break
        except Exception:
            print("Please enter a valid name.")
    
    while True:
        print(f"Hello {user_name}")
        returned_item_id = input("\nEnter the ID of the item you want to return (or 'exit' to go back): ")

        if returned_item_id.lower() == 'exit':
            break

        if returned_item_id.isdigit():
            equipment_id = int(returned_item_id)
            if equipment_id in rented_equipment:
                rented_quantity = rented_equipment[equipment_id]["quantity"]
                if rented_quantity > 0:
                    rental_duration = int(input("Enter the number of days the item was rented: "))
                    quantity_to_return = get_quantity_to_return(rented_quantity)
                    total_return_charge, fine_amount = calculate_return_charge(rental_duration, rented_equipment[equipment_id]["price"])
                    total_return_charge *= quantity_to_return
                    total_return_charge += fine_amount
                    return_item(rented_equipment, equipment_id, rental_duration, quantity_to_return, total_return_charge, fine_amount)
                    Equipment.update_quantity(rented_equipment, equipment_id, quantity_to_return)
                    Equipment.save_equipment_data(rented_equipment, "data.txt")
                else:
                    print("The item was not rented.\n")
            else:
                print("Invalid equipment ID. Please enter a valid ID.\n")

def display_rented_equipment(rented_equipment):
    headers = ["ID", "Name", "Brand", "Price ($)", "Rental Duration", "Quantity"]
    rented_display = []

    for equipment_id, details in rented_equipment.items():
        name = details["name"]
        brand = details["brand"]
        price = details["price"]
        rental_duration = details.get("rental_duration", 0)
        quantity = details["quantity"]
        rented_display.append([equipment_id, name, brand, price, rental_duration, quantity])

    table = tabulate(rented_display, headers=headers, tablefmt="grid")
    print(table)
    

def get_quantity_to_return(rented_quantity):
    while True:
        try:
            quantity = int(input(f"Enter the quantity you want to return (up to {rented_quantity} rented): "))
            if quantity <= 0 or quantity > rented_quantity:
                print(f"Please enter a valid quantity (1 to {rented_quantity}).")
            else:
                return quantity
        except ValueError:
            print("Please enter a valid number.")
            
def calculate_fine(rental_duration):
    if rental_duration > 5:
        late_days = rental_duration - 5
        return FINE_RATE * late_days
    else:
        return 0            

def return_item(rented_equipment, equipment_id, rental_duration, quantity_to_return, total_return_charge, fine_amount):
    item = rented_equipment[equipment_id]
    item_name = item["name"]
    item_brand = item["brand"]
    rental_charge, _ = calculate_return_charge(rental_duration, item["price"])
    late_fine = calculate_fine(rental_duration)
    fine_amount += late_fine
    
    print("\nReturn Summary:")
    print(f"Equipment: {item_name}")
    print(f"Brand: {item_brand}")
    print(f"Return Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Quantity Returned: {quantity_to_return}")
    print(f"Rental Duration: {rental_duration} days")
    print(f"Fine for {rental_duration - 5} day(s) late: ${late_fine:.2f}")
    print(f"Total Return Charge (including fine): ${total_return_charge + fine_amount:.2f}")
    
    rented_equipment[equipment_id]["quantity"] -= quantity_to_return


   # Increase the quantity of returned items
    Equipment.update_quantity(rented_equipment, equipment_id, quantity_to_return)
    Equipment.save_equipment_data(rented_equipment, "data.txt")  # Save updated data to file
    
    invoice = generate_invoice(item_name, item_brand, quantity_to_return, rental_duration, total_return_charge, fine_amount)
    save_invoice_to_file(invoice, item_name)

def calculate_return_charge(rental_duration, item_price):
    range_index = 0
    for days_range in RANGE_DAYS:
        if days_range[0] <= rental_duration <= days_range[1]:
            fine_days = max(0, rental_duration - days_range[1])
            fine_amount = FINE_RATE * fine_days
            return item_price * (range_index + 1), fine_amount
        range_index += 1
    fine_days = max(0, rental_duration - RANGE_DAYS[-1][1])
    fine_amount = FINE_RATE * fine_days
    return item_price * (range_index + 1), fine_amount

def generate_invoice(item_name, item_brand, quantity_to_return, rental_duration, total_return_charge, fine_amount):
    invoice = f"""
Return Summary:
Equipment: {item_name}
Brand: {item_brand}
Return Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Quantity Returned: {quantity_to_return}
Rental Duration: {rental_duration} days
Fine for {rental_duration - 5} day(s) late: ${fine_amount:.2f}
Total Return Charge with fine: ${total_return_charge + fine_amount:.2f}
"""
    return invoice

#function to write invoice in the txt file if returned equipment
def save_invoice_to_file(invoice, item_name):
    invoice_file_name = f"{item_name.replace(' ', '_')}_ReturnInvoice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(invoice_file_name, "w") as file:
        file.write(invoice)
    print(f"Invoice generated: Your invoice is generated in {invoice_file_name} file")

if __name__ == "__main__":
    return_equipment()





























# import datetime
# from tabulate import tabulate
# import Equipment

# FINE_RATE = 3
# RANGE_DAYS = [(1, 5), (6, 10), (11, 15), (16, 20)]  # Define the day ranges and their corresponding multipliers

# def return_equipment():
#     print("Available Equipment:")
#     rented_equipment = Equipment.load_equipment_data("data.txt")
#     display_rented_equipment(rented_equipment)
    
#     while True:
#         try:
#             user_name = input("Enter your name: ").strip()
#             if not user_name:
#                 print("\nPlease enter a valid name.")
#             else:
#                 break
#         except Exception:
#             print("Please enter a valid name.")
    
#     while True:
#         print(f"Hello {user_name}")
#         returned_item_id = input("\nEnter the ID of the item you want to return (or 'exit' to go back): ")

#         if returned_item_id.lower() == 'exit':
#             break

#         if returned_item_id.isdigit():
#             equipment_id = int(returned_item_id)
#             if equipment_id in rented_equipment:
#                 rented_quantity = rented_equipment[equipment_id]["quantity"]
#                 if rented_quantity > 0:
#                     rental_duration = int(input("Enter the number of days the item was rented: "))
#                     quantity_to_return = get_quantity_to_return(rented_quantity)
#                     total_return_charge, fine_amount = calculate_return_charge(rental_duration, rented_equipment[equipment_id]["price"])
#                     total_return_charge *= quantity_to_return
#                     total_return_charge += fine_amount
#                     return_item(rented_equipment, equipment_id, rental_duration, quantity_to_return, total_return_charge, fine_amount)
#                     Equipment.update_quantity(rented_equipment, equipment_id, quantity_to_return)
#                     Equipment.save_equipment_data(rented_equipment, "data.txt")
#                 else:
#                     print("The item was not rented.\n")
#             else:
#                 print("Invalid equipment ID. Please enter a valid ID.\n")

# def display_rented_equipment(rented_equipment):
#     headers = ["ID", "Name", "Brand", "Price ($)", "Rental Duration", "Quantity"]
#     rented_display = []

#     for equipment_id, details in rented_equipment.items():
#         name = details["name"]
#         brand = details["brand"]
#         price = details["price"]
#         rental_duration = details.get("rental_duration", 0)
#         quantity = details["quantity"]
#         rented_display.append([equipment_id, name, brand, price, rental_duration, quantity])

#     table = tabulate(rented_display, headers=headers, tablefmt="grid")
#     print(table)
    

# def get_quantity_to_return(rented_quantity):
#     while True:
#         try:
#             quantity = int(input(f"Enter the quantity you want to return (up to {rented_quantity} rented): "))
#             if quantity <= 0 or quantity > rented_quantity:
#                 print(f"Please enter a valid quantity (1 to {rented_quantity}).")
#             else:
#                 return quantity
#         except ValueError:
#             print("Please enter a valid number.")
            
# def calculate_fine(rental_duration):
#     if rental_duration > 5:
#         late_days = rental_duration - 5
#         return FINE_RATE * late_days
#     else:
#         return 0            

# def return_item(rented_equipment, equipment_id, rental_duration, quantity_to_return, total_return_charge, fine_amount):
#     item = rented_equipment[equipment_id]
#     item_name = item["name"]
#     item_brand = item["brand"]
#     rental_charge, _ = calculate_return_charge(rental_duration, item["price"])
#     late_fine = calculate_fine(rental_duration)
#     fine_amount += late_fine
    
#     print("\nReturn Summary:")
#     print(f"Equipment: {item_name}")
#     print(f"Brand: {item_brand}")
#     print(f"Return Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     print(f"Total Quantity Returned: {quantity_to_return}")
#     print(f"Rental Duration: {rental_duration} days")
#     print(f"Total Return Charge: ${total_return_charge:.2f}")
#     print(f"Fine for {rental_duration - 5} day(s) late: ${late_fine:.2f}")
    
#     rented_equipment[equipment_id]["quantity"] -= quantity_to_return


#    # Increase the quantity of returned items
#     Equipment.update_quantity(rented_equipment, equipment_id, quantity_to_return)
#     Equipment.save_equipment_data(rented_equipment, "data.txt")  # Save updated data to file
    
#     invoice = generate_invoice(item_name, item_brand, quantity_to_return, rental_duration, total_return_charge, fine_amount)
#     save_invoice_to_file(invoice, item_name)

# def calculate_return_charge(rental_duration, item_price):
#     range_index = 0
#     for days_range in RANGE_DAYS:
#         if days_range[0] <= rental_duration <= days_range[1]:
#             fine_days = max(0, rental_duration - days_range[1])
#             fine_amount = FINE_RATE * fine_days
#             return item_price * (range_index + 1), fine_amount
#         range_index += 1
#     fine_days = max(0, rental_duration - RANGE_DAYS[-1][1])
#     fine_amount = FINE_RATE * fine_days
#     return item_price * (range_index + 1), fine_amount

# def generate_invoice(item_name, item_brand, quantity_to_return, rental_duration, total_return_charge, fine_amount):
#     invoice = f"""
# Return Summary:
# Equipment: {item_name}
# Brand: {item_brand}
# Return Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Total Quantity Returned: {quantity_to_return}
# Rental Duration: {rental_duration} days
# Fine for {rental_duration - 5} day(s) late: ${fine_amount:.2f}
# Total Return Charge: ${total_return_charge:.2f}
# """
#     return invoice

# def save_invoice_to_file(invoice, item_name):
#     invoice_file_name = f"{item_name.replace(' ', '_')}_ReturnInvoice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
#     with open(invoice_file_name, "w") as file:
#         file.write(invoice)
#     print(f"Invoice generated: Your invoice is generated in {invoice_file_name} file")

# if __name__ == "__main__":
#     return_equipment()









# import datetime
# from tabulate import tabulate
# import Equipment

# def return_equipment():
#     print("Rented Equipment:")
#     rented_equipment = Equipment.load_equipment_data("data.txt")
#     display_rented_equipment(rented_equipment)
    
#     while True:
#         try:
#             user_name = input("Enter your name: ").strip()
#             if not user_name:
#                 print("/nPlease enter a valid name.")
#             else:
#                 break
#         except Exception:
#             print("Please enter a valid name.")
    
#     while True:
#         print(f"Hello {user_name}")
#         returned_item_id = input("\nEnter the ID of the item you want to return (or 'exit' to go back): ")

#         if returned_item_id.lower() == 'exit':
#             break

#         if returned_item_id.isdigit():
#             equipment_id = int(returned_item_id)
#             if equipment_id in rented_equipment:
#                 rented_quantity = rented_equipment[equipment_id]["quantity"]
#                 if rented_quantity > 0:
#                     rental_duration = int(input("Enter the number of days the item was rented: "))
#                     quantity_to_return = get_quantity_to_return(rented_quantity)
#                     if quantity_to_return <= rented_quantity:
#                         return_item(rented_equipment, equipment_id, rental_duration, quantity_to_return)
#                         Equipment.update_quantity(rented_equipment, equipment_id, quantity_to_return)  # Increase the quantity
#                         Equipment.save_equipment_data(rented_equipment, "data.txt")  # Save updated data
#                     else:
#                         print("Sorry, invalid quantity.")
#                 else:
#                     print("The item was not rented.\n")
#             else:
#                 print("Invalid equipment ID. Please enter a valid ID.\n")

# def display_rented_equipment(rented_equipment):
#     headers = ["ID", "Name", "Brand", "Price ($)", "Rental Duration", "Quantity"]
#     rented_display = []

#     for equipment_id, details in rented_equipment.items():
#         name = details["name"]
#         brand = details["brand"]
#         price = details["price"]
#         rental_duration = details.get("rental_duration", 0)
#         quantity = details["quantity"]
#         rented_display.append([equipment_id, name, brand, price, rental_duration, quantity])

#     table = tabulate(rented_display, headers=headers, tablefmt="grid")
#     print(table)
    

# def get_quantity_to_return(rented_quantity):
#     while True:
#         try:
#             quantity = int(input(f"Enter the quantity you want to return (up to {rented_quantity} rented): "))
#             if quantity <= 0:
#                 print("Please enter a valid positive quantity.")
#             else:
#                 return quantity
#         except ValueError:
#             print("Please enter a valid number.")

# def return_item(rented_equipment, equipment_id, rental_duration, quantity_to_return):
#     item = rented_equipment[equipment_id]
#     item_name = item["name"]
#     item_brand = item["brand"]
#     item_price = item["price"]
#     rental_charge = calculate_rental_charge(rental_duration, item_price)
    
#     print("\nReturn Summary:")
#     print(f"Equipment: {item_name}")
#     print(f"Brand: {item_brand}")
#     print(f"Return Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     print(f"Total Quantity Returned: {quantity_to_return}")
#     print(f"Rental Duration: {rental_duration} days")
#     print(f"Total Rental Charge: ${rental_charge:.2f}")
    
#     # this will update in the rented equipment dictionary
#     rented_equipment[equipment_id]["quantity"] += quantity_to_return

#     Equipment.update_quantity(rented_equipment, equipment_id, -quantity_to_return)  # Update quantity here
#     Equipment.save_equipment_data(rented_equipment, "data.txt")  # Saves the updated data
    
#     invoice = generate_invoice(item_name, item_brand, quantity_to_return, rental_duration, rental_charge)
#     save_invoice_to_file(invoice, item_name)
# def calculate_rental_charge(rental_duration, item_price):
#     if rental_duration > 5:
#         extra_days = rental_duration - 5
#         return item_price + (10 * extra_days)
#     return item_price

# def generate_invoice(item_name, item_brand, quantity_to_return, rental_duration, rental_charge):
#     invoice = f"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Equipment Return Invoice
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Invoice Number: {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}
# Return Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Equipment Name: {item_name}
# Brand: {item_brand}
# Total Quantity Returned: {quantity_to_return}
# Rental Duration: {rental_duration} days
# Total Rental Charge: ${rental_charge:.2f}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Thank You!
# """
#     return invoice

# def save_invoice_to_file(invoice, item_name):
#     invoice_file_name = f"{item_name}_ReturnInvoice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
#     with open(invoice_file_name, "w") as file:
#         file.write(invoice)
#     print(f"Invoice generated: Your invoice is generated in {invoice_file_name} file")

# if __name__ == "__main__":
#     return_equipment()















