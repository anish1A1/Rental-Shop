import datetime
from tabulate import tabulate
import Equipment

def sell_equipment():
    print("Available Equipment:")
    equipment = Equipment.load_equipment_data("data.txt")
    display_equipment(equipment)
    
    while True:
        sold_item_id = input("\nEnter the ID of the item you want to rent (or 'exit' to go back): ")

        if sold_item_id.lower() == 'exit':
            break

        if sold_item_id.isdigit():
            equipment_id = int(sold_item_id)
            if equipment_id in equipment:
                available_quantity = equipment[equipment_id]["quantity"]
                if available_quantity > 0:
                    customer_name = input("Enter customer name: ")
                    quantity_to_rent = get_quantity_to_rent(available_quantity)
                    days_to_rent = get_days_to_rent()
                    total_rental_charge = calculate_rental_charge(equipment[equipment_id]["price"], days_to_rent) * quantity_to_rent
                    sell_item(equipment, equipment_id, customer_name, quantity_to_rent, days_to_rent, total_rental_charge)  
                    
                    
                    Equipment.update_quantity(equipment, equipment_id, -quantity_to_rent)  # Update the quantity
                    Equipment.save_equipment_data(equipment, "data.txt")  # Save updated data
                else:
                    print("The item is not available for rent.\n")
            else:
                print("Invalid equipment ID. Please enter a valid ID.\n")

def display_equipment(equipment):
    headers = ["ID", "Name", "Brand", "Price ($)", "Quantity"]
    equipment_display = []

    for equipment_id, details in equipment.items():
        name = details["name"]
        brand = details["brand"]
        price = details["price"]
        quantity = details["quantity"]
        equipment_display.append([equipment_id, name, brand, price, quantity])

    table = tabulate(equipment_display, headers=headers, tablefmt="grid")
    print(table)

def get_quantity_to_rent(available_quantity):
    while True:
        try:
            quantity = int(input(f"Enter the quantity you want to rent (up to {available_quantity} available): "))
            if quantity <= 0:
                print("Please enter a valid positive quantity.")
            else:
                return quantity
        except ValueError:
            print("Please enter a valid number.")
            
def get_days_to_rent():
    while True:
        try:
            days = int(input("Enter the number of days to rent: "))
            if days <= 0:
                print("Please enter a valid number of days.")
            else:
                return days
        except ValueError:
            print("Please enter a valid number.")
            
def calculate_rental_charge(price, days_to_rent):
    ranges = [(1, 5), (6, 10), (11, 15), (16, 20)]  # Day ranges and corresponding multipliers
    charge = 0
    
    for range_start, range_end in ranges:
        if range_start <= days_to_rent <= range_end:
            charge = price * (ranges.index((range_start, range_end)) + 1)
            break
    
    return charge


def sell_item(equipment, equipment_id, customer_name, quantity_to_rent, days_to_rent, total_rental_charge):
    print("\nRent Summary:")
    print(f"Equipment: {equipment[equipment_id]['name']}")
    print(f"Brand: {equipment[equipment_id]['brand']}")
    print(f"Customer: {customer_name}")
    print(f"Rental Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Quantity Rented: {quantity_to_rent}")
    print(f"Rental Duration: {days_to_rent} days")
    print(f"Total Rental Charge: ${total_rental_charge:.2f}")

    invoice = generate_invoice(customer_name, equipment[equipment_id]['name'], equipment[equipment_id]['brand'], quantity_to_rent, days_to_rent, total_rental_charge)
    save_invoice_to_file(invoice, customer_name)

def generate_invoice(customer_name, equipment_name, brand, quantity_to_rent, days_to_rent, total_rental_charge):
    invoice = f"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Equipment Rental Invoice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Invoice Number: {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}
Customer Name: {customer_name}
Rental Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Equipment Name: {equipment_name}
Brand: {brand}
Total Quantity Rented: {quantity_to_rent}
Rental Duration: {days_to_rent} days
Total Rental Charge: ${total_rental_charge:.2f}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Thank you!
"""
    return invoice

def save_invoice_to_file(invoice, customer_name):
    invoice_file_name = f"{customer_name}_RentalInvoice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(invoice_file_name, "w") as file:
        file.write(invoice)
    print(f"{invoice_file_name}")

if __name__ == "__main__":
    sell_equipment()


