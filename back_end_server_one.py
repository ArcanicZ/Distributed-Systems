import Pyro4

@Pyro4.expose
class ProccessOrders(object):
    def __init__(self):
        self.all_orders = []
        #Full Menu
        self.restMenus = [["Pizza Hut",  
                            {"starters": [("Garlic bread with cheese", 2,), ("Chicken bites", 1.50), ("Chicken wings", 2)], 
                            "mains": [("Pepperoni melt", 4.50), ("Mac 'n' cheese", 2), ("Garlic mushroom melt", 3)], 
                            "desserts": [("Cinnamon bites", 1.50), ("Chocolate chip cookie dough", 2), ("Ice Cream", 1)], 
                            "drinks": [("Ginger ale", 1),("Cappuccino", 1),("Espresso", 1)]}],
                        ["The Curry House",  
                            {"starters": [("Meat Samosa", 1), ("Bombay Potatoes", 1.50), ("Onion bhajis", 1)], 
                            "mains": [("Donner wrap", 4), ("Pilau rice with chicken tikka masala", 3), ("Lamb Biriyani", 5)], 
                            "desserts": [("Cheesecake", 1.80), ("Chocolate gateaux", 1.80), ("Jalebi", 1)], 
                            "drinks": [("Water", 1.20),("Pepsi", 0.80),("Fanta", 0.80)]}],
                        ["ASK Italian",  
                            {"starters": [("Garlic bread with cheese", 1.50), ("Tomato bruschetta", 1), ("Smoked chicken canapés", 2)], 
                            "mains": [("Lasagne", 3), ("Spaghetti bolognese", 4), ("Pasta carbonara", 4)], 
                            "desserts": [("Tiramisu", 1.50), ("Cinnamon rolls", 1), ("Apple pie", 1)], 
                            "drinks": [("Red wine", 5),("Water", 1),("Orange juice", 1.50)]}],
                        ["Don's Tacos and Burritos",  
                            {"starters": [("Tortillas chips with salsa", 1), ("Chicken wings", 1.20), ("Fries", 1.50)], 
                            "mains": [("Beef burrito", 4), ("Chicken burrito", 4), ("Beef taco", 3)], 
                            "desserts": [("Chocolare cake", 2), ("Churros", 1.50), ("Cheesecake", 2)], 
                            "drinks": [("J20", 1),("7up", 1),("Dr Pepper", 1)]}]]
    
    #Sends full menu
    def send_all_menus(self):
        print("Sending Menus")
        return self.restMenus


    #Tries to update for all servers
    def update_order(self, items):
        print("Updating order")
        self.all_orders.append(items)
        try:
            backend2.update(self.all_orders)
        except:
            print("Failed to update server 2's order list!")

        try:
            backend3.update(self.all_orders)
        except:
            print("Failed to update server 3's order list!")
        
        return self.all_orders
    
    #Goes to web service or retrieves from stored array
    def get_address(self, postcode):
        print("Checking postcode!")
        try:
            return postcode1.get_address(postcode)
        except:
            try:
                return postcode2.get_address(postcode)
            except:
                return None

    #Sends the past orders of the user
    def past_orders(self, name):
        print("Retrieving past orders!")
        client_orders = []
        for i in self.all_orders:
            if i[0] == name:
                client_orders.append(i)

        if len(client_orders) == 0:
            return 0
        else:
            allClient = []
            for j in client_orders:
                result = name + ", your order from"
                result += " " +j[1] + " contained:"
                for k in range(2, len(j)-3):
                    result += " " + j[k]
                result += " " + "which totalled to: £" + str(j[-3])
                result += ". This order was placed at " + str(j[-2]) + " in post code area: " + str(j[-1])
                allClient.append(result)

            return allClient

    #Checks between two lists and see if there is a difference, if so then fill out the missing ones
    def update(self, new):
        for i in self.all_orders:
            if i not in new:
                new.append(i)

        self.all_orders = new
        print("SELF", self.all_orders)
        print("NEW", new)
        print("Updating order lists!")


#When updating all orders, check to see which are missing and add it on.

backend2 = Pyro4.Proxy("PYRONAME:BackEnd2")
backend3 = Pyro4.Proxy("PYRONAME:BackEnd3")

postcode1 = Pyro4.Proxy("PYRONAME:PostCode1")
postcode2 = Pyro4.Proxy("PYRONAME:PostCode2")

# make a Pyro daemon
daemon = Pyro4.Daemon()
# find the name server         
ns = Pyro4.locateNS()              

# register the greeting maker as a Pyro object
uri = daemon.register(ProccessOrders())  
# register the object with a name in the name server
ns.register("BackEnd1", uri)   

print("Ready.")
# start the event loop of the server to wait for calls
daemon.requestLoop()                