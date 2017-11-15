import pandas as pd
import io
import requests
import time
import csv
from urllib.request import urlopen
 
def google_stocks(symbol, startdate, enddate = None):
 
    startdate = str(startdate[0]) + '+' + str(startdate[1]) + '+' + str(startdate[2])
    
    if not enddate:
        enddate = time.strftime("%m+%d+%Y")
    else:
        enddate = str(enddate[0]) + '+' + str(enddate[1]) + '+' + str(enddate[2])
    
    stock_url = "https://finance.google.com/finance/historical?q=" + symbol + \
                "&startdate=" + startdate + "&enddate=" + enddate + "&output=csv"

    raw_response = requests.get(stock_url).content
    
    stock_data = pd.read_csv(io.StringIO(raw_response.decode('utf-8')))
    return stock_data

if __name__ == '__main__':
    with open("Tickers_test.txt", 'r', encoding='utf-8') as tickers:
        for ticker in tickers:
            ticker = ticker.rstrip('\n')
               
            stock_data = []
            stock_detail = google_stocks(symbol = ticker, startdate = (11, 1, 2017))    

            for i in stock_detail.values:
                stock_data = stock_data + [(ticker, i[0], i[1], i[2], i[3], i[4], i[5])]    # Ticker, Date, Open, High, Low, Close, Volume
        
            with open("StockPrice_History_" + ticker + ".csv", 'w') as outfile:
                writer = csv.writer(outfile, delimiter=',')
                writer.writerows(stock_data)

            outfile.close()

    tickers.close()