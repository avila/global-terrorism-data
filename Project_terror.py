
# coding: utf-8

# # Project Terror
# 
# Betriebssystem und Programmierung - Lehrveranstaltung 3 | Prof. Dr. Kristian Rother
# Students:
# - Julia ..
# - Marcelo Avila
# - Marek ..
# 
# The objective of the project is to get some data containing geocoordinate information so that can be displayed geographically as a map, while also using other statistical and analytical tools Python. Nonetheless, not only the analysis is the focus of the project, but all the work related to the collection, cleaning, analysing and displaying the resulst. 
# 
# The tools used in this project are: 
# - jupyter
# - pandas
# - bokeh ? 
# - map... package
# - ...
# 
# 
# ## The data
# 
# The [data](http://www.start.umd.edu/gtd/contact/) which is provided by the University of Maryland. It consists of..
# ..
# 
# ..
# ..
# 
# have in mind: [How to finx the flaws in the GTDatabase](https://www.washingtonpost.com/news/monkey-cage/wp/2014/08/11/how-to-fix-the-flaws-in-the-global-terrorism-database-and-why-it-matters/).
# ..

# ## Reading the data

# In[1]:

import pandas as pd
import csv
import requests
import os


# ### request data 
# request the data and save a local copy named as "GTD_full.xlsx".
# (download might take up to ~5 min depending on internet connection)
# 
# The data is publicly available at the [University of Maryland](http://www.start.umd.edu/gtd/contact/) website. One might need to fill up a formular in order to get the data, though. 

# In[2]:

url = "http://apps.start.umd.edu/gtd/downloads/dataset/globalterrorismdb_0617dist.xlsx"

resp = requests.get(url)

output = open("GTD_full.xlsx", 'wb')
output.write(resp.content)
output.close()


# The data of Year 1993 was lost and they provide some of the data in a separate file. Therefore we need to download and append this file into the main file.

# In[53]:

url93 = "http://apps.start.umd.edu/gtd/downloads/dataset/gtd1993_0617dist.xlsx"

resp = requests.get(url93)

output = open("GTD_1993.xlsx", 'wb')
output.write(resp.content)
output.close()


# ### Read data into Pandas 
# 
# We we will save data for year 1993 as data frame and drop one column ("individual") which consists of only zeros (0) and this collumn is not present in the full database

# In[104]:

df_full = pd.read_excel("GTD_full.xlsx") # can take up to few minutes.

df_93 = pd.read_excel("GTD_1993.xlsx")
df_93.drop("individual", axis=1, inplace=True)


# Next we will append the 1993 data into the full data frame, while we do that we also make sure the collumns ordering are kept as before and we fit (sort) the 1993 in its right place. 

# In[151]:

df_full = df_full.append(df_93, ignore_index=True)[df_full.columns.tolist()]
df_full = df.sort_values("eventid", ascending=True)
df_full.head()


# Now we make a list of variables to keep and drop the rest of the data frame and call the data frame we will be working with "df". 

# In[228]:

keep = ["eventid", "iyear", "imonth", "iday", 
        "country", "country_txt", "city", "region", "region_txt",
        "city", "latitude", "longitude", "attacktype1", "attacktype1_txt", 
        "weaptype1", "weaptype1_txt", "targtype1", "targtype1_txt", "gname", 
        "nkill", "nkillter", "nwound", "propextent", "propvalue",]
df = df_full[keep]
df.head()


# lets save what we've got in a excel file

# In[225]:

df.to_excel("df_small.xlsx") # might take a minute


# In[3]:

df = pd.read_excel("df_small.xlsx")


# ## Missing data
# 
# It turns out there is not much missing data for the most interesting variables (although there are plenty of "unknown" events, which isn't technically missing values but its not *real* information also.)
# The exception are:
# - nkillter (number of perpretators killed)
# - propextent (extension of damage to affected property)
# - propvalue (value of damage to property)

# In[4]:

print(len(df) - df.count(),"\nobservations: ", len(df))


# Still we have three opttions: 
# 1. do nothing about it
# 2. drop the missing data
# 3. fill it up with mean or median (so that other information are not lost)

# In[208]:

df['nkill'].fillna(df['nkill'].median(), inplace=True)
df['nkillter'].fillna(df['nkillter'].median(), inplace=True)


# In[247]:

df.head()


# ## Data Analysis

# In[257]:

df[["iyear", "nkill", "nkillter"]].groupby("iyear").sum().sort_values("nkill", 
    ascending = False)


# In[6]:

# get ust some columns of interest.
colsmall = ["country_txt", "nkill", "nkillter", "gname"]
# parameters by which to group by
grpby = ["country_txt"]# , "iyear"]


df[colsmall].groupby(grpby).sum().sort_values("nkill", ascending = False)


# In[13]:

df[colsmall].groupby("gname").sum().sort_values("nkill", ascending = False).head(25)

