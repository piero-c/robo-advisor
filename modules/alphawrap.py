# This is a wrapper module for the AlphaVantage API. It requests data, and returns it in a more digestible format (e.g csv)
#   Dependencies: pandas, requests, io, relativedelta
#   Created by: Piero C

import pandas as pd
import requests as r
import io
from dateutil.relativedelta import relativedelta

# Allows user to set a global key so that they don't have to pass it to each function
#  Should be called before any functions
def set_global_key(key):
    global GLOBAL_KEY
    GLOBAL_KEY = key

# STOCK OBJECT
#  Provides functions for accessing day-by-day and month-by-month historical data for any given stock ticker,
#   as well as company overview
class Stock:
    def __init__(self, ticker = None, key = None):
        self.ticker = ticker
        if key:
            self.key = key
        elif (key is None) and (GLOBAL_KEY is not None):
            self.key = GLOBAL_KEY
        else:
            print("Warning: no global key has been set and no key has been passed to the Stock object")

    # Time-series information for stock ("Raw (as-traded) daily open/high/low/close/volume values, daily adjusted close values,
    #  and historical split/dividend events")
    #   Returntype: Pandas DataFrame / None
    def history(self, start = None, end = None, interval = '1d'):
        match interval:
            # Day-by-day
            case '1d':
                # Request data from AlphaVantage
                try:
                    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&datatype=csv&outputsize=full&apikey={self.key}'
                    data = r.get(url)
                    data = data.content
                except:
                    print(f"Stock.history: {self.ticker}: Invalid ticker or key / AlphaVantage may be down / No internet")
                    raise 

                # Decode, convert to DataFrame, set index
                try:
                    day_df = pd.read_csv(io.StringIO(data.decode('utf-8')))
                    day_df.index = day_df.iloc[:, 0].values.tolist()
                    day_df.drop(columns = day_df.columns[0], inplace = True)
                except:
                    print(f"Stock.history: {self.ticker}: Something went wrong decoding the request. Ticker may be invalid")
                    raise

                # Drop non-adjusted close, capitalize and normalize columns
                try:
                    day_df.drop(columns = "close", inplace = True)
                    day_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Splits']
                except:
                    print(f"Stock.history: {self.ticker}: Stock history data structure is incorrect. Key may be invalid")
                    raise

                # Add a day to end date (to include it in final DataFrame), ensure proper formatting of end and start
                try:
                    end = str((pd.to_datetime(end) + relativedelta(days = 1)).strftime("%Y-%m-%d"))
                    start = str((pd.to_datetime(start)).strftime("%Y-%m-%d"))
                except:
                    print(f"Stock.history: {self.ticker}: Invalid format for start / end date")
                    raise

                x = 0

                # Grab DataFrame slice for start and end date
                while True:
                    x += 1

                    # Too many iterations, something went wrong
                    if x > 10:
                        print(f"Stock.history: {self.ticker}: Something went wrong. Dates may be incorrect or out of range")
                        raise
                    
                    # Try getting the DataFrame slice, adjust dates if necessary (e.g weekends need to be converted to weekdays)
                    # Flip rows so that DataFrame is in order
                    try:
                        day_df.loc[start]
                        try:
                            day_df.loc[end]
                            return day_df.loc[start:end:-1,:]
                        except:
                            # Subtract one day from end
                            end = str((pd.to_datetime(end) - relativedelta(days = 1)).strftime("%Y-%m-%d"))
                    except:
                        # Add one day to start
                        start = str((pd.to_datetime(start) + relativedelta(days = 1)).strftime("%Y-%m-%d"))

            # Month-by-month
            case '1mo':
                # Request data from AlphaVantage
                try:
                    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={self.ticker}&datatype=csv&outputsize=full&apikey={self.key}'
                    data = r.get(url)
                    data = data.content
                except:
                    print(f"Stock.history: {self.ticker}: Invalid ticker or key / AlphaVantage may be down / No internet")
                    raise

                # Decode, convert to DataFrame, set index
                try:
                    month_df = pd.read_csv(io.StringIO(data.decode('utf-8')))
                    month_df.index = month_df.iloc[:, 0].values.tolist()
                    month_df.drop(columns = month_df.columns[0], inplace = True)
                except:
                    print(f"Stock.history: {self.ticker}: Something went wrong decoding the request. Ticker may be invalid")
                    raise

                # Ensure proper formatting of end and start for DataFrame filtering
                try:
                    start = str((pd.to_datetime(start)).strftime("%Y-%m"))
                    end = str((pd.to_datetime(end)).strftime("%Y-%m"))
                except:
                    print(f"Stock.history: {self.ticker}: Invalid format for start / end date")
                    raise

                # Grab proper dates for DataFrame row indexing (month-end dates)
                try:
                    start = month_df.filter(like = start, axis = 0).index[0]
                    end = month_df.filter(like = end, axis = 0).index[0]
                except:
                    print(f"Stock.history: {self.ticker}: There is no stock history for the dates specified. Invalid ticker or key / dates out of range")
                    raise

                # Drop non-adjusted close, capitalize and normalize columns (monthly does not have info for splits)
                try:
                    month_df.drop(columns = "close", inplace = True)
                    month_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends']
                except:
                    print(f"Stock.history: {self.ticker}: Stock history data structure is incorrect. Key may be invalid")
                    raise

                # Grab DataFrame slice for start and end date
                # Flip rows so that DataFrame is in order
                try:
                    return month_df.loc[start:end:-1,:]
                except:
                    print(f"Stock.history: {self.ticker}: Something went wrong, dates may be incorrect or out of range")
                    raise
                
    # Company overview ("Company information, financial ratios, and other key metrics")
    #  Returntype: JSON / None
    def info(self):
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={self.key}'
            data = r.get(url)
            data = data.json()
        except:
            print(f"Stock.info: {self.ticker}: Invalid ticker or key / AlphaVantage may be down / No internet")
            raise
        
        return data
    
# Current risk-free (5-year American Bond) rate
#   Returntype: float / None
def rf(key = None):
    if key is None:
        key = GLOBAL_KEY

    try:
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=5year&apikey={key}'
        data = r.get(url)
        data = data.json()
        return float(data['data'][0]['value']) / 100
    except:
        print(f"rf: Invalid key / AlphaVantage may be down / No internet")
        raise

    
# Testing purposes:
if __name__ == "__main__":
    pass