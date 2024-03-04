import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from django.conf import settings
import os
import warnings
import time
from datetime import datetime

warnings.filterwarnings("ignore")
#from datetime import date
import re
import requests
from scrapy.selector import Selector
import json
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
myheaders = {'User-Agent': user_agent} 

def stripgame(gameid):

    printdf = True
    printdict = False

    # strip initial dataframes from espn url
    url = f'https://www.espn.com/mens-college-basketball/boxscore/_/gameId/{gameid}'
    # If the game has not started, blank dictionaries and lists will return
    try:
        game = pd.read_html(url)
    except Exception:
        print('GAME HAS NOT STARTED')
        file_path = os.path.join(settings.MEDIA_ROOT+'/gamesdata', gameid+'.json')
        data ={
            'totalscoredict':{},
            'hometeamdict':{},
            'awayteamdict':{},
            'homeplayernamelist':[],
            'awayplayernamelist':[]

        }

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return {}, {}, {}, [], []
        

    # total score
    totalscoredf = game[0]
    totalscoredf = totalscoredf.rename(columns={'Unnamed: 0': 'name'})
    hometeamname = totalscoredf.loc[0][0]
    awayteamname = totalscoredf.loc[1][0]
    totalscoredf = totalscoredf.rename(index={0: hometeamname})
    totalscoredf = totalscoredf.rename(index={1: awayteamname})
    totalscoredf = totalscoredf.drop(totalscoredf.columns[0], axis=1)
    if (printdf or printdict): print(f'{hometeamname} vs {awayteamname}')
    if printdf: print(totalscoredf)

    totalscoredict = totalscoredf.to_dict()
    if printdict: print(json.dumps(totalscoredict,indent=2))

    # Strip Hometeam player stats
    game[1] = game[1].reset_index()
    game[2] = game[2].reset_index()
    df = pd.merge(game[1], game[2], on='index')
    df = df.drop(columns='index')

    # reset header
    new_header = df.iloc[0]  # grab the first row for the header
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header

    # drop column useless middle column
    df = df.drop([6]).reset_index().drop(columns='index')
    df = df.drop(index=df.index[-1], axis=0)

    # create better name list w/o position at the end
    homeplayernamelist = []
    for player in df['starters']:
        player = player[:-2]
        #print(player)
        homeplayernamelist.append(player)
    playernamelistdf = pd.DataFrame(homeplayernamelist)
    playernamelistdf = playernamelistdf.reset_index()
    df = df.reset_index()
    df = pd.merge(playernamelistdf, df, on='index')
    df = df.drop(columns='index').drop(columns='starters')
    df = df.rename(columns={0: 'player'})

    hometeamplayerstats = df
    if printdf: print(hometeamplayerstats)

    # create dictionary of Hometeamplayerstats
    hometeamdict = hometeamplayerstats.transpose()
    new_header = hometeamdict.iloc[0]  # grab the first row for the header
    hometeamdict = hometeamdict[1:]  # take the data less the header row
    hometeamdict.columns = new_header  # set the header row as the df header
    hometeamdict = hometeamdict.to_dict()
    if printdict: print(json.dumps(hometeamdict,indent=2))

    # Strip Awayteam player stats
    game[3] = game[3].reset_index()
    game[4] = game[4].reset_index()
    df = pd.merge(game[3], game[4], on='index')
    df = df.drop(columns='index')

    # new header
    new_header = df.iloc[0]  # grab the first row for the header
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header
    # drop useless column
    df = df.drop([6]).reset_index().drop(columns='index')
    df = df.drop(index=df.index[-1], axis=0)
    
    # create better name list w/o position at the end
    awayplayernamelist = []
    for player in df['starters']:
        player = player[:-2]
        awayplayernamelist.append(player)
    playernamelistdf = pd.DataFrame(awayplayernamelist)
    playernamelistdf = playernamelistdf.reset_index()
    df = df.reset_index()
    df = pd.merge(playernamelistdf, df, on='index')
    df = df.drop(columns='index').drop(columns='starters')
    df = df.rename(columns={0: 'player'})

    awayteamplayerstats = df
    if printdf: print(awayteamplayerstats)

    # create dictionary of Awayteamplayerstats
    awayteamdict = awayteamplayerstats.transpose()
    new_header = awayteamdict.iloc[0]  # grab the first row for the header
    awayteamdict = awayteamdict[1:]  # take the data less the header row
    awayteamdict.columns = new_header  # set the header row as the df header
    awayteamdict = awayteamdict.to_dict()
    if printdict: print(json.dumps(awayteamdict,indent=2))

    # extractgamestats
    comparisonurl = re.sub("boxscore", "matchup", url)
    game = pd.read_html(comparisonurl)
    df = game[1].rename(columns={'Unnamed: 1': f'{hometeamname}', 'Unnamed: 2': f'{awayteamname}'}).transpose()

    # reset header
    new_header = df.iloc[0]  # grab the first row for the header
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header
    if printdf: print(df)
    if printdict: print(json.dumps(df.to_dict(),indent=2))

    if (printdict or printdf): print(homeplayernamelist)
    if (printdict or printdf): print(awayplayernamelist)
    
    file_path = os.path.join(settings.MEDIA_ROOT+'/gamesdata', gameid+'.json')
    data ={
        'totalscoredict':totalscoredict,
        'hometeamdict':hometeamdict,
        'awayteamdict':awayteamdict,
        'homeplayernamelist':homeplayernamelist,
        'awayplayernamelist':awayplayernamelist

    }

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    #return totalscoredict, hometeamdict, awayteamdict, homeplayernamelist, awayplayernamelist



def schedule_api():
    #stripgame
    print('hello')
    media_path = os.path.join(settings.MEDIA_ROOT+'/gamesdata', 'gameIDdictionary.json')

    with open(media_path, 'r') as file:
        games_data = json.load(file)
        
    # Get today's date in the format used in the JSON data
    today_date_str = datetime.today().strftime("%a, %b %d")
    # Filter games happening today
    for i in games_data.items():
        if(i[1]['date']==today_date_str):
            stripgame(i[0])
def get_gameid():
    print('getting game')

    url = 'https://www.espn.com/mens-college-basketball/teams'
    reqs = requests.get(url,headers=myheaders)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    teamnamelist = []
    teamidlist = []
    for link in soup.find_all('a'):
        newlink = link.get('href')
        newlink = str(newlink)
        string = '/team/_/id/'
        if string in newlink:
            teamname = newlink.split('/')[-1]
            teamname = re.sub("-", " ", teamname)
            teamname = ' '.join(elem.capitalize() for elem in teamname.split())
            teamnamelist.append(teamname)
            teamid = newlink.split('/')[-2]
            teamidlist.append(teamid)
            print(f'team:{teamname} ---- id: {teamid}')

    teamnamedf = pd.DataFrame(teamnamelist).reset_index()
    teamidlist = pd.DataFrame(teamidlist).reset_index()
    df = pd.merge(teamnamedf,teamidlist,on='index')
    df = df.drop(columns='index').rename(columns = {'0_x':'teamname','0_y':'id'})
    teamnameiddf = df.drop_duplicates().reset_index().drop(columns='index')
    print(teamnameiddf)
    teamnameiddf['rosterlist'] = ''
    rosterlist = []
    fullnamerosterlist = []
    rosterlistdictlist = []
    for teamid in teamnameiddf['id']:
        print(teamid)
        try:
            df = pd.read_html(f'https://www.espn.com/mens-college-basketball/team/roster/_/id/{teamid}')
        except ValueError as ve:
            print(f"Error reading HTML table: {ve}")
            namelist = ['No Roster Available']
            fullnamelist = ['No Roster Available']
            rosterlistdict = {'No Roster Available': 'No Roster Available'}
            df = pd.DataFrame({'Name': namelist})  # Create a simple DataFrame with 'Name' column
            print('No roster')
            rosterlist.append(namelist)
            fullnamerosterlist.append(fullnamelist)
            rosterlistdictlist.append(rosterlistdict)
            namelistdf = pd.DataFrame(namelist).rename(columns={0:'name'}).reset_index()
        else:    
            df = df[0].drop(columns='Unnamed: 0').reset_index()
            namelist = []
            fullnamelist = []
            i = 0
            rosterlistdict = {}
            for name in df['Name']:
                pattern = r'[0-9]'
                name = re.sub(pattern, '', name)
                fullname = name
                fullnamelist.append(name)
                #get the first initial and last name of the player
                # Pattern to match the first space character and capture the rest
                pattern = re.compile(r'^\S+\s(.*)$')
                # Use the pattern to search for a match in the input string
                player = pattern.search(fullname)
                player = player.group(1)
                player = fullname.split()[0][0] + '. ' + player
                namelist.append(player)
                rosterlistdict[player] = fullname
                
            rosterlist.append(namelist)
            fullnamerosterlist.append(fullnamelist)
            rosterlistdictlist.append(rosterlistdict)
            namelistdf = pd.DataFrame(namelist).rename(columns={0:'name'}).reset_index()
            df = pd.merge(namelistdf,df,on='index')
            df = df.drop(columns='index').drop(columns = 'Name').rename(columns={'name':'Name'}).drop(columns=['POS','HT','WT','Class','Birthplace'])

    teamnameiddf['rosterlist'] = rosterlist
    teamnameiddf['fullnamerosterlist'] = fullnamerosterlist
    teamnameiddf['rosterlistdictionary'] = rosterlistdictlist
    # teamnameiddf.to_excel('teamnameidroster.xlsx')
    # print(teamnameiddf)

    import json
    newteamnameiddf = teamnameiddf
    newteamnameiddf = newteamnameiddf.drop(columns = 'rosterlist').drop(columns = 'fullnamerosterlist').drop(columns = 'teamname')
    print(newteamnameiddf)
    teamidrosterdict = {}
    for index,row in newteamnameiddf.iterrows():
        teamid = row['id']
        rosterdict = row['rosterlistdictionary']
        teamidrosterdict[teamid] = rosterdict
    teamidrosterdict
    # with open('teamidrosterdict.json', 'w') as fp:
    #     json.dump(teamidrosterdict, fp)

    #opens schedule of specific teamid
    gameiddict1 = {}
    for teamid in teamnameiddf['id']:
        gametimelist = []
        url = f'https://www.espn.com/mens-college-basketball/team/schedule/_/id/{teamid}'

        #scrapes all the urls on the website
        reqs = requests.get(url,headers=myheaders)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        #get the times out of the links
        times = pd.read_html(url)
        times = times[0]
        times = times.rename(columns = {0:'Date',1:'Opponent',2:'Time'})

        # Get all the dates of the games
        for i,row in times.iterrows():
            line = str(times['Date'][i])
            if len(line) < 10 or len(line)> 11:
                times = times.drop(labels=[i],axis=0)
        times = times.reset_index().drop(columns='index').drop(columns=3).drop(columns=4).drop(columns=5).drop(columns=6).drop(columns=7).drop(columns = 'Opponent').drop(columns = 'Time')
        times = times.reset_index()
        # Add dates to list
        for date in times['Date']:
            gametimelist.append(date)
        i = 0
        #goes through each link on page
        for link in soup.find_all('a'):
            newlink = link.get('href')
            newlink = str(newlink)

            #keeps only the right links for games
            string = 'game/_/gameId/'

            #extracts gameid from the game links
            if string in newlink:
                gameid = newlink.split('/')[-1]

                #add game id to the list
                if gameid in gameiddict1.keys():
                    teamid2 = {}
                    teamid2['teamid2'] = teamid
                    gameiddict1[f'{gameid}'] += [teamid2]
                else:
                    teamid1 = {}
                    teamid1['teamid1'] = teamid
                    gameiddict1[f'{gameid}'] = [teamid1]
                    gamedate = {}
                    gamedate['date'] = gametimelist[i]
                    gameiddict1[f'{gameid}'] += [gamedate]
                i = i + 1
                #print(f'team:{teamname} ---- id: {teamid}')

    # clean up the data by getting rid of games with only 1 game id
    import json
    gameiddict2 = gameiddict1
    for k in list(gameiddict2.keys()):
        if len(gameiddict2[k]) < 3:
            del gameiddict2[k]

    niceprint = json.dumps(gameiddict2,indent=3)
    print(len(gameiddict2))
    print(niceprint)
    #gameiddict2

    newdict2 = pd.DataFrame.from_dict(gameiddict2).transpose().reset_index().rename(columns = {'index':'gameid',0:'teamID1',1:'date',2:'teamID2'})
    teamid1list = []
    teamid2list = []
    datelist = []
    for value in newdict2['teamID1']:
        value = value['teamid1']
        teamid1list.append(value)
    for value in newdict2['teamID2']:
        value = value['teamid2']
        teamid2list.append(value)
    for value in newdict2['date']:
        value = value['date']
        datelist.append(value)
    newdict2['teamID1'] = teamid1list
    newdict2['teamID2'] = teamid2list
    newdict2['date'] = datelist
    gameiddf = newdict2
    #display(newdict2)

    gameiddfnew = pd.merge(gameiddf,teamnameiddf,left_on='teamID1',right_on='id',how='left')
    gameiddfnew = gameiddfnew.rename(columns = {'teamname':'teamID1name','rosterlist':'teamID1roster'}).drop(columns = 'id')
    gameiddfnew = pd.merge(gameiddfnew,teamnameiddf,left_on = 'teamID2',right_on='id',how='left')
    gameiddfnew = gameiddfnew.rename(columns = {'teamname':'teamID2name','rosterlist':'teamID2roster'}).drop(columns = 'id')
    gameiddfnew['gamename'] = gameiddfnew['teamID1name'] + ' vs ' + gameiddfnew['teamID2name']

    gameIDdictionary = gameiddfnew.transpose()
    new_header = gameIDdictionary.iloc[0] #grab the first row for the header
    gameIDdictionary = gameIDdictionary[1:] #take the data less the header row
    gameIDdictionary.columns = new_header #set the header row as the df header
    #display(gameIDdictionary)
    gameIDdictionary = gameIDdictionary.to_dict()
    import json
    media_path = os.path.join(settings.MEDIA_ROOT+'/gamesdata', 'gameIDdictionary.json')

    with open(media_path, 'w') as fp:
        json.dump(gameIDdictionary, fp)
    
   