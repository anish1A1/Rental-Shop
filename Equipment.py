from tabulate import tabulate

def load_equipment_data(file_path):       #this function reads equipments data from file_path
    equipment = {}

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                values = line.split(",")
                equipment_id = int(values[0].strip())
                name = values[1].strip()
                brand = values[2].strip()
                price = float(values[3].replace("$", ""))
                quantity = int(values[4].strip())

                equipment[equipment_id] = {   #equipment_id as a key value
                    "name": name,
                    "brand": brand,
                    "price": price,
                    "quantity": quantity
                }

    return equipment


def display_equipment():
    print("    Equipment Inventory")
    equipment_data =load_equipment_data("data.txt")
    headers = ["ID", "Name", "Brand", "Price ($)", "Quantity"]
    equipment_display = []

    for equipment_id, details in equipment_data.items():
        name = details["name"]
        brand = details["brand"]
        price = details["price"]
        quantity = details["quantity"]
        equipment_display.append([equipment_id, name, brand, price, quantity])

    table = tabulate(equipment_display, headers=headers, tablefmt="grid")
    print(table)
########    
    # this is added to update
def update_quantity(equipment, equipment_id, quantity_change):
    if equipment_id in equipment:
        equipment[equipment_id]["quantity"] += quantity_change
    else:
        print("Invalid equipment ID.")    

def save_equipment_data(equipment, file_path):
    with open(file_path, "w") as file:
        for equipment_id, details in equipment.items():
            line = f"{equipment_id},{details['name']},{details['brand']},${details['price']},{details['quantity']}\n"
            file.write(line)   
##########
if __name__ == "__main__":
    display_equipment()











