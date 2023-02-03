import Pyro4

@Pyro4.expose
class ProccessOrders(object):

    #Retrieves the restaurants and their menus
    def get_all_menus(self):
        try:
            return backend1.send_all_menus()
        except:
            #print(e)
            try:
                return backend2.send_all_menus()
            except:
                #print(e)
                try:
                    return backend3.send_all_menus()
                except:
                    #print(e)
                    return None

    #Tries to update the order, if it fails then tries on the next server until all servers fail.
    def update_order(self, items):
        try:
            return backend1.update_order(items)
        except:
            #print(e)
            try:
                return backend2.update_order(items)
            except: 
                #print(e)
                try:
                    return backend3.update_order(items)
                except: 
                    #print(e)
                    return None

    #Tries to update the order, if it fails then tries on the next server until all servers fail.      
    def past_orders(self, name):
        try:
            test = backend1.past_orders(name)
            print(test)
            return test
        except:
            #print(e)
            try:
                return backend2.past_orders(name)
            except:
                #print(e)
                try:
                    return backend3.past_orders(name)
                except:
                    #print(e)
                    return None

    #Tries to get address for a server, if it fails then tries on the next server until all servers fail.
    def get_address(self, postcode):
        try:
            return backend1.get_address(postcode)
        except:
            #print(e)
            try:
                return backend2.get_address(postcode)
            except :
                #print(e)
                try:
                    return backend3.get_address(postcode)
                except:
                    #print(e)
                    return None




#Creates proxies for other pyro objects
backend1 = Pyro4.Proxy("PYRONAME:BackEnd1")
backend2 = Pyro4.Proxy("PYRONAME:BackEnd2")
backend3 = Pyro4.Proxy("PYRONAME:BackEnd3")

# make a Pyro daemon
daemon = Pyro4.Daemon()
# find the name server               
ns = Pyro4.locateNS()                  

# register the greeting maker as a Pyro object
uri = daemon.register(ProccessOrders)   
# register the object with a name in the name server
ns.register("process.orders", uri)   

print("Ready.")
 # start the event loop of the server to wait for calls
daemon.requestLoop()                  
