# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:45:01 2022

@author: aryan
"""
import pandas as pd
import numpy as np
import scipy.stats as stats

def nhl_correlation():
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    nhl_2018 = nhl_df[(nhl_df['year'] == 2018)]
    nhl_2018 = nhl_2018[['team', 'W', 'L']]

    nhl_2018.drop([0,9,18,26],0,inplace=True)

    for i in nhl_2018.index:  
          nhl_2018.at[i, 'W/L'] = int((nhl_2018.at[i, 'W'])) / (int(nhl_2018.at[i, 'W']) + int(nhl_2018.at[i, 'L']))  

    for i in nhl_2018.index:  
          nhl_2018.at[i, 'team'] = nhl_2018.at[i, 'team'].replace("*", "")

    nhl_2018['city'] = nhl_2018['team']
    nhl_2018['city'] = nhl_2018['city'].map({'Tampa Bay Lightning':'Tampa Bay Area',
         'Boston Bruins':'Boston',
         'Toronto Maple Leafs':'Toronto',
         'Florida Panthers':'Miami–Fort Lauderdale',
         'Detroit Red Wings':'Detroit',
         'Montreal Canadiens':'Montreal',
         'Ottawa Senators':'Ottawa',
         'Buffalo Sabres':'Buffalo',
         'Washington Capitals':'Washington, D.C.',
         'Pittsburgh Penguins':'Pittsburgh',
         'Philadelphia Flyers':'Philadelphia',
         'Columbus Blue Jackets':'Columbus',
         'New Jersey Devils':'New York City',
         'Carolina Hurricanes':'Raleigh',
         'New York Islanders':'New York City',
         'New York Rangers':'New York City',
         'Nashville Predators':'Nashville',
         'Winnipeg Jets':'Winnipeg',
         'Minnesota Wild':'Minneapolis–Saint Paul',
         'Colorado Avalanche':'Denver',
         'St. Louis Blues':'St. Louis',
         'Dallas Stars':'Dallas–Fort Worth',
         'Chicago Blackhawks':'Chicago',
         'Vegas Golden Knights':'Las Vegas',
         'Anaheim Ducks':'Los Angeles',
         'San Jose Sharks':'San Francisco Bay Area',
         'Los Angeles Kings':'Los Angeles',
         'Calgary Flames':'Calgary',
         'Edmonton Oilers':'Edmonton',
         'Vancouver Canucks':'Vancouver',
         'Arizona Coyotes':'Phoenix'})

    cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
    cities.set_index('Metropolitan area', inplace = True)
    nhl_2018.set_index("city", inplace = True)
    nhl_2018_final = nhl_2018.join(cities, how = 'left')
    nhl_2018_final = nhl_2018_final[['W/L', 'Population (2016 est.)[8]']]

    nhl_2018_final['W/L'] = nhl_2018_final['W/L'].apply(lambda x : float(x))
    nhl_2018_final['Population (2016 est.)[8]'] = nhl_2018_final['Population (2016 est.)[8]'].apply(lambda x : float(x))

    repeat= []
    for i in range(0,  nhl_2018_final.shape[0]-1): 
          if ((nhl_2018_final.index[i] == nhl_2018_final.index[i+1]) and (nhl_2018_final.index[i] not in repeat)):
                repeat.append(nhl_2018_final.index[i])

    for i in repeat:
          nhl_2018_final.at[i, 'W/L'] = np.average(nhl_2018_final.at[i, 'W/L'])

    nhl_2018_final = nhl_2018_final[~nhl_2018_final.index.duplicated(keep='first')]

    population_by_region = nhl_2018_final['Population (2016 est.)[8]'].tolist() # pass in metropolitan area population from cities
    win_loss_by_region   = nhl_2018_final['W/L'].tolist() # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]


    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    raise NotImplementedError()
    
    population_by_region = [] # pass in metropolitan area population from cities
    win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


#####################################################################################################################
    
nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nba_correlation():
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    nba_2018 = nba_df[(nba_df['year'] == 2018)]
    nba_2018 = nba_2018[['team', 'W', 'L']]

    for i in nba_2018.index:  
              nba_2018.at[i, 'W/L'] = int((nba_2018.at[i, 'W'])) / (int(nba_2018.at[i, 'W']) + int(nba_2018.at[i, 'L']))  

    for i in nba_2018.index:
          nba_2018.at[i, 'team'] = nba_2018.at[i, 'team'].replace("*", "")
          nba_2018.at[i, 'team'] = nba_2018.at[i, 'team'].replace("(", "")
          nba_2018.at[i, 'team'] = nba_2018.at[i, 'team'].replace(")", "")
          nba_2018.at[i, 'team'] = nba_2018.at[i, 'team'].replace(u"\xa0", u"")
          nba_2018.at[i, 'team'] = nba_2018.at[i, 'team'].rstrip() 
          nba_2018.at[i, 'team'] = ''.join([i for i in nba_2018.at[i, 'team'] if not i.isdigit()])

    nba_2018['city'] = nba_2018['team']
    nba_2018['city'] = nba_2018['city'].map({'Toronto Raptors':'Toronto',
         'Boston Celtics':'Boston',
         'Philadelphia ers':'Philadelphia',
         'Cleveland Cavaliers':'Cleveland',
         'Indiana Pacers':'Indianapolis',
         'Miami Heat':'Miami–Fort Lauderdale',
         'Milwaukee Bucks':'Milwaukee',
         'Washington Wizards':'Washington, D.C.',
         'Detroit Pistons':'Detroit',
         'Charlotte Hornets':'Charlotte',
         'New York Knicks':'New York City',
         'Brooklyn Nets':'New York City',
         'Chicago Bulls':'Chicago',
         'Orlando Magic':'Orlando',
         'Atlanta Hawks':'Atlanta',
         'Houston Rockets':'Houston',
         'Golden State Warriors':'San Francisco Bay Area',
         'Portland Trail Blazers':'Portland',
         'Oklahoma City Thunder':'Oklahoma City',
         'Utah Jazz':'Salt Lake City',
         'New Orleans Pelicans':'New Orleans',
         'San Antonio Spurs':'San Antonio',
         'Minnesota Timberwolves':'Minneapolis–Saint Paul',
         'Denver Nuggets':'Denver',
         'Los Angeles Clippers':'Los Angeles',
         'Los Angeles Lakers':'Los Angeles',
         'Sacramento Kings':'Sacramento',
         'Dallas Mavericks':'Dallas–Fort Worth',
         'Memphis Grizzlies':'Memphis',
         'Phoenix Suns':'Phoenix'})

    cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
    cities.set_index('Metropolitan area', inplace = True)
    nba_2018.set_index("city", inplace = True)
    nba_2018_final = nba_2018.join(cities, how = 'left')
    nba_2018_final = nba_2018_final[['W/L', 'Population (2016 est.)[8]']]

    nba_2018_final['W/L'] = nba_2018_final['W/L'].apply(lambda x : float(x))
    nba_2018_final['Population (2016 est.)[8]'] = nba_2018_final['Population (2016 est.)[8]'].apply(lambda x : float(x))

    repeat= []
    for i in range(0,  nba_2018_final.shape[0]-1): 
          if ((nba_2018_final.index[i] == nba_2018_final.index[i+1]) and (nba_2018_final.index[i] not in repeat)):
                repeat.append(nba_2018_final.index[i])

    for i in repeat:
          nba_2018_final.at[i, 'W/L'] = np.average(nba_2018_final.at[i, 'W/L'])

    nba_2018_final = nba_2018_final[~nba_2018_final.index.duplicated(keep='first')]
    
    
    population_by_region = nba_2018_final['Population (2016 est.)[8]'].tolist() # pass in metropolitan area population from cities
    win_loss_by_region   = nba_2018_final['W/L'].tolist() # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

######################################################################################################################################
mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def mlb_correlation(): 
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    mlb_2018 = mlb_df[(mlb_df['year'] == 2018)]
    mlb_2018 = mlb_2018[['team', 'W', 'L']]

    for i in mlb_2018.index:  
              mlb_2018.at[i, 'W/L'] = int((mlb_2018.at[i, 'W'])) / (int(mlb_2018.at[i, 'W']) + int(mlb_2018.at[i, 'L']))  

    for i in mlb_2018.index:
          mlb_2018.at[i, 'team'] = mlb_2018.at[i, 'team'].replace("*", "")
          mlb_2018.at[i, 'team'] = mlb_2018.at[i, 'team'].replace("(", "")
          mlb_2018.at[i, 'team'] = mlb_2018.at[i, 'team'].replace(")", "")
          mlb_2018.at[i, 'team'] = mlb_2018.at[i, 'team'].replace(u"\xa0", u"")
          mlb_2018.at[i, 'team'] = mlb_2018.at[i, 'team'].rstrip() 
          mlb_2018.at[i, 'team'] = ''.join([i for i in mlb_2018.at[i, 'team'] if not i.isdigit()])


    mlb_2018['city'] = mlb_2018['team']
    mlb_2018['city'] = mlb_2018['city'].map({'Boston Red Sox':'Boston',
         'New York Yankees':'New York City',
         'Tampa Bay Rays':'Tampa Bay Area',
         'Toronto Blue Jays':'Toronto',
         'Baltimore Orioles':'Baltimore',
         'Cleveland Indians':'Cleveland',
         'Minnesota Twins':'Minneapolis–Saint Paul',
         'Detroit Tigers':'Detroit',
         'Chicago White Sox':'Chicago',
         'Kansas City Royals':'Kansas City',
         'Houston Astros':'Houston',
         'Oakland Athletics':'San Francisco Bay Area',
         'Seattle Mariners':'Seattle',
         'Los Angeles Angels':'Los Angeles',
         'Texas Rangers':'Dallas–Fort Worth',
         'Atlanta Braves':'Atlanta',
         'Washington Nationals':'Washington, D.C.',
         'Philadelphia Phillies':'Philadelphia',
         'New York Mets':'New York City',
         'Miami Marlins':'Miami–Fort Lauderdale',
         'Milwaukee Brewers':'Milwaukee',
         'Chicago Cubs':'Chicago',
         'St. Louis Cardinals':'St. Louis',
         'Pittsburgh Pirates':'Pittsburgh',
         'Cincinnati Reds':'Cincinnati',
         'Los Angeles Dodgers':'Los Angeles',
         'Colorado Rockies':'Denver',
         'Arizona Diamondbacks':'Phoenix',
         'San Francisco Giants':'San Francisco Bay Area',
         'San Diego Padres':'San Diego'})


    cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
    cities.set_index('Metropolitan area', inplace = True)
    mlb_2018.set_index("city", inplace = True)
    mlb_2018_final = mlb_2018.join(cities, how = 'left')
    mlb_2018_final = mlb_2018_final[['W/L', 'Population (2016 est.)[8]']]

    mlb_2018_final['W/L'] = mlb_2018_final['W/L'].apply(lambda x : float(x))
    mlb_2018_final['Population (2016 est.)[8]'] = mlb_2018_final['Population (2016 est.)[8]'].apply(lambda x : float(x))

    repeat= []
    for i in range(0,  mlb_2018_final.shape[0]-1): 
          if ((mlb_2018_final.index[i] == mlb_2018_final.index[i+1]) and (mlb_2018_final.index[i] not in repeat)):
                repeat.append(mlb_2018_final.index[i])

    for i in repeat:
          mlb_2018_final.at[i, 'W/L'] = np.average(mlb_2018_final.at[i, 'W/L'])

    mlb_2018_final = mlb_2018_final[~mlb_2018_final.index.duplicated(keep='first')]

    population_by_region = mlb_2018_final['Population (2016 est.)[8]'].tolist() # pass in metropolitan area population from cities
    win_loss_by_region   = mlb_2018_final['W/L'].tolist() # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]


    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

##############################################################################################################################
    
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nfl_correlation(): 
    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    nfl_2018 = nfl_df[(nfl_df['year'] == 2018)]
    nfl_2018 = nfl_2018[['team', 'W', 'L']]

    inval = []
    for i in nfl_2018.index:
          nfl_2018.at[i, 'team'] = nfl_2018.at[i, 'team'].replace("*", "")
          nfl_2018.at[i, 'team'] = nfl_2018.at[i, 'team'].replace("(", "")
          nfl_2018.at[i, 'team'] = nfl_2018.at[i, 'team'].replace(")", "")
          nfl_2018.at[i, 'team'] = nfl_2018.at[i, 'team'].replace(u"\xa0", u"")
          nfl_2018.at[i, 'team'] = nfl_2018.at[i, 'team'].replace("+", "")
          nfl_2018.at[i, 'team'] = nfl_2018.at[i, 'team'].rstrip() 

          if (nfl_2018.at[i, "W"].rstrip().isdigit() == False):
                inval.append(i)

    nfl_2018.drop(inval,0,inplace=True)

    for i in nfl_2018.index:  
          nfl_2018.at[i, 'W/L'] = int((nfl_2018.at[i, 'W'])) / (int(nfl_2018.at[i, 'W']) + int(nfl_2018.at[i, 'L']))  

    nfl_2018['city'] = nfl_2018['team']
    nfl_2018['city'] = nfl_2018['city'].map({'New England Patriots':'Boston',
         'Miami Dolphins':'Miami–Fort Lauderdale',
         'Buffalo Bills':'Buffalo',
         'New York Jets':'New York City',
         'Baltimore Ravens':'Baltimore',
         'Pittsburgh Steelers':'Pittsburgh',
         'Cleveland Browns':'Cleveland',
         'Cincinnati Bengals':'Cincinnati',
         'Houston Texans':'Houston',
         'Indianapolis Colts':'Indianapolis',
         'Tennessee Titans':'Nashville',
         'Jacksonville Jaguars':'Jacksonville',
         'Kansas City Chiefs':'Kansas City',
         'Los Angeles Chargers':'Los Angeles',
         'Denver Broncos':'Denver',
         'Oakland Raiders':'San Francisco Bay Area',
         'Dallas Cowboys':'Dallas–Fort Worth',
         'Philadelphia Eagles':'Philadelphia',
         'Washington Redskins':'Washington, D.C.',
         'New York Giants':'New York City',
         'Chicago Bears':'Chicago',
         'Minnesota Vikings':'Minneapolis–Saint Paul',
         'Green Bay Packers':'Green Bay',
         'Detroit Lions':'Detroit',
         'New Orleans Saints':'New Orleans',
         'Carolina Panthers':'Charlotte',
         'Atlanta Falcons':'Atlanta',
         'Tampa Bay Buccaneers':'Tampa Bay Area',
         'Los Angeles Rams':'Los Angeles',
         'Seattle Seahawks':'Seattle',
         'San Francisco 49ers':'San Francisco Bay Area',
         'Arizona Cardinals':'Phoenix'}) 


    cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
    cities.set_index('Metropolitan area', inplace = True)
    nfl_2018.set_index("city", inplace = True)
    nfl_2018_final = nfl_2018.join(cities, how = 'left')
    nfl_2018_final = nfl_2018_final[['W/L', 'Population (2016 est.)[8]']]

    nfl_2018_final['W/L'] = nfl_2018_final['W/L'].apply(lambda x : float(x))
    nfl_2018_final['Population (2016 est.)[8]'] = nfl_2018_final['Population (2016 est.)[8]'].apply(lambda x : float(x))

    repeat= []
    for i in range(0,  nfl_2018_final.shape[0]-1): 
          if ((nfl_2018_final.index[i] == nfl_2018_final.index[i+1]) and (nfl_2018_final.index[i] not in repeat)):
                repeat.append(nfl_2018_final.index[i])

    for i in repeat:
          nfl_2018_final.at[i, 'W/L'] = np.average(nfl_2018_final.at[i, 'W/L'])

    nfl_2018_final = nfl_2018_final[~nfl_2018_final.index.duplicated(keep='first')]

    population_by_region = nfl_2018_final['Population (2016 est.)[8]'].tolist() # pass in metropolitan area population from cities
    win_loss_by_region   = nfl_2018_final['W/L'].tolist() # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]


    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q3: There should be 26 teams being analysed for nfl"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

