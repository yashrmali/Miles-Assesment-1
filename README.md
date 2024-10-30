# Miles-Assesment-1
# 📈 Reading Data from a WebSocket and Storing it in a Tabular Format

## Overview
This project involves connecting to a WebSocket endpoint that streams live stock market data in JSON format. The goal is to read the data and store it in a CSV file. If the connection is interrupted, the function should be able to reconnect and continue saving the data. 

## WebSocket Data Structure
The incoming data will be in the following format:
```json
{
  "symbol": "AAPL",
  "price": 145.67,
  "volume": 1500
}
```

### Fields:
- **symbol**: The stock symbol (e.g., 'AAPL')
- **price**: The current price (e.g., 145.67)
- **volume**: The number of shares traded (e.g., 1500)

## Expected Output (CSV Format)
The data will be stored in a CSV format like this:
```
symbol,price,volume
AAPL,145.67,1500
GOOGL,2725.67,2000
MSFT,289.12,3000
```

## 🛠️ Implementation

### Requirements
- Python 3.x
- `websocket-client` library
- `pandas` library for CSV handling


## 🔍 Key Considerations
- **Reconnection Handling**: The code attempts to reconnect if the WebSocket connection is closed.
- **Batch Inserts**: Data is buffered and written to CSV in batches for performance optimization.

## 🚀 Getting Started
1. Install the required libraries:
   ```bash
   pip install websocket-client pandas
   ```
2. Replace `"wss://your.websocket.endpoint"` with the actual WebSocket URL.
3. Run the script and monitor the generated `stock_data.csv` file.


 Happy coding! 🎉
