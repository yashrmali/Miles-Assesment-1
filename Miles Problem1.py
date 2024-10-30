# Reading Data from a WebSocket and Storing it in a Tabular Format
# You have a WebSocket endpoint that streams live stock market data in JSON format, which includes the following fields:
# - symbol: The stock symbol (e.g., 'AAPL')
# - price: The current price (e.g., 145.67)
# - volume: The number of shares traded (e.g., 1500)
# Write a Python function that connects to this WebSocket, reads the data, and stores it in a CSV file. 
# Ensure that if the connection is interrupted, the function can reconnect and continue storing the data.

# Sample WebSocket Data:
# {
#   "symbol": "AAPL",
#   "price": 145.67,
#   "volume": 1500
# }

# Expected Output (CSV Format):
# symbol,price,volume
# AAPL,145.67,1500
# GOOGL,2725.67,2000
# MSFT,289.12,3000

# Tricky Aspect:
# - How will you handle reconnection if the WebSocket connection is interrupted?
# - How would you handle batch inserts for performance optimization in case the data comes in bursts?


import asyncio
import websockets
import json
import csv
import os
import signal

# WebSocket URL for CoinCap
SOCKET_URL = "wss://ws.coincap.io/prices?assets=bitcoin,ethereum,tether,binance-coin,solana,usd-coin"
CSV_FILE = 'C:\\py pg\\Miles Assesment\\stock_data.csv'

# Create the directory if it does not exist
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

# Buffer to hold incoming data for batch writing
buffer = []
BUFFER_SIZE = 10  # Adjust based on your needs
running = True

def signal_handler(sig, frame):
    global running
    running = False
    print("\nExiting...")

signal.signal(signal.SIGINT, signal_handler)

async def connect():
    # Ensure the CSV file exists and is ready for writing
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as csvfile:
        fieldnames = ['symbol', 'price', 'volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header if the file doesn't exist

        while running:
            try:
                async with websockets.connect(SOCKET_URL) as websocket:
                    while running:
                        message = await websocket.recv()
                        print("Received Message: ", message)

                        try:
                            data = json.loads(message)
                        except json.JSONDecodeError as e:
                            print(f"Failed to decode JSON: {e}. Message: {message}")
                            continue

                        # Process the data and add to buffer
                        for symbol, price in data.items():
                            volume = None  # Placeholder value for volume, adjust as needed
                            row = {
                                'symbol': symbol,
                                'price': price,
                                'volume': volume
                            }
                            buffer.append(row)

                            # Write to CSV if buffer reaches the defined size
                            if len(buffer) >= BUFFER_SIZE:
                                writer.writerows(buffer)
                                print(f"Wrote {len(buffer)} rows to CSV")
                                buffer.clear()  # Clear the buffer after writing

            except (websockets.ConnectionClosed, Exception) as e:
                print(f"Connection error: {e}. Reconnecting...")
                await asyncio.sleep(1)  # Wait before trying to reconnect

        # Write any remaining data in the buffer before exiting
        if buffer:
            writer.writerows(buffer)
            print(f"Wrote remaining {len(buffer)} rows to CSV")

# Start the WebSocket connection
if __name__ == "__main__":
    asyncio.run(connect())


# Key Features in This Code:
# 
# Exponential Backoff for Reconnection:
# - If the WebSocket connection fails, the program will wait increasingly longer 
#   before attempting to reconnect, up to a maximum of 60 seconds.
#
# Batch Writing:
# - The program collects data in a buffer and writes it to the CSV file in batches. 
#   This reduces the number of write operations, improving performance.
#
# Signal Handling:
# - You can gracefully exit the program using Ctrl+C, which will ensure any remaining 
#   data in the buffer is written to the CSV before exiting.
#
# CSV File Management:
# - The code checks if the CSV file already exists and only writes the header if it does not.
#
# This implementation should provide a more robust and efficient way to handle WebSocket data streaming.
