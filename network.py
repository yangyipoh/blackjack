import socket
import pickle

class Network:
    def __init__(self, server_ip, port_no=5555, buff_size=8192):
        """Creates a network class to handle network functionality for the client

        Args:
            server_ip (str): ip address of the server
            port_no (int, optional): port number of the server. Defaults to 5555.
            buff_size (int, optional): size of the buffer to be sent. Defaults to 2048.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server_ip, port_no)
        self.buff_size = buff_size
        self.p_id = self.connect()

    def getP(self):
        return self.p_id
    
    def connect(self):
        """Establishes a connection between the client and server. Once connection is enstablished, return the ID of the player

        Returns:
            int: the playerID
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(self.buff_size).decode()
        except:
            pass

    def send(self, data):
        """Send data to the server

        Args:
            data (str): Data to be sent

        Returns:
            BlackjackTable: Response from the server
        """
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(self.buff_size))
        except socket.error as e:
            print(e)
