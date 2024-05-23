import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()

    print("Connection from: ", addr)

    data = conn.recv(1024).decode("utf-8")
    print("Data: ", data)

    path = data.split()[1]
    print("Path: ", path)
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
        conn.send(response.encode())
    
    elif path.startswith("/echo"):
        echoPath = path[6:]
        print("Echo path: ", echoPath)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echoPath)}\r\n\r\n{echoPath}\r\n"
        conn.send(response.encode())

    elif path.startswith("/user-agent"):


    
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.send(response.encode())



if __name__ == "__main__":
    main()
