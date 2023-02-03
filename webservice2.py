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
            j = urllib.request.urlopen('http://api.getthedata.com/postcode/' + postcode)

            #Decode item from web service request
            str_response = j.read().decode('utf-8')
            js = json.loads(str_response)

            token = js['status']
            country = js['data']['country']

            #If postcode not valid then return None else return the country that the postcode is in.
            if token != 'match':
                return None
            else:
                self.stored[postcode] = country
                return country


 # make a Pyro daemon
daemon = Pyro4.Daemon()
# find the name server
ns = Pyro4.locateNS()                
# register the greeting maker as a Pyro object
uri = daemon.register(Postcode)
# register the object with a name in the name server
ns.register("PostCode2", uri)

print("Ready.")
# start the event loop of the server to wait for calls
daemon.requestLoop()