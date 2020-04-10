# Code for CV Client which continuously sends data to server by using keywords like GLOBAL and USERINPUT
import socket
import threading
import time


#global variables
global coord_one
global coord_two
global user_input

def init_CV():
    # assigning default values to coordinates
    coord_one = 0
    coord_two = 0
    user_input = ""

    # establishing connection
    SERVER = "127.0.0.1"
    PORT = 10005
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    return client

def close_CV(client):
    client.close()


class global_send(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
    def run(self):

        global coord_one
        global coord_two
        while True:
            clientinput="GLOBAL"
            #Signally that this is the global data
            client.sendall(bytes(clientinput, 'UTF-8'))
            #sending coord_one
            self.client.sendall((int(coord_one).to_bytes(2, byteorder='big')))
            #sending coord two
            self.client.sendall((int(coord_one).to_bytes(2, byteorder='big')))
            #send data after every 0.5 seconds
            time.sleep(0.5)

class userinput_send(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):

        global user_input
        while True:
            #Signally that this is the global data
            client_input= "INPUT"
            client.sendall(bytes(client_input, 'UTF-8'))
            #taking input from the user and sending it
            user_input = input("Input your data: ")
            client.sendall(bytes(user_input, 'UTF-8'))



if __name__ == '__main__':

    # intialising client
    client = init_CV()

    # making a thread for each task
    global_thread = global_send(client)
    userinp_thread = userinput_send(client)
    global_thread.start()
    userinp_thread.start()

    # signal that CV has been started
    c_input = "INPUT"
    client.sendall(bytes(c_input, 'UTF-8'))


