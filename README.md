# Predicting LoL winner
This project has been made as a group project for University of Tartu course LTAT.02.002. 

## Business goals

The main idea of the project is to predict League of Legends (LoL) game winner (blue or red) based on the first ten minutes of the match. 
LoL has a system of ranking players
based on their skills and to make the predicting more accurate we chose to take one of the highest ranks/skill levels as our focus. 
The higher the rank, the more players make conscious choices. Therefore choosing higher rank is desired for our project. 
There are also servers (regions) in LoL and we looked at Europe servers (EUNE and EUW) as it is the most relevant to us. 
We chose to take data from ranked solo games in Diamond I elo from EUNE and EUW. \
In addition to predicting the game winner we also wanted to look into
differences between EUNE and EUW servers based on our data. The reason for this was to find out which server has better players (based on our data) in Diamond I elo.

## Resources

The data for this project was required using Riot API and development API key. For requesting data we wrote Python code that is in the file [request_info.py](/request_info.py). 
For more explanations about the code check the code file. \
\
We collected about 16 000 games from each server with 40 columns. Those 40 columns were the same as
a [Kaggle dataset](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min). \
\
All of the data that we collected is numerical. The 40 columns consist of 18 per team, the matchId (incase we need to acces the game data later), 
as well as the outcome of the match described by a “1” or a “0” based on whether the blue team won or not.
The 18 columns of each team consist mostly of stats that should be helpful in training a model to determine the winner of the match. 
The specific attributes for each team are the following: Wards placed, wards destroyed, first blood (first kill of the game - 1 or 0), kills, deaths, assists, 
dragons, heralds, elite monsters (in total), towers destroyed, total gold, average level, total experience, total minions killed, total jungle monsters killed, gold difference, experience difference, minions/monsters killed per minute, gold per minute.
For explanations about the terms check the [D4_report.pdf](/D4_report.pdf) file's glossary. 
