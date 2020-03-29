import socket
import json


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
    PORT = 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    return client

def close_NLP(client):
    client.close()


if __name__ == '__main__':
    client = init_NLP()
    while True:
        out_data= input()
        if out_data=='SEND':
            send_data('data.json', client, out_data, 'IDLE')
        elif out_data == 'DISCONNECT':
            send_message('DISCONNECT')
            close_NLP(client)
            break
        elif out_data=='RECEIVE':
            data, state = client_receive(client, out_data)
