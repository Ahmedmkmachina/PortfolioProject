#!/usr/bin/env python
# coding: utf-8

# # Scraping A Data From Real Website + Pandas

# In[1]:


from bs4 import BeautifulSoup
import requests


# In[11]:


url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')


# In[3]:


soup


# In[4]:


soup.find_all('table')[1]


# In[5]:


table = soup.find_all('table')[1]


# In[12]:


world_titles = table.find_all('th')


# In[21]:


world_table_titles = (title.text.strip() for title in world_titles)

# Option 1: Convert to list and print
#print(list(world_table_titles))

# Option 2: Iterate through the generator
for title in world_table_titles:
   print(title)


# In[28]:


import pandas as pd

# Convert generator to list
world_table_titles = [title.text.strip() for title in world_titles]

# Now use it as columns
df = pd.DataFrame(columns=world_table_titles)

print(df)


# In[30]:


df


# In[32]:


column_data = table.find_all('tr')


# In[38]:


for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]  
    length = len(df)
    df.loc[length] =  individual_row_data


# In[40]:


df


# In[51]:


df.to_csv('.\downloads\Python TT\companies.csv') 


# In[ ]:




