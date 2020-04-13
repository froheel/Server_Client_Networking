import socket
import threading
import json

# Initially Idle state
global current_state
coord = [] # first position is x and the second is y


def send_data(jsonfilename, client, clientinput, state):
    # sending input to server (ie DISCONNECT)
    client.sendall(bytes(clientinput, 'UTF-8'))

    # loading data from file
    data=json.load(open(jsonfilename))

    # sending state and json data
    client.send(bytes(json.dumps(data), 'UTF-8'))
    client.sendall(bytes(state, 'UTF-8'))

    # receiving confirmation that data has been sent
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())


def send_wav_data(wavfilename, client, clientinput):
    # sending input to server (ie DISCONNECT)
    client.sendall(bytes(clientinput, 'UTF-8'))

    # loading and sending from wav file
    with open('output.wav', 'rb') as f:
        for l in f:
            client.sendall(l)
        f.close()
        client.sendall(bytes('end', 'UTF-8'))

def client_receive(client,clientinput):
    # sending client input
    client.sendall(bytes(clientinput, 'UTF-8'))
    msg= 'received'
    # receiving data and state from server
    data = client.recv(1024)
    print("data from client", data)
    state = client.recv(1043)
    print("state from client", state)
    # sending message to server that transmission was successful
    client.send(bytes(msg, 'UTF-8'))
    return data, state

def send_message(input_msg):
    client.sendall(bytes(input_msg, 'UTF-8'))


def init_NLP():
    # establishing connection
    SERVER = "127.0.0.1"
    PORT = 10005
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    return client

def close_NLP(client):
    client.close()

class ClientThread(threading.Thread):
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client = client
    def run(self):
        global current_state
        # Recieve from server
        client.sendall(bytes('BLENDER', 'UTF-8'))
        global coord
        msg = 'transferred'
        while True:
            server_input = client.recv(1043)
            if server_input.upper() == 'UPDATE_STATE':
                state = client.recv(1043)
                current_state = int.from_bytes(state, byteorder='big')
            elif server_input.upper() == 'CV_INPUT':
                coords_input = client.recv(1025)
                coord = [x for x in coords_input]
                print(coord)
            elif server_input.upper() == 'SEND_JSON':
                # server receive
                data = self.csocket.recv(2048)

                print("data from client", data)
                state = self.csocket.recv(2048)
                print("state from client", state)
                self.csocket.send(bytes(msg, 'UTF-8'))
                self.csocket.send(bytes(msg, 'UTF-8'))
                print('here')
            elif server_input.upper() == 'SEND_WAV':
                # server receives wav file
                with open('rcvd_file.wav', 'wb') as f:
                    while True:
                        l = self.csocket.recv(2048);
                        if l == bytes('end', 'UTF-8'): break
                        f.write(l)
                    print("Wav file received")
                    f.close()

            elif server_input.upper() == 'RECEIVE':
                # loading data from file and reading state
                state = 'THINKING'
                data = json.load(open('data.json'))
                # sending state and json data
                self.csocket.send(bytes(json.dumps(data), 'UTF-8'))
                self.csocket.sendall(bytes(state, 'UTF-8'))
                # receiving confirmation that data has been sent
                in_data = self.csocket.recv(2048)
                print("From Client ", self.caddress, " : ", in_data.decode())




#state 0 ---> Idle
#state 1 ---> Listening
#state 2 ---> Thinking
#state 3 ---> Speaking


def start_nlp(client):
    while True:
        print("nlp_Start")
        input("press enter to start nlp")
        client.sendall(bytes('start', 'UTF-8'))


#main program
if __name__ == '__main__':

    #initialising variables
    global current_state
    current_state= 0
    client = init_NLP()
    client.sendall(bytes('BlENDER', 'UTF-8'))
    status = client.recv(1024)
    print(status.decode())
    # To get state from server without blocking the main program
    newthread = ClientThread(client)
    newthread.start()
    nlp_control = threading.Thread(target=start_nlp, args=(client, ))
    nlp_control.start()
    while True:
        if current_state == 0:
            #print("Idle State")
            #do something
            a = 0
        elif current_state == 1:
            #print("Listening State")
            # do something
            a = 0
        elif current_state == 2:
            #print("Thinking State")
            # do something
            a = 0
        elif current_state == 3:
            #print("Speaking State")
            # do something
            a = 0
        else:
            #print("Invalid State")
            # do something
            a = 0
