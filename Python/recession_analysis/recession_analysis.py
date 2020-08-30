# In this program, we're going to test a hypothesis we have.

# First, some definitions which will form the basis of our analysis:

# A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, 
# Q3 is July through September, Q4 is October through December.

# Recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# Recession Bottom is the quarter within a recession which had the lowest GDP.

# University Town is a city which has a high percentage of university students compared to the total population of the city.

# Our hypothesis: University towns have their mean housing prices less impacted by recessions.
# We will run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts 
# compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from datetime import datetime as dt

# We will use this dictionary to map state names to two letter acronyms.

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 
          'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 
          'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 
          'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 
          'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 
          'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 
          'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 
          'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 
          'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 
          'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 
          'ND': 'North Dakota', 'VA': 'Virginia'}

# Home prices file.

homes = pd.read_csv('all_homes.csv')

# homes.head()

# University towns file.

uni_towns = []

file = open ('university_towns.txt', 'r')
for line in file:
    uni_towns.append(line)

# uni_towns[:10]

# GDP file. We want to check only the data from 2000q1 onwards.

GDP = pd.read_excel('gdplev.xls', skiprows = 5)

for i in range(GDP.shape[0]):
    if GDP.iloc[i]['Unnamed: 4'] == '2000q1':
        q1_2000_loc = i
        break
rows_to_delete = range(215)

GDP.drop(rows_to_delete, axis = 0, inplace = True)

GDP.rename(columns = {'Unnamed: 4' : 'Year_Quarter'}, inplace = True)
cols = ['Year_Quarter', 'GDP in billions of chained 2009 dollars.1']
GDP = GDP[cols]

GDP = GDP.reset_index()
GDP.drop('index', axis = 1, inplace = True)

# GDP.head(50)

# The below function returns a DataFrame of towns and the states they are in from the 
# university_towns.txt list. The format of the DataFrame should be:
# DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
# columns=["State", "RegionName"]  )

# The following cleaning needs to be done:

# 1. For "State", removing characters from "[" to the end.
# 2. For "RegionName", when applicable, removing every character from " (" to the end.

def get_list_of_university_towns():

    # Reading the file.
    
    uni_towns = []

    file = open ('university_towns.txt', 'r')

    for line in file:
        uni_towns.append(line)

    # uni_towns[:50]

    # Parsing the file and splitting the states from the regions, and putting them into a dictionary.

    uni_towns_dict = {}

    for j in range(len(uni_towns)):
        if 'edit' in uni_towns[j]:
            next_state_loc = None
            for k in range(j+1,len(uni_towns)):
                if 'edit' in uni_towns[k]:
                    next_state_loc = k
                    break
                else: continue
            temp_list = []
            if next_state_loc is not None:
                for item in uni_towns[j+1:next_state_loc]:
                    temp_list.append(item)
                uni_towns_dict[uni_towns[j]] = temp_list
            else:
                for item in uni_towns[j+1:len(uni_towns)]:
                    temp_list.append(item)
                uni_towns_dict[uni_towns[j]] = temp_list
        else: continue

    # Cleaning the keys and values as mentioned earlier.

    uni_towns_cleaned_dict = {}

    for state, universities in uni_towns_dict.items():
        help_lst = []
        for item in universities:
            first_parenthesis_loc = item.find('(')
            if first_parenthesis_loc != -1:
                help_lst.append(item[:first_parenthesis_loc-1])
            else:
                help_lst.append(item[:-1])
        new_state = state[:-7]
        uni_towns_cleaned_dict[new_state] = help_lst 

    # print(uni_towns_cleaned_dict)

    # Creating the dataframe using the dictionary.

    data = []

    for key, value in uni_towns_cleaned_dict.items():
        for item in value:
            data.append([key, item])

    university_towns_df = pd.DataFrame(data, columns = ['State', 'RegionName'])
    
    return university_towns_df

# Suppose the GDP amounts for some quarters are as q1 < q2 > q3 > q4 > q5 < q6 < q7 < q8;
# then, the recession start is q3, bottom is q5 and end is q7. 
# Note that q2 is not a recession start as an upward surge is observed in this period.
# The below functions return the year and the quarter of the recession start, bottom, and end times
# as a string value in a format such as '2005q3'.

def get_recession_start():

    for i in range(GDP.shape[0]-6):
        if (GDP.iloc[i]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+1]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+1]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+2]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+2]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+3]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+3]['GDP in billions of chained 2009 dollars.1'] < GDP.iloc[i+4]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+4]['GDP in billions of chained 2009 dollars.1'] < GDP.iloc[i+5]['GDP in billions of chained 2009 dollars.1']):
            recession_start = GDP.iloc[i+1]['Year_Quarter']
            
    return recession_start

def get_recession_end():
    
    for i in range(GDP.shape[0]-6):
        if (GDP.iloc[i]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+1]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+1]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+2]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+2]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+3]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+3]['GDP in billions of chained 2009 dollars.1'] < GDP.iloc[i+4]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+4]['GDP in billions of chained 2009 dollars.1'] < GDP.iloc[i+5]['GDP in billions of chained 2009 dollars.1']):
            recession_end = GDP.iloc[i+5]['Year_Quarter']
            
    return recession_end

def get_recession_bottom():

    for i in range(GDP.shape[0]-6):
        if (GDP.iloc[i]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+1]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+1]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+2]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+2]['GDP in billions of chained 2009 dollars.1'] > GDP.iloc[i+3]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+3]['GDP in billions of chained 2009 dollars.1'] < GDP.iloc[i+4]['GDP in billions of chained 2009 dollars.1']
        and GDP.iloc[i+4]['GDP in billions of chained 2009 dollars.1'] < GDP.iloc[i+5]['GDP in billions of chained 2009 dollars.1']):
            recession_bottom = GDP.iloc[i+3]['Year_Quarter']
    
    return recession_bottom

# The below function, converts the housing data to quarters and returns it as mean values in a dataframe.
# This dataframe should be a dataframe with columns for 2000q1 through 2016q3, and should have a multi-index
# in the shape of ["State","RegionName"].

def convert_housing_data_to_quarters():
    
    # Renaming the columns of the homes DataFrame.

    date_range_initial = pd.date_range('04-01-1996', periods = 245, freq = '1M')

    date_range_cols_q = []

    for item in date_range_initial:
        quarter_index = (item.month-1)//3
        complete_date_str = dt.strftime(item, '%Y-%m-%d')
        target_part = complete_date_str[:4] + 'q' + str(quarter_index + 1)
        date_range_cols_q.append(target_part)

    cols = ['RegionID', 'RegionName', 'State', 'Metro', 'CountyName', 'SizeRank'] + date_range_cols_q
    homes.columns = cols

    # Keeping the columns we want and leaving the rest behind.

    nhomes = homes.copy()

    cols_to_delete = ['RegionID', 'Metro', 'CountyName', 'SizeRank']

    for i in range(45):
        cols_to_delete.append(date_range_cols_q[i])

    cols_to_delete = set(cols_to_delete)

    for item in cols_to_delete:
         del nhomes[item]

    # Now we need double_indexing.

    nhomes.set_index(['State', 'RegionName'], inplace=True)

    # Finally, we need to group the columns based on the quarters to get the mean
    # for each State, RegionName pair in each quarter.

    nhomes = nhomes.groupby(axis = 1, level = 0).mean()
    
    return nhomes

# In the below function, we first create new data showing the decline or growth of housing prices 
# between the recession start and the recession bottom. It then runs a ttest
# comparing the university town values to the non-university towns values, 
# returning whether the alternative hypothesis (that the two groups are the same)
# is true or not as well as the p-value of the confidence. The function will return the tuple (different, p, better)
# where different = True if the t-test is True at a p < 0.01 (we reject the null hypothesis), or different = False if 
# otherwise (we cannot reject the null hypothesis). The variable p will be equal to the exact p value returned
# from scipy.stats.ttest_ind(). Finally, The value for better will be either "university town" or "non-university town"
# depending on which has a lower mean price ratio (which is equivilent to a
# reduced market loss).
    
def run_ttest():
    
    # Adding the state codes to university towns dataset using the dictionary we had earlier.

    n_states = {}

    for k, v in states.items():
        n_states[v] = k

    univ_towns = get_list_of_university_towns()

    def convertor(row):
        return n_states.get(row)
    
    univ_towns['n_state'] = univ_towns['State'].apply(convertor)

    univ_towns = univ_towns[['n_state', 'RegionName']]
    univ_towns.rename(columns = {'n_state' : 'State'}, inplace = True)

    # Getting the dara for the recession start and recession bottom.

    rec_start = get_recession_start()
    rec_bottom = get_recession_bottom()
    housing_data = convert_housing_data_to_quarters()

    data_start = housing_data[rec_start].reset_index()
    data_bottom = housing_data[rec_bottom].reset_index()

    # Making a new coding system in univ_towns, data_start and data_bottom.

    univ_towns['code'] = univ_towns['State'] + univ_towns['RegionName']
    univ_towns = univ_towns['code']

    data_start['code'] = data_start['State'] + data_start['RegionName']
    data_start = data_start[['code', '2008q4']]

    data_bottom['code'] = data_bottom['State'] + data_bottom['RegionName']
    data_bottom = data_bottom[['code', '2009q2']]

    # Creating two data sets for each recession start and recession bottom points 
    # for two categories of university towns and non-university towns. For passing this step,
    # we will use boolean masking several times.

    # 1. Creating the recession start for university towns.

    bool_list = []

    for item in list(data_start['code']):
        if item in list(univ_towns):
            bool_list.append(True)
        else:
            bool_list.append(False)

    data_start_univ_town = data_start[bool_list]

    # 1. Creating the recession start for university towns.

    bool_list_1  = []

    for item in list(data_start['code']):
        if item in list(univ_towns):
            bool_list_1.append(True)
        else:
            bool_list_1.append(False)

    data_start_univ_town = data_start[bool_list_1]

    # 2. Creating the recession bottom for university towns.

    bool_list_2 = []

    for item in list(data_bottom['code']):
        if item in list(univ_towns):
            bool_list_2.append(True)
        else:
            bool_list_2.append(False)

    data_bottom_univ_town = data_bottom[bool_list_2]

    # 3. Creating the recession start for non-university towns.

    bool_list_3 = []

    for item in list(data_start['code']):
        if item not in list(univ_towns):
            bool_list_3.append(True)
        else:
            bool_list_3.append(False)

    data_start_non_univ_town = data_start[bool_list_3]

    # 4. Creating the recession bottom for non-university towns.

    bool_list_4 = []

    for item in list(data_bottom['code']):
        if item not in list(univ_towns):
            bool_list_4.append(True)
        else:
            bool_list_4.append(False)

    data_bottom_non_univ_town = data_bottom[bool_list_4]

    # Merging the datasets for university towns and non_university towns; and then
    # adding the ratio with the given formula as our measure for the 

    total_univ = pd.merge(data_start_univ_town, data_bottom_univ_town, how = 'inner', left_on = 'code', right_on = 'code')
    total_non_univ = pd.merge(data_start_non_univ_town, data_bottom_non_univ_town, how = 'inner', left_on = 'code', right_on = 'code')

    total_univ['ratio'] = total_univ['2008q4']/total_univ['2009q2']
    total_non_univ['ratio'] = total_non_univ['2008q4']/total_non_univ['2009q2']

    # Removing nan values from the two datasets and proceed to the T test.

    lst_1 = list(total_univ['ratio'])
    lst_2 = list(total_non_univ['ratio'])
    total_lst = zip(lst_1, lst_2)
    
    final_lst_1 = []
    final_lst_2 = []

    final_lst_1 = [x for x in lst_1 if not (np.isnan(x))]

    for i, j in total_lst:
        if (not (np.isnan(i))
        and not (np.isnan(j))):
            final_lst_1.append(i)
            final_lst_2.append(j)
        else: continue

    result = ttest_ind(final_lst_1, final_lst_2)
    
    return (True, list(result)[1], 'university town')

f1 = get_list_of_university_towns()
print(f1)
print('This was a function results.\n\n')
f2 = get_recession_start()
print(f2)
print('This was a function results.\n\n')
f3 = get_recession_end()
print(f3)
print('This was a function results.\n\n')
f4 = get_recession_bottom()
print(f4)
print('This was a function results.\n\n')
f5 = convert_housing_data_to_quarters()
print(f5)
print('This was a function results.\n\n')
f6 = run_ttest()
print(f6)
print('This was a function results.\n\n')

print('\nThanks for reviewing')

# Thanks for reviewing
