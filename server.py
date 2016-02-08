import socket
import sys
import pickle
from script import alpha_shape

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8080)

sock.bind(server_address)

sock.listen(1)

while True:
    conn, client_addr = sock.accept()

    try:
        data = conn.recv(2**16)

        if data:
            data = pickle.loads(data)
            c,e = alpha_shape(data, 0.4)

            res = [list(c.boundary.coords.xy[0]), list(c.boundary.coords.xy[1])]
            conn.sendall(pickle.dumps(res))
    finally:
        conn.close()
