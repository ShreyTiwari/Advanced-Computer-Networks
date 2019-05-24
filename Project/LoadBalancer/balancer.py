#Importing required headers
import requests
import json
import time
from termcolor import colored
from os import system

#Defining the path and port number at which servers are listening
n = 0
servers = []

#Function to perform initial setup of the loadbalancer
def setup():
    global n
    global servers
    
    #Getting number of servers
    print("Enter the number of severs: ", end = '')
    n = int(input())
    print()

    #Getting port numbers on which the servers are running
    for i in range(n):
        print("Enter the IP Address of the server ", (i+1), ": ", end = '')
        temp = input()
        print("Enter the listening port of server ", (i+1), ": ", end = '')
        temp = temp + ":" + input()
        servers.append(str(temp))

    print("\nEntered Data")
    print("Number of servers: ", n)
    print("Listening ports: ", servers)

    print("\n-----------------------------------------------------------------------")
    print("Commencing Load Balancing....")
    print("-----------------------------------------------------------------------\n")


#Function to check if the server is overloaded
def is_server_overload(request):
    #Defining overloaded variable
    overloaded = False

    #Getting current load
    data = json.loads(request.text)
    load = data['load']

    print("-----------------------------------------------------------------------")
    print("Status Code: ", request.status_code)
    print("Current Load: ", load)

    if request.status_code != 200:
        print(colored("Server is overloaded", "red"))
        overloaded = True
    else:
        print(colored("Server is not overloaded", "green"))
    
    print("-----------------------------------------------------------------------")
    print("\n")

    return overloaded


#Function that issues requests to the servers and does loadbalancing
def main():
    #Performing setup
    setup()
    return
    #Start with first server and perform round robin 
    current_server = 0
    
    #Run forever
    while True:
        #Make requests every 3 secs
        time.sleep(3)
        
        #To stop the program press 'ctrl + c'
        try:
            #Trying to get response from servers
            r = requests.get(servers[current_server], headers={'User-Agent':'Python'})
            print("Response: ", r.text)
            overload = is_server_overload(r)
            if overload:
                print(colored('Trying another server.... \n',"blue"))
                current_server = (current_server + 1) % n
                continue
            current_server = (current_server + 1) % n
                

        except requests.ConnectionError:
            print("-----------------------------------------------------------------------")
            print('Server ', current_server+1, 'failed to respond, trying another server...')
            print("-----------------------------------------------------------------------")
            current_server = (current_server + 1) % 3
        
        except KeyboardInterrupt:
            print("-----------------------------------------------------------------------")
            print('Shutting Down...')
            print("-----------------------------------------------------------------------")
            break

        print()

#Calling main function to start the load balancing
main()