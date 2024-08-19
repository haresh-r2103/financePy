import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import requests
from bs4 import BeautifulSoup

st.title("STOCK DASHBOARD")


#-----SIDEBAR----------
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")


#-----------stock header------------------
url = f'https://finance.yahoo.com/quote/{ticker}/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#header = soup.find(class_="yf-3a2v0c").text
#---LINE CHART---

data = yf.download(ticker,start=start_date,end=end_date)
fig = px.line(data,x=data.index,y=data['Adj Close'],title=ticker)
st.plotly_chart(fig)


#---TABS------
pricing_data,  news = st.tabs(["Pricing Data",  "Top 10 news"])

with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    st.write(data)
    #ANNUAL Return
    annual_return  = data2['% Change'].mean()*252*100
    st.write("Annual Return is ",annual_return,'%')
    #STANDAR DEVIATION (1YEAR EXCLUDING THE WEEKEND)
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is ',stdev*100,'%')
    #RISK ADJUSTED
    st.write("Risk Adj. Return is ", annual_return/(stdev%100))


