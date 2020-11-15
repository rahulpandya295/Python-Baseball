from matplotlib.pyplot import axis, xticks
from numpy.lib.shape_base import column_stack
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

from frames import games, info, events

games: DataFrame = games
events: DataFrame = events
print("Games ->")
print(games)
print("events ->")
print(events)
#plays = games.query()

plays = games.query("type == 'play' and event != 'NP'")
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team','player' ]]
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA')

events = events.set_index(['year','game_id','team','event_type'])
events = events.unstack().fillna(0).reset_index()
events.columns = events.columns.droplevel()
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']

events = events.rename_axis('None', axis='columns')
events_plus_pa = pd.merge(events, pa, how='outer', left_on=['year', 'game_id', 'team'], right_on=['year', 'game_id', 'team'])

defense = pd.merge(events_plus_pa, info)
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense["ROE"]) / (defense['PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))

defense.loc[:, 'year'] = pd.to_numeric(defense['year'])
der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']]
der = der.pivot(index='year', columns = 'defense', values='DER')

der.plot(x_compat=True, xticks=range(1978, 2018, 4), rot = 45)
plt.show()