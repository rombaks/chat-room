import socket
import threading


def send_message(client: socket.socket) -> None:
    while True:
        message = input("You: ").strip()
        if message:
            client.send(message.encode("utf-8"))


def recieve_message(client: socket.socket) -> None:
    while True:
        message = client.recv(1024).decode("utf-8")
        print(message)


def start_send_recieve_threads(client: socket.socket) -> None:
    t1 = threading.Thread(target=send_message, args=(client,))
    t1.start()

    t2 = threading.Thread(target=recieve_message, args=(client,))
    t2.start()


def register_username(client: socket.socket) -> None:
    name = input("HELLO! Put your name here: ")
    print(f"-= {name}, welcome to the chat room! =-\n")
    client.send(name.encode("utf-8"))


def run_client(host: str, port: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    register_username(client=client)

    start_send_recieve_threads(client=client)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    run_client(host=HOST, port=PORT)
