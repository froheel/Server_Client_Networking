import socket
from multiprocessing import shared_memory


if __name__ == '__main__':
    # establishing connection
    SERVER = "127.0.0.1"
    PORT = 10010
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    precision = 10000
    shared_data = shared_memory.ShareableList(name='coords')
    while True:
        x = client.recv(2048)
        client.sendall(bytes('got x', 'UTF-8'))
        y = client.recv(2048)
        client.sendall(bytes('got y ', 'UTF-8'))
        try:
            shared_data[1] = (int.from_bytes(x, byteorder='big') - precision) / precision
            shared_data[2] = (int.from_bytes(x, byteorder='big') - precision) / precision
            shared_data[0] = True
            print(shared_data)
        except ValueError:
            print('no worries')