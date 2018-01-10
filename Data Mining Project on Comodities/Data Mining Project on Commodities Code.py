# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 09:49:08 2017

@author: andjones
"""
#%%

#read in all packages
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle, islice

#Read in primary commodities dataset and supplementary GDP dataset
Commodities_Raw = pd.read_csv('Commodities_Data_v5.csv') #source World Bank: Global Economic Monitor Commodities (selection UI)
GDP_Raw = pd.read_excel('GDP Constant 2010 USD.xlsx') #source World Bank: GDP Real 2010 USD (selection UI)


#%%
#Line Chart Function - created a function because many line charts are created for the presentation
def linechart(df, ylabel = 'Price in Real 2010 USD', xlabel = 'Year', legend = True, title = 'Commodities', percentage = False):
    try:
        df.drop('Total', inplace = True)
    except ValueError:
        pass
    
    if percentage == False:
        df.plot(legend = legend)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.legend(loc = 'upper center', bbox_to_anchor=(0.5 , -0.15), ncol = 2, fancybox = True, shadow = True)
        plt.show()
    else:
        ax = df.plot(legend = legend)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.legend(loc = 'upper center', bbox_to_anchor=(0.5 , -0.15), ncol = 2, fancybox = True, shadow = True)
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:.0f}%'.format(x*100) for x in vals])
        plt.show()
    


#%% All linechart data  frames are created, sliced and pivoted in this area to faciliate charting at the end

#Create dataframes for: Commodities data removing unecessary columns
Commodities = Commodities_Raw.set_index('Series')
Commodities = Commodities.drop(['Commodity','Unit', 'Series Code', 'Category'], axis = 1 )

#Create dataframes for: GDP by Country in Real 2010 USD
GDP_Constant2010USD = GDP_Raw.set_index('Country Name')
GDP_Constant2010USD = GDP_Constant2010USD.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis = 1)

#Create dataframes for: feeding into most expesnive by measurement type datafarmes
Most_Expensive_Commodity = Commodities_Raw.drop(['Commodity','Series Code','Category'], axis = 1)
Most_Expensive_Commodity = Most_Expensive_Commodity.set_index('Series')

#Create dataframes for: Commodities measured in Metric Tons and Top 10 most expensive within
Metric_Tons = Most_Expensive_Commodity[Most_Expensive_Commodity.Unit == 'Metric Ton']
Metric_Tons = Metric_Tons.drop('Unit', axis = 1)
Metric_Tons_Top10 = Metric_Tons.sort_values(by = '2016', ascending = False).head(n = 10)

#Create dataframes for: Commodites measured in Kilograms, Zinc specific outsized chart, and generalized Top 10 most expensive within
Kilograms = Most_Expensive_Commodity[Most_Expensive_Commodity.Unit == 'Kilograms']
Kilograms = Kilograms.drop('Unit', axis = 1)
Kilograms_Outsized = Kilograms.sort_values(by = '2016', ascending = False).head(n=11)
Kilograms_Top10 = Kilograms_Outsized.tail(n = 10)

#Create dataframes for: commodites percent dataframe that feeds into largest / smallest growth charts as well as focus subject charts
Commodities_Percent = Commodities.pct_change(axis = 1)
Commodities_Percent = Commodities_Percent.drop('DAP, $/mt, real 2010$')

#Create dataframes for: commodites largest growth and smallest growth as a percent
Commodities_LargestGrowth = Commodities_Percent
Commodities_LargestGrowth['Average Growth'] = Commodities_LargestGrowth.mean(axis = 1)
Commodities_LargestGrowth = Commodities_LargestGrowth.sort_values(by = 'Average Growth', ascending = False)
Commodities_LargestGrowth_Top10 = Commodities_LargestGrowth.head(n = 10)
Commodities_SmallestGrowth_Top10 = Commodities_LargestGrowth.tail(n = 10)

#Create dataframes for: Focus Subject OPEC and Oil
Oil = Commodities_Raw[Commodities_Raw.Series == 'Crude oil, avg, spot, $/bbl, real 2010$']
Oil = Oil.drop(['Unit','Commodity','Series Code', 'Category'], axis = 1).set_index('Series')
OPEC_Countries = GDP_Constant2010USD.T.loc[:,['Algeria','Angola','Ecuador','Equatorial Guinea','Gabon','Iraq','Kuwait','Nigeria','Qatar','Saudi Arabia','United Arab Emirates','Iran, Islamic Rep.','Venezuela, RB']]
OPEC_Countries = OPEC_Countries.T

Oil_Percent = Oil.pct_change(axis = 1)
OPEC_Countries_Percent = OPEC_Countries.pct_change(axis = 1)

OPEC_Countries_Percent.loc['Average GDP: OPEC Countries'] = OPEC_Countries_Percent.mean(axis = 0)
OPEC_Countries_Average_Percent = OPEC_Countries_Percent.loc['Average GDP: OPEC Countries']
OPEC_Countries_Average_Percent = pd.DataFrame(OPEC_Countries_Average_Percent).T

OPEC_Transposed = OPEC_Countries_Percent.T
OPEC_Transposed = OPEC_Transposed.reset_index()
Oil_Transposed = Oil_Percent.T
Oil_Transposed = Oil_Transposed.reset_index()
OPEC_Average_Percent = OPEC_Countries_Average_Percent.T
OPEC_Average_Percent = OPEC_Average_Percent.reset_index()

Oil_Transposed['index'] = Oil_Transposed.astype(str)
OPEC_Transposed['index'] = OPEC_Transposed.astype(str)
OPEC_Average_Percent['index']=OPEC_Average_Percent.astype(str)

OPEC_OIL_Combined = OPEC_Transposed.merge(Oil_Transposed).set_index('index')
OPEC_OIL_Combined2 = OPEC_Average_Percent.merge(Oil_Transposed).set_index('index')

#Create dataframes for: Focus Subject Precious Metals
Precious_Metals = Commodities_Percent.loc[['Platinum, $/toz, real 2010$', 'Gold, $/toz, real 2010$','Silver, $/toz, real 2010$'],:].drop('Average Growth', axis =1)

#%%

#Create the Pie charts comparing 1960's to 2016 comparative product makeup
Pie = Commodities_Raw
Pie = Pie.drop(['Unit','Commodity','Series Code', 'Series'], axis = 1).set_index('Category')
Pie_Grouped = Pie.groupby(Pie.index).sum()


Pie_Grouped.plot.pie(y= '1960', autopct='%.2f', legend = False, explode = (0,0.5,0))
plt.show()
Pie_Grouped.plot.pie(y = '2016',autopct='%.2f', legend = False, explode = (0,0.5,0))
plt.show()

#%%

#Create the histogram that will show the distribution of price movements
PercentChange_Histogram = Commodities_Percent.drop(['Average Growth', '1960'], axis = 1)

my_colors = list(islice(cycle(['g', 'g', 'g', 'g', 'g']), None, len(PercentChange_Histogram)))


ax = PercentChange_Histogram.T.plot.hist(bins = 25, legend = False, color = my_colors, title = 'All Commodities YOY Change: Lognormal')
vals = ax.get_xticks()
ax.set_xticklabels(['{:.0f}%'.format(x*100) for x in vals])

#%%
#Pass all dataframes to their respective line chart functions

#These linchart function calls will NOT trip the "else" condition of the plotting function as they use fixed numerical values for the y axis
linechart(Metric_Tons_Top10.T, title = 'Commodities: Most Expensive (mt)')
linechart(Kilograms_Outsized.T, title = 'Commodities: Zinc Dominates and Fluctuates')
linechart(Kilograms_Top10.T, title = 'Commodities: Most Expensive (kg)')

#These linechart function calls will trip the "else" condition of the plotting function as they use a % formatted y axis
linechart(Commodities_Percent.T, ylabel = 'Percent Change', title = 'Commodities: High Variance', legend = False, percentage = True)
linechart(Commodities_LargestGrowth_Top10.T, ylabel = 'Percent Change', title = 'Commodities: Highest Average Growth', percentage = True)
linechart(Commodities_SmallestGrowth_Top10.T, ylabel = 'Percent Change', title = 'Commodities: Lowest Average Growth', percentage = True)
linechart(OPEC_OIL_Combined2, ylabel = 'Percent Change', title = 'OPEC: Oil Price Affect GDP?', percentage = True)
linechart(Precious_Metals.T, ylabel = 'Percent Change', title = 'Precious Metals', percentage = True)
