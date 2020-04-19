import socket
import json
import wave
from threading import Thread, Event
from time import time
import os
import mmap

wait = False

out_data = ''
posture_input = ''
time_input = None
flag_gesture_input = False  # use this flag to identify if there was an input from CV in past duration


def send_data(jsonfilename, client, clientinput, state):
    # sending input to server (ie DISCONNECT)
    client.sendall(bytes(clientinput, 'UTF-8'))

    # loading data from file
    data = json.load(open(jsonfilename))

    # sending state and json data
    client.sendall(bytes(json.dumps(data), 'UTF-8'))
    client.sendall(bytes(state, 'UTF-8'))

    # receiving confirmation that data has been sent
    print('here')
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())


def send_wav_data(wavfilename, client, clientinput):
    # sending input to server (ie DISCONNECT)
    client.sendall(bytes(clientinput, 'UTF-8'))
    sizu = os.path.getsize(wavfilename)
    print(sizu)
    file_size_b = sizu.to_bytes(4, 'big')
    sent = 0
    counter = 0
    # loading and sending from wav file
    client.sendall(file_size_b)
    #client.sendall(int(sizu).to_bytes(2, byteorder='big'))
    with open(wavfilename, 'rb') as f:
        for l in f:
            sent += client.send(l)
            counter += 1
        print(counter)


        f.close()
    client.sendall(bytes('end','UTF-8'))    # this is the termination bytes
        # client.sendall(bytes('end', 'UTF-8'))
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())


def client_receive(client, clientinput):
    # sending client input
    client.sendall(bytes(clientinput, 'UTF-8'))
    msg = 'received'
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


def main_job(e):
    while True:
        event_is_set = e.wait()
        out_data = input("Input your choice: ")
        out_data = out_data.upper()
        print(out_data)
        if out_data == 'SEND_JSON':
            send_data('data.json', client, out_data, 'IDLE')

        elif out_data == 'SEND_WAV':
            send_wav_data('output.wav', client, out_data)
            print("wav file data sent")
        elif out_data == 'DISCONNECT':
            send_message('DISCONNECT')
            close_NLP(client)
            break
        elif out_data == 'UPDATE_STATE':
            inp = input("Enter state")
            # send state to the client
            send_message('Update_State')
            with open('states.txt', 'r+b') as f:
                mm = mmap.mmap(f.fileno(), 0)
                mm.write(int(inp).to_bytes(1, byteorder='big'))
                f.close()
            client.sendall((int(inp).to_bytes(2, byteorder='big')))
        elif out_data == 'RECEIVE':
            data, state = client_receive(client, out_data)
        e.set()
        e.clear()


def flag_check(event):
    state = 0
    while True:
        with open('states.txt', 'r+b')as f:
            mm = mmap.mmap(f.fileno(), 0)
            #print(mm[0])
            #print(mm[1])
            if mm[1] == 1:
                event.set()
                mm.seek(1)
                mm.write(state.to_bytes(1, byteorder='big'))
                f.close()


def init_NLP():
    # establishing connection
    SERVER = "127.0.0.1"
    PORT = 10005
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    return client


def close_NLP(client):
    client.close()


if __name__ == '__main__':
    client = init_NLP()
    client.sendall(bytes('NLP', 'UTF-8'))
    status = client.recv(1024)
    print(status.decode())
    e = Event()
    cv_event = Event()
    work = Thread(target=main_job, args=(e,))
    CV_Input = Thread(target=flag_check, args=(e,))
    work.start()
    CV_Input.start()
    state = 3

    while True:
        server_input = client.recv(1025)

        server_input = server_input.decode()
        print(server_input)
        # if server_input.upper() == 'UPDATE_STATE':
        #     data = client.recv(1025)
        #     decoded = data.decode()
        #     if decoded.upper() == 'START':
        #         e.set()
        if server_input.upper() == 'CV_INPUT':
            posture_input = client.recv(1025)
            posture_input = posture_input.decode()
            print(posture_input)
