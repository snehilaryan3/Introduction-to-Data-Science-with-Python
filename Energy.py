# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 10:47:04 2022

@author: aryan
"""


'''### Question 1
Load the energy data from the file `assets/Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](assets/Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **Energy**.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

`['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`

Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**). For all countries which have  missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.

Rename the following list of countries (for use in later questions):

```"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"```

There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.  `'Switzerland17'` should be `'Switzerland'`.

Next, load the GDP data from the file `assets/world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 

Make sure to skip the header, and rename the following list of countries:

```"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"```

Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `assets/scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index', 'Energy Supply',
       'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

*This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".*

'''

import pandas as pd 
import numpy as np 
import re


Energy = pd.read_excel("assets\Energy Indicators.xls")
GDP    = pd.read_csv("assets\world_bank.csv",header = 4)
ScimEn = pd.read_excel("assets\scimagojr-3.xlsx")


def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls")
    GDP    = pd.read_csv("assets/world_bank.csv",header = 4)
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


###################################Cleaning Energy Data ##########################################

    Energy = Energy.iloc[17:244]
    Energy = Energy[["Unnamed: 1","Unnamed: 3", "Unnamed: 4", "Unnamed: 5" ]]
    Energy.rename(columns = {'Unnamed: 1' : 'Country', 
               'Unnamed: 3' : 'Energy Supply',
               'Unnamed: 4' : 'Energy Supply per Capita', 
               'Unnamed: 5' : '% Renewable'}, inplace = True)

    Energy['Energy Supply'] = Energy['Energy Supply'].replace("...", np.nan)
    Energy['Energy Supply per Capita'] = Energy['Energy Supply per Capita'].replace("...", np.nan)
    Energy['Energy Supply'] = Energy['Energy Supply'].transform(lambda x: x * 1000000)
    Energy['Country'] = Energy['Country'].replace(" ", '')

    Energy['Country'] = Energy['Country'].replace({'Republic of Korea' : 'South Korea',
                                                'United States of America' : "United States",
                                                'United Kingdom of Great Britain and Northern Ireland' : "United Kingdom",
                                                'China, Hong Kong Special Administrative Region' : "Hong Kong"})
      
    Energy['Country'] = Energy['Country'].transform(lambda x : re.sub(r'\([^)]*\)','', x))
    Energy['Country'] = Energy['Country'].transform(lambda x : ''.join(i for i in x if not i.isdigit()))
    Energy['Country'] = Energy['Country'].transform(lambda x : x.rstrip())
      
######################Cleaning World Bank Data################################################### 

    GDP.rename(columns = {'Country Name' : 'Country'}, inplace = True)

    GDP['Country'] = GDP['Country'].replace({'Korea, Rep.' : "South Korea",
                                          'Iran, Islamic Rep.' : "Iran", 
                                          'Hong Kong SAR, China' : "Hong Kong" })
            
######################Merging the Datasets#######################################################

    Energy.set_index('Country', inplace = True)  
    GDP.set_index('Country', inplace = True)            
    ScimEn.set_index('Country', inplace = True) 

###Filtering only top 15 countries###

    ScimEn = ScimEn[ScimEn['Rank'] <= 15] 

    temp_df1 = ScimEn.merge(Energy, how = 'left', on='Country')   

    def pick_cols_year(cur_year, offset, interval):
        cols_last_off = [cur_year]
        for i in range (0, offset-1):
            cur_year = str((pd.Timestamp(cur_year) - pd.DateOffset(years = interval)).year)
            cols_last_off.append(cur_year)
            
        return [ele for ele in reversed(cols_last_off)]
            
    cols_last_ten = pick_cols_year('2015', 10, 1)

    GDP = GDP[cols_last_ten]

    df = temp_df1.merge(GDP, how = 'left', on = 'Country')


    return df


####################################################################################################################
'''
Question 2
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?

This function should return a single number.
'''



###################################################################################################################          
'''            
Question 3
What are the top 15 countries for average GDP over the last 10 years?

This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
'''    
                
top_cont = answer_one()

#def pick_cols_year(cur_year, offset, interval):
#        cols_last_off = [cur_year]
#        for i in range (0, offset-1):
#            cur_year = str((pd.Timestamp(cur_year) - pd.DateOffset(years = interval)).year)
#            cols_last_off.append(cur_year)
#            
#        return [ele for ele in reversed(cols_last_off)]
#            
#cols_last_ten = pick_cols_year('2015', 10, 1)
#
#top_cont = top_cont[cols_last_ten]
#top_cont["Average_GDP"] = top_cont.agg(np.mean, axis = 1)
#
#avgGDP = top_cont["Average_GDP"].sort_values(ascending=False)

def answer_three():
    import pandas as pd 
    import numpy as np
    
    top_cont = answer_one()

    def pick_cols_year(cur_year, offset, interval):
            cols_last_off = [cur_year]
            for i in range (0, offset-1):
                cur_year = str((pd.Timestamp(cur_year) - pd.DateOffset(years = interval)).year)
                cols_last_off.append(cur_year)
            
            return [ele for ele in reversed(cols_last_off)]
            
    cols_last_ten = pick_cols_year('2015', 10, 1)

    top_cont = top_cont[cols_last_ten]
    top_cont["Average_GDP"] = top_cont.agg(np.mean, axis = 1)

    avgGDP = top_cont["Average_GDP"].sort_values(ascending=False)

    return avgGDP


#####################################################################################################################
'''
Question 4
By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

This function should return a single number.
'''
#top_cont = answer_one()
#avg_gd   = answer_three()
#
#temp_df = top_cont.merge(avg_gd, on = 'Country')
#temp_df.sort_values(by = ["Average_GDP"], ascending=False, inplace = True)
#res = temp_df.iloc[5]['2015'] - temp_df.iloc[5]['2006'] 

def answer_four():
    top_cont = answer_one()
    avg_gd   = answer_three()

    temp_df = top_cont.merge(avg_gd, on = 'Country')
    temp_df.sort_values(by = ["Average_GDP"], ascending=False, inplace = True)
    
    return temp_df.iloc[5]['2015'] - temp_df.iloc[5]['2006']

'''
Question 5
What is the mean energy supply per capita?

This function should return a single number.
'''

def answer_five():
    top_cont = answer_one()
    sum = 0
    for i in range (0, top_cont.shape[0]):
        sum = sum + top_cont.iloc[i]["Energy Supply per Capita"]
      
    return sum/top_cont.shape[0]

'''
Question 6
What country has the maximum % Renewable and what is the percentage?

This function should return a tuple with the name of the country and the percentage.
'''

#top_cont = answer_one()
#top_cont = top_cont[top_cont['% Renewable'] == np.max(top_cont['% Renewable'])]
#top_cont.filter(items = ['Country', '% Renewable'])
#
#res = (top_cont.index[0], top_cont.iloc[0]['% Renewable'])

def answer_six():
    top_cont = answer_one()
    top_cont = top_cont[top_cont['% Renewable'] == np.max(top_cont['% Renewable'])]
    top_cont.filter(items = ['Country', '% Renewable'])

    return (top_cont.index[0], top_cont.iloc[0]['% Renewable']) 


'''
Question 7
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?

This function should return a tuple with the name of the country and the ratio.
'''

#top_cont = answer_one()
#
#for i in top_cont.index:
#      
#      x = top_cont.at[i,'Self-citations']/top_cont.at[i, 'Citations']
#      top_cont.at[i,"Self to Totla Citation"] = x 
#
#top_cont = top_cont[top_cont['Self to Totla Citation'] == np.max(top_cont['Self to Totla Citation'])]
#top_cont.filter(items = ['Country', 'Self to Totla Citation'])
#
#res = (top_cont.index[0], top_cont.iloc[0]['Self to Totla Citation'])

def answer_seven():
    top_cont = answer_one()
    for i in top_cont.index:  
        top_cont.at[i,"Self to Totla Citation"] = top_cont.at[i,'Self-citations']/top_cont.at[i, 'Citations']

    top_cont = top_cont[top_cont['Self to Totla Citation'] == np.max(top_cont['Self to Totla Citation'])]
    top_cont.filter(items = ['Country', 'Self to Totla Citation'])

    return (top_cont.index[0], top_cont.iloc[0]['Self to Totla Citation'])
    raise NotImplementedError()
    
answer_seven()
##############################################################################################################################
'''
Question 8
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?

This function should return the name of the country
'''

def answer_eight():
      top_cont = answer_one()
      for i in top_cont.index:
            top_cont.at[i, "Population Estimate"] = top_cont.at[i, "Energy Supply"] / top_cont.at[i, "Energy Supply per Capita"]
    
      top_cont.sort_values(by = 'Population Estimate', ascending = False, inplace = True)        
      
      top_cont = top_cont[top_cont['Population Estimate'] == top_cont.iloc[2]['Population Estimate']]
      return top_cont.filter(items = ['Country']).index[0]


########################################################################################################################################
'''
Question 9
Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).

This function should return a single number.

(Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)
'''
def answer_nine():
    top_cont = answer_one()
    for i in top_cont.index:
        top_cont.at[i, "Citable Documents per Person"] = top_cont.at[i, 'Citations']/(top_cont.at[i, "Energy Supply"] / top_cont.at[i, "Energy Supply per Capita"])
      
    top_cont = top_cont[['Citable Documents per Person', 'Energy Supply per Capita']]
    return top_cont.corr(method = 'pearson').iloc[0]['Energy Supply per Capita']
    raise NotImplementedError()
    
def plot9():
    import matplotlib as plt
    %matplotlib inline
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

plot9()
##################################################################################################################################
'''
Question 10
Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.
'''
top_cont = answer_one()

for i in top_cont.index:
      
      if(top_cont.at[i, "% Renewable"] >= np.median(top_cont["% Renewable"])):
            top_cont.at[i, "HighRenew"] = 1
      
      else :
            top_cont.at[i, "HighRenew"] = 0
            
res = top_cont["HighRenew"]
#################################################################################################################################
'''
Question 11
Use the following dictionary to group the Countries by Continent, then create a DataFrame that 
displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
This function should return a DataFrame with index named Continent 
['Asia', 'Australia', 'Europe', 'North America', 'South America'] and 
columns ['size', 'sum', 'mean', 'std']
'''

top_cont = answer_one()
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

for i in top_cont.index:
      top_cont.at[i, 'Continent'] = ContinentDict[i]
      
for i in top_cont.index:
        top_cont.at[i, "Population Estimate"] = top_cont.at[i, "Energy Supply"] / top_cont.at[i, "Energy Supply per Capita"]

x = top_cont.groupby('Continent').size()
top_cont.set_index('Continent', inplace = True)

cols = {'size' : np.size,
        'sum': np.sum,
        'mean' : np.mean,
        'std' : np.std} 

result = top_cont.groupby(level=0)['Population Estimate'].agg(cols)
############################################################################################################################
'''
Question 12
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. 
How many countries are in each of these groups?

This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. 
Do not include groups with no countries.      
'''

def answer_twelve():
    top_cont = answer_one()

    top_cont = answer_one()
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

    for i in top_cont.index:
        top_cont.at[i, 'Continent'] = ContinentDict[i]
    top_cont.set_index(['Continent', '% Renewable'])
    top_cont['% Renewable'] = pd.cut(top_cont['% Renewable'], 5)

    return top_cont.groupby(by = ['Continent', '% Renewable']).size()

    raise NotImplementedError()

answer_twelve()

#########################################################################################################################

'''Question 13
Convert the Population Estimate series to a string with thousands separator (using commas). 
Use all significant digits (do not round the results).

e.g. 12345678.90 -> 12,345,678.90

This function should return a series 
PopEst whose index is the country name and whose values are the population estimate string
'''


top_cont = answer_one()
for i in top_cont.index:
      top_cont.at[i, "Population Estimate"] = str(top_cont.at[i, "Energy Supply"] / top_cont.at[i, "Energy Supply per Capita"])

      
for i in top_cont.index:
      x = "{:,}".format(float(top_cont.at[i, "Population Estimate"]))
      top_cont.at[i, "Population Estimate"] = x
      
PopEst = top_cont["Population Estimate"]



























