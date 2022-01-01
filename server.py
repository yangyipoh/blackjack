import socket
from _thread import *
import pickle
from blackjack import *
import argparse

import os


ADMIN_KEY = 'kYeVsv1o2qfuBUP508rl'


def threaded_client(conn, count, game, lobby_id, buff_size=8192):
    """Client thread. Spawns when new client is added

    Args:
        conn (Socket): communication channel
        count (int): number of players that have tried to joined
        game (BlackjackTable): shared game
        buff_size (int, optional): buffer size to be sent. Defaults to 8192.
    """

    data = conn.recv(buff_size).decode()
    lobby_id_parse, name = data.split(',')

    if lobby_id_parse == lobby_id and name == ADMIN_KEY:
        conn.sendall(str.encode(str('Admin')))
        admin_client(conn, game, buff_size)
        return

    # wrong lobby id
    if lobby_id_parse != lobby_id:
        conn.sendall(str.encode(str(-1)))
        conn.close()
        return
    
    # add player to the game
    if name == '':
        name = f'Player {count}'
    new_player = Player(name)
    err_code, in_game_id = game.join(new_player)

    # lobby is too full
    if err_code == -1:
        conn.sendall(str.encode(str(-2)))
        conn.close()
        return

    # send game id to client to let them know which ID they are
    conn.sendall(str.encode(str(in_game_id)))

    while True:
        try:
            # receive data
            data = conn.recv(buff_size).decode()
            
            # just in case
            if not data:
                break

            # possible moves to do in the game
            if data == 'get':
                pass
            elif data == 'Ready':
                game.player_ready(in_game_id)
            elif data == '-':
                game.sub_bet(in_game_id)
            elif data == '+':
                game.add_bet(in_game_id)
            elif data == 'Bet':
                game.confirm_bet(in_game_id)
            elif data == 'Hit':
                game.hit(in_game_id)
            elif data == 'Stand':
                game.stand(in_game_id)
            elif data == 'Continue':
                game.reset(in_game_id)

            conn.sendall(pickle.dumps(game))
        except:
            break
    print(f'Player {in_game_id}: Connection lost')
    conn.close()
    game.disconnect(in_game_id)


def admin_client(conn, game, buff_size):
    print('Console login')
    while True:
        try:
            # receive data
            data = conn.recv(buff_size).decode()
            
            # just in case
            if not data:
                break
            
            cmd = data.split()
            # Admin console
            if cmd[0] == 'shutdown':
                os._exit(1)
            elif cmd[0] == 'set_money':
                player_id = int(cmd[1])
                amount = int(cmd[2])
                game.set_money(player_id, amount)
            else:
                print('Command not found')

            conn.sendall(pickle.dumps(game))
        except:
            break
    print(f'Admin connection lost')
    conn.close()



def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def main():
    # argparse
    parser = argparse.ArgumentParser(description='Change parameters for the server')
    parser.add_argument('-lobby', '--lobby_id', metavar='', type=str, default='', help='Lobby ID for the server')
    parser.add_argument('-port', '--find_open_port', action='store_true', help='Automatically find open ports')

    args = parser.parse_args()

    LOBBY_ID = args.lobby_id
    FIND_OPEN_PORT = args.find_open_port

    # server info
    hostname = socket.gethostname()
    server = socket.gethostbyname(hostname)

    if FIND_OPEN_PORT:
        port = 0
    else:
        port = 5555

    # create server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        print(e)

    server_ip, server_port = s.getsockname()
    s.listen()

    # print server and lobby details details
    clear_console()
    print('SERVER DETAILS:')
    if LOBBY_ID == '':
        print('No lobby ID set')
    else:
        print(f'Lobby ID: {LOBBY_ID}')

    print(f'Server IP: {server_ip}, Server Port: {server_port}')
    
    game = BlackjackTable()
    print()
    
    count = 0
    print('Logs:')
    while True:
        # wait until connection is accepted
        conn, addr = s.accept()
        print(f'Connected to: {addr}')
        count += 1

        # start player
        start_new_thread(threaded_client, (conn, count, game, LOBBY_ID))


if __name__ == '__main__':
    main()
