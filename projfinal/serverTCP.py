import socket
import threading
import signal
import sys

LIGHT = 50
MODERATE = 80

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

def generate_response(msg):
    global LIGHT
    global MODERATE
    print(msg)
    if msg.split(" ")[0] == "CSS":
        msg = msg.split(" ")
        LIGHT = float(msg[1])
        MODERATE = float(msg[2])

        return "Server settings updated"
    
    else:
        cpu_usage = float(msg.split(" ")[3])
        print("cpu usage: ", cpu_usage)
        if cpu_usage <= LIGHT:
            return "CPU under light usage"
        if cpu_usage <= MODERATE:
            return "Be carefull, CPU under moderate usage"
        return "WARNING!!!!! CPU under heavy usage"


def handle_client_connection(client_socket,address): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                client_socket.close()
            else:
                msg = generate_response(request.decode())
                print('Received {}'.format(msg))
                msg=(msg).encode()
                client_socket.send(msg)
    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))


ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, tcp_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(ip_addr, tcp_port))

while True:
    client_sock, address = server.accept()
    client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address),daemon=True)
    client_handler.start()


