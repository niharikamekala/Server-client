import socket
import threading

clients = []
usernames = {}

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                username = usernames[client_socket]
                broadcast(f"{username}: {message.decode()}".encode(), client_socket)
            else:
                remove(client_socket)
                break
        except:
            continue

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        username = usernames.pop(client_socket)
        broadcast(f"{username} has left the chat.".encode(), client_socket)

def server_program():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print("Server is listening...")
    
    while True:
        client_socket, address = server_socket.accept()
        print("Connection from: {address}")
        
        client_socket.send("Enter your username: ".encode())
        username = client_socket.recv(1024).decode()
        usernames[client_socket] = username
        clients.append(client_socket)
        
        print(f"Username '{username}' has joined the chat.")
        broadcast(f"{username} has joined the chat.".encode(), client_socket)
        
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == '__main__':
    server_program()
