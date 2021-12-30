import socket
from _thread import *
import pickle
from blackjack import *


def threaded_client(conn, in_game_id, game, buff_size=8192):
    conn.send(str.encode(str(in_game_id)))

    while True:
        try:
            data = conn.recv(buff_size).decode()

            if not data:
                break

            # possible moves to do in the game
            if data == 'get':
                pass
            elif data == 'Ready':
                game.player_ready(in_game_id)
                print(f'{game.players[str(in_game_id)].name} is ready')
            elif data == '-':
                pass
            elif data == '+':
                pass
            elif data == 'Bet':
                pass

            conn.sendall(pickle.dumps(game))
        except:
            break
    print('Connection lost')
    conn.close()
    game.disconnect(in_game_id)


def main():
    count = 0
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

        new_player = Player(f'Player {count}')
        count += 1
        err_code, in_game_id = game.join(new_player)

        if err_code == 0:
            start_new_thread(threaded_client, (conn, in_game_id, game))
        else:
            print('Lobby is too full')


if __name__ == '__main__':
    main()
