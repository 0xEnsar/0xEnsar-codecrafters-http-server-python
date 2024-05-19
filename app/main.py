import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()

    print("Connection from: ", addr)

    data = conn.recv(1024).decode("utf-8")
    print("Received: ", data)



if __name__ == "__main__":
    main()
