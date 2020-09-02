# In this program we use Pandas library to answer some questions about two sets of data
# respectively about the history of medals countries have gained in olympics, and the
# census in the US.

import pandas as pd

# We begin with some questions about the Olympics dataset
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

# Modifying the names of some columns
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

# Splittinf the index by '(')
names_ids = df.index.str.split('\s\(')

# Turning mere country names to indexes and separating the abbreviatins as IDs
df.index = names_ids.str[0] 
df['ID'] = names_ids.str[1].str[:3] 

df = df.drop('Totals')
df.head()

# We want to know which country has won the most gold medals in summer games?

def most_golds():
    top_country = df[df['Gold'] == df['Gold'].max()].index[0]
    print(top_country)
    return top_country

# most_golds()
# print('THIS IS FIXED')

# We want to know which country had the biggest difference between their summer
# and winter gold medal counts?

def biggest_difference():
    top_difference = df[(df['Gold']-df['Gold.1']) == (df['Gold'] - df['Gold.1']).max()].index[0]
    print(top_difference)
    return top_difference

# biggest_difference()
# print('THIS IS FIXED')

# We want to know Which country has the biggest difference between their summer
# gold medal counts and winter gold medal counts relative to their total gold medal count?
# Note that we're counting only the countries that have won at least 1 gold in both summer
# and winter.

def biggest_fraction():
    df_n = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    top_fraction = df_n[((df_n['Gold']-df_n['Gold.1'])/(df_n['Gold'] + df_n['Gold.1'])) 
    == ((df_n['Gold'] - df_n['Gold.1'])/(df_n['Gold'] + df_n['Gold.1'])).max()].index[0]
    print(top_fraction)
    return top_fraction


# biggest_fraction()
# print('THIS IS FIXED')

# This is a function that creates a Series called "Points" which is a weighted value where each
# gold medal (Gold.2) counts for 3 points, silver medals (Silver.2) for 2 points, and bronze medals
# (Bronze.2) for 1 point. The function should return only the column (a Series object) which you
# created, with the country names as indices.

def score_calculator():
    Points = (df['Gold.2']*3+df['Silver.2']*2+df['Bronze.2']*1)
    print(Points)
    return Points

# score_calculator()
# print('THIS IS FIXED')

# We follow with some questions about the Census dataset

census_df = pd.read_csv('census.csv')
census_df.head()

# We want to know Which state has the most counties in it?

def most_counties():
    census_df = pd.read_csv('census.csv')
    census_df = census_df[census_df['SUMLEV'] == 50]
    states = census_df['STNAME'].unique()
    states_counts = {}
    for i in states:
        count = census_df[census_df['STNAME'] == i]['CTYNAME'].count()
        states_counts[count] = i
    counts = states_counts.keys()
    maximum_counter = max(counts)
    answer = states_counts[maximum_counter]
    print(answer)
    return answer

# most_counties()
# print('THIS IS FIXED')

# Only looking at the three most populous counties for each state, We want to know
# what are the three most populous states (in order of highest population to lowest 
# population)? We'll be using the data in CENSUS2010POP column.

def top_three_states():
    census_df = pd.read_csv('census.csv')
    census_df = census_df[census_df['SUMLEV'] == 50]
    states = census_df['STNAME'].unique()
    states_pops = {}
    for i in states:
        pops = (census_df[census_df['STNAME'] == i]['CENSUS2010POP']).sort_values(ascending = False)
        maximum_pops_sum = pops[0:3].sum()
        states_pops[maximum_pops_sum] = i
    populations = sorted(states_pops.keys(), reverse = True)
    top_3_pops = populations[0:3]
    top_3_states = []
    for j in top_3_pops:
        top_3_states.append(states_pops[j])
    print(top_3_states)
    return top_3_states

# top_three_states()
# print('THIS IS FIXED')

# We want to know Which county has had the largest absolute change in population within the
# period 2010-2015? Note that population values are stored in columns POPESTIMATE2010 through 
# POPESTIMATE2015, and we'll use all six columns.
# E.g., if a county population in the 5 year period is 100, 120, 80, 105, 100, 130, then
# its largest change in the period would be |130-80| = 50.

def Largest_change():
    census_df = pd.read_csv('census.csv')
    census_df = census_df[census_df['SUMLEV'] == 50]
    popcols = ["POPESTIMATE20"+ str(x) for x in range(10,16)]
    cols = ['SUMLEV','CTYNAME'] + popcols
    dfp = census_df[cols]
    dfp = dfp.set_index('CTYNAME')
    dfp['ABSCHANGE'] = (dfp[popcols].max(axis = 1)) - (dfp[popcols].min(axis = 1))
    maximum_change = dfp['ABSCHANGE'].max()
    Largest_change_county = dfp[dfp['ABSCHANGE'] == maximum_change].index[0]
    print(Largest_change_county)
    return Largest_change_county

# Largest_change()
# print('THIS IS FIXED')

# Finally, we want to know the counties that belong to regions 1 or 2, whose name starts
# with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.

def target_segment():
    census_df = pd.read_csv('census.csv')
    result = census_df[((census_df['REGION'] == 1) | (census_df['REGION'] == 2))
     & (census_df['CTYNAME'].str[0:10] == 'Washington')
      & (census_df['POPESTIMATE2015'] >= census_df['POPESTIMATE2014'])][['STNAME', 'CTYNAME']]
    print(result)
    return result

# target_segment()
# print('THIS IS FIXED')

print('\nThanks for reviewing')

# Thanks for reviewing
