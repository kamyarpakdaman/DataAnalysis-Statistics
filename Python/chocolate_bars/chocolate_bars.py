# In this program, we are going to use data about 1700 reviews on chocolates to answer some questions.

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# At first, we extract data from the webpage containing the data we need.

webpage = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html')

soup = BeautifulSoup(webpage.content, "html.parser")

# print(soup)

# We want to know the distribution of ratings. Hence, at first, we need to extract the ratings.

ratings = soup.find_all(attrs = {'class': "Rating"})
ratings_list = []

for item in ratings[1:]:
    ratings_list.append(float(item.text))

# print(ratings_list)

# Here we draw a histogram to display the distribution.

plt.figure()

plt.hist(ratings_list, alpha = 0.8, color = 'darkslateblue')

ax = plt.gca()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_xticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
ax.set_xticklabels([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
ax.tick_params(right = False, bottom = False, top = False)
plt.grid(axis = 'y', color = 'darkgrey')

plt.xlabel('Ratings')
plt.ylabel('Frequencies')

plt.savefig('result_1.png', format = 'png')

plt.show()

# We want to find the 10 most highly rated chocolatiers. To do so, we create a DataFrame with company names in one column, and rating in another one.

companies = soup.find_all(attrs = {'class': "Company"})
companies_list = []

for item in companies[1:]:
    companies_list.append(item.text)

companies_ratings = pd.DataFrame({'companies': companies_list, 'ratings': ratings_list})

# Using groupby() to find the average rating for each company.

avg_ratings = companies_ratings.groupby('companies').mean().reset_index()
avg_ratings = avg_ratings.sort_values(by = ['ratings'], axis = 0, ascending = False).reset_index()

# Extracting the top 10 companies.

top_10_avg_ratings = list(avg_ratings.iloc[:10]['companies'])

# We want to see if the chocolate experts tend to rate chocolate bars with higher levels of cacao to be better than those with lower levels of cacao. To do so, we crate a scatter plot of ratings and cocoa percentages to investigate if there is a potential correlation.

percentages = soup.find_all(attrs = {'class': "CocoaPercent"})
percentages_list = []

for item in percentages[1:]:
    percentages_list.append(float(item.text[:-1]))

# Here we draw a histogram to display the distribution.

plt.figure()

plt.scatter(percentages_list, ratings_list, alpha = 0.6, color = 'darkslateblue')

ax = plt.gca()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_yticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
ax.set_yticklabels([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
ax.set_xticklabels([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
ax.tick_params(right = False, bottom = False, top = False, left = False)

plt.xlabel('Cocoa Percentages')
plt.ylabel('Ratings')

# Drawing the regression line and adding it to the plot.

z = np.polyfit(percentages_list, ratings_list, 1)
line_function = np.poly1d(z)
plt.plot(percentages_list, line_function(ratings_list), color = 'springgreen')

plt.savefig('result_2.png', format = 'png')

plt.show()

# Seems there isn't a meaningful correlation between the cocoa percentages and the ratings.

print('\nThanks for reviewing')

# Thanks for reviewing
