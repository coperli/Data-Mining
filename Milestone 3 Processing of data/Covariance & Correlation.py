#!/usr/bin/env python
# coding: utf-8

# # Milestones 3
# ## Covariance & Correlation
# ### Prepared by:
# WQD170042                                          
# WQD180006                             
# WQD180048                                  
# WQD180066                                              
# WQD180029 

# ## Loading Data
# The stock data is obtained from web scrapping as well as from stock's historical website (Investing.com) for stock history before Feb 2019 (Remark: We started scrapping from Feb).

# In[1]:


# Importing related packages or libraries.

import pandas as pd
import numpy as np
import os


# In[2]:


# Load stock data (EOD) for all "Telecommunications & Media" companies that listed in KLSE Main Board.
# The data is obtained from the scraping activities during Milestone 1 and 2. 
# In this Milestone 3, we will loaded the data to stock dataframe for analysis.

list_of_companies = ['Amtel_Telco', 'AsiaMedia_Media', 'Astro_Media', 'Axiata_Telco', 'BerjayaMedia_Media', 'Digi_Telco',
                     'EcoBuilt_Media', 'GreenPacket_Telco', 'Maxis_Telco', 'MediaChineseInternational_Media', 'MediaPrima_Media',
                     'OCKGroup_Telco', 'Pelangi_Media', 'Sasbadi_Media', 'SeniJaya_Media', 'Star_Media', 'TimeDotCom_Telco',
                     'TM_Telco', 'Utusan_Media']

stock = pd.DataFrame({"Date":[],"Price":[],"Open":[],"High":[],"Low":[],"Volume":[],"Change%":[],"Company":[]})
stock = stock.set_index('Date')

# Loaded all stock information for respective companies to stock dataframe.
for company in list_of_companies:
    path = "Data/" + company + ".csv"
    df = pd.read_csv(path, sep=",", header=0, parse_dates=[0])
    df.columns =["Date","Price","Open","High","Low","Volume","Change%"]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df["Company"] = company
    stock = stock.append(df)

stock.head(10)


# In[3]:


# Rearrange columns.

stock = stock[['High','Low','Open','Price','Volume','Change%','Company']]
cols = list(stock.columns.values)
print(cols)


# ## Data Cleansing

# In[4]:


# DATA CLEANSING - "Volume" column.

# Issue with "Volume" column. 
# It using ordinal representation (K or M) instead of numeric representation (000 or 000000), e.g. 309.50K.
# Due to that the data column type is object (should be integer).
# Implication - Can't be used for calc. or chart plotting directly.
# Need for data cleasing as below.
# Below will remove K or M and will replace it with 000 or 000000.

#print(stock.shape)     # for debugging purpose.
i = 0

while i < 931:
    # x is cell value under Volumn field.
    x = stock.iloc[i,4]
    #print(x)           # for debugging purpose.

    # K or M
    Ordinal = x[-1]
    if Ordinal == "K":
        y = x[0:-2]
        y = float(y) * 1000
        #print(y)          # for debugging purpose.
        #print(type(y))    # for debugging purpose.
    
    if Ordinal == "M":
        y = x[0:-2]
        y = float(y) * 1000000
        #print(y)          # for debugging purpose.
        #print(type(y))    # for debugging purpose.
    
    stock.ix[i, 'Volume'] = y
    i = i + 1

# The K and M has been changed to numerical representation.
# So, now we may proceed to change the "Volume" column type.

stock["Volume"] = stock["Volume"].astype(int)


# In[5]:


# Verification step to make sure issue on "Volume" column has been catered. 

print(stock.shape,'\n')
print(stock.info(),'\n')
stock.head()


# In[6]:


# DATA CLEANSING - "Change%" column.

# Issue with "Change%" column. 
# At every cell, the value provided by the scrapped website is with % symbol, e.g. 1.53%.
# Due to that the data column type is object (should be float).
# Implication - Can't be used for calc. or chart plotting directly.
# Need for data cleasing as below.
# Below will remove the % symbol from every cell under "Change%" column.

#print(stock.shape)     # for debugging purpose.
i = 0

while i < 931:
    # x is cell value under "Change%" field.
    x = stock.iloc[i,5]
    #print(x)           # for debugging purpose.

    # Remove % symbol.
    y = x[0:-2]
    #print(y)          # for debugging purpose.
    #print(type(y))    # for debugging purpose.
    
    stock.ix[i, 'Change%'] = y
    i = i + 1

# The % symbol has been removed.
# So, now we may proceed to change the "Change%" column type.

stock["Change%"] = stock["Change%"].astype(float)


# In[7]:


# Verification step to make sure issue on "Change%" column has been catered. 

print(stock.shape,'\n')
print(stock.info(),'\n')
stock.head()


# ## Variance, Covariance and Correlation
# We choose Digi stock history from Jan to March as example.
# The stock data is obtained from web scrapping as well as from stock's historical website (Investing.com) for stock history before Feb 2019 (Remark: We started scrapping from Feb).

# In[8]:


# Calculation of Variance of Every Variable.

Digi = stock.loc[stock['Company'] == 'Digi_Telco']          
# User may try with other companies stock data by changing the company name. In this case change 'Digi_Telco' to other company.
Digi[['Open', 'High', 'Low', 'Price','Volume','Change%']].var()


# In[9]:


# Calculation of Covariance between Multivariate.

Digi[['Open', 'High', 'Low', 'Price','Volume','Change%']].cov()


# ### Correlation Value Strength
# 0.0 – 0.2 ~ Weak correlation
# 
# 0.3 – 0.6 ~ Moderate correlation
# 
# 0.7 – 1.0 ~ Strong correlation

# In[10]:


# Calculation of Correlation between Multivariate.

Digi[['Open', 'High', 'Low', 'Price','Volume','Change%']].corr()


# In[11]:


# Plotting Correlation Matrix.

Digi = Digi[['Open', 'High', 'Low', 'Price','Volume','Change%']]
corr = Digi.corr()
corr.style.background_gradient(cmap='coolwarm')


# In[ ]:




