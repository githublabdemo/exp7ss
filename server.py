import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

clients = []

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    clients.append(conn)
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from {addr}: {data}")
            for client in clients:
                if client != conn:
                    client.sendall(data.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            clients.remove(conn)
            break

    conn.close()

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
