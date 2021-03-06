import socket
import pickle
from settings import IP, PORT, MESSAGE_SIZE, END_SYMBOL

from hanabi_client import print_position, finish_game, move

NAME = input()

def recieve_data(sock, buffer):
    message = sock.recv(MESSAGE_SIZE)
    buffer.extend(message.split(END_SYMBOL)[:-1])
    
def next_command(buffer):
    result = buffer.pop(0)
    return pickle.loads(result)

def connect(name, ip, port, buffer):
    sock = socket.socket()
    sock.connect((ip, port))
    print('connect')
    sock.send(bytes(name, encoding='utf-8'))
    recieve_data(sock, buffer)
    start_game = next_command(buffer)
    print('game started')
    recieve_data(sock, buffer)
    players_list = next_command(buffer).split(' ')
    print(players_list)
    turn_num = players_list.index(name)
    return players_list, turn_num, sock

def game(sock, players, buffer):
    while True:
        if not buffer:
            recieve_data(sock, buffer)
        data = next_command(buffer)
        if 'Position' == data[0]:
            client_position = data[1]
            print_position(client_position, players, turn_num)
        elif 'Your turn' == data[0]:
            sock.send(pickle.dumps(move(client_position, players, turn_num)))
        elif 'Game over' == data[0]:
            finish_game(data[1], players)
            return
            
buffer = []
players, turn_num, sock = connect(NAME, IP, PORT, buffer)
game(sock, players, buffer)
input()