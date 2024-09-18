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

        for ticker in top_10_tickers:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period="1d")
                stocks_data[ticker] = stock_info
                time.sleep(1)  # Add a delay to avoid hitting rate limits
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")

        return stocks_data  # Return the data

    except Exception as e:
        print(f"Error fetching top 10 stocks data: {e}")
        return {}


# if __name__ == "__main__":
#     fetch_top_10_most_active_stocks()
