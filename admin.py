from network import Network
import argparse
import os


ADMIN_KEY = 'kYeVsv1o2qfuBUP508rl'


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def main():
    # argparse
    parser = argparse.ArgumentParser(description='Change parameters for the game')
    parser.add_argument('-ip', '--server_ip', metavar='', type=str, required=True, help='IP address of server')
    parser.add_argument('-port', '--port_no', metavar='', type=int, default=5555, help='Port number from the server')
    parser.add_argument('-lobby', '--lobby_id', metavar='', type=str, default='', help='Lobby ID for the server')

    args = parser.parse_args()

    SERVER_IP = args.server_ip
    PORT_NO = args.port_no
    LOBBY_ID = args.lobby_id

    n = Network(SERVER_IP, port_no=PORT_NO, lobby_id=LOBBY_ID, name=ADMIN_KEY)

    clear_console()

    while True:
        cmd = input()
        n.send(cmd)
        if cmd == 'shutdown':
            break


if __name__ == '__main__':
    main()
