import csv
import math
import os
import random
import pandas as pd

GD = 0


# Function to calculate the expected score
def expected_score(elo_a, elo_b):
    return 1 / (1 + math.pow(10, (elo_b - elo_a) / 1000))


kscale = 0.6


# Function to update Elo ratings
def update_elo(winner_elo, loser_elo, xG):
    if GD == 0:
        k = 80 * kscale + 10 * (1.31 - xG)
        expected_winner_score = expected_score(winner_elo, loser_elo)
        expected_loser_score = 1 - expected_winner_score
        new_winner_elo = winner_elo + k * (0.5 - expected_winner_score)
        new_loser_elo = loser_elo + k * (0.5 - expected_loser_score)
        return new_winner_elo, new_loser_elo
    else:
        if GD == 1:
            k = 100 * kscale + 10 * (1.31 - xG)  # Elo update factor
        if GD == 2:
            k = 120 * kscale + 10 * (1.31 - xG)
        if GD == 3:
            k = 150 * kscale + 10 * (1.31 - xG)
        if GD == 4:
            k = 200 * kscale + 10 * (1.31 - xG)
        if GD == 5:
            k = 220 * kscale + 10 * (1.31 - xG)
        if GD == 6:
            k = 230 * kscale + 10 * (1.31 - xG)
        if GD == 7:
            k = 240 * kscale + 10 * (1.31 - xG)
        else:
            k = 250 * kscale + 10 * (1.31 - xG)

        expected_winner_score = expected_score(winner_elo, loser_elo)
        expected_loser_score = 1 - expected_winner_score
        new_winner_elo = winner_elo + k * (1 - expected_winner_score)
        new_loser_elo = loser_elo + k * (0 - expected_loser_score)
        return new_winner_elo, new_loser_elo


# Read CSV file and update Elo ratings
teams_elo = {}  # Dictionary to store Elo ratings for each team
# Divide teams into Eastern and Western conferences
eastern_teams = ['AUG', 'JAC', 'LAR', 'PRO', 'LRO', 'SPR', 'DOV', 'LEX', 'TOL', 'DES', 'CHM', 'MOB', 'MAN', 'SJU']
western_teams = ['ANC', 'FAR', 'SFS', 'OAK', 'SAS', 'REN', 'BAK', 'BOI', 'EUG', 'FOR', 'ALB', 'WIC', 'TUC', 'TAC']
all_teams = ['AUG', 'JAC', 'LAR', 'PRO', 'LRO', 'SPR', 'DOV', 'LEX', 'TOL', 'DES', 'CHM', 'MOB', 'MAN', 'SJU', 'ANC', 'FAR', 'SFS', 'OAK', 'SAS', 'REN', 'BAK', 'BOI', 'EUG', 'FOR', 'ALB', 'WIC', 'TUC', 'TAC']
all_teams_dict = {team: 0 for team in all_teams}
master_elo = {} # Contains set of elos for each bootstrap

reader = None
data = None
a = 0
b = 0

numbootstraps = 10000
with open("NSL_Regular_Season_Data.csv", mode='r') as file:
    reader = csv.DictReader(file)
    data = list(reader)
    for bootstrap in range(numbootstraps):
        
        a = list(range(476))
        for y in range(476):
            b = random.choice(a)
            row = data[b]
            a.pop(a.index(b))
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']

            home_score = int(row['HomeScore'])
            away_score = int(row['AwayScore'])

            home_xG = float(row['Home_xG'])
            away_xG = float(row['Away_xG'])

            # Initialize Elo ratings if not already present
            teams_elo.setdefault(home_team, 1000)
            teams_elo.setdefault(away_team, 1000)

            # Update Elo ratings based on game result
            if home_score > away_score:
                GD = home_score - away_score
                teams_elo[home_team], teams_elo[away_team] = update_elo(teams_elo[home_team], teams_elo[away_team], home_xG)
            elif away_score > home_score:
                GD = away_score - home_score
                teams_elo[away_team], teams_elo[home_team] = update_elo(teams_elo[away_team], teams_elo[home_team], away_xG)
            elif away_score == home_score:
                teams_elo[home_team], teams_elo[away_team] = update_elo(teams_elo[home_team], teams_elo[away_team], home_xG)


        # Separate teams into their conferences and order them based on Elo ratings within each conference
        eastern_teams_elo = {team: teams_elo[team] for team in eastern_teams}
        western_teams_elo = {team: teams_elo[team] for team in western_teams}
        all_teams_elo = {**eastern_teams_elo, **western_teams_elo}
        # sorted_all_teams = sorted(all_teams_elo.items(), key=lambda x: x[1], reverse=True)
        for team in all_teams_elo:
        
            all_teams_dict[team]+=all_teams_elo[team]

for team in all_teams_dict:
    all_teams_dict[team]/=numbootstraps
# Write final Elo ratings to separate CSV files for each conference
file_path_eastern = 'final_elo_ratings_eastern.csv'
file_path_western = 'final_elo_ratings_western.csv'
file_path_all = 'final_elo_ratings.csv'

# with open(file_path_all, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Team', 'Elo Rating'])
#     for team, elo in all_teams_elo:
#         writer.writerow([team, elo])
print(all_teams_dict)
finaldict = {"Team":all_teams_dict.keys(), 'AvgElos':all_teams_dict.values()}
df = pd.DataFrame(finaldict)
print(df.head())
df.to_csv('avgelos.csv')