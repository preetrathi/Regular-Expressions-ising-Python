import socket

def start_client(host='127.0.0.1', port=65432):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    while True:
        symbol = input("Enter stock symbol (or 'exit' to quit): ")
        if symbol.lower() == 'exit':
            break
        client.send(symbol.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        print(response)

    client.close()

if __name__ == "__main__":
    start_client()
