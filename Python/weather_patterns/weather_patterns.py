# In this program, we're going to read the documentation and familiarize ourselves with it; then write some python code
# which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014.
# Further, The area between the record high and record low temperatures for each day will be shaded. Then, we're going to
# overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high
# or record low was broken in 2015.
# Note. The data in the dataset comes from somewhere near Ann Arbor, Michigan, United States.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime as dt

df = pd.read_csv('weather.csv')

# Some initial cleanings.

df['Date_day'] = df['Date'].apply(lambda x: dt.strptime(x, '%Y-%m-%d').day)
df['Date_year'] = df['Date'].apply(lambda x: dt.strptime(x, '%Y-%m-%d').year)
df['Date_yday'] = df['Date'].apply(lambda x: int(dt.strftime((dt.strptime(x, '%Y-%m-%d')), '%j')))

cols = ['Date_yday', 'Element', 'Date_year', 'Data_Value']
df = df[cols]

df_max_temp = df[df['Element'] == 'TMAX'][['Date_yday', 'Date_year', 'Data_Value']]
df_max_temp = df_max_temp[df_max_temp['Date_year'] < 2015]
df_min_temp = df[df['Element'] == 'TMIN'][['Date_yday', 'Date_year', 'Data_Value']]
df_min_temp = df_min_temp[df_min_temp['Date_year'] < 2015]

# High and low records for each day in the 10-year period.

days_max_10y = df_max_temp.groupby('Date_yday')['Data_Value'].agg({'max' : np.max})
days_min_10y = df_min_temp.groupby('Date_yday')['Data_Value'].agg({'min' : np.min})

# Detecting when the records were broken in 2015.

max_rec_2015 = df[df['Element'] == 'TMAX'][['Date_yday', 'Date_year', 'Data_Value']]
max_rec_2015 = max_rec_2015[max_rec_2015['Date_year'] ==  2015]
min_rec_2015 = df[df['Element'] == 'TMIN'][['Date_yday', 'Date_year', 'Data_Value']]
min_rec_2015 = min_rec_2015[min_rec_2015['Date_year'] ==  2015]

days_max_2015 = max_rec_2015.groupby('Date_yday')['Data_Value'].agg({'max' : np.max})
days_min_2015 = min_rec_2015.groupby('Date_yday')['Data_Value'].agg({'min' : np.min})

# As we can see, the high temperature record was broken in 2015 at some points.

comparison_2015_10_max = pd.merge(days_max_2015, days_max_10y, how = 'inner', left_index = True, right_index = True)
records_2015_max = comparison_2015_10_max[comparison_2015_10_max['max_x'] > comparison_2015_10_max['max_y']]
records_2015_max = records_2015_max.rename(columns = {'max_x' : 'max'})

# As we can see, the low temperature record was broken in 2015 at some points.

comparison_2015_10_min = pd.merge(days_min_2015, days_min_10y, how = 'inner', left_index = True, right_index = True)
records_2015_min = comparison_2015_10_min[comparison_2015_10_min['min_x'] < comparison_2015_10_min['min_y']]
records_2015_min = records_2015_min.rename(columns = {'min_x' : 'min'})

# Drawing the plot.

plt.close('all')

plt.figure(figsize = (30, 10))

x_values = range(1, 367)

y_max_10 = days_max_10y['max']
y_min_10 = days_min_10y['min']

# Yearly max and min temperatures from 2005 to 2014.

plt.plot(x_values, y_max_10, color = 'tab:red')
plt.plot(x_values, y_min_10, color = 'steelblue')
plt.fill_between(x_values, y_max_10, y_min_10, color = 'whitesmoke')

x_max_2015 = list(records_2015_max.index)
y_max_2015 = records_2015_max['max']
x_min_2015 = list(records_2015_min.index)
y_min_2015 = records_2015_min['min']

# Max and Min temperatures in 2015, breaking the records. 

plt.scatter(x_max_2015, y_max_2015, color = 'crimson', marker = 'o', s = 100)
plt.scatter(x_min_2015, y_min_2015, color = 'darkturquoise', marker = 'o', s = 100)

plt.xlabel('Days of the Year', fontsize = 15)
plt.ylabel('Temperatures', fontsize = 15)
plt.title('High/Low Temperature Records per Day, 2005-2015', fontsize = 18)

plt.legend(['10 year max', '10 year min', '', '2015 max', '2015 min' ], frameon = False, fontsize = 15)

plt.tick_params(top = False, left = False, right = False, bottom = False)

ax = plt.gca()

ax.set_xticks(range(0, 367, 50))
ax.set_xticklabels(range(0, 367, 50), fontsize = 15)
ax.set_yticks(range(-300, 401, 100))
ax.set_yticklabels(range(-300, 401, 100), fontsize = 15)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.get_legend().legendHandles[2].set_visible(False)

plt.savefig('Weather_Patterns.png', format = 'png')

plt.show()

print('\nThanks for reviewing')

# Thanks for reviewing
