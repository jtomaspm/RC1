import psutil
import socket
import sys

def generate_cpu_usage_string(time=5):
    cpu_str = str(psutil.cpu_percent(time))
    return "CPU usage at: " + cpu_str + " %"

def send_mensage(message, sock):
    message = message.encode()
    try: 
        if len(message)>1:
            sock.send(message)
            print("client messsge: " + message.decode())
            response = sock.recv(4096).decode()
            print('Server response: {}'.format(response))
            print()
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)

class client_ui:
    def __init__(self, sock):
        self.sock = sock

        self.STATES = {
                "initial" : {
                    "print" : """
What do you want to do?
[1] : manual mode
[2] : auto mode
[3] : change server settings
                    """,
                    "links" : {
                        1 : "manual",
                        2 : "auto",
                        3 : "server_settings",
                        },
                    "options" : {
                        1 : self.update_state,
                        2 : self.update_state,
                        3 : self.update_state,
                        }
                    },


                "manual" : {
                    "print" : """
For how long do you want to capture CPU usage?
("0" to return to previous menu)
                    """,
                    "cache" : {
                        "time" : 5,
                        },
                    "options" : {
                        0 : self.update_state("initial"),
                        #(self.STATES["manual"]["cache"]["time"])
                        }
                    },


                "auto" : {
                    "print" : """
For how long do you want to capture CPU usage?
How many times?
("x y" where x is the capture time, and y for the loop times. y<=0 means it will "run forever")  
("0" to return to previous menu)
                    """,
                    "cache" : {
                        "time" : 5,
                        "loops" : -1,
                        },
                    "options" : {
                        0 : self.update_state("initial"),
                        #(self.STATES["auto"]["cache"]["time"],self.STATES["auto"]["cache"]["loops"])
                        }
                    },


                "server_settings" : {
                    "print" : """
Set the light and moderate cap.
Light cap (x): if CPU usage is under this value, it is under light load 
Moderate cap (y): if CPU usage is under this value, it is under moderate load, and the client should be carefull 
If the client CPU usage is above this value the server will warn him.
("x y" where x is the light cap, and y is the moderate cap)
("0" to return to previous menu)
                    """,
                    "cache" : {
                        "light" : 50,
                        "moderate" : 80,
                        },
                    "options" : {
                        0 : self.update_state("initial"),
                        #(self.STATES["server_settings"]["cache"]["light"],self.STATES["server_settings"]["cache"]["moderate"])
                        }
                    },

                }

        self.state = "initial"


    def update_state(self, state):
        self.state = state


    def handle_input(self, client_input):

        if self.state == "initial":
            if int(client_input) not in self.STATES["initial"]["options"].keys():
                print("invalid input")
            else:
                self.STATES["initial"]["options"][int(client_input)](self.STATES["initial"]["links"][int(client_input)])
            return None

        elif self.state == "manual":
            client_input = int(client_input)
            if client_input == 0:
                self.update_state("initial")
            elif client_input > 0:
                send_mensage(generate_cpu_usage_string(client_input), self.sock)
            else:
                print("invalid input")
        
        elif self.state == "auto":
            ci =client_input.split(" ")
            if len(ci) == 1:
                if int(client_input) == 0:
                    self.state = "initial"
            elif len(ci) == 2:
                ci = (float(ci[0]), int(ci[1]))
                temp = 0
                if ci[1] > 0:
                    while temp < ci[1]:
                        send_mensage(generate_cpu_usage_string(ci[0]), self.sock)
                        temp +=1
                else:
                    while True:
                        send_mensage(generate_cpu_usage_string(ci[0]), self.sock)
            else:
                print("invalid input")
        
        elif self.state == "server_settings":
            ci =client_input.split(" ")
            if not len(ci) == 2:
                if int(client_input) == 0:
                    self.state = "initial"
                else:
                    print("invalid input")
            else:
                self.state = "initial"
                send_mensage("CSS " + str(ci[0]) + " " + str(ci[1]), self.sock)

        else:
            self.state = "initial"

    
