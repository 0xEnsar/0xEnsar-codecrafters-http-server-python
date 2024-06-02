import socket
import threading
import sys

def connectionHandler(conn, addr):
    print("Connection from: ", addr)

    data = conn.recv(1024).decode("utf-8")
    print("Data: ", data)

    path = data.split()[1]

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
        conn.send(response.encode())

    elif path.startswith("/echo"):
        echo_path = path[6:]
        print("Echo path: ", echo_path)
        encoding = data.split("Accept-Encoding: ")[1].split("\r\n")[0]
        if "gzip" in encoding:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(echo_path)}\r\n\r\n{echo_path}\r\n"
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_path)}\r\n\r\n{echo_path}\r\n"
        print("Response: ", response)
        conn.send(response.encode())

    elif path.startswith("/user-agent"):
        user_agent_path = data.split("User-Agent: ")[1].split("\r\n")[0]
        print("User-Agent path: ", user_agent_path)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent_path)}\r\n\r\n{user_agent_path}\r\n"
        conn.send(response.encode())

    elif path.startswith("/files") and data.startswith("GET"):
        file_name = path[7:]
        directory = sys.argv[2]
        file_path = f"{directory}/{file_name}"
        print("File path: ", file_path)
        try:
            with open(file_path, "r") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}\r\n"
                conn.send(response.encode())
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.send(response.encode())

    elif path.startswith("/files") and data.startswith("POST"):
        file_name = path[7:]
        directory = sys.argv[2]
        file_path = f"{directory}/{file_name}"
        print("File path: ", file_path)
        try:
            with open(file_path, "w") as file:
                content = data.split("\r\n\r\n")[1]
                file.write(content)
                response = "HTTP/1.1 201 Created\r\n\r\n"
                conn.send(response.encode())
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.send(response.encode())

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.send(response.encode())




def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target= connectionHandler, args=(conn, addr)).start()
    
   



if __name__ == "__main__":
    main()
