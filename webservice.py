import Pyro4
import json
import urllib
import urllib.request


@Pyro4.expose
class Postcode(object):
    def __init__(self):
        #Stores the postcodes that have been read by the web service, used in case web service goes down
        self.stored = {}

    def get_address(self, postcode):
        #If its not stored use web service
        if postcode in self.stored:
            return self.stored[postcode]
        else:
            j = urllib.request.urlopen('https://api.postcodes.io/postcodes/' + postcode)

            #Decode item from web service request
            str_response = j.read().decode('utf-8')
            js = json.loads(str_response)

            token = js['status']
            region = js['result']['region']

            #If postcode not valid then return 404 else return the region that the postcode is in.
            if token == '404':
                return 404
            else:
                self.stored[postcode] = region
                return region


# make a Pyro daemon
daemon = Pyro4.Daemon()            
# find the name server 
ns = Pyro4.locateNS()               

# register the greeting maker as a Pyro object
uri = daemon.register(Postcode)
# register the object with a name in the name server
ns.register("PostCode1", uri)

print("Ready.")
# start the event loop of the server to wait for calls
daemon.requestLoop()