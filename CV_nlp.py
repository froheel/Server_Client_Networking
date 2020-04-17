from socket import socket
from socket import  AF_INET
from socket import SOCK_STREAM


def init_CV_NLP():
    # assigning default values to coordinates


    # establishing connection
    SERVER = "127.0.0.1"
    PORT = 10005
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((SERVER, PORT))
    return client


if __name__ == '__main__':
    client = init_CV_NLP()
    client.sendall(bytes('CV_NLP', 'UTF-8'))
    status = client.recv(1024)
    print(status.decode())
    while True:
        user_input = input("nlp or cv ")
        if user_input == 'nlp':
            client.sendall(bytes(user_input, 'UTF-8'))
            if client.recv(2056) == bytes('got it', 'UTF-8'):
                user_input = input("Enter the information that you wish to send")
                client.sendall(bytes(user_input, 'UTF-8'))
        elif user_input =='cv':
            client.sendall(bytes(user_input, 'UTF-8'))
            server_message = client.recv(2056)
            print(server_message)
            if server_message == bytes('got it', 'UTF-8'):
                user_input  = input("Enter the state ")
                client.sendall(int(user_input).to_bytes(2, byteorder='big'))
        else:
            print('Wrong input ')