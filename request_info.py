# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 23:14:04 2022

@author: kukkv
"""

# Get the API key from api_key.txt
def getAPI_key():
    f = open("api_key.txt","r")
    return f.read()

# Get the 40 attributes of the game based on game_info timeline
def get_game_info(game_info):
    # If game_info is empty, there is nothing to look at
    if(game_info != None):
        if("info" in game_info and "metadata" in game_info):
            # Some of the games had corrupted data, so we exclude those
            if(len(game_info["info"]["frames"]) < 2):
                return None
            # Game timeline is in the info -> frames
            timeline = game_info["info"]["frames"]
            # We save the matchId so that it can be used later if needed to look up a game
            matchId = game_info["metadata"]["matchId"]
            
            # Defining all the attributes
            blueWardsPlaced = 0 
            blueWardsDestroyed = 0
            blueFirstBlood = 0 
            blueKills = 0 
            blueDeaths = 0 
            blueAssists = 0 
            blueDragons= 0 
            blueHeralds= 0 
            blueEliteMonsters = 0 
            blueTowersDestroyed= 0 
            blueTotalGold= 0 
            blueAvgLevel= 0 
            blueTotalExperience= 0 
            blueTotalMinionsKilled= 0 
            blueTotalJungleMinionsKilled= 0 
            blueGoldDiff = 0 
            blueExperienceDiff= 0 
            blueCSPerMin = 0 
            blueGoldPerMin = 0 
            
            redWardsPlaced= 0
            redWardsDestroyed= 0
            redFirstBlood= 0
            redKills= 0
            redDeaths= 0
            redAssists= 0
            redEliteMonsters= 0
            redDragons= 0
            redHeralds= 0
            redTowersDestroyed= 0
            redTotalGold= 0
            redAvgLevel= 0
            redTotalExperience= 0
            redTotalMinionsKilled= 0
            redTotalJungleMinionsKilled= 0
            redGoldDiff= 0
            redExperienceDiff= 0
            redCSPerMin= 0
            redGoldPerMin= 0
            
            blueWins = 0
            
            jungleMinionsKilled = [0,0,0,0,0,0,0,0,0,0]
            minionsKilled = [0,0,0,0,0,0,0,0,0,0]
            totalGold = [0,0,0,0,0,0,0,0,0,0]
            level = [0,0,0,0,0,0,0,0,0,0]
            totalExperience = [0,0,0,0,0,0,0,0,0,0]
            wardsPlaced = [0,0,0,0,0,0,0,0,0,0]
            wardsDestroyed = [0,0,0,0,0,0,0,0,0,0]
            
            # Looking at the timeline
            timestamp = 0
            for x in timeline:
                # If the timestamp is bigger than 600000 then it means that it has passed the first 10 minutes of the game
                if(x["timestamp"] <= 600000):
                    timestamp = x["timestamp"]
                    # Timestamp has a summary for each player
                    for i in range(0,10,1):
                        jungleMinionsKilled[i] = x["participantFrames"][str(i+1)]["jungleMinionsKilled"]
                        minionsKilled[i] = x["participantFrames"][str(i+1)]["minionsKilled"]
                        totalGold[i] = x["participantFrames"][str(i+1)]["totalGold"]
                        level[i] = x["participantFrames"][str(i+1)]["level"]
                        totalExperience[i] = x["participantFrames"][str(i+1)]["xp"]
                    # Timestamp has events
                    for event in x["events"]:
                        # If event has a type, then we are interested in it, otherwise there is no data to look at
                        if("type" in event):
                            # Placing a ward
                            if(event["type"] == "WARD_PLACED" ):
                                wardsPlaced[(int)(event["creatorId"])-1] += 1
                            # Destroying a ward
                            elif(event["type"] == "WARD_KILL"):
                                wardsDestroyed[(int)(event["killerId"])-1] += 1
                            # Killing a dragon or herald
                            elif(event["type"] == "ELITE_MONSTER_KILL"):
                                if(event["monsterType"] == "DRAGON"):
                                    if(event["killerTeamId"] == 100):
                                        blueDragons += 1
                                    else:
                                        redDragons += 1
                                elif(event["monsterType"] == "RIFTHERALD"):
                                    if(event["killerTeamId"] == 100):
                                        blueHeralds += 1
                                    else:
                                        redHeralds += 1
                            # Destroying a tower
                            elif(event["type"] == "BUILDING_KILL" and event["buildingType"]=="TOWER_BUILDING"):
                                if((int)(event["killerId"]) > 5):
                                    redTowersDestroyed += 1
                                else:
                                    blueTowersDestroyed += 1
                            # Killing a champion and assisting in killing
                            elif(event["type"]=="CHAMPION_KILL" ):
                                if((int)(event["killerId"]) > 5):
                                    redKills += 1
                                    if("assistingParticipantIds" in event):
                                        redAssists += len(event["assistingParticipantIds"])
                                    blueDeaths += 1
                                elif((int)(event["killerId"]) > 0):
                                    blueKills += 1
                                    if("assistingParticipantIds" in event):
                                        blueAssists += len(event["assistingParticipantIds"])
                                    redDeaths += 1
                            # Checking the team of first blood
                            elif("killType" in event):
                                if(event["killType"] == "KILL_FIRST_BLOOD"):
                                    if((int) (event["killerId"]) > 5):
                                        redFirstBlood = 1
                                    else:
                                        blueFirstBlood = 1
                            elif(event["type"] == "GAME_END"):
                                if(event["winningTeam"] == 100):
                                    blueWins = 1
                else:
                    # Checking the game winner
                    for event in x["events"]:
                        if(event["type"] == "GAME_END"):
                            if(event["winningTeam"] == 100):
                                blueWins = 1
                                
            # If last timestamp was was less than 300000, then we do not want that game in our dataset
            if(timestamp < 300000):
                return None
            # Additional calcucaltions for attributes
            for i in range(0,10,1):
                if(i < 5):
                    blueAvgLevel += level[i]
                    blueWardsPlaced += wardsPlaced[i]
                    blueWardsDestroyed += wardsDestroyed[i]
                    blueTotalGold += totalGold[i]
                    blueTotalExperience += totalExperience[i]
                    blueTotalMinionsKilled += minionsKilled[i]
                    blueTotalJungleMinionsKilled += jungleMinionsKilled[i]
                else:
                    redAvgLevel += level[i]
                    redWardsPlaced += wardsPlaced[i]
                    redWardsDestroyed += wardsDestroyed[i]
                    redTotalGold += totalGold[i]
                    redTotalExperience += totalExperience[i]
                    redTotalMinionsKilled += minionsKilled[i]
                    redTotalJungleMinionsKilled += jungleMinionsKilled[i]
            
            blueAvgLevel = blueAvgLevel / 5
            redAvgLevel = redAvgLevel / 5
            redGoldDiff = blueTotalGold - redTotalGold
            blueGoldDiff = redTotalGold - blueTotalGold
            redExperienceDiff = blueTotalExperience - redTotalExperience
            blueExperienceDiff = redTotalExperience - blueTotalExperience
            blueEliteMonsters = blueDragons+blueHeralds
            redEliteMonsters = redDragons+redHeralds
            redCSPerMin = redTotalMinionsKilled / (timestamp/60000)
            blueCSPerMin = blueTotalMinionsKilled / (timestamp/60000)
            redGoldPerMin = redTotalGold / (timestamp/60000)
            blueGoldPerMin = blueTotalGold / (timestamp/60000) 
            # Game info
            game = {"matchId": matchId, "blueWardsPlaced":blueWardsPlaced,"blueWardsDestroyed":blueWardsDestroyed,
                    "blueFirstBlood":blueFirstBlood,"blueKills":blueKills,"blueDeaths":blueDeaths,
                    "blueAssists":blueAssists,"blueDragons":blueDragons,"blueHeralds":blueHeralds,
                    "blueEliteMonsters":blueEliteMonsters,"blueTowersDestroyed":blueTowersDestroyed,
                    "blueTotalGold":blueTotalGold,"blueAvgLevel":blueAvgLevel,
                    "blueTotalExperience":blueTotalExperience,"blueTotalMinionsKilled":blueTotalMinionsKilled,
                    "blueTotalJungleMinionsKilled":blueTotalJungleMinionsKilled,"blueGoldDiff":blueGoldDiff,
                    "blueExperienceDiff":blueExperienceDiff,"blueCSPerMin":blueCSPerMin,"blueGoldPerMin":blueGoldPerMin,"redWardsPlaced":redWardsPlaced,"redWardsDestroyed":redWardsDestroyed,
                            "redFirstBlood":redFirstBlood,"redKills":redKills,"redDeaths":redDeaths,
                            "redAssists":redAssists,"redDragons":redDragons,"redHeralds":redHeralds,
                            "redEliteMonsters":redEliteMonsters,"redTowersDestroyed":redTowersDestroyed,
                            "redTotalGold":redTotalGold,"redAvgLevel":redAvgLevel,
                            "redTotalExperience":redTotalExperience,"redTotalMinionsKilled":redTotalMinionsKilled,
                            "redTotalJungleMinionsKilled":redTotalJungleMinionsKilled,"redGoldDiff":redGoldDiff,
                            "redExperienceDiff":redExperienceDiff,"redCSPerMin":redCSPerMin,"redGoldPerMin":redGoldPerMin,"bluewins":blueWins}
            return game
    return None


import requests
import pandas as pd
import time
from pathlib import Path 

# Requesting summonerId-s in Diamond I
def read_summoners():
    # change page= to get next page of players from Diamond I eune
    # change the eun1 to euw1 for euw players
    api_link_summoners = "https://eun1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&api_key=" + getAPI_key()
    resp = requests.get(api_link_summoners)
    summoner_in_tier_info = resp.json()
    with open('summonerIds.txt',"w") as fp:
        for summoner in summoner_in_tier_info:
            id_summ = summoner["summonerId"]
            fp.write(id_summ+"\n")
# Requesting summoner puuid based on summonerId
def read_summoner_puuids():
    # change the eun1 to euw1 for euw players
    api_link_puuids = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/"
    summonerPuuids = []
    with open('summonerIds.txt',"r") as fp:
        for line in fp:
            ids = line[:-1]
            api_link_person_puuid = api_link_puuids + ids + "?api_key=" + getAPI_key()
            time.sleep(1)
            resp = requests.get(api_link_person_puuid)
            summoner_info = resp.json()
            puuid = summoner_info['puuid']
            summonerPuuids.append(puuid)
    with open('summonerPuuids.txt',"w") as fp:
        for ids in summonerPuuids:
            fp.write(ids+"\n")
# Request last 20 ranked games based on summoner puuid
def read_gameIds():
    api_link_gameIds = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
    gameIds = []
    with open('summonerPuuids.txt','r') as fp:
        for line in fp:
            api_link_person_gameIds = api_link_gameIds + line[:-1] + "/ids?type=ranked&start=0&count=20&api_key=" + getAPI_key()
            time.sleep(1)
            resp = requests.get(api_link_person_gameIds)
            summoner_games = resp.json()
            for game in summoner_games:
                gameIds.append(game)
    with open('gameIds.txt','w') as fp:
        for game in gameIds:
            fp.write(game+"\n")

# Request game timeline based on matchId
def read_timelines():
    api_link_timelines = "https://europe.api.riotgames.com/lol/match/v5/matches/"
    games = []
    with open('gameIds.txt','r') as fp:
        for line in fp:
            api_link_game_timeline = api_link_timelines + line[:-1] + "/timeline?api_key=" + getAPI_key()
            time.sleep(1)
            resp = requests.get(api_link_game_timeline)
            game_timeline = resp.json()
            gameinfo = get_game_info(game_timeline)
            if(gameinfo != None):
                games.append(gameinfo)
            else:
                time.sleep(1)
    df = pd.DataFrame(games)
    filepath = Path('eune_data1.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    df.to_csv(filepath) 
# Uncomment and run in this order, also API key is required to get data
#read_summoners()
#read_summoner_puuids()
#read_gameIds()
#read_timelines()
