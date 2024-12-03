import socket
import threading
import requests
import json

API_KEY = 'AIWGLVREW6F8FIJ0'
API_URL = "https://www.alphavantage.co/query"

# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
def fetch_stock_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',  # You can choose different intervals
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get('Time Series (1min)')
        if time_series:
            latest_time = sorted(time_series.keys())[0]
            latest_data = time_series[latest_time]
            return latest_data['1. open']  # Get the opening price
    return None

def handle_client(client_socket):
    while True:
        symbol = client_socket.recv(1024).decode('utf-8')
        if not symbol:
            break
        price = fetch_stock_price(symbol)
        if price is not None:
            client_socket.send(f"The current price of {symbol} is ${price}\n".encode('utf-8'))
        else:
            client_socket.send(f"Could not fetch price for {symbol}\n".encode('utf-8'))
    client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()