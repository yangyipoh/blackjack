import socket
from _thread import *
import pickle
from blackjack import *


LOBBY_ID = ''
FIND_OPEN_PORT = False


def threaded_client(conn, count, game, buff_size=8192):
    """Client thread. Spawns when new client is added

    Args:
        conn (Socket): communication channel
        count (int): number of players that have tried to joined
        game (BlackjackTable): shared game
        buff_size (int, optional): buffer size to be sent. Defaults to 8192.
    """

    data = conn.recv(buff_size).decode()
    lobby_id, name = data.split(',')
    if lobby_id != LOBBY_ID:
        print('Invalid Lobby')
        conn.sendall(str.encode(str('Invalid lobby')))
        conn.close()
        return
    
    # add player to the game
    if name == '':
        name = f'Player {count}'
    new_player = Player(name)
    err_code, in_game_id = game.join(new_player)
    if err_code == -1:
        print('Lobby is too full')
        conn.sendall(str.encode(str('Lobby full')))
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
                print(f'{game.players[str(in_game_id)].name} is ready')
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
    print('Connection lost')
    conn.close()
    game.disconnect(in_game_id)


def main():
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
    print(f'Server started: ip: {server_ip}, port: {server_port}')
    
    game = BlackjackTable()
    print('Started game. Waiting for a connection')
    
    count = 0
    while True:
        # wait until connection is accepted
        conn, addr = s.accept()
        print(f'Connected to: {addr}')
        count += 1

        # start player
        start_new_thread(threaded_client, (conn, count, game))


if __name__ == '__main__':
    main()
