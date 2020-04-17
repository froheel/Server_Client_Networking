# Code for CV Client which continuously sends data to server by using keywords like GLOBAL and USERINPUT
import socket
import threading
import time
import random


#global variables
coord_one = 0
coord_two = 0
user_input = ''

def init_CV():
    # assigning default values to coordinates


    # establishing connection
    SERVER = "127.0.0.1"
    PORT = 10005
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    return client

def close_CV(client):
    client.close()


# class global_send(threading.Thread):
#     def __init__(self, client):
#         threading.Thread.__init__(self)
#         self.client = client
#     def run(self):
def global_send(client):
        global coord_one
        global coord_two
        while True:
            clientinput="GLOBAL"
            precision = 10000
            # for translation multiply with precision and then add precision
            coord_one = random.randint(0,(precision * 2) + 1 )
            coord_two = random.randint(0, (precision * 2) + 1)
            #Signally that this is the global data
            client.sendall(bytes(clientinput, 'UTF-8'))
            client.recv(2048).decode()
            #sending coord_one
            client.sendall((int(coord_one).to_bytes(4, byteorder='big')))
            client.recv(2048).decode()
            #sending coord two
            client.sendall((int(coord_one).to_bytes(4, byteorder='big')))
            client.recv(2048).decode()
            #send data after every 0.5 seconds


if __name__ == '__main__':

    # intialising client
    client = init_CV()
    client.sendall(bytes('CV', 'UTF-8'))
    status = client.recv(1024)
    print(status.decode())
    # making a thread for each task
    global_send(client)



