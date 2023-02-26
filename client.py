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
HOST = "127.0.0.1"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello server")
    data = s.recv(1024)

print(f"Received {data}")