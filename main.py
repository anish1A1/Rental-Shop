import Equipment
import SellEquip
import ReturnEquip

def main():
     welcome_message = """
    
    ************************************************************************************************************************************
    *                                               Event Equipment Rental Shop                                                        *
    ************************************************************************************************************************************
            
        Welcome to the Event Equipment Rental Shop!
            
        We have a wide range of equipment available for rent,
        perfect for making your event a success.

    *************************************************************************************************************************************
    
    """
    
     print(welcome_message)
     #print("\n")
     user_name= input("Enter your name: ").strip().title()
    
     
     while True:
         
        print("Which option would you like to choose:")
        print("(1)  ->   View The Item")
        print("(2)  ->   Borrow The Item")
        print("(3)  ->   Return The Item")
        print("(4)  ->   Exit\n")
        
        
        try:
            print(f'Hello, {user_name}.')
            option = input("Enter the option you would like to choose: ").strip()
        except ValueError:
            print("Enter a valid option (1-4)\n")
            continue
        print()
        
        
          
        if option == '1':
            Equipment.display_equipment()
            #Sellinglaptop.sell()
           
        
        elif option == '2':
            #
            SellEquip.sell_equipment()
            
        elif option == '3':
            ReturnEquip.return_equipment()
            #
           
        
        elif option == '4':
            print("Thank you for Visiting Us!")
            print("**" * 80)
            
            break
            
        else:
            print("Enter a valid option (1-4)\n")
            
            
            
if __name__ == '__main__':
    main()
                
            
     



