import socket
from _thread import *
import pickle
from blackjack import *


def threaded_client(conn, in_game_id, game, buff_size=8192):
    """Client thread. Spawns when new client is added

    Args:
        conn (Socket): communication channel
        in_game_id (int): player ID
        game (BlackjackTable): shared game
        buff_size (int, optional): buffer size to be sent. Defaults to 8192.
    """
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
    server = '192.168.1.108'
    port = 5555

    # create server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        print(e)

    s.listen(5)
    print('Server started')
    
    game = BlackjackTable()
    print('Started game. Waiting for a connection')
    
    count = 0
    while True:
        # wait until connection is accepted
        conn, addr = s.accept()
        print(f'Connected to: {addr}')

        # add player to the game
        new_player = Player(f'Player {count}')
        count += 1
        err_code, in_game_id = game.join(new_player)

        # start player
        if err_code == 0:
            start_new_thread(threaded_client, (conn, in_game_id, game))
        else:
            print('Lobby is too full')


if __name__ == '__main__':
    main()
