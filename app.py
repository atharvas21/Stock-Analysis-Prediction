import streamlit as st
import pandas as pd
import numpy as np
import requests
import tweepy
import psycopg2
from tweepy import api
#import config
import psycopg2
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import csv
import datetime 
import cufflinks as cf
import plotly.offline
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
import time

import os
from IPython.display import clear_output
import smtplib
from yahoo_fin import stock_info as si
import plotly.graph_objects as go
from plotly.offline import plot
primaryColor="#6eb52f"
backgroundColor="#f0f0f5"
secondaryBackgroundColor="#e0e0ef"
textColor="#262730"
font="sans serif"



def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']




#connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
#cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

ticker_lst = []

st.title('Equitopedia')

st.sidebar.title('Options')

ticker = st.sidebar.text_input("Enter Ticker",value="AAPL")
ticker_lst.append(ticker)

ticker = st.sidebar.selectbox("Watchlist", ticker_lst)


option = st.sidebar.selectbox("Select Dashboard", ('Live Market Price','Company Info','Financials','Quarterly Analysis','Prediction'))



st.header(option)

if option =='Twitter':
    st.subheader('Twitter Dashboard')

    tweets =api.user_timeline('traderstewie')

    for tweet in tweets:
        if '$' in tweet.text:
            words = tweet.text.split(' ')
            for word in words:
                if word.startswith('$') and word[1:].isalpha():
                    symbol = word[1:]
                    st.write(symbol)
                    st.write(tweet.text)
                    st.image(f'https://finviz.com/quote.ashx?t={ticker}')

if option =='Financials':
    st.subheader("Dividend:")
    st.text(pd.DataFrame(yf.Ticker(ticker).dividends))
    st.subheader("Balance Sheet Of the Company")
    st.text(yf.Ticker(ticker).balance_sheet)
    st.subheader("Cash Flow:")
    st.text(yf.Ticker(ticker).cashflow)
    st.subheader("Financials:")
    st.text(yf.Ticker(ticker).financials)
    
    #st.subheader("Major Shareholders:")
    #st.text(yf.Ticker(ticker).major_holders())

        
if option =='Quarterly Analysis':
    st.subheader("Balancesheet:")
    st.text(yf.Ticker(ticker).quarterly_balance_sheet)
    st.subheader("Cashflow")
    st.text(yf.Ticker(ticker).quarterly_cashflow)
    st.subheader("Financials:")
    st.text(yf.Ticker(ticker).quarterly_financials)

if option == 'Live Market Price':
    now = datetime.datetime.now()
    time1 = now.strftime("%H:%M:%S")
    tickers = yf.Ticker(ticker)
    todays_data = tickers.history(period='1d')
    
    
    time.sleep(2)
    company= get_symbol(ticker)
    st.subheader(company)
    st.text(ticker)
    st.subheader("Current:")
    st.text(todays_data['Close'][0])
    
    df= yf.Ticker(ticker).info['open']
    st.subheader("Opening price: ")
    st.text(df)

    df= yf.Ticker(ticker).info['previousClose']
    st.subheader("Previous Close: ")
    st.text(df)

    st.subheader("52 Weeks High")
    st.text(yf.Ticker(ticker).info['fiftyTwoWeekHigh'])
    st.subheader("52 Weeks Low")
    st.text(yf.Ticker(ticker).info['fiftyTwoWeekLow'])
    tickers = yf.Ticker(ticker)
    todays_data = tickers.history(period='1y')
    year_old_price = todays_data['Close'][0]
    current = si.get_live_price(ticker)
    st.text("52 week change: {:.2f} %".format(((current - year_old_price)*100)/year_old_price))
    
    
    
    START = "2015-01-01"
    TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
    
   
    
    
    selected_stock = ticker
    
    
    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data
    
    	
    
    data = load_data(selected_stock)
  
    
    st.subheader('Intraday Data')
    st.write(data.tail())
    
    # Plot raw data
    def plot_raw_data():
    	fig = go.Figure()
    	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    	fig.layout.update(title_text='Opening & Closing Price Chart', xaxis_rangeslider_visible=True)
    	st.plotly_chart(fig)
    	
    plot_raw_data()
    








if option == 'Company Info':
    company= get_symbol(ticker)
    st.subheader(company)
#    st.text("Average Revenue(in ₹):")
#    st.text(yf.Ticker(ticker).calendar.loc['Revenue Average'][0])
#    st.text("Dated-")
#    st.text(yf.Ticker(ticker).calendar.loc['Earnings Date'][0])
#    st.text("Social Score:")
#    st.text(str(yf.Ticker(ticker).sustainability.loc['socialScore']))
#    st.text("Environment Score:")
#    st.text(yf.Ticker(ticker).sustainability.loc['environmentScore'])
    st.subheader("Splits offered by the company:")
    st.text(pd.DataFrame(yf.Ticker(ticker).splits))
    st.subheader("Shareholders:")
    st.text(yf.Ticker(ticker).get_institutional_holders().head().drop('Date Reported',axis=1))
    

    
    

    


if option == 'Stocktwits':
    
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])
        
if option =='Prediction':
    st.subheader('Prediction Dashboard')
    company= get_symbol(ticker)
    st.subheader(company)
    
    
    START = "2015-01-01"
    TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
    
   
    
    
    selected_stock = ticker
    
    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365
    
    
    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data
    
    	
    
    data = load_data(selected_stock)
    
    
    
    
    # Plot raw data
   
    
    # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    
    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
    
    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)