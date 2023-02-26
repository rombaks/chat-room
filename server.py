import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

clients_list = {}


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


def register_username(client: socket.socket) -> str:
    while True:
        username = client.recv(1024).decode("utf-8")

        if username in clients_list.values():
            new_name_message = "Sorry, name is already taken.\nPlease, put new name:"
            client.send(new_name_message.encode("utf-8"))
        else:
            clients_list[client] = username
            break

    return username


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print("[SERVER_STARTED]")

    while True:
        client, _ = server.accept()
        username = register_username(client)
        start_new_client_thread(client)
