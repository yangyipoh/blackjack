import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.bind((local_ip, 0))
ip, port = so.getsockname()

print(f'IP: {ip}, port: {port}')

so.close()
