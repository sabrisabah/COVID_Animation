import pycountry
import pandas as pd
import urllib.request

from datetime import datetime
timenow = datetime.now()
timenow_iso = timenow.strftime('%Y-%m-%dT%H:%M:%S')

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
output = '1.csv'
urllib.request.urlretrieve(url, output)

# Aggregate the dataset
df_confirm = pd.read_csv('C:\\project\\timeline\\1.csv')  
df_confirm = df_confirm.drop(columns=['Province/State','Lat', 'Long'])
df_confirm = df_confirm.groupby('Country/Region').agg('sum')
date_list = list(df_confirm.columns)

def get_country_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None

df_confirm['country'] = df_confirm.index
df_confirm['iso_alpha_3'] = df_confirm['country'].apply(get_country_code)

df_long = pd.melt(df_confirm, id_vars=['country','iso_alpha_3'], value_vars=date_list)
import plotly.express as px


fig = px.choropleth(df_long,                            # Input Dataframe
                     locations="iso_alpha_3",           # identify country code column
                     color="value",                     # identify representing column
                     hover_name="country",              # identify hover name
                     animation_frame="variable",        # identify date column
                     projection="natural earth",        # select projection
                     color_continuous_scale = 'Peach',  # select prefer color scale
                     range_color=[0,50000]              # select range of dataset
                     )        
fig.show()          
fig.write_html("eworld.html")           
