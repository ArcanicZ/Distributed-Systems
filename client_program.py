import Pyro4
import sys
from datetime import datetime

order = Pyro4.Proxy("PYRONAME:process.orders")

name = input("Welcome, what is your name? ").strip()

#Keeps looping until a condition breaks the loop
while True:
    print (30 * '-')
    print ("   J U S T  H U N G R Y")
    print (30 * '-')
    print ("1. Make an order")
    print ("2. View Past Orders")
    print (30 * '-')
    option = input("Please choose either option 1 or 2: ")

    if option == '1':
        #Displays the restaurant names
        client_order = []
        print("Option 1")
        all_menus = order.get_all_menus()
        print (2 * '\n')
        print (30 * '-')
        print ("   R E S T A U R A N T S")
        print (30 * '-')
        for i in range(len(all_menus)):
            print("{}. {}".format(i+1, all_menus[i][0]))
        print (30 * '-')

        while True:
            
            try:
                restaurant = input("Please choose an option: ")
                rest = int(restaurant) - 1
            except:
                print("Option is not a valid integer!\n")
            else:
                if rest > -1 and rest < 4:
                    #Adds name and restaurant to client order
                    client_order.append(name)
                    client_order.append(all_menus[rest][0])
                    #Prints the menu of selected restaurant
                    print (2 * '\n')
                    print (30 * '-')
                    print ("           M E N U")
                    print (30 * '-')
                    count = 1
                    for key in all_menus[rest][1]:
                        print (30 * '-')
                        print ("          " + key.upper())
                        print (30 * '-')
                        for value in all_menus[rest][1][key]:
                            print("{}. {:^18} = £{:.2f}".format(count, value[0], value[1]))
                            count += 1
                        print('\n')


                    total = 0
                    #Loop to pick which food items user wants while also keeping track of the total and displaying it
                    while True:
                        print("Total Amount = £{:.2f}".format(total))
                        item = input("Input item number (input 'c' to cancel order or input 'f' to finish order): ")
                        if item == 'c':
                            sys.exit()
                            break
                        elif item == 'f':
                            break
                        else:
                            try:
                                index = int(item) - 1
                            except:
                                print("Expected item number, 'f' or 'c'!")
                            else:
                                if index > -1 and index < 12:
                                    if index >= 0 and index <=2:
                                        total += all_menus[rest][1]["starters"][index][1]
                                        client_order.append(all_menus[rest][1]["starters"][index][0])
                                    elif index >= 3 and index <=5:
                                        total += all_menus[rest][1]["mains"][5-index][1]
                                        client_order.append(all_menus[rest][1]["mains"][5-index][0])
                                    elif index >= 6 and index <=8:
                                        total += all_menus[rest][1]["desserts"][8-index][1]
                                        client_order.append(all_menus[rest][1]["desserts"][8-index][0])
                                    elif index >= 9 and index <=11:
                                        total += all_menus[rest][1]["drinks"][11-index][1]
                                        client_order.append(all_menus[rest][1]["drinks"][11-index][0])
                                else:
                                     print("Expected item number between 1 and 12")
        

                    client_order.append(total)

                    #Validates postcode and checks to see if atleast one server is still running
                    postcode = input("What is your Postcode? ").replace(' ','')
                    reg = order.get_address(postcode)
                    if(reg == None):
                        print("Unable to validate postcode!")
                    elif(reg == 404):
                        print("Postcode is invalid!")
                    else:
                        print("Region/Country =", reg)
                        timeNow = datetime.now()
                        dt_string = timeNow.strftime("%d/%m/%Y %H:%M:%S")
                        strTime = str(dt_string)
                        client_order.append(strTime)
                        client_order.append(reg)
                        update = order.update_order(client_order)
                        if(update == None):
                            print("Server is offline!")
                        else:
                            print("You have successfully placed an order!")

                    break
                else:
                    print("Expected an option between 1 and 4!\n")
        break

    elif option == '2':
        past = order.past_orders(name)
        if(past == 0):
            print("You have not made any previous orders!")
        else:
            for a in past:
                print(a)
        break

    else:
        print("Invalid option, please try again!\n")

    # use name server object lookup uri shortcut

