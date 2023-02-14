# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 20:37:59 2023

@author: pablo
"""
################ Final Assignment ############################
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period = "max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')
soup.find_all("tbody")[0]

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
    

read_html_pandas_data = pd.read_html(str(soup))

tesla_revenue = read_html_pandas_data[1]
column_names = {'Tesla Quarterly Revenue(Millions of US $)':'Date', 'Tesla Quarterly Revenue(Millions of US $).1':'Revenue'}
tesla_revenue.rename(columns=column_names, inplace=True)

# Clean the data
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail(5)


###### GameStop ######
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period = "max")
gme_data.reset_index(inplace=True)

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')
read_html_pandas_data = pd.read_html(str(soup))
gme_revenue = read_html_pandas_data[1]
column_names = {'GameStop Quarterly Revenue(Millions of US $)':'Date', 'GameStop Quarterly Revenue(Millions of US $).1':'Revenue'}
gme_revenue.rename(columns=column_names, inplace=True)

# Clean the data
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]


gme_revenue.tail(5)


##### Graphs

make_graph(tesla_data, tesla_revenue, 'Tesla')
