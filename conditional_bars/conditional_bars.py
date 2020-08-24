
# In this program, we will draw the bar chart for some data and change the color of bars based on
# the value in the y-axis which is of interest for the user. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# A made-up data set.

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

# For each segment, we retrieve the mean and the margin of error using the 0.95 two tailed t-value.

data_1992 = df.loc[1992]
mean_1992 = np.mean(data_1992)
me_1992 = (np.std(data_1992)/np.sqrt(3650))*1.960

data_1993 = df.loc[1993]
mean_1993 = np.mean(data_1993)
me_1993 = (np.std(data_1993)/np.sqrt(3650))*1.960

data_1994 = df.loc[1994]
mean_1994 = np.mean(data_1994)
me_1994 = (np.std(data_1994)/np.sqrt(3650))*1.960

data_1995 = df.loc[1995]
mean_1995 = np.mean(data_1995)
me_1995 = (np.std(data_1995)/np.sqrt(3650))*1.960

means = [mean_1992, mean_1993, mean_1994, mean_1995]
errors = [me_1992, me_1993, me_1994, me_1995]

# Drawing the bars.

plt.close('all')

plt.figure()

plt.cla()

x_values = range(4)

# This is the value about which the user interested. Actuall, based on the position of the value
# regarding the means of the four segment, each bar will be colored.

y_interest = mean_1994

bars = plt.bar(x_values, means, yerr = errors, capsize = 5)

# Drawing the line indicating the value of interest.

plt.hlines(y_interest, xmin = -0.5, xmax = 3.5, linestyle = 'dashed')
plt.text(5.5, y_interest, 'y = {}'.format(y_interest), ha='right', va='center')

plt.xlabel('Years')
plt.ylabel('Total')

plt.tick_params(top = False, right = False, bottom = False, left = False)

ax = plt.gca()
ax.set_xticks(x_values)
ax.set_xticklabels(['1992', '1993', '1994', '1995'])
ax.ticklabel_format(style='plain', axis = 'y')

# Conditionally modifying the colors.

for bar in bars:
    if bar.get_height() - y_interest > 0:
        bar.set_color('crimson')
    elif bar.get_height() - y_interest < 0:
        bar.set_color('lightskyblue')
    else:
        bar.set_color('lavender')

plt.savefig('Conditional_Bars.png', format = 'png')

plt.show()

print('\nThanks for reviewing')

# Thanks for reviewing
