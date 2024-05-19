import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()

    print("Connection from: ", addr)

    data = conn.recv(1024).decode("utf-8")
    print("Received: ", data)

    path = data.split()[1]
    if path == "/":
        server_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
    
    else:
        server_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")



if __name__ == "__main__":
    main()
