import logging
import socket
import threading
from typing import Optional

HOST = "127.0.0.1"
PORT = 12345
DISCONNECT_MESSAGE = "!bb"


clients_list = {}

logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


def print_starting_info():
    print("[SERVER_STARTED]")
    logging.info("[SERVER_STARTED]")
    print("HINT: press 'Ctrl + C' to shutdown.")


def send_join_info(name: str) -> None:
    join_message = f"{name} joined CHAT"
    print(f"[USER_CONNECT]: {join_message}")
    print(f"[ACTIVE_CLIENTS]: {len(clients_list)}")
    sendall_except_user(name, join_message)


def send_chat_message(name: str, text: str, address: str) -> None:
    chat_message = f"{name}: {text}"
    logging.info(f"{address}::: {chat_message}")
    sendall_except_user(name, chat_message)


def send_disconnect_message(name: str) -> None:
    disconnect_message = f"{name} leave CHAT"
    print(f"[USER_DISCONNECT]: {disconnect_message}")
    sendall_except_user(name, disconnect_message)


def sendall_except_user(name: str, message: str) -> None:
    error_clients = []

    for client in clients_list:
        if clients_list[client] != name:
            try:
                client.send(message.encode("utf-8"))
            except socket.error:
                error_clients.append(client)

    clean_clients_list(error_clients=error_clients)


def clean_clients_list(error_clients: list[Optional[socket.socket]]) -> None:
    for client in error_clients:
        remove_from_clients_list(client=client)


def remove_from_clients_list(client: socket.socket) -> None:
    clients_list.pop(client)
    print(f"[ACTIVE_CLIENTS]: {len(clients_list)}")


def disconnect_client(client: socket.socket) -> None:
    username = clients_list.get(client)
    send_disconnect_message(username)
    remove_from_clients_list(client=client)


def new_client(client: socket.socket, username: str) -> None:
    address = client.getpeername()
    send_join_info(username)

    with client:
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
            except socket.error:
                disconnect_client(client=client)
                break

            if message == DISCONNECT_MESSAGE:
                disconnect_client(client=client)
                break
            elif message:
                send_chat_message(username, message, address)


def start_new_client_thread(client: socket.socket, username: str) -> None:
    thread = threading.Thread(target=new_client, args=(client, username))
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


def shutdown_server(server: socket.socket) -> None:
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    print("[SERVER_SHUTDOWN]")
    logging.info("[SERVER_SHUTDOWN]")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print_starting_info()

        while True:
            try:
                client, _ = server.accept()
                username = register_username(client)
                start_new_client_thread(client, username)
            except KeyboardInterrupt:
                shutdown_server(server=server)
                break
            
    except Exception as e:
        print(f"Oh, no!\n\nServer failed on {HOST}:{PORT}\n{e}\nSee you later!")
