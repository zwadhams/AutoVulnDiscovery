import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"Hello, Server!", ("127.0.0.1", 7000))
sock.close()
