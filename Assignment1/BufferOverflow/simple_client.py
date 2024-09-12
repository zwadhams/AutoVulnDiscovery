import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"What's the lab's address?", ("127.0.0.1", 8080))
# Receive response from server
data, addr = sock.recvfrom(1024)
print("Server says: ", data.decode(errors='replace'))
sock.close()
