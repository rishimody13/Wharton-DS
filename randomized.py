import pandas as pd
randomized = pd.read_csv("randomized.csv")
print(randomized.head())
teams = ['AUG', 'JAC', 'LAR', 'PRO', 'LRO', 'SPR', 'DOV', 'LEX', 'TOL', 'DES', 'CHM', 'MOB', 'MAN', 'SJU', 'ANC', 'FAR', 'SFS', 'OAK', 'SAS', 'REN', 'BAK', 'BOI', 'EUG', 'FOR', 'ALB', 'WIC', 'TUC', 'TAC']
elos = []
for team in teams:
    teamdf = randomized.loc[(randomized.Team == team)]

    elos.append(teamdf.EloRating.mean())
print(elos)
dict = {'Team': teams, 'AvgElos': elos}
df = pd.DataFrame(dict)
df.to_csv('avgelos.csv')