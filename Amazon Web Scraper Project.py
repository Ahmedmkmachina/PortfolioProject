#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries 

from bs4 import BeautifulSoup
import requests
import time
import datetime

import smtplib


# In[5]:


import requests
from bs4 import BeautifulSoup

URL = 'https://www.amazon.com/s?k=gaming'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

# Send request
page = requests.get(URL, headers=headers)

# Parse HTML
soup = BeautifulSoup(page.content, "html.parser")

# Find all product containers
products = soup.find_all("div", {"data-component-type": "s-search-result"})

# Loop through first 5 products
for product in products[:5]:
    title_elem = product.h2
    title = title_elem.text.strip() if title_elem else "No title found"

    price_whole = product.find("span", class_="a-price-whole")
    price_frac = product.find("span", class_="a-price-fraction")
    
    if price_whole and price_frac:
        price = f"${price_whole.text.strip()}.{price_frac.text.strip()}"
    elif price_whole:
        price = f"${price_whole.text.strip()}"
    else:
        price = "Price not available"

    print(f"Title: {title}")
    print(f"Price: {price}")
    print("-" * 40)



# In[6]:


# Clean up the data a little bit

price = price.strip()[1:]
title = title.strip()

print(title)
print(price)


# In[7]:


# Create a Timestamp for your output to track when data was collected

import datetime

today = datetime.date.today()

print(today)


# In[12]:


import csv
from datetime import datetime

# Sample data
title = "Gaming Mouse XYZ"
price = "$29.99"
today = datetime.today().strftime('%Y-%m-%d')

# Write to CSV
header = ['Title', 'Price', 'Date']
data = [title, price, today]

with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)

print("CSV file created successfully.")


# In[13]:


import os

print("File saved to:", os.path.abspath("AmazonWebScraperDataset.csv"))


# In[14]:


import pandas as pd

df = pd.read_csv('/Users/Aubasmac/AmazonWebScraperDataset.csv')

print(df)


# In[15]:


#Now we are appending data to the csv

with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)


# In[20]:


import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os

def check_price():
    URL = 'https://www.amazon.com/s?k=gaming'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all product containers
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Today's date
    today = datetime.date.today()

    # Prepare CSV
    file_name = 'AmazonWebScraperDataset.csv'
    file_exists = os.path.isfile(file_name)

    with open(file_name, 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Title', 'Price', 'Date'])

        # Loop through first 5 products
        for product in products[:5]:
            title_elem = product.h2
            title = title_elem.text.strip() if title_elem else "No title found"

            price_whole = product.find("span", class_="a-price-whole")
            price_frac = product.find("span", class_="a-price-fraction")
            
            if price_whole and price_frac:
                price = f"${price_whole.text.strip()}.{price_frac.text.strip()}"
            elif price_whole:
                price = f"${price_whole.text.strip()}"
            else:
                price = "Price not available"

            writer.writerow([title, price, today])
            print("Saved:", title, price, today)

# Run the function
check_price()


# In[ ]:


#import time  # ← You need to import time!

#while True:
   # check_price()
   # time.sleep(86400)  # Waits 24 hours before next run


# In[ ]:


import pandas as pd

df = pd.read_csv(r'C:\Users\Aubasmac\AmazonWebScraperDataset.csv')

print(df)


# In[26]:


import smtplib
import ssl

def send_mail():
    sender_email = "Ahmadmachina488@gmail.com"
    receiver_email = "Ahmadmachina488@gmail.com"
    password = "xxxxxxxxxxxxxx"  # ⚠️ Replace with App Password, not your real password

    subject = "Gaming Mouse XYZ is below $24.99!"
    body = (
        "Ahmed, this is the moment we have been waiting for.\n"
        "Now is your chance to pick up the gaming gear of your dreams.\n"
        "Link here: https://www.amazon.com/s?k=gaming"
    )
    
    message = f"Subject: {subject}\n\n{body}"

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    print("Email sent!")


# In[ ]:




