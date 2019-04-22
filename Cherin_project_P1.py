#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 00:02:46 2018

@author: cherinhamadi
"""
# import required packages 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pip install pandas-datareader
# I get the following error msg: The Python package manager (pip) can only be used from outside of IPython.
# I use Anacoda prompt to install the package
import pandas_datareader as pdr
from pandas_datareader import data
import os
os.getcwd()
os.chdir(r'C:\Users\Cherin\Desktop\Metro College\Python')

# import realtime data (stock market)from yahoo finance
# I imported data for the most active stocks as per yahoo finance on September 21, 2018
mydata=pdr.get_data_yahoo(['AAPL', 'MSFT', 'FB', 'AMD', 'GE','BAC','F','TWTR', 'MU', 'INTC', 'CSCO'])
mydata.tail()
mydata.info()
mydata.to_excel('mydata.xlsx')
#Q1. what were the top five traded stocks over the last month?
# 1.1- stack dataframe

stackedmydata1=mydata.stack(level=1)
stackedmydata1.tail()
type(stackedmydata1)
stackedmydata1.columns

# 1.2- take a subset with date, Symbols, Volume
topstocks= stackedmydata1['Volume']
stackedmydata1['Volume']
topstocks.tail()
type(topstocks)

#1.3. Unstack data and tak a subset of the last 14 observations (transactions in September 2018)
topstocks1= topstocks.unstack()
topstocks1.tail()
topstocks1.tail(14)
topstocks2=topstocks1.tail(14)

#1.4- compute the total traded volume for each stock over the month
topstocks_2= topstocks2.sum()
type(topstocks_2)
topstocks_2.head()

#1.5 write the dataset to excel and re-import it
# if you dont want to write it to excel you should consider converting/
# data series into data frame as follows:
# vol= pd.dataframe(topstocks_2)

import os
os.getcwd()
os.chdir(r'C:\Users\Cherin\Desktop\Metro College\Python')
topstocks_2.to_excel('vol.xlsx')
vol=pd.read_excel('vol.xlsx')
type(vol)
vol.tail()
#1.6. rename columes 
vol.columns=['Symbols','Volume']
vol.set_index('Symbols')

#1.7- sort the total traded volum
v=vol.sort_values(by='Volume', ascending= False)
v.head()

#1.8- show result in bar chart
import matplotlib.pyplot as plt
plt.interactive(False)


bar=v.plot.bar(y='Volume', x= 'Symbols', color='r')
plt.title('Top Traded Stocks', fontsize=30)
plt.xlabel('Stocks')
plt.ylabel('Volume: in bn USD')
plt.show()
v
#1.9. Rank dataframe in a decending order and show the top 5
v.rank(ascending=False)
v['volume_rank']= v['Volume'].rank(ascending=0)
v
v.head()

# Q2. which stock had the highest return since the begining of this month?
# 2.1 take another subset with close (closign price)
S_return= stackedmydata1['Close']
S_return.head()

#2.2- transpose dataframe
S_return1=S_return.unstack()
S_return1.head()

# 2.3 compute the return of each stock
S_return2=S_return1.pct_change()
S_return2.head()

#2.4 compute the annualized mean of return 
S_return_Sep= S_return2.tail(14)
Avg_return= S_return_Sep.mean()*250
Avg_return.to_excel('ret.xlsx')
ret=pd.read_excel('ret.xlsx')
ret.head()
ret.columns=('Symbols','Return')
#.2.5. Show result in bar graph
ret.plot.bar(x='Symbols', y='Return', color='b')
plt.xlabel('Stocks')
plt.ylabel('Return (%)')
plt.title('Stock return in September 2018', fontsize=30)
plt.show()


#2.6.- sort stock return, then rank and show the top five
r=ret.sort_values(by='Return', ascending=0)
r['Return_rank']= r['Return'].rank(ascending=0)
r.head()

#Q3.  Do the top five traded stocks have the top return? 
#3.1. merge two data frame (volume, return)
TopSt= pd.merge(v, r)
#3.2 print the first five observations 
TopSt.columns=('Symbols', 'V', 'V_Rank', 'R', 'R_Rank')
TopSt.head()

#Q4. what is the price trend in your chosen stock?
# AMD recorded the highest traded volume as well as the highest return for Sept2018 
#4.1. unstack dataset with the closing price
type(S_return)
P= S_return.unstack()
P.head()
type(P)

#4.2. take a subset with the chosen stock
AMD_P=P['AMD']

#4.3.rename columns
AMD_P.columns=('Date', 'CloseP')
AMD_P.tail()

#4.4. lineplot the stock price
plt.plot(AMD_P)
plt.ylabel('USD')
plt.title('Historical Price of Advanced Micro Devices', fontsize=26)
plt.show()

#Q5. When is it the best time to buy and when is it the best time to sell?
# compute price moving average and plot with real price 
''' if moving average crossed the price from the above, then it is time for short sale'''
''' if moving average crossed the prie from below, then it is time for buying on margin'''

#5.1. slice AMD price for the last 2 years 
AMD= AMD_P.tail(500)

#5.2-Compute price simple moving average 

smv10d=AMD.rolling(window=10).mean()
smv10d.tail()


smv20d=AMD.rolling(window=20).mean() 
smv50d=AMD.rolling(window=50).mean()

#5.3.lineplot price, short term moving average andlong term moving average?
plt.plot(AMD, label='Price')
plt.plot(smv10d, label='10-day SMA' )
plt.plot (smv20d,label= '20-day SMA')
plt.plot(smv50d, label= '50-day SMA')
plt.legend(['Price', '10-day SMA', '50-day SMA'], loc=4)
plt.title('Advanced Micro Devices: Real Price Vs. Moving Average', fontsize=26)
plt.ylabel('USD')
plt.show()    