import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
MESSAGE_LENGTH = 2048
DECODE = 'utf-8'

active_clients = []


def listen_for_messages(client:socket.socket, username:str):
    while 1:
        message = client.recv(MESSAGE_LENGTH).decode(DECODE)
        if message != '':
            final_message = f"{username}~{message}"
            send_message_to_all(final_message)
            print(f"Successfully to send message {final_message} to all client")
        else:
            print("The message from client {username} is empty!")

def send_message_to_client(client:socket.socket, message:str):
    client.sendall(message.encode())

def send_message_to_all(message:str):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client:socket.socket):
    while 1:
        username = client.recv(MESSAGE_LENGTH).decode(DECODE)
        if username != '':
            active_clients.append((username, client))
            message = f"SERVER~User {username} join the chat"
            send_message_to_all(message)
            break
        else:
            print("Client username is empty!")
    
    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    # AF_INET: IPv4 address
    # SOCK_STREAM: TCP protocols
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((HOST, PORT))
        print(f"Server is running on {HOST}:{PORT}")
    except:
        print(f"Unable to connect to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()