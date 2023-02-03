What this System is:
A fault-tolerant distributed system, called “Just Hungry”, based on passive replication, supporting online food ordering and delivery.

Instructions to run system:

The way in which you should run the system is by running the bat file called 'runall.bat'. What this does is open up every single python file in separate command prompts, this makes it easier just to open all files. If you want to run another client file, you should open another command prompt and type 'python client_program.py' to run it. An important warning is that there should be a command prompt with the input 'python -m Pyro4.naming' running always in order for the system to work. This is already called in the bat file but in case the bat file was not used, you must ensure this is done before running the system.

Resources used:

I have used two webservices in order look up and validate the user inputted postcode. These are Postcodes.io and GetTheData. Two webservices for the postcode lookup has been used in case one of the services goes down. Even if both of the services go down, as long as the postcode inputted was searched by the server earlier on, the postcode can still be validated without the two web services.