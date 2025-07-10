import socket
import threading

def receive_messages(client_socket):
    """
    Receives and displays messages from the server.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Server: {message}")
            else:
                break
        except:
            print("An error occurred!")
            break

def client_program():
    """
    Connects to the server and sends messages.
    """
    host = input("Enter server address (e.g., localhost): ")
    port = 5000

    client_socket = socket.socket()
    
    try:
        client_socket.connect((host, port))

        # Set username
        username = input("Enter your username: ")
        client_socket.send(username.encode())

        # Start a thread to handle incoming messages
        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.start()

        while True:
            message = input("")  # User input
            if message.lower() == 'exit':
                print("You have left the chat.")
                client_socket.send("exit".encode())
                break
            client_socket.send(message.encode())  # Send message to server
        
    except Exception as e:
        print(f"Unable to connect to the server: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    client_program()
