import numpy as np
import plotly.express as px
import requests
import streamlit as st
import yfinance as yf
from bs4 import BeautifulSoup

st.title("STOCK DASHBOARD")

#-----SIDEBAR----------
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Check if any input is missing
if not ticker:
    st.sidebar.error("Please enter a ticker symbol.")
if not start_date or not end_date:
    st.sidebar.error("Please select both a start and end date.")

# Only proceed if all inputs are provided
if ticker and start_date and end_date:
    # Retrieve stock information
    stock_info = yf.Ticker(ticker).info

    # Extract the company name
    company_name = stock_info.get('longName', ticker)

    # Set the company name as the title
    st.title(f"{company_name} Stock Dashboard")

    #-----------stock header------------------
    url = f'https://finance.yahoo.com/quote/{ticker}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #---LINE CHART---
    data = yf.download(ticker, start=start_date, end=end_date)
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=company_name)
    st.plotly_chart(fig)

    #---TABS------
    pricing_data, news = st.tabs(["Pricing Data", "Top 10 News"])

    with pricing_data:
        st.header("Price Movements")
        data2 = data
        data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
        st.write(data)
        # ANNUAL Return
        annual_return = data2['% Change'].mean() * 252 * 100
        st.write("Annual Return is ", annual_return, '%')
        # STANDARD DEVIATION (1 YEAR EXCLUDING THE WEEKEND)
        stdev = np.std(data2['% Change']) * np.sqrt(252)
        st.write('Standard Deviation is ', stdev * 100, '%')
        # RISK ADJUSTED
        st.write("Risk Adj. Return is ", annual_return / (stdev % 100))

    with news:
        st.header("Top 10 News Articles")

        # Scrape news related to the stock
        news_url = f'https://finance.yahoo.com/quote/{ticker}/news'
        news_response = requests.get(news_url)
        news_soup = BeautifulSoup(news_response.text, 'html.parser')

        # Find the news articles
        articles = news_soup.find_all('li', {'class': 'js-stream-content'}, limit=10)

        # Display each article's title and link
        for article in articles:
            title = article.find('h3').text
            link = article.find('a')['href']
            full_link = f"https://finance.yahoo.com{link}"
            st.write(f"[{title}]({full_link})")

else:
    st.write("Please provide a ticker, start date, and end date to see the stock dashboard.")
