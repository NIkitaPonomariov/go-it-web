import socket

def main():
    host = socket.gethostname()
    port = 5000

    server = socket.socket()
    server.bind((host,port))
    server.listen()

    conn, adress = server.accept()
    print(f"connect from {adress}")

    while True:
        msg = conn.recv(1024).decode()
        if not msg:
            break
        print(msg)
        message = input(">>> ")
        conn.send(message)
    conn.close()
    server.close()






if __name__ == "__main__":
    main()