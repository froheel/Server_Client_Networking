import socket
import threading
import json


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress=clientAddress
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", self.caddress)
        msg = 'transferred'
        while True:

            # instruction from client
            client_message = self.csocket.recv(2048)
            client_message = client_message.decode()
            if client_message == 'DISCONNECT':
                break
            elif client_message== 'SEND':
                # server receive
                data = self.csocket.recv(2048)
                print ("data from client", data)
                state= self.csocket.recv(2048)
                print("state from client", state)
                self.csocket.send(bytes(msg, 'UTF-8'))
            elif client_message=='RECEIVE':
                # loading data from file and reading state
                state= 'THINKING'
                data = json.load(open('data.json'))
                # sending state and json data
                self.csocket.send(bytes(json.dumps(data), 'UTF-8'))
                self.csocket.sendall(bytes(state, 'UTF-8'))
                # receiving confirmation that data has been sent
                in_data = self.csocket.recv(2048)
                print("From Client ", self.caddress, " : ", in_data.decode())

        print ("Client at ", self.caddress, " disconnected...")


def init_server():
    LOCALHOST = "127.0.0.1"
    PORT = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Server started")
    print("Waiting for client request..")
    while True:
        # creating threads for every client
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()


if __name__ == '__main__':
    init_server()