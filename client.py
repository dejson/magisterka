import socket
import sys
import pickle


def send_via_net(message, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (host, port)
    sock.connect(server_address)

    try:
        message = pickle.dumps(message)
        sock.sendall(message)

        data = sock.recv(2**16)

        return pickle.loads(data)
    finally:
        sock.close()
