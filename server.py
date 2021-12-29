import socket
from _thread import *
import pickle
from blackjack import *


def threaded_client(conn, p, game):
    conn.send(str.encode(str(p)))


def main():
    id_count = 0

    server = '192.168.1.108'
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(e)

    s.listen(5)

    game = BlackjackTable()

    print('Server Started')
    print('Waiting for a connection')

    while True:
        conn, addr = s.accept()
        print(f'Connected to: {addr}')

        id_count += 1

        start_new_thread(threaded_client, (conn, id_count, game))


if __name__ == '__main__':
    main()
