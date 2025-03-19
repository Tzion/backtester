from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

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
    """
    # Implement data fetching logic based on symbol, interval, since, and to
    # Could read from files, database, or other data sources

    return {"message": "OHLCV data retrieval not implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
