#Importing required headers
from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil
import json
import sys

#Defining the threshold for indicating overload
MaxUtilizationAllowed = 30 

#Setting the current servers ID and port at which it is listening
#Will be used in load balancing
SERVER_ID = int(sys.argv[1])
PORT_NUMBER = int(sys.argv[2])


#Function to get CPU utilization percentage
#[Note: Here we use CPU utilization as the metric for load balancing]
def get_cpuload():
    return psutil.cpu_percent()


#Class to handle requests to server.
class RequestHanlder(BaseHTTPRequestHandler):
    def do_GET(self):
        #Checking if overloaded
        current_load = get_cpuload()

        if(current_load < MaxUtilizationAllowed):
            #Sending Appropriate Response codes and headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            #Sending response
            response = dict()
            response['server'] = SERVER_ID
            response['load'] = current_load
            response['State'] = "Currently serving requests"
            self.wfile.write(json.dumps(response).encode())

        else:
             #Sending Appropriate Response codes and headers
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            #Sending response
            response = dict()
            response['server'] = SERVER_ID
            response['load'] = current_load
            response['State'] = "Overloaded! Currently Unavailable"
            self.wfile.write(json.dumps(response).encode())
        return response


def main():
    try:
        server = HTTPServer(('', PORT_NUMBER), RequestHanlder)
        print("---------------------------------------------------------------------------------------")
        print('Started server:', SERVER_ID, '\nOn port: ', PORT_NUMBER)
        print("---------------------------------------------------------------------------------------")
        server.serve_forever()

    except KeyboardInterrupt:
        print('Shutting down...')
        server.socket.close()
main()