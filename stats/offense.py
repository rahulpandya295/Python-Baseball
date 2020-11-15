import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

from data import games

games: DataFrame = games

plays = games[games['type'] == 'play']
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning','event']]

hits['inning'] = hits['inning'].apply(pd.to_numeric)
#print(hits)

replacements = {r'^S(.*)': 'single',r'^D(.*)': 'double',r'^T(.*)': 'triple',r'^HR(.*)': 'hr'}
#print(replacements)

hit_type = hits.replace(replacements, regex=True)

#print(hit_type)

hits = hits.assign(hit_type=hit_type['event'])
#print(hits)
hits = hits.groupby(['inning','hit_type']).size().reset_index(name='count')
print(hits)
print(hits.dtypes)
hits['hit_type'] = pd.Categorical(hits.hit_type, ['single', 'double', 'triple', 'hr'])
print(hits)
print(hits.dtypes)
#print(hits)

hits = hits.sort_values(by = ['inning','hit_type'])

hits = hits.pivot(index='inning', columns='hit_type', values='count')

print(hits)

hits.plot(kind='bar', stacked=True)
plt.show()