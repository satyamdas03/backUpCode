from yahooquery import Screener 
import yfinance as yf
import pandas as pd
import time

def fetch_top_10_most_active_stocks():
    try:
        s = Screener()
        screen = s.get_screeners('most_actives', count=10)
        top_10_stocks = screen['most_actives']['quotes']  # type: ignore
        
        top_10_tickers = [stock['symbol'] for stock in top_10_stocks]  # type: ignore

        stocks_data = {}
        stocks_output = "Top 10 Most Active Stocks:\n"
        for ticker in top_10_tickers:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period="1d")
                stocks_data[ticker] = stock_info
                stocks_output += f"\n--- {ticker} ---\n{stock_info}\n"
                time.sleep(1)  # Add a delay to avoid rate limit
            except Exception as e:
                stocks_output += f"Error fetching data for {ticker}: {e}\n"

        return stocks_output  # Return the formatted string

    except Exception as e:
        return f"Error fetching top 10 stocks data: {e}"

if __name__ == "__main__":
    result = fetch_top_10_most_active_stocks()
    print(result)
