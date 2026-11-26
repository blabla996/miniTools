from tavily import TavilyClient
import yfinance as yf
import os
from datetime import datetime, timezone

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(
    query: str,
    max_results: int = 5,
    seen_urls: set[str] = set()
) -> str:
    try:
        response = tavily_client.search(
            query=query,
            search_depth="basic",  
            topic="news",         
            days=3,                
            max_results=max_results,
        )
    except Exception as e:
        return (
            f'<external_search_data query="{query}">\n'
            f"Search error: {e}\n"
            f"</external_search_data>"
        )
    
    results = response.get("results", [])
    
    if not results:
        return (
            f'<external_search_data query="{query}">\n'
            f"No data found\n"
            f"</external_search_data>"
        )
    
    formatted_result = []
    for result in results:
        url = (result.get("url") or "").strip()
        
        if not url or url in seen_urls:
            continue
        
        seen_urls.add(url)
        
        title = (result.get("title") or "No title").strip()
        content = (result.get("content") or "No content").strip()
        published_date = (result.get("published_date") or "No published_date").strip()
        
        formatted_result.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"Published date: {published_date}\n"
            f"URL: {url}\n"
        )
    
    if not formatted_result:
        return (
            f'<external_search_data query="{query}">\n'
            f"No new data found (all URL were seen)\n"
            f"</external_search_data>"
        )
        
    body = "\n\n".join(formatted_result)
    
    return (
        f'<external_search_data query="{query}">\n'
        f"{body}\n"
        f"</external_search_data>"
    )
        

WATCHLIST = {
    # --- Índices EE. UU. ---
    "S&P 500": "^GSPC",
    "NASDAQ Composite": "^IXIC",
    "Dow Jones": "^DJI",
    "Russell 2000 (Small Caps)": "^RUT",

    # --- Índices Europa y Asia ---
    "Euro Stoxx 50": "^STOXX50E",
    "IBEX 35": "^IBEX",
    "DAX (Alemania)": "^GDAXI",
    "FTSE 100 (Reino Unido)": "^FTSE",
    "Nikkei 225 (Japón)": "^N225",
    "Hang Seng (Hong Kong)": "^HSI",

    # --- Renta Fija, Volatilidad y Dólar ---
    "US 10Y Treasury Yield": "^TNX",
    "US 13W T-Bill Yield": "^IRX", # T-Bill 13W (proxy tipos corto plazo en Yahoo)
    "VIX (Volatilidad)": "^VIX",
    "US Dollar Index (DXY)": "DX-Y.NYB",

    # --- ETFs Sectoriales EE. UU. (para detectar rotación de capital) ---
    "Tech Sector (XLK)": "XLK",
    "Financials Sector (XLF)": "XLF",
    "Energy Sector (XLE)": "XLE",
    "Healthcare Sector (XLV)": "XLV",
    "Semiconductors ETF (SOXX)": "SOXX",

    # --- Mega-Caps & Semiconductores ---
    "NVIDIA": "NVDA",
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Tesla": "TSLA",
    "TSMC": "TSM",
    "Broadcom": "AVGO",
    "AMD": "AMD",
    "ASML": "ASML",

    # --- Materias Primas y Cripto ---
    "Gold (Oro)": "GC=F",
    "Silver (Plata)": "SI=F",
    "WTI Crude Oil": "CL=F",
    "Brent Crude Oil": "BZ=F",
    "Copper (Cobre)": "HG=F",
    "Bitcoin USD": "BTC-USD",

    # --- Divisas Principales ---
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "USDJPY=X",
}
     
def search_market_data() -> str:
    tickers = list(WATCHLIST.values())
    
    try:
        data = yf.download(
            tickers=tickers,
            period="5d",
            interval="1d",
            group_by="ticker",
            progress=False,
            threads=True
        )
        
    except Exception as e:
        return f"<yahoo_market_data>\nMarket data error: {e}\n</yahoo_market_data>"
        
    market_data=[]
    
    for name, symbol in WATCHLIST.items():
        try:
            df=data[symbol].dropna(subset=["Close"])
            
            
            if(len(df) < 2):
                continue
            
            prev_close = float(df["Close"].iloc[-2])
            last_close = float(df["Close"].iloc[-1])
            prev_date = df.index[-2].strftime("%Y-%m-%d")
            last_date = df.index[-1].strftime("%Y-%m-%d")
            
          
            if symbol in {"^TNX", "^IRX"}:
                last_close = last_close / 10.0
                prev_close = prev_close / 10.0
                
            pct_change = ((last_close-prev_close)/prev_close) * 100
            
            market_data.append(
                f"{name} {symbol}: {last_close:,.2f} | "
                f"Percentage change: {pct_change:+.2f}% | "
                f"Previos date: {prev_date} | "
                f"Last date: {last_date} | "
                f"URL: https://finance.yahoo.com/quote/{symbol}"
            )
            
        except Exception as e:
            print(f"[WARN] Market data failed for {symbol}: {e}")
            continue
        
    if not market_data:
        return f"<yahoo_market_data>\nNo Market data available\n</yahoo_market_data>"
    
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = "\n\n".join(market_data)
    return (
        f'<yahoo_market_data source="Yahoo Finance (yfinance)" fetched_at="{fetched_at}">\n'
        f"{body}\n"
        f"</yahoo_market_data>"
    )