import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.basemap import Basemap

import statsmodels.api as sm

import os

def get_airbnb_data(city, data_to_fetch):


    """
    Get Calendar, listings and reviews data for a city
    
    INPUT
    city (string) - city to fetch data for
    data_label (string) - which data to fetch: calendar, listings or reviews
                                         
    OUTPUT
    pandas DataFrame
    """
    data_labels = {'calendar': 'calendar.csv', 
                     'listings': 'listings.csv',
                     'reviews': 'reviews.csv'}
        
    return pd.read_csv(os.path.join(city, data_labels[data_to_fetch]))


def to_date_time(col):
    return pd.to_datetime(col)

def to_numeric(col):
    return col.replace('[\$\,\%]', '', regex=True).astype(np.float)

def plot_time_series(dates, prices):
    #create axes and figure
    fig, ax = plt.subplots(figsize=(12,8)) 
    ax.grid(True)

    #Select x-tick locations and x_tick label formatting
    year = mdates.YearLocator(month=1)    
    month = mdates.MonthLocator(interval=2)
    year_format = mdates.DateFormatter('%Y:%m')
    month_format = mdates.DateFormatter('%m')

    #Set x-ticks as selected above
    ax.xaxis.set_minor_locator(month)
    ax.xaxis.grid(True, which='minor')
    ax.xaxis.set_major_locator(year)
    ax.xaxis.set_major_formatter(year_format)

    plt.plot(dates, prices, "-b")
    plt.xlabel('time')
    plt.ylabel('average listing price')


def plot_geographical(latitude_list, longitude_list, distribution_1, distribution_2):

    """
    Overly city geographical map with city listings scatter plot

    INPUT
    latitude_list - latitudes of listings
    longitude_list - longitudes of listings
    distribution_1 - distribution of first feature
    distribution_2 - distribution of second feature
    
    OUTPUT
    matplotlib.Baseplot object overlaid with scatter plt of listings
    """
    lat_0 = latitude_list.min()
    lat_1 = latitude_list.max()
    lon_0 = longitude_list.min()
    lon_1 = longitude_list.max()

    #Set up geographical map of Seattle by projecting actual map onto a cylindrical plane
    fig = plt.figure(figsize=(10,10))
    m = Basemap(projection='cyl', resolution='c', 
                llcrnrlat=lat_0-0.05, urcrnrlat=lat_1+0.05,
               llcrnrlon=lon_0-0.05, urcrnrlon=lon_1+0.05)
    
    #Draw Basemap by plotting coastlines, country lines and county lines 
    m.drawcoastlines(linewidth=1)    
    m.drawcountries(linewidth=1)
    m.drawcounties(color='red', linewidth=1)
    
    #Produce scatter plot on top of Basemap
    m.scatter(longitude_list, latitude_list, c=distribution_1, s=distribution_2*15, cmap='cividis', alpha=0.2)
    
    plt.colorbar(label='price ($)')
    quantile_94 = distribution_1.quantile(0.94)
    plt.clim(0, quantile_94)
    
    #Set up legend for activity distribution 
    for a in [1,3,5]:
        plt.scatter([], [], c='k', alpha=0.5, s=a*15, label=str(a)+' review(s) / month')
        
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc='lower left')

    plt.show()



def drop_cols(df, max_unique_entries = 50, min_unique_entries=2):
    """
    INPUT
    df - pandas dataframe
    max_unique_entries - Drop any column that has unique entries more than max unique entries
    min_unique_entries - Drop any column that contains only 1 unique 
    entry
    
    OUTPUT
    df - modified dataframe
    """
    for col in df.select_dtypes(include=['object']).columns:
        if (df[col].unique().shape[0] > max_unique_entries) or (df[col].unique().shape[0] < min_unique_entries):
            df.drop(col, axis=1, inplace=True)
    return df