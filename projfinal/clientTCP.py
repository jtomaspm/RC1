############################################################### MAIN ################################################################################################
import socket
import signal
import sys
from client_ui import *

### Exit 
def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)


    



signal.signal(signal.SIGINT, signal_handler)
###


ip_addr = "127.0.0.1"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

client_interface = client_ui(sock)
### Welcome
print('Press Ctrl+C to exit...')
print()
print('Welcome!')
print()
###

while True:
    print(client_interface.STATES[client_interface.state]["print"])
    client_input = input()
    client_interface.handle_input(client_input)




