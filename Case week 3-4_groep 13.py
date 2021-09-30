#!/usr/bin/env python
# coding: utf-8

# # Project Title 

# In[118]:


#setting project title 
project_title = "Case week 3-4"
group_13 = {'Jasper Smit': 500804795,
        'Romario Thiel': 500633961,
        'Gian van Veen': 500808194,
        'Esra Weijenberg': 500835601}


# # 1 system setup

# 
# **Credits :**   
# https://github.com/Kaushik-Varma/Marketing_Data_Analysis   
# https://towardsdatascience.com/exploratory-data-analysis-eda-python-87178e35b14   
# https://seaborn.pydata.org/generated/seaborn.boxplot.html   
# 

# **Working directory setup**
# * **/Data/** for all data related maps
# * **/Data/raw/** for all raw incoming data
# * **/Data/clean/** for all clean data to be used during analysis
# * **/Data/staging/** for all data save during cleaning 
# * **/Data/temp/** for all tempral data saving 
# * **/Figs/temp/** for all tempral data saving 
# * **/Docs/** reference documentation
# * **/Results/** reference documentation
# * **/Code/** reference documentation
# 
# 
# **references:**
# https://docs.python-guide.org/writing/structure/
# 
# 

# Setup packages required for analysis
# 

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import plotly.express as px
import requests
import plotly.graph_objects as go
import json
from matplotlib.widgets import CheckButtons
get_ipython().run_line_magic('matplotlib', 'inline')


# Set working directories 

# In[3]:


print("Current working directory: {0}".format(os.getcwd()))


# In[4]:


working_dir = os.getcwd()


# Code below created project structure

# In[5]:


arr_map_structure  = [os.getcwd() + map for map in   ['/Data','/Data/raw','/Data/clean','/Data/staging',
                      '/Data/temp','/Figs','/Figs/temp','/Docs','/Results','/Code'] ]

[os.makedirs(map) for map in arr_map_structure if  not os.path.exists( map)]


# In[6]:


raw_data_dir = working_dir +'/Data/raw/'


# # 2 Import data

# show contents of working directory

# In[7]:


os.listdir(raw_data_dir)


# In[8]:


#inladen van de api's en opslaan als aparte dataframes
url_geslacht = 'https://onderwijsdata.duo.nl/datastore/dump/dc9a7f70-2950-4c46-926f-4d21c1a6e00e?format=json'
url_vorm = 'https://onderwijsdata.duo.nl/datastore/dump/6c648c28-28da-486e-86af-a7be10a37d69?format=json'
url_niveau = 'https://onderwijsdata.duo.nl/datastore/dump/e0a02a03-948a-4e45-a6cb-6ef5a18b1b5b?format=json'

data_geslacht = json.loads(requests.get(url_geslacht).content)
df_geslacht = pd.json_normalize(data_geslacht['records'])

data_vorm = json.loads(requests.get(url_vorm).content)
df_vorm = pd.json_normalize(data_vorm['records'])

data_niveau = json.loads(requests.get(url_niveau).content)
df_niveau = pd.json_normalize(data_niveau['records'])


# In[9]:


df_geslacht.head()


# In[10]:


df_niveau.head()


# In[11]:


df_vorm.head()


# # 3 Exploratory Data Analysis

# In[12]:


whos


# ## 3.1 EDA per dataframe

# Eerst kijken naar de veldnamen en data types

# In[13]:


df_geslacht.shape


# In[14]:


df_vorm.shape


# In[15]:


df_niveau.shape


# In[16]:


df_geslacht.dtypes


# In[17]:


df_geslacht.dtypes


# In[18]:


df_vorm.dtypes


# In[19]:


df_niveau.info()


# Dan kijken naar de statistieken van alle kolommen  

# In[20]:


df_geslacht.head()


# In[21]:


df_geslacht.nunique(axis=0)


# In[22]:


df_vorm.nunique(axis=0)


# In[23]:


df_niveau.nunique(axis=0)


# ## 3.1.1 kolommen splitsen / verwijderen / hernoemen / 

# **merging de 3 dataframes**

# In[24]:


df = df_geslacht.copy(deep=True)


# In[25]:


df = df.merge(df_vorm, on=['DIPLOMAJAAR','PROVINCIENAAM','GEMEENTENUMMER','GEMEENTENAAM', 'SOORT_INSTELLING', 'BRINNUMMER_ACTUEEL', 'INSTELLINGSNAAM_ACTUEEL', 'CROHO_ONDERDEEL', 'CROHO_SUBONDERDEEL', 'SOORT_DIPLOMA'],how='left')


# In[26]:


# _id droppen aangezien het niet van toepassing is.
df.drop('_id_y', axis = 1, inplace = True)


# In[27]:


df.drop('AANTAL_GEDIPLOMEERDEN_y',axis=1,inplace=True)


# In[28]:


df = df.merge(df_niveau, on=['DIPLOMAJAAR','PROVINCIENAAM','GEMEENTENUMMER','GEMEENTENAAM', 'SOORT_INSTELLING', 'BRINNUMMER_ACTUEEL', 'INSTELLINGSNAAM_ACTUEEL', 'CROHO_ONDERDEEL', 'CROHO_SUBONDERDEEL', 'SOORT_DIPLOMA'],how='left')


# In[29]:


# Drop the _id as it is of no use.
df.drop('_id', axis = 1, inplace = True)


# In[30]:


df.drop('AANTAL_GEDIPLOMEERDEN', axis = 1, inplace = True)


# In[31]:


df = df[['_id_x', 'DIPLOMAJAAR', 'PROVINCIENAAM', 'GEMEENTENUMMER', 'GEMEENTENAAM', 'SOORT_INSTELLING','BRINNUMMER_ACTUEEL','INSTELLINGSNAAM_ACTUEEL', 'CROHO_ONDERDEEL', 'CROHO_SUBONDERDEEL', 'OPLEIDINGSCODE_ACTUEEL', 'OPLEIDINGSNAAM_ACTUEEL', 'SOORT_DIPLOMA', 'OPLEIDINGSVORM', 'GESLACHT', 'AANTAL_GEDIPLOMEERDEN_x']]


# In[32]:


df.drop('_id_x', axis = 1, inplace = True)


# In[33]:


df.drop('SOORT_INSTELLING', axis = 1, inplace = True)


# In[34]:


#Hernoemen van de aantal gediplomeerden_x kolom.
df = df.rename(columns={"AANTAL_GEDIPLOMEERDEN_x": "AANTAL_GEDIPLOMEERDEN"})


# In[35]:


df.head()


# In[36]:


df.shape


# **Resultaat** 

# In[37]:


df_Staging = df.copy(deep=True) 


# ## 3.1.2 generieke verkenning

# In[38]:


#Verkennen van de dataset.
df_Staging.describe()


# In[39]:


df_Staging.dtypes


# In[40]:


#Herkennen van unieke waardes in de dataset
df_Staging.nunique(axis=0)


# Wat valt op:
# * Aantal gediplomeerde is vreemd verdeeld: mean ligt bijna tegen 75% aan en er zit een enorm verschil tussen 25% en 75%
# * aantal gediplomeerde heeft een bizare max

# In[41]:


#Controleren op missende waardes
df_geslacht.isnull().sum()


# In[42]:


# Tellen van het aantal mannen en vrouwen
df_geslacht['GESLACHT'].value_counts()


# ## 3.2  DATASET inclusief geslacht

# #### Aantal gediplomeerde

# In[43]:


# Tellen van het aantal gediplomeerden
df_geslacht['DIPLOMAJAAR'].value_counts()


# In[44]:


df_geslacht


# In[45]:


# Filteren van data door middel van het diplomajaar
gd_2014 = df_geslacht.loc[df_geslacht['DIPLOMAJAAR']==2014].reset_index()
gd_2015 = df_geslacht.loc[df_geslacht['DIPLOMAJAAR']==2015].reset_index()
gd_2016 = df_geslacht.loc[df_geslacht['DIPLOMAJAAR']==2016].reset_index()
gd_2017 = df_geslacht.loc[df_geslacht['DIPLOMAJAAR']==2017].reset_index()
gd_2018 = df_geslacht.loc[df_geslacht['DIPLOMAJAAR']==2018].reset_index()


# In[46]:


# Histogram van het aantal gediplomeerden per jaar
gd_2014.AANTAL_GEDIPLOMEERDEN.hist(bins=10,histtype='step')
gd_2015.AANTAL_GEDIPLOMEERDEN.hist(bins=10,histtype='step')
gd_2016.AANTAL_GEDIPLOMEERDEN.hist(bins=10,histtype='step')
gd_2017.AANTAL_GEDIPLOMEERDEN.hist(bins=10,histtype='step')
gd_2018.AANTAL_GEDIPLOMEERDEN.hist(bins=10,histtype='step')
plt.legend(['2014','2015','2016','2017','2018'])
plt.title('Aantal gediplomeerden per jaar')
plt.xlabel('Aantal gediplomeerden')
plt.ylabel('Frequentie')
plt.rcParams["figure.figsize"] = (10,5)
plt.show()


# #### Opleidingen

# In[47]:


# Zoeken naar unieke waardes
gd_2014.CROHO_ONDERDEEL.unique()


# In[48]:


gd_2014.describe()


# In[49]:


# Optellen van alle gediplomeerden in 2015
gd_2015.AANTAL_GEDIPLOMEERDEN.sum()


# In[50]:


gd_2016.CROHO_ONDERDEEL.value_counts()


# In[51]:


gd_2017.CROHO_ONDERDEEL.value_counts()


# In[52]:


gd_2018.CROHO_ONDERDEEL.value_counts()


# In[53]:


# Het aantal gediplomeerden per croho onderdeel
tot_gd = df_geslacht.groupby('CROHO_ONDERDEEL')['AANTAL_GEDIPLOMEERDEN'].sum()


# In[54]:


# Kolom toevoegen met de som van het aantal gediplomeerden
df_geslacht['Totaal'] = df_geslacht.groupby('CROHO_ONDERDEEL')['AANTAL_GEDIPLOMEERDEN'].transform('sum')
df_geslacht.head()


# In[55]:


df_geslacht['AANTAL_GEDIPLOMEERDEN'].value_counts().sort_index()


# In[56]:


# Bar chart van het aantal gediplomeerden per onderdeel
tot_gd.plot.bar(title="Aantal Gediplomeerden per onderdeel")
plt.rcParams["figure.figsize"] = (15,15)
plt.show()


# #### Man-Vrouw

# In[57]:


# Aantal gediplomeerde mannen per croho onderdeel tellen
man = df_geslacht.loc[df_geslacht['GESLACHT']=='MAN']
man_vc = man.groupby('CROHO_ONDERDEEL')['AANTAL_GEDIPLOMEERDEN'].sum()
man_vc


# In[58]:


# Aantal gediplomeerde vrouwen per croho onderdeel tellen
vrouw = df_geslacht.loc[df_geslacht['GESLACHT']=='VROUW']
vrouw_vc = vrouw.groupby('CROHO_ONDERDEEL')['AANTAL_GEDIPLOMEERDEN'].sum()
vrouw_vc


# In[59]:


# Percentgae man en vrouw geslaagd
df_geslacht['GESLACHT'].value_counts(normalize=True)


# In[60]:


# Bar chart van het aantal gediplomeerden per opleiding per geslacht
x = ['Economie', 'Gedrag en Maatschappij', 'Gezondheidszorg', 'Landbouw en Natuurlijke Omgeving', 'Onderwijs', 'Sectoroverstijgend', 'Taal en Cultuur', 'Techniek']
plt.bar(x,man_vc, color ='blue', label = 'Man')
plt.bar(x,vrouw_vc,bottom = man_vc, color='red', label = 'Vrouw')
plt.xticks(x, rotation = 90)
plt.ylabel('Aantal Gediplomeerden')
plt.legend(['Man', 'Vrouw'])
plt.title('Aantal gediplomeerden per opleiding per geslacht')
plt.rcParams["figure.figsize"] = (20,10)
plt.show()


# In[61]:


# boxplot
ax = sns.boxplot(x=df.loc[df['GESLACHT']=='VROUW']['CROHO_ONDERDEEL'],y=df.loc[df['GESLACHT']=='VROUW']['AANTAL_GEDIPLOMEERDEN'])
plt.title('Aantal gediplomeerde vrouwen per onderdeel')


# In[62]:


ax = sns.boxplot(x=df.loc[df['GESLACHT']=='MAN']['CROHO_ONDERDEEL'],y=df.loc[df['GESLACHT']=='MAN']['AANTAL_GEDIPLOMEERDEN'])
plt.xticks(rotation = 90)
plt.title('Aantal gediplomeerde mannen per onderdeel')
plt.show()


# In[63]:


# Swarmplot van het aantal gediplomeerden per croho onderdeel
ax = sns.swarmplot(x=df_geslacht['CROHO_ONDERDEEL'],y=df_geslacht['AANTAL_GEDIPLOMEERDEN'])
plt.title('Aantal gediplomeerden per croho onderdeel')
plt.xticks(rotation = 90)
plt.show()


# In[64]:


# Scatter plot van het aantal degiplomeerden per croho onderdeel
plt.scatter(df_geslacht.CROHO_ONDERDEEL,df_geslacht.AANTAL_GEDIPLOMEERDEN)
plt.title('Aantal gediplomeerden per croho onderdeel')
plt.xticks(rotation = 90)
plt.show()


# In[65]:


# Scatter plot van het aantal gediplomeerden per diplomajaar
df_geslacht.plot.scatter(x="DIPLOMAJAAR",y="AANTAL_GEDIPLOMEERDEN")
plt.title('Aantal gediplomeerden per diplomajaar')
plt.show()


# In[66]:


# Scatter matrix van het aantal gediplomeerden per croho onderdeel per diplomajaar per geslacht.
geslacht_color_map = {'MAN': 'rgb(67, 52, 235)', 'VROUW': 'rgb(235, 52, 52)' }
fig =px.scatter_matrix(
    data_frame = df_geslacht, 
    dimensions =['AANTAL_GEDIPLOMEERDEN','CROHO_ONDERDEEL','DIPLOMAJAAR'],
    color = 'GESLACHT',
    opacity = 0.3,
    color_discrete_map = geslacht_color_map,
    title = 'Scatter Matrix van HBO gediplomeerden',
)
fig.update_traces(diagonal_visible=False)
fig.update_layout(
    width=1000,
    height=1000
    )
fig.show()


# In[67]:


# Kdeplot van het aantal gediplomeerden
sns.kdeplot(data=df_geslacht['AANTAL_GEDIPLOMEERDEN'])
plt.ylabel('Density')
plt.xlabel('Aantal Gediplomeerden')
plt.title('Gediplomeerdem density plot')
plt.show()


# In[68]:


df_geslacht.head()


# In[69]:


# Bar chart van het aantal gediplomeerden per opleiding per geslacht
x = ['Economie', 'Gedrag en Maatschappij', 'Gezondheidszorg', 'Landbouw en Natuurlijke Omgeving', 'Onderwijs', 'Sectoroverstijgend', 'Taal en Cultuur', 'Techniek']
fig, ax = plt.subplots(figsize=(20, 6))
ax.set_title('Aantal gediplomeerden per opleiding per geslacht')
ax.set_xlabel('CROHO_ONDERDEEL', fontsize=12)
ax.set_ylabel('Aantal Gediplomeerden', fontsize=12)

man, =  ax.plot(x, man_vc, color ='blue', label = 'Man')
vrouw, = ax.plot(x, vrouw_vc, color='red', label= "vrouw")
ax.legend()

lines = [man, vrouw]
rax = plt.axes([0.01,0.68, 0.060, 0.2])
labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)

def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()

check.on_clicked(func)

plt.title("Filter")
plt.show()


# # 3.3 Opleidingsniveau

# In[70]:


#Aantal gediplomeerden t.o.v de diplomajaar

year_color_map = {'2014':'rgb(255,0,0)','2015':'rgb(0,0,255)','2016':'rgb(0,255,0)','2017':'rgb(0,255,255)','2018':'rgb(255,255,0)'}
fig = px.histogram(df_niveau, 
                   x ='DIPLOMAJAAR',y= 'AANTAL_GEDIPLOMEERDEN',
                   color = 'DIPLOMAJAAR',
                   color_discrete_map = year_color_map,
                   title = 'Aantal gediplomeerden per jaar', 
                   labels = {'DIPLOMAJAAR':'Diplomajaar','AANTAL_GEDIPLOMEERDEN':'Aantal gediplomeerden'})
fig.update_layout()
fig.show()


# In[71]:


#Jaar 2014
opleidingniveau2014 = df_niveau[df_niveau['DIPLOMAJAAR'] == 2014]
#Soorten diploma t.o.v Aantal gediplomeerden
soort_color_map = {'hbo bachelor':'rgb(255,0,0)','hbo master':'rgb(0,0,255)','hbo associate degree':'rgb(0,255,0)'}
fig = px.histogram(opleidingniveau2014, x ='SOORT_DIPLOMA',y = 'AANTAL_GEDIPLOMEERDEN',
                   color = 'SOORT_DIPLOMA',
                   color_discrete_map = soort_color_map,
                   title = 'Aantal gediplomeerden per soort diploma in 2014', labels = {'AANTAL_GEDIPLOMEERDEN':'Aantal Gediplomeerden','SOORT_DIPLOMA':'Soort Diploma'})
fig.show()


# In[72]:


#Jaar 2015
opleidingniveau2015 = df_niveau[df_niveau['DIPLOMAJAAR'] == 2015]
#Soorten diploma t.o.v Aantal gediplomeerden
soort_color_map = {'hbo bachelor':'rgb(255,0,0)','hbo master':'rgb(0,0,255)','hbo associate degree':'rgb(0,255,0)'}
fig = px.histogram(opleidingniveau2015, x ='SOORT_DIPLOMA',y = 'AANTAL_GEDIPLOMEERDEN',
                   color = 'SOORT_DIPLOMA',
                   color_discrete_map = soort_color_map,
                   title = 'Aantal gediplomeerden per soort diploma in 2015', labels = {'AANTAL_GEDIPLOMEERDEN':'Aantal Gediplomeerden','SOORT_DIPLOMA':'Soort Diploma'})
fig.show()


# In[73]:


#Jaar 2016
opleidingniveau2016 = df_niveau[df_niveau['DIPLOMAJAAR'] == 2016]
#Soorten diploma t.o.v Aantal gediplomeerden
soort_color_map = {'hbo bachelor':'rgb(255,0,0)','hbo master':'rgb(0,0,255)','hbo associate degree':'rgb(0,255,0)'}
fig = px.histogram(opleidingniveau2016, x ='SOORT_DIPLOMA',y = 'AANTAL_GEDIPLOMEERDEN',
                   color = 'SOORT_DIPLOMA',
                   color_discrete_map = soort_color_map,
                   title = 'Aantal gediplomeerden per soort diploma in 2016', labels = {'AANTAL_GEDIPLOMEERDEN':'Aantal Gediplomeerden','SOORT_DIPLOMA':'Soort Diploma'})
fig.show()


# In[74]:


#Jaar 2017
opleidingniveau2017 = df_niveau[df_niveau['DIPLOMAJAAR'] == 2017]
#Soorten diploma t.o.v Aantal gediplomeerden
soort_color_map = {'hbo bachelor':'rgb(255,0,0)','hbo master':'rgb(0,0,255)','hbo associate degree':'rgb(0,255,0)'}
fig = px.histogram(opleidingniveau2017, x ='SOORT_DIPLOMA',y = 'AANTAL_GEDIPLOMEERDEN',
                   color = 'SOORT_DIPLOMA',
                   color_discrete_map = soort_color_map,
                   title = 'Aantal gediplomeerden per soort diploma in 2017', labels = {'AANTAL_GEDIPLOMEERDEN':'Aantal Gediplomeerden','SOORT_DIPLOMA':'Soort Diploma'})
fig.show()


# In[75]:


#Jaar 2018
opleidingniveau2018 = df_niveau[df_niveau['DIPLOMAJAAR'] == 2018]
#Soorten diploma t.o.v Aantal gediplomeerden
soort_color_map = {'hbo bachelor':'rgb(255,0,0)','hbo master':'rgb(0,0,255)','hbo associate degree':'rgb(0,255,0)'}
fig = px.histogram(opleidingniveau2018, x ='SOORT_DIPLOMA',y = 'AANTAL_GEDIPLOMEERDEN',
                   color = 'SOORT_DIPLOMA',
                   color_discrete_map = soort_color_map,
                   title = 'Aantal gediplomeerden per soort diploma in 2018', labels = {'AANTAL_GEDIPLOMEERDEN':'Aantal Gediplomeerden','SOORT_DIPLOMA':'Soort Diploma'})
fig.show()


# In[76]:


# Bar chart van het aantal gediplomeerden per diplomasoort per jaar
hbobachelor = df_niveau[df_niveau['SOORT_DIPLOMA'] == 'hbo bachelor']
hboassociate = df_niveau[df_niveau['SOORT_DIPLOMA'] == 'hbo associate degree']
hbomaster = df_niveau[df_niveau['SOORT_DIPLOMA'] == 'hbo master']
hbobvc = hbobachelor.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
hboavc = hboassociate.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
hbomvc = hbomaster.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
jaarcombined = ['2014','2015','2016','2017','2018']
fig = go.Figure(data=[
    go.Bar(name='Hbo Bachelor', x=jaarcombined, y=hbobvc,marker_color ='rgb(255,0,0)'),
    go.Bar(name='Hbo Associate Degree', x=jaarcombined, y=hboavc,marker_color = 'rgb(0,0,255)'),
    go.Bar(name='Hbo Master', x=jaarcombined, y=hbomvc,marker_color = 'rgb(0,255,0)')])
fig.update_xaxes(title_text ='Jaar')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per diplomasoort per jaar')


# Vervolgens gaan we naar de Gediplomeerden per provincie per jaar kijken

# In[77]:


df_niveau.groupby('PROVINCIENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()


# In[78]:


# Bar chart van het aantal gediplomeerden per provincie
provincie_color = {'Drenthe':'rgb(255,0,0)','Flevoland':'rgb(0,0,255)','Friesland':'rgb(0,255,0)','Gelderland':'rgb(0,255,255)','Groningen':'rgb(255,255,0)','Limburg':'rgb(255,0,255)','Noord-Brabant':'rgb(100,255,100)','Noord-Holland':'rgb(255,100,100)','Overijssel':'rgb(100,100,255)','Utrecht':'rgb(100,255,200)','Zeeland':'rgb(255,200,100)','Zuid-Holland':'rgb(200,100,255)'}
fig = px.histogram(df_niveau, x = 'PROVINCIENAAM',y = 'AANTAL_GEDIPLOMEERDEN',
                   color = 'PROVINCIENAAM',
                   color_discrete_map = provincie_color,
                   title = 'Aantal gediplomeerden per provincie', labels= {'PROVINCIENAAM':'Provincie'})
#dropdown_buttons = [{'label': "Drenthe", 'method': "update",'args':[{'visible':[True,False,False,False,False,False,False,False,False,False,False,False]},{'title':'Drenthe'}]},'label': "Flevoland",'label': "Friesland", 'method': "update",'label': "Gelderland", 'method': "update",'label': "Groningen", 'method': "update",'label': "Limburg", 'method': "update",'label': "Noord-Brabant", 'method': "update",'label': "Noord-Holland", 'method': "update",'label': "Overijssel", 'method': "update",'label': "Utrecht", 'method': "update",'label': "Zeeland", 'method': "update",'label': "Zuid-Holland", 'method': "update"}]
dropdown_buttons = [{'label': "Alle Provincie", 'method': "update",'args':[{'visible':[True,True,True,True,True,True,True,True,True,True,True,True]},{'title':'Alle Provincie'}]},
                    {'label': "Drenthe", 'method': "update",'args':[{'visible':[True,False,False,False,False,False,False,False,False,False,False,False]},{'title':'Drenthe'}]},
                    {'label': "Flevoland", 'method': "update",'args':[{'visible':[False,True,False,False,False,False,False,False,False,False,False,False]},{'title':'Flevoland'}]},
                    {'label': "Friesland", 'method': "update",'args':[{'visible':[False,False,True,False,False,False,False,False,False,False,False,False]},{'title':'Friesland'}]},
                    {'label': "Gelderland", 'method': "update",'args':[{'visible':[False,False,False,True,False,False,False,False,False,False,False,False]},{'title':'Gelderland'}]},
                    {'label': "Groningen", 'method': "update",'args':[{'visible':[False,False,False,False,True,False,False,False,False,False,False,False]},{'title':'Groningen'}]},
                    {'label': "Limburg", 'method': "update",'args':[{'visible':[False,False,False,False,False,True,False,False,False,False,False,False]},{'title':'Limburg'}]},
                    {'label': "Noord-Brabant", 'method': "update",'args':[{'visible':[False,False,False,False,False,False,True,False,False,False,False,False]},{'title':'Noord-Brabant'}]},
                    {'label': "Noord-Holland", 'method': "update",'args':[{'visible':[False,False,False,False,False,False,False,True,False,False,False,False]},{'title':'Noord-Holland'}]},
                    {'label': "Overijssel", 'method': "update",'args':[{'visible':[False,False,False,False,False,False,False,False,True,False,False,False]},{'title':'Overijssel'}]},
                    {'label': "Utrecht", 'method': "update",'args':[{'visible':[False,False,False,False,False,False,False,False,False,True,False,False]},{'title':'Utrecht'}]},
                    {'label': "Zeeland", 'method': "update",'args':[{'visible':[False,False,False,False,False,False,False,False,False,False,True,False]},{'title':'Zeeland'}]},
                    {'label': "Zuid-Holland", 'method': "update",'args':[{'visible':[False,False,False,False,False,False,False,False,False,False,False,True]},{'title':'Zuid-Holland'}]}]
fig.update_layout({'updatemenus':[{'type':"dropdown",'x':1.15,'y':1.1,'showactive':True,'active':0,'buttons':dropdown_buttons}]})
fig.show()


# In[79]:


# Bar chart van het aantal gediplomeerden per provincie per jaar
drenthe = df_niveau[df_niveau['PROVINCIENAAM'] == 'Drenthe']
flevoland = df_niveau[df_niveau['PROVINCIENAAM'] == 'Flevoland']
friesland = df_niveau[df_niveau['PROVINCIENAAM'] == 'Friesland']
gelderland = df_niveau[df_niveau['PROVINCIENAAM'] == 'Gelderland']
groningen = df_niveau[df_niveau['PROVINCIENAAM'] == 'Groningen']
limburg = df_niveau[df_niveau['PROVINCIENAAM'] == 'Limburg']
nb = df_niveau[df_niveau['PROVINCIENAAM'] == 'Noord-Brabant']
nh = df_niveau[df_niveau['PROVINCIENAAM'] == 'Noord-Holland']
overijssel = df_niveau[df_niveau['PROVINCIENAAM'] == 'Overijssel']
utrecht = df_niveau[df_niveau['PROVINCIENAAM'] == 'Utrecht']
zeeland = df_niveau[df_niveau['PROVINCIENAAM'] == 'Zeeland']
zh = df_niveau[df_niveau['PROVINCIENAAM'] == 'Zuid-Holland']
drenthesum = drenthe.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
flevolandsum = flevoland.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
frieslandsum = friesland.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
gelderlandsum = gelderland.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
groningensum = groningen.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
limburgsum = limburg.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
nbsum = nb.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
nhsum = nh.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
overijsselsum = overijssel.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
utrechtsum = utrecht.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
zeelandsum = zeeland.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
zhsum = zh.groupby('DIPLOMAJAAR')['AANTAL_GEDIPLOMEERDEN'].sum()
provinciecombined = ['2014','2015','2016','2017','2018']
fig = go.Figure(data=[
    go.Bar(name='Drenthe', x=provinciecombined, y=drenthesum,marker_color ='rgb(255,0,0)'),
    go.Bar(name='Flevoland', x=provinciecombined, y=flevolandsum,marker_color = 'rgb(0,0,255)'),
    go.Bar(name='Friesland', x=provinciecombined, y=frieslandsum,marker_color = 'rgb(0,255,0)'),
    go.Bar(name='Gelderland', x=provinciecombined, y=gelderlandsum,marker_color = 'rgb(0,255,255)'),
    go.Bar(name='Groningen', x=provinciecombined, y=groningensum,marker_color = 'rgb(255,255,0)'),
    go.Bar(name='Limburg', x=provinciecombined, y=limburgsum,marker_color = 'rgb(255,0,255)'),
    go.Bar(name='Noord-Brabant', x=provinciecombined, y=nbsum,marker_color = 'rgb(100,255,100)'),
    go.Bar(name='Noord-Holland', x=provinciecombined, y=nhsum,marker_color = 'rgb(255,100,100)'),
    go.Bar(name='Overijssel', x=provinciecombined, y=overijsselsum,marker_color = 'rgb(100,100,255)'),
    go.Bar(name='Utrecht', x=provinciecombined, y=utrechtsum,marker_color = 'rgb(100,255,200)'),
    go.Bar(name='Zeeland', x=provinciecombined, y=zeelandsum,marker_color = 'rgb(255,200,100)'),
    go.Bar(name='Zuid-Holland', x=provinciecombined, y=zhsum,marker_color = 'rgb(200,100,255)')])

fig.update_xaxes(title_text ='Jaar')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per provincie per jaar')
fig.show()


# In[80]:


df_niveau['AANTAL_GEDIPLOMEERDEN'].div(df_niveau['AANTAL_GEDIPLOMEERDEN'].sum())


# In[81]:


# Bar chart van het aantal gediplomeerden in Drenthe in 2014
drenthe2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Drenthe') & (df_niveau['DIPLOMAJAAR'] == 2014)]
drenthe2014sum = drenthe2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Assen','Emmen','Meppel']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=drenthe2014sum,marker_color = 'rgb(255,0,0)')])
fig.update_xaxes(title_text ='Gemeenten/s')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Drenthe in 2014')
fig.show()


# In[82]:


# Bar chart van het aantal gediplomeerden in Flevoland in 2014
flevoland2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Flevoland') & (df_niveau['DIPLOMAJAAR'] == 2014)]
flevoland2014sum = flevoland2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Almere','Dronten']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=flevoland2014sum,marker_color = 'rgb(0,0,255)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Flevoland in 2014')
fig.show()


# In[83]:


# Bar chart van het aantal gediplomeerden in Friesland in 2014
friesland2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Friesland') & (df_niveau['DIPLOMAJAAR'] == 2014)]
friesland2014sum = friesland2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Leeuwarden','Terschelling']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=friesland2014sum,marker_color = 'rgb(0,255,0)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Friesland in 2014')
fig.show()


# In[84]:


# Bar chart van het aantal gediplomeerden in Gelderland in 2014
gelderland2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Gelderland') & (df_niveau['DIPLOMAJAAR'] == 2014)]
gelderland2014sum = gelderland2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Apeldoorn','Arnhem','Doetinchem','Ede','Nijmegen','Rheden','Wageningen']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=gelderland2014sum,marker_color = 'rgb(0,255,255)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Gelderland in 2014')
fig.show()


# In[85]:


# Bar chart van het aantal gediplomeerden in Groningen in 2014
groningen2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Groningen') & (df_niveau['DIPLOMAJAAR'] == 2014)]
groningen2014sum = groningen2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Groningen']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=groningen2014sum,marker_color = 'rgb(255,255,0)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Groningen in 2014')
fig.show()


# In[86]:


# Bar chart van het aantal gediplomeerden in Limburg in 2014
limburg2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Limburg') & (df_niveau['DIPLOMAJAAR'] == 2014)]
limburg2014sum = limburg2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Heerlen','Maastricht','Sittard-Geleen','Venlo']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=limburg2014sum,marker_color = 'rgb(255,0,255)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Limburg in 2014')
fig.show()


# In[87]:


# Bar chart van het aantal gediplomeerden in Noord-Brabant in 2014
nb2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Noord-Brabant') & (df_niveau['DIPLOMAJAAR'] == 2014)]
nb2014sum = nb2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['s-Hertogenbosch','Bergen op Zoom','Breda','Eindhoven','Helmond','Meierijstad','Tilburg']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=nb2014sum,marker_color = 'rgb(100,255,100)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Noord-Brabant in 2014')
fig.show()


# In[88]:


# Bar chart van het aantal gediplomeerden in Noord-Holland in 2014
nh2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Noord-Holland') & (df_niveau['DIPLOMAJAAR'] == 2014)]
nh2014sum = nh2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Alkmaar','Amsterdam','Diemen','Haarlem','Hilversum']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=nh2014sum,marker_color = 'rgb(255,100,100)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Noord-Holland in 2014')
fig.show()


# In[89]:


# Bar chart van het aantal gediplomeerden in Overijssel in 2014
overijssel2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Overijssel') & (df_niveau['DIPLOMAJAAR'] == 2014)]
overijssel2014sum = overijssel2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Deventer','Enschede','Zwolle']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=overijssel2014sum,marker_color = 'rgb(100,100,255)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Overijssel in 2014')
fig.show()


# In[90]:


# Bar chart van het aantal gediplomeerden in Utrecht in 2014
utrecht2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Utrecht') & (df_niveau['DIPLOMAJAAR'] == 2014)]
utrecht2014sum = utrecht2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Amersfoort','Utrecht']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=utrecht2014sum,marker_color = 'rgb(100,255,200)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Utrecht in 2014')
fig.show()


# In[91]:


# Bar chart van het aantal gediplomeerden in Zeeland in 2014
zeeland2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Zeeland') & (df_niveau['DIPLOMAJAAR'] == 2014)]
zeeland2014sum = zeeland2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['Middelburg','Vlissingen']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=zeeland2014sum,marker_color = 'rgb(255,200,100)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Zeeland in 2014')
fig.show()


# In[92]:


# Bar chart van het aantal gediplomeerden in Zuid-Holland in 2014
zh2014 = df_niveau[(df_niveau['PROVINCIENAAM'] == 'Zuid-Holland') & (df_niveau['DIPLOMAJAAR'] == 2014)]
zh2014sum = zh2014.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].sum()
gemeenten= ['s-Gravenhage','Delft','Dordrecht','Gouda','Leiden','Rotterdam','Zoetermeer']
fig = go.Figure(data=[
    go.Bar(name='Zuid-Holland', x= gemeenten, y=zh2014sum,marker_color = 'rgb(200,100,255)')])
fig.update_xaxes(title_text ='Gemeenten')
fig.update_yaxes(title_text = 'Aantal Gediplomeerden')
fig.update_layout(barmode='group',title ='Aantal gediplomeerden per gemeente in Zuid-Holland in 2014')
fig.show()


# In[93]:


gelderland2014sum = gelderland.groupby('GEMEENTENAAM')['AANTAL_GEDIPLOMEERDEN'].min()
print(gelderland2014sum)


# # 3.4 Opleidingsvorm

# In[94]:


df_vorm.nunique(axis=0)


# In[95]:


df_vorm.head()


# In[96]:


df_vorm.describe()


# In[97]:


# Selecteren van kolommen
df1 = df_vorm.iloc[:,10:13]
print(df1)


# In[98]:


df_vorm['OPLEIDINGSVORM'].value_counts()


# In[99]:


df_vorm['SOORT_DIPLOMA'].value_counts()


# In[100]:


# Swarmplot van het aantal gediplomeerden per provincie
ax = sns.swarmplot(x=df_vorm['PROVINCIENAAM'],y=df_vorm['AANTAL_GEDIPLOMEERDEN'])
plt.xticks(rotation = 90)
plt.title('Aantal gediplomeerden per provincie')
plt.show()


# In[101]:


# Bar chart van het percentage van het aantal gediplomeerden per soort diploma
x = ['HBO Bachelor', 'HBO Associate Degree', 'HBO Master']
y = [67.8, 14, 18.1]

plt.figure(figsize = (8, 4))
plt.bar(x, y)
plt.title('Percentage aantal gediplomeerden per soort diploma')
plt.xlabel('Soort diploma')
plt.ylabel('Percentage aantal gediplomeerden')
plt.show()


# In[102]:


df4 = df_vorm.groupby('INSTELLINGSNAAM_ACTUEEL')['AANTAL_GEDIPLOMEERDEN'].sum()
print(df4)


# In[103]:


# Bar chart van het aantal gediplomeerden per instelling
df4.plot(kind='bar', title='Aantal gediplomeerden per instelling', figsize=(15, 8))
plt.show()


# In[104]:


df5 = df_vorm['INSTELLINGSNAAM_ACTUEEL']
df5.value_counts()


# In[105]:


# Som van het aantal gediplomeerden per opleidingsvorm
df5 = df_vorm.groupby('OPLEIDINGSVORM')['AANTAL_GEDIPLOMEERDEN'].sum()
print(df5)


# In[106]:


# Bar chart van het percentage van het aantal gediplomeerden per opleidingsvorm
x = ['DT', 'DU', 'VT']
y = [2.77, 3.17, 84.06]

plt.figure(figsize = (8, 4))
plt.bar(x, y)
plt.title('Percentage aantal gediplomeerden per opleidingsvorm')
plt.xlabel('Opleidingsvorm')
plt.ylabel('Percentage aantal gediplomeerden')
plt.show()


# In[107]:


# Slider van het aantal gediplomeerden per provincie per jaar
fig = px.scatter(
    data_frame=df_vorm,
y='AANTAL_GEDIPLOMEERDEN', 
x='DIPLOMAJAAR', 
color='PROVINCIENAAM', 
animation_frame='DIPLOMAJAAR', 
animation_group='PROVINCIENAAM') 

fig.update_layout({
    'yaxis': {'range': [0, 150]},
    'xaxis': {'range': [2013, 2019]}
})


# # 3.5 Crossrefferencing full dataset

# In[108]:


# Kolom namen bekijken
df_Staging.columns


# In[109]:


pd.crosstab(index = df_Staging.DIPLOMAJAAR,
           columns = df_Staging.CROHO_ONDERDEEL)
            


# In[110]:


pd.crosstab(index = df_Staging.DIPLOMAJAAR,
           columns = [df_Staging.CROHO_ONDERDEEL,df_Staging.AANTAL_GEDIPLOMEERDEN])
    


# # 4. Cleaning your dataset
# 

# In[111]:


# Data opschonen
df_cleaned = df_Staging.copy()


# In[112]:


df_Staging.columns


# In[113]:


# Kijken of er dubbele waardes zijn
df_Staging.duplicated()


# In[114]:


df_Staging.duplicated().sum()


# Duplicaten zoeken op specifieke kolommen
# 

# In[115]:


df_Staging.duplicated(subset=['DIPLOMAJAAR','AANTAL_GEDIPLOMEERDEN','CROHO_ONDERDEEL','GESLACHT'], keep='first')


# In[116]:


df_Staging.duplicated(subset=['DIPLOMAJAAR','AANTAL_GEDIPLOMEERDEN','CROHO_ONDERDEEL','GESLACHT'], keep='first').sum()


# In[117]:


df_Staging.isnull().sum()

