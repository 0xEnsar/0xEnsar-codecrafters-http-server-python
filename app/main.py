import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()

    print("Connection from: ", addr)



if __name__ == "__main__":
    main()
