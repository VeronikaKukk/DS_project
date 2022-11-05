# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 23:14:04 2022

@author: kukkv
"""

def getAPI_key():
    f = open("api_key.txt","r")
    return f.read()


def get_game_info(game_info):
    if(game_info != None):
        if("info" in game_info and "metadata" in game_info):
            if(len(game_info["info"]["frames"]) < 2):
                return None
            timeline = game_info["info"]["frames"]
        
            matchId = game_info["metadata"]["matchId"]
            
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
            
        
            timestamp = 0
            for x in timeline:
                if(x["timestamp"] <= 600000):
                    timestamp = x["timestamp"]
                    for i in range(0,10,1):
                        jungleMinionsKilled[i] = x["participantFrames"][str(i+1)]["jungleMinionsKilled"]
                        minionsKilled[i] = x["participantFrames"][str(i+1)]["minionsKilled"]
                        totalGold[i] = x["participantFrames"][str(i+1)]["totalGold"]
                        level[i] = x["participantFrames"][str(i+1)]["level"]
                        totalExperience[i] = x["participantFrames"][str(i+1)]["xp"]
                    for event in x["events"]:
                        if("type" in event):
                            if(event["type"] == "WARD_PLACED" ):
                                wardsPlaced[(int)(event["creatorId"])-1] += 1
                            elif(event["type"] == "WARD_KILL"):
                                wardsDestroyed[(int)(event["killerId"])-1] += 1
                            elif(event["type"] == "ELITE_MONSTER_KILL"):
                                if(event["monsterType"] == "DRAGON"):
                                    if(event["killerTeamId"] == "100"):
                                        blueDragons += 1
                                    else:
                                        redDragons += 1
                                elif(event["monsterType"] == "RIFTHERALD"):
                                    if(event["killerTeamId"] == "100"):
                                        blueHeralds += 1
                                    else:
                                        redHeralds += 1
                            elif(event["type"] == "BUILDING_KILL" and event["buildingType"]=="TOWER_BUILDING"):
                                if((int)(event["killerId"]) > 5):
                                    redTowersDestroyed += 1
                                else:
                                    blueTowersDestroyed += 1
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
                    for event in x["events"]:
                        if(event["type"] == "GAME_END"):
                            if(event["winningTeam"] == 100):
                                blueWins = 1
                                
            
            if(timestamp < 300000):
                return None
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

def read_summoners():
    # change page= to get next page of players from Diamond I eune
    api_link_summoners = "https://eun1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&api_key=" + getAPI_key()
    resp = requests.get(api_link_summoners)
    summoner_in_tier_info = resp.json()
    with open('summonerIds.txt',"w") as fp:
        for summoner in summoner_in_tier_info:
            id_summ = summoner["summonerId"]
            fp.write(id_summ+"\n")

def read_summoner_puuids():
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

read_summoners()
read_summoner_puuids()
read_gameIds()
read_timelines()