from os import name
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

from data import games

plays = games.loc[games['type'] == 'play']
strike_outs : DataFrame = plays.loc[plays['event'].str.contains('K')]
print(strike_outs)
print('********')
strike_outs = strike_outs.groupby(['year', 'game_id']).size()
print(strike_outs)
print('********')
strike_outs = strike_outs.reset_index(name='strike_outs')
print(strike_outs)
print('********')
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)
print(strike_outs)
print('********')

strike_outs.plot(x='year', y='strike_outs', kind='scatter').legend('Strike Outs')
plt.show()