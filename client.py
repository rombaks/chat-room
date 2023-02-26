import socket
import threading

DISCONNECT_MESSAGE = "!bb"


def send_message(client: socket.socket) -> None:
    while True:
        try:
            message = input().strip()
            if message == DISCONNECT_MESSAGE:
                disconnect_client(client)
                break
            if message:
                client.send(message.encode("utf-8"))

        except socket.error as e:
            print("[LOSE_CONNECTION_SEND]")
            disconnect_client(client)
            break
        except Exception as e:
            print("[ERROR_DURING_SEND] :", e)
            break


def recieve_message(client: socket.socket) -> None:
    while True:
        try:
            data = client.recv(1024)
            if len(data) == 0:
                print(f"\nINFO: Server was shutdown")
                disconnect_client(client)
                break
            message = data.decode("utf-8")

            if message:
                print(message)

        except socket.error as e:
            print("[LOSE_CONNECTION_RECV]")
            disconnect_client(client)
            break
        except Exception as e:
            print("[ERROR_DURING_RECV] :", e)
            break


def disconnect_client(client: socket.socket) -> None:
    client.close()
    print("\n-= See you later! =-")


def start_send_recieve_threads(client: socket.socket) -> None:
    t1 = threading.Thread(target=send_message, args=(client,))
    t1.start()

    t2 = threading.Thread(target=recieve_message, args=(client,))
    t2.daemon = True
    t2.start()


def print_greeting(name: str) -> None:
    print(f"-= {name}, welcome to the chat room! =-\n")
    print(f"HINT: send {DISCONNECT_MESSAGE} to leave chat.\n")


def register_username(client: socket.socket) -> None:
    name = input("HELLO! Put your name here: ")
    print_greeting(name)
    client.send(name.encode("utf-8"))


def run_client(host: str, port: str) -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        register_username(client=client)
        start_send_recieve_threads(client=client)

    except Exception as e:
        print(f"\nOh, no!\nFail to connect to {HOST}:{PORT}\n{e}\nSee you later!")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    run_client(host=HOST, port=PORT)
