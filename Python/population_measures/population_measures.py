# In this program, we will draw two plots displaying the populaiton density and
# the median age for three countries of Iran, Saudi Arabia, and Turkey, from 1965 to 2015.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

population = pd.read_csv('population-density.csv')
age = pd.read_csv('median-age.csv')

# Making some cleaning and editing to both data sets.

# population density.

population.rename(columns = {'Entity' : 'Country',
                             'Population density (people per sq. km of land area) (people per km² of land area)' : 'Density'}, inplace = True)
cols = ['Country', 'Year', 'Density']
population = population[cols]

population_iran = population[(population['Country'] == 'Iran') & (population['Year'] >= 1965) & (population['Year'] <= 2015)]
population_turkey = population[(population.Country == 'Turkey') & (population['Year'] >= 1965) & (population['Year'] <= 2015)]
population_saudi_arabia = population[(population.Country == 'Saudi Arabia') & (population['Year'] >= 1965) & (population['Year'] <= 2015)]

# median age.

age.rename(columns = {'Entity' : 'Country',
                             'UN Population Division (Median Age) (2017) (years)' : 'Median'}, inplace = True)
cols = ['Country', 'Year', 'Median']
age = age[cols]

age_iran = age[(age['Country'] == 'Iran') & (age['Year'] >= 1965) & (age['Year'] <= 2015)]
age_turkey = age[(age['Country'] == 'Turkey') & (age['Year'] >= 1965) & (age['Year'] <= 2015)]
age_saudi_arabia = age[(age['Country'] == 'Saudi Arabia') & (age['Year'] >= 1965) & (age['Year'] <= 2015)]

# Drawing the plots.

plt.close('all')

plt.figure(figsize = (12, 10))

plt.subplot(2, 1, 1)

x_values_pop = range(1965, 2016)

y_iran_pop = population_iran['Density']
y_turkey_pop = population_turkey['Density']
y_saudi_arabia_pop = population_saudi_arabia['Density']

plt.plot(x_values_pop, y_iran_pop, color = 'steelblue')
plt.plot(x_values_pop, y_turkey_pop, color = 'firebrick')
plt.plot(x_values_pop, y_saudi_arabia_pop, color = 'green')

plt.ylabel('Population per km² of Land Area')
plt.title('Historical Population Density,\nIran, Turkey, and Saudi Arabia')
plt.tick_params(top = False, bottom = False, right = False, left = False)

ax1 = plt.gca()
ax1.spines['left'].set_visible(True)
ax1.spines['bottom'].set_visible(True)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

plt.grid(axis = 'y')
plt.legend(['Iran Population', 'Turkey Population', 'Saudi Arabia Population'], frameon = True)

plt.subplot(2, 1, 2)

x_values_age = range(1965, 2016, 5)

y_iran_age = age_iran['Median']
y_turkey_age = age_turkey['Median']
y_saudi_arabia_age = age_saudi_arabia['Median']

plt.plot(x_values_age, y_iran_age, color = 'steelblue')
plt.plot(x_values_age, y_turkey_age, color = 'firebrick')
plt.plot(x_values_age, y_saudi_arabia_age, color = 'green')

plt.ylabel('Median Age')
plt.title('Historical Median Age,\nIran, Turkey, and Saudi Arabia')
plt.tick_params(top = False, bottom = False, right = False, left = False)

ax2 = plt.gca()
ax2.spines['left'].set_visible(True)
ax2.spines['bottom'].set_visible(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.grid(axis = 'y')
plt.legend(['Iran Median Age', 'Turkey Median Age', 'Saudi Arabia Median Age'], frameon = True)

plt.savefig('Result.png')

plt.show()

print('\nThanks for reviewing')

# Thanks for reviewing
