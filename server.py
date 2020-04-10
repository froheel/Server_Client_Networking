import socket
import threading
from threading import Condition
import json
import wave


blender_state = None
nlp_state = None
Cv_blender = [None] * 2
Cv_nlp = None
Condition1 = Condition()
Condition2 = Condition()
Condition3 = Condition()
Condition4 = Condition()


class nlpThreadlisten(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", self.caddress)
        msg = 'transferred'
        while True:

            # instruction from client
            client_message = self.csocket.recv(2048)
            client_message = client_message.decode()
            if client_message == 'DISCONNECT':
                break
            elif client_message == 'SEND_JSON':
                # server receive
                data = self.csocket.recv(2048)
                print("data from client", data)
                state = self.csocket.recv(2048)
                print("state from client", state)
                self.csocket.send(bytes(msg, 'UTF-8'))
                self.csocket.send(bytes(msg, 'UTF-8'))
                print('here')
            elif client_message == 'SEND_WAV':
                # server receives wav file
                with open('rcvd_file.wav', 'wb') as f:
                    while True:
                        l = self.csocket.recv(2048);
                        if l == bytes('end', 'UTF-8'): break
                        f.write(l)
                    print("Wav file received")
                    f.close()

            elif client_message == 'RECEIVE':
                # loading data from file and reading state
                state = 'THINKING'
                data = json.load(open('data.json'))
                # sending state and json data
                self.csocket.send(bytes(json.dumps(data), 'UTF-8'))
                self.csocket.sendall(bytes(state, 'UTF-8'))
                # receiving confirmation that data has been sent
                in_data = self.csocket.recv(2048)
                print("From Client ", self.caddress, " : ", in_data.decode())

            elif client_message == "Update_State":
                # send updated state
                client_message = self.csocket.recv(2048)

                # send state to the client
                global blender_state
                global Condition1
                Condition1.acquire()
                try:
                    blender_state = client_message
                    Condition1.notify()
                finally:
                    Condition1.release()

        print("Client at ", self.caddress, " disconnected...")




class Threadsend(threading.Thread):
    def __init__(self, clientAddress, clientsocket, Condition, send_message):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        self.Condition = Condition
        self.message = send_message
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", self.caddress)

        global state_update
        global blender_state
        while True:
            with self.Condition:
                self.Condition.wait()
                self.csocket.sendall(self.message)


class blenderThreadlisten(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        client_message = self.csocket.recv(1024)

        # send state to the client
        global nlp_state
        global Condition2
        while True:
            client_message = self.csocket.recv(1024)
            Condition2.acquire()
            try:
                nlp_state = client_message
                Condition2.notify()
            finally:
                Condition2.release()

class CVThreadlisten(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        client_message = self.csocket.recv(1024)

        # send state to the client
        global Cv_blender
        global Cv_nlp
        global Condition3
        global Condition4
        while True:
            client_message = self.csocket.recv(4096)
            client_message = client_message.decode()
            if client_message.upper == 'GLOBAL':
                x = self.csocket.recv(4096) #get x coord from CV
                y = self.csocket.recv(4086) #get y coord from CV
                Condition4.acquire()
                try:
                    Cv_blender[0] = x
                    Cv_blender[1] = y
                    Condition4.notify()
                finally:
                    Condition4.release()
            elif client_message.upper == 'USER_INPUT':
                message = self.csocket.recv(4096)
                Condition3.acquire()
                try:
                    Cv_nlp = message
                    Condition3.notify()
                finally:
                    Condition3.release()
            else:
                self.csocket.sendall("wrong input",'UTF-8' )


def inialize_threads(thread_type, clientAddress, clientsock):
    rcv = 'Recived'
    global Condition1
    global Condition2
    global Condition3
    global Condition4
    global nlp_state
    global blender_state
    global Cv_blender
    global Cv_nlp
    if thread_type.upper == 'NLP':
        clientsock.send(bytes(rcv, 'UTF-8'))
        nlp = nlpThreadlisten(clientAddress, clientsock)
        nlp2 = Threadsend(clientAddress, clientsock, Condition1,nlp_state )
        nlp3 = Threadsend(clientAddress, clientsock, Condition3, Cv_nlp)
        nlp.start()
        nlp2.start()
        nlp3.start()

    elif thread_type.upper == 'BlENDER':
        blender = Threadsend(clientAddress, clientsock, Condition2, blender_state)
        blender2 = blenderThreadlisten(clientAddress, clientsock)
        blender3 = Threadsend(clientAddress, clientsock, Condition4, Cv_blender)
        blender.start()
        blender2.start()
        blender3.start()

    elif thread_type.upper == 'CV':
        a = 0
    else:
        return 0
    return 1


def init_server():
    LOCALHOST = "192.168.100.88"
    PORT = 10005
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Server started")
    print("Waiting for client request..")
    # creating threads for every client
    while True:

        print("Waiting for client request..")
        server.listen(1)
        clientsock, clientAddress = server.accept()
        if inialize_threads(clientsock.recv(), clientAddress, clientsock):
            clientsock.sendall(bytes('Connection Established', 'UTF-8'))
        else:
            clientsock.sendall(bytes('invalid Connection string', 'UTF-8'))






if __name__ == '__main__':
    init_server()
