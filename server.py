import socket
from _thread import *

server = "" # replace this with your ip

port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("waiting for connection, Server started")
logged_in_players = [0, 0, 0]
message = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]

def get_message(lst):
    msg = ""
    for i in range(0, len(lst)):
        if i == len(lst) - 1:
            msg += lst[i]
            break
        msg += lst[i] + ","
    return msg

def send_message(message_str, from_player):
    for i in range(0, len(message)):
        if i == from_player:
            continue
        message[i][from_player] = message_str

def threaded_client(conn, player):
    send = ""
    conn.send(str.encode(str(player)))
    send_message("1", player)
    while True:
        try:
            data = conn.recv(2048).decode("utf-8")
            if not data:
                print("Disconnected")
                send_message("0", player)
                break
            if data[-1] == ".":
                if data[1:-1] == "":
                    send = "~"
                else:
                    send = data[1:-1]
                send_message(send, player)
            print(message[0])
            conn.sendall(str.encode(get_message(message[player])))
        except:
            break
    print("Lost Connection")
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("connected to: ", addr)
    logged_in_players[current_player] = 1
    print(current_player)
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
