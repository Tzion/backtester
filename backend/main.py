from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
from fastapi import HTTPException
from datetime import datetime, timezone

from charts import TRADES_DIR, OBSERVERS_DIR, CHARTS_DIR

app = FastAPI()

# CORS to allow Vue frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/trades")
def list_trades():
    """List all trade files with metadata"""
    trades = []
    for filename in os.listdir(TRADES_DIR):
        filepath = os.path.join(TRADES_DIR, filename)
        trades.append({"filename": filename, "path": filepath, "size": os.path.getsize(filepath), "created": os.path.getctime(filepath)})
    return trades


@app.get("/trades/{trade_name}")
def get_trade_details(trade_name: str):
    """Fetch details of a specific trade"""
    filepath = os.path.join(TRADES_DIR, trade_name)
    if not os.path.exists(filepath):
        return {"error": "Trade not found"}

    with open(filepath, 'r') as f:
        content = f.read()

    return {"filename": trade_name, "content": content}


@app.get("/observers")
def list_observer_charts():
    """List all observer chart files"""
    charts = []
    for filename in os.listdir(OBSERVERS_DIR):
        filepath = os.path.join(OBSERVERS_DIR, filename)
        charts.append({
            "filename": filename,
            "path": filepath,
            "type": "html"  # Assuming HTML charts
        })
    return charts


@app.get("/observers/{chart_name}")
def get_observer_chart(chart_name: str):
    """Serve a specific observer chart"""
    filepath = os.path.join(OBSERVERS_DIR, chart_name)
    if not os.path.exists(filepath):
        return {"error": "Chart not found"}

    return FileResponse(filepath)


@app.get("/ohlcv")
def get_ohlcv_data(symbol: str, interval: str, since: int = None, to: int = None):
    """
    Fetch OHLCV data for a specific symbol and interval
    
    :param symbol: Stock symbol (e.g., 'SPY')
    :param interval: Time interval (e.g., '1m')
    :param since: Unix timestamp for start of data (optional)
    :param to: Unix timestamp for end of data (optional)
    :return: Filtered OHLCV data
    """
    # Construct filename
    filename = f"{symbol}-{interval}-5days.csv"
    filepath = os.path.join('data_feeds', filename)

    # Check if file exists
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"No data found for {symbol} with {interval} interval")

    # Read CSV file
    try:
        df = pd.read_csv(filepath, parse_dates=['time'])

        # Convert time column to Unix timestamp
        df['timestamp'] = df['time'].apply(lambda x: int(x.timestamp()))

        # Filter by since and to timestamps if provided
        if since is not None:
            df = df[df['timestamp'] >= since]

        if to is not None:
            df = df[df['timestamp'] <= to]

        # Convert to list of dictionaries for JSON serialization
        data = df.to_dict('records')

        return {"symbol": symbol, "interval": interval, "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}") from e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
