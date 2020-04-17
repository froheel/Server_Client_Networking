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
        user_input = input("Input your data: ")
        client.sendall(bytes(user_input, 'UTF-8'))