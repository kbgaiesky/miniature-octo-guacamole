#!/usr/bin/env python
# coding: utf-8

# # CryptoCompare Product Analyst Assignment 2021
# 
# ## Data Analysis Task
# 
# ### Author: Kris Gaiesky
# ### Date: 2 November 2021
# 
# 1. Use CryptoCompare API to query historical Bitcoin (BTC) and Etherium (ETH) prices for the past 30 days.
# 
#     a) Which coin performed better in the last 30 days? Calculate the daily returns
#     b) What is the average, median, and standard deviation of the daily returns?
#     
# 2. Use the CryptoCompare API to query blockchain data for BTC over the past 30 days.
#     
#     a) Plot a chart for the BTC price and its hashrate in a dual axis chart, with the x-axis 
#        as the date
#     b) What is the correlation of price and hashrate?

# In[34]:


# CryptoCompare Data Analysis Task

#import libraries
import numpy as np
import pandas as pd
import cryptocompare as cc
import matplotlib.pyplot as plt
import datetime as datetime
import requests


# In[ ]:


# Question 1

# set API key and url

apiKey = "1cfa0ee52b058cfa4ae9f9126417cd0735514f88c5269d12f20dea4b6c95e391" #personal api key
url = "https://min-api.cryptocompare.com/data/histoday" #historical price data by day


# In[3]:


# create Bitcoin (BTC) dataframe
payload_btc = {
    "api_key": apiKey,
    "fsym": "BTC", #coin to examine - Bitcoin
    "tsym": "EUR", # measure in Euros
    "limit": 30 # we want to look at the previous month or past 30 days
}

# create Etherium (ETH) payload and dataframe
payload_eth = {
    "api_key": apiKey,
    "fsym": "ETH", # coin to examine - Etherium
    "tsym": "EUR", # measure in Euros
    "limit": 30 # we want to look at the previous month or past 30 days
}


# In[36]:


#BTC results
result_btc = requests.get(url, params=payload_btc).json() #class dictionary

#ETH results
result_eth = requests.get(url, params=payload_eth).json() #class dictionary


# In[5]:


#BTC dataframe
df_btc = pd.DataFrame(result_btc['Data']) #convert from dictionary to dataframe

#ETH dataframe
df_eth = pd.DataFrame(result_eth['Data']) #convert from dictionary to dataframe


# In[6]:


print(df_btc.head()) # get snapshot of dataframe; will be similar structure to ETH df


# In[7]:


#time is represented as epoch or unix time
#change time to show date %Y-%M-%D
# converted_df = pd.to_datetime(df['Date'], unit='s')

#BTC time convert
df_btc['time'] = pd.to_datetime(df_btc['time'], unit = 's')

#ETH time convert
df_eth['time'] = pd.to_datetime(df_eth['time'], unit = 's')


# In[8]:


# We are examing daily returns of BTC and ETH
# Orderbooks don't "close" like regular stock markets
# We need to choose a common timestamp point: we will use the coin price @ 'close'

#BTC subset
df_btc_sub = df_btc[['time','close']]

#ETH subset
df_eth_sub = df_eth[['time','close']]


# In[9]:


# make 'time' as index for both subset dataframes

#BTC
df_btc_sub = df_btc_sub.set_index('time')

#ETH
df_eth_sub = df_eth_sub.set_index('time')


# In[48]:


# calculate 30 day return for BTC and ETH; print to output
# price at last day
first_day = (df_btc_sub.index[0]) # first day
last_day = (df_btc_sub.index[-1]) # last day

print("First day:", first_day)
print("Last day:", last_day)


# In[56]:


#30 day return of BTC
thirty_day_return_btc = (df_btc_sub.pct_change(periods=30))*100

print(thirty_day_return_btc.iloc[[30]])


# In[59]:


#30 day return of ETH
thirty_day_return_eth = (df_eth_sub.pct_change(periods=30))*100
print(thirty_day_return_eth.iloc[[30]])


# Between October 3, 2021 and November 2, 2021, Bitcoin had a 30 day return of 32.88%. In comparison, Etherium had a 30 day return rate of 31.90%.
# 
# Bitcoin has outperformed Etherium over the past 30 days by 0.98%.

# In[60]:


# use perc change to calculate daily returns

#BTC daily returns
df_btc_daily_rtn = df_btc_sub.pct_change()

#ETH daily returns
df_eth_daily_rtn = df_eth_sub.pct_change()


# In[61]:


# change 'close' column heading to '[coin]_daily_return'

#BTC
df_btc_daily_rtn = df_btc_daily_rtn.rename({'close':'btc_daily_return'},axis=1)

#ETH
df_eth_daily_rtn = df_eth_daily_rtn.rename({'close':'eth_daily_return'},axis=1)


# In[62]:


# combine both dataframes into one based on time index
# df3 = pd.merge(df1, df2, left_index=True, right_index=True)

df_returns = pd.merge(df_btc_daily_rtn,df_eth_daily_rtn, left_index = True, right_index = True)

print(df_returns.head())

# NaN values are excluded. No need to drop
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html

print(df_returns.describe())


# For the period between October 3, 2021 and November 2, 2021:
# 
# # 1. Bitcoin
#    # a. Average Daily Return: 
#          1.0017%
#         
#    # b. Median Daily Return: 
#         # 0.9957%
#         
#    # c. Standard Deviation of Daily Returns
#         # 3.2213%
#         
# # 2. Etherium
#    # a. Average Daily Return:
#         # 0.09787%
#         
#    # b. Median Daily Return:
#         # 0.3864%
#         
#    # c. Standard Deviation of Daily Returns
#         # 3.2913%
#     

# In[72]:


#plot returns of BTC and ETH
plt.plot(df_returns)

#add axis labels
plt.xlabel('Date')
plt.xticks(rotation=45) #rotate dates to fit on plot

plt.ylabel('Rate of Return')

#add title
plt.suptitle("Daily Rates of Return for BTC and ETH")

plt.show()


# In[73]:


# Question 2

# set blockchain endpoint as url2

url2 = "https://min-api.cryptocompare.com/data/blockchain/histo/day"


# In[75]:


# similar steps to Question 1.

payload_btc_blockchain = {
    "api_key": apiKey,
    "fsym": "BTC", #coin to examine - Bitcoin
    "limit": 30 # we want to look at the previous month or past 30 days
}


# In[76]:


result_btc_blockchain = requests.get(url2, params=payload_btc_blockchain).json() # dictionary


# In[77]:


df_btc_blockchain = pd.DataFrame(result_btc_blockchain['Data']) # dictionary to df


# In[78]:


df_btc_blockchain.info()


# In[79]:


df_btc_blockchain_updt = df_btc_blockchain['Data'].apply(pd.Series)
df_btc_blockchain_updt.info()


# In[23]:


# convert Unix timestamps

df_btc_blockchain_updt['time'] = pd.to_datetime(df_btc_blockchain_updt['time'], unit = 's')


# In[24]:


# create subset of blockchain data. Focus only on time and hashrate of BTC

df_btc_blockchain_sub = df_btc_blockchain_updt[['time','hashrate']]


# In[85]:


df_btc_blockchain_sub.head() #quick look 


# In[86]:


#merge datasets

df_price_hash = pd.merge(df_btc_sub,df_btc_blockchain_sub, left_index = True, right_index = True)


# In[87]:


df_price_hash.head()


# In[123]:


fig, ax = plt.subplots()

ax.set_xlabel('Date')
ax.tick_params(axis = 'x',labelrotation = 45)

ax.set_ylabel('BTC Price (Euros)', color="blue")
ax.plot(df_price_hash['close'], color="blue")
ax.tick_params(axis='y', labelcolor="blue")

ax2 = ax.twinx()
ax2.plot(df_price_hash['hashrate'], color = "green")
ax2.set_ylabel('BTC Hashrate', color="green")
ax2.tick_params(axis='y', labelcolor="green")

ax.set_title('Relationship between BTC Price and Hashrate')

plt.savefig("BTC_Price_Hashrate.png",bbox_inches="tight")


# In[112]:


# calculate the correlation between BTC price and BTC hashrate

corr_df = df_price_hash.corr()
print(corr_df)


# For the period between October 3, 2021 and November 2, 2021:
# 
# # The correlation between BTC price (Euros) and BTC hashrate was 0.288.
