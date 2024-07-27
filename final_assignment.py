# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 20:37:59 2023

@author: pablo
"""
################ Final Assignment ############################
import matplotlib.pyplot as plt
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
tesla_revenue.rename(columns={'Tesla Quarterly Revenue (Millions of US $)': 'Date', 'Tesla Quarterly Revenue (Millions of US $).1': 'Revenue'}, inplace=True)

# Clean the data
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"",regex=True).astype(float)
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',', '').str.replace('$', '').astype(float)
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail(5)

tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
###### GameStop ######
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period = "max")
gme_data.reset_index(inplace=True)

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')
read_html_pandas_data = pd.read_html(str(soup))
gme_revenue = read_html_pandas_data[1]
gme_revenue.rename(columns={'GameStop Quarterly Revenue (Millions of US $)':'Date', 'GameStop Quarterly Revenue (Millions of US $).1':'Revenue'}, inplace=True)

# Clean the data
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"",regex=True).astype(float)

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue["Date"] = pd.to_datetime(gme_revenue["Date"])

gme_revenue.tail(5)


##### Graphs
def make_graph(stock_data, revenue_data, company_name):
    fig, ax1 = plt.subplots()

    # Graficar los precios de las acciones
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price ($US)', color='tab:blue')
    ax1.plot(stock_data['Date'], stock_data['Close'], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Crear un segundo eje para los ingresos
    ax2 = ax1.twinx()
    ax2.set_ylabel('Revenue ($US Millions)', color='tab:red')
    ax2.plot(revenue_data['Date'], revenue_data['Revenue'], color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Agregar título y mostrar gráfico
    plt.title(f'{company_name} Historical Stock Price and Revenue')
    fig.tight_layout()
    plt.show()
    
    
make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')
