import socket
import threading

HOST = "127.0.0.1"
PORT = 12345


def new_client(client: socket.socket) -> None:
    with client:
        while True:
            data = client.recv(1024)
            if not data:
                break
            print(f"Received {data}")
            client.sendall(b"Hello client")


def start_new_client_thread(client: socket.socket) -> None:
    thread = threading.Thread(target=new_client, args=(client,))
    thread.daemon = True
    thread.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    while True:
        client, _ = server.accept()
        start_new_client_thread(client)
