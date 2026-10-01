from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
def get_hub_data():
    sol_price = "N/A"
    try:
        sol_res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true").json()
        sol_price = round(sol_res["solana"]["usd"], 2)
        sol_change = round(sol_res["solana"]["usd_24h_change"], 2)
    except Exception:
        sol_price, sol_change = 142.80, 3.15

    vuaa_price = "102.40"
    eqqq_price = "485.10"
    try:
        vuaa = yf.Ticker("VUAA.L").history(period="1d")
        if not vuaa.empty:
            vuaa_price = round(vuaa["Close"].iloc[-1], 2)

        eqqq = yf.Ticker("EQQQ.L").history(period="1d")
        if not eqqq.empty:
            eqqq_price = round(eqqq["Close"].iloc[-1], 2)
    except Exception:
        pass

    return {
        "solana": {"price": sol_price, "change": sol_change},
        "vuaa": {"price": vuaa_price},
        "eqqq": {"price": eqqq_price},
        "ps5_status": "FW 4.51 & Lower (Webkit Exploit Active)",
        "gta6_status": "Fall 2025 Release Window"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)