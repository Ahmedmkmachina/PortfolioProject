#!/usr/bin/env python
# coding: utf-8

# In[1]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
#Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

#NOTE:
# I had to go in and put "jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10"
# Into the Anaconda Prompt to change this to allow to pull data

# If that didn't work try using the local host URL as shown in the video


# In[2]:


type(data)


# In[3]:


import pandas as pd


#This allows you to see all the columns, not just like 15
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[4]:


#This normalizes the data and makes it all pretty in a dataframe

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[9]:


import os
import json
import pandas as pd
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from time import sleep
from datetime import datetime

# Initialize global dataframe
df = pd.DataFrame()

def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        df2 = pd.json_normalize(data['data'])
        df2['Timestamp'] = pd.to_datetime('now')
        df = pd.concat([df, df2], ignore_index=True)
        print(f"[{datetime.now()}] API Runner completed")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"[{datetime.now()}] Error: {e}")

# Run the API every minute for 333 times
for i in range(333):
    api_runner()
    sleep(60)

# Optional: Save results to CSV
df.to_csv("crypto_data.csv", index=False)
print("All data saved to 'crypto_data.csv'")

exit()


# In[11]:


df


# In[12]:


# One thing I noticed was the scientific notation. I like it, but I want to be able to see the numbers in this case

pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[13]:


df


# In[14]:


# Now let's look at the coin trends over time

df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3


# In[15]:


df4 = df3.stack()
df4


# In[16]:


type(df4)


# In[17]:


df5 = df4.to_frame(name='values')
df5


# In[18]:


df5.count()


# In[27]:


index = pd.Index(range(90))
df6 = df5.reset_index()
df6


# In[28]:


df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[31]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])
df7


# In[32]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[33]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[41]:


df10 = df[['name','quote.USD.price','Timestamp']]
df10 = df10.query("name == 'Bitcoin'")
df10


# In[43]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='Timestamp', y='quote.USD.price', data = df10)


# In[ ]:




