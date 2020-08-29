# In this program, we will use three datasets to answer some questions.

import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

# Energyy file.

def energy():
    
    # Loading the first file and  omitting some rows from the top and bottom.
    
    energy = pd.read_excel('energy.xls', skiprows = 17)
    energy.drop(energy.index[227:], inplace = True)
    energy.drop(energy.columns[0:2], axis = 1, inplace = True)
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    
    # Turning missing values in the form of '...' into np.NaN.
    
    for i in range(energy.shape[0]):
        if type(energy.iloc[i]['Energy Supply']) == type('a'):
            energy.at[i, 'Energy Supply'] = np.NaN
    
    for i in range(energy.shape[0]):
        if type(energy.iloc[i]['Energy Supply per Capita']) == type('a'):
            energy.at[i, 'Energy Supply per Capita'] = np.NaN
    
    # Adusting column dtypes for later avoiding errors. Further, converting Energy Supply to 
    # gigajoules (there are 1,000,000 gigajoules in a petajoule)
    
    energy['Energy Supply'] = pd.to_numeric(energy['Energy Supply'])
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    energy['Energy Supply per Capita'] = pd.to_numeric(energy['Energy Supply per Capita'])
    
    # Editing the names of some countries.
    
    name_changes_energy = {"Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"}
    
    for i in range(energy.shape[0]):
        for j in name_changes_energy.keys():
            if energy['Country'].iloc[i] == j:
                energy['Country'].iloc[i] = name_changes_energy[j]
    
    # First, finding the names for some countries which have unwanted names including
    # numbers and/or parenthesis; and then, editing them.
    
    name_changes_indicators = ['(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    name_changes = []
    for i in range(energy.shape[0]):
        for j in name_changes_indicators:
            if j in energy['Country'].iloc[i]:
                if energy['Country'].iloc[i] not in name_changes:
                    name_changes.append(energy['Country'].iloc[i])
    
    name_changes_energy_2 = {}
    for i in name_changes:
        name_changes_energy_2[i] = None
    
    # print(name_changes_energy_2) this is for finding the names so that we can
    #                              manually create a dictionary in the next step to revise the names.
    
    name_changes_energy_2 = {'Australia1': 'Australia',
    'Bolivia (Plurinational State of)': 'Bolivia',
     'China, Hong Kong Special Administrative Region3': 'Hong kong',
     'China, Macao Special Administrative Region4': 'China, Macao Special Administrative Region',
     'China2': 'China',
     'Denmark5': 'Denmark',
     'Falkland Islands (Malvinas)': 'Falkland Islands',
     'France6': 'France',
     'Greenland7': 'Greenland',
     'Indonesia8': 'Indonesia',
     'Iran (Islamic Republic of)': 'Iran',
     'Italy9': 'Italy',
     'Japan10': 'Japan',
     'Kuwait11': 'Kuwait',
     'Micronesia (Federated States of)': 'Micronesia',
     'Netherlands12': 'Netherlands',
     'Portugal13': 'Portugal',
     'Saudi Arabia14': 'Saudi Arabia',
     'Serbia15': 'Serbia',
     'Sint Maarten (Dutch part)': 'Sint Maarten',
     'Spain16': 'Spain',
     'Switzerland17': 'Switzerland',
     'Ukraine18': 'Ukraine',
     'United Kingdom of Great Britain and Northern Ireland19': 'United Kingdom',
     'United States of America20': 'United States',
     'Venezuela (Bolivarian Republic of)': 'Venezuela'}
    
    for i in range(energy.shape[0]):
        for j in name_changes_energy_2.keys():
            if energy['Country'].iloc[i] == j:
                energy['Country'].iloc[i] = name_changes_energy_2[j]
    
    # print(energy.info())
    # print(energy.iloc[[0, -1]])
    
    return energy

# GDP file.

def GDP():
    
    GDP = pd.read_csv('gdp.csv', skiprows = 4)
    
    # Editing the names of some countries.
    
    name_changes_GDP = {"Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"}
    for i in range(GDP.shape[0]):
        for j in name_changes_GDP.keys():
            if GDP['Country Name'].iloc[i] == j:
                GDP['Country Name'].iloc[i] = name_changes_GDP[j]
    
    # Changing the name of 'Country Name' column
    
    GDP.rename(columns = {'Country Name' : 'Country'}, inplace = True)
    
    # Keeping only the last 10 years, 2005-2016.
    
    cols_GDP = ['Country']
    
    years = range(2006, 2016)
    for i in years:
        cols_GDP.append(str(i))
    
    GDP = GDP[cols_GDP]
    
    # print(GDP.info())
    # print(GDP.iloc[[0, -1]])
    
    return GDP

# ScimEn file.

def ScimEn():
    
    ScimEn = pd.read_excel('science.xlsx')
    
    # print(ScimEn.info())
    # print(ScimEn.iloc[[-1, 0]])
    
    return ScimEn

# Merging the three datasets into one comprehensive dataset.

def total_data():
    
    energy_table = energy()
    
    GDP_table = GDP()
    
    ScimEn_table = ScimEn()
    
    # Merging the three datasets into one, using the country names.
    
    part_1 = pd.merge(energy_table, GDP_table, how = 'inner', left_on = 'Country', right_on = 'Country')
    All_data = pd.merge(part_1, ScimEn_table, how = 'inner', left_on = 'Country', right_on = 'Country')
    
    # Getting only the records for the top 15 ranked countries.
    
    Result_data = All_data[All_data['Rank'] <= 15]
    
    # Setting Country names as index.
    
    Result_data.set_index('Country', inplace = True)
    
    # Reordering columns.
    
    cols = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 
            'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', 
            '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    
    Result_data = Result_data[cols]
    
    return Result_data

# The previous function joins three datasets then reduces this to just the top 15 entries.
# In the below function, we find out how many entries we lost through this merge.

def data_loss():
    
    energy_table = energy()
    
    GDP_table = GDP()
    
    ScimEn_table = ScimEn()
    
    # Inner merges.
    
    part_1 = pd.merge(energy_table, GDP_table, how = 'inner', left_on = 'Country', right_on = 'Country')
    All_data = pd.merge(part_1, ScimEn_table, how = 'inner', left_on = 'Country', right_on = 'Country')
    
    # Outer merges.
    
    part_1_o = pd.merge(energy_table, GDP_table, how = 'outer', left_on = 'Country', right_on = 'Country')
    All_data_o = pd.merge(part_1_o, ScimEn_table, how = 'outer', left_on = 'Country', right_on = 'Country')
    
    # print(len(All_data_o) - len(All_data))
    
    return (All_data_o.shape[0]) - (All_data.shape[0])

# Finding out the average GDP over the last 10 years for each country.

def avg_GDP():

    Top15 = total_data()

    yrs = range(2006, 2016)
    cols_10 = []

    for i in yrs:
        cols_10.append(str(i))
    
    Top15['average_GDP'] = Top15.apply(lambda row: np.mean(row[cols_10]), axis = 1)
    s = Top15['average_GDP']
    avgGDP = s.sort_values(ascending = False)

    return avgGDP

# Finding out how much has the GDP changed over the 10 year span for the country with the 6th largest average GDP.

def GDP_change():

    Top15 = total_data()
    
    first_GDP = Top15.loc['United Kingdom']['2006']
    last_GDP = Top15.loc['United Kingdom']['2015']
    
    result = last_GDP - first_GDP
    
    return result

# Finding out the mean Energy Supply per Capita.

def mean_ESC():

    Top15 = total_data()

    return np.mean(Top15['Energy Supply per Capita'])

# Finding out the country that has the maximum % Renewable and its percentage?

def max_RNW():

    Top15 = total_data()

    max_percentage = np.max(Top15['% Renewable'])
    country_name = list(Top15.where(Top15['% Renewable'] == np.max(Top15['% Renewable'])).dropna().index)[0]

    result = (country_name, max_percentage)

    return result

# Creating a new column that is the ratio of Self-Citations to Total Citations; and then, finding out 
# the maximum value for this new column, and the country that has the highest ratio.

def max_cit_ratio():

    Top15 = total_data()

    Top15['self_citation_ratio'] = Top15['Self-citations']/Top15['Citations']

    max_self_citation = np.max(Top15['self_citation_ratio'])

    country_name = list(Top15.where(Top15['self_citation_ratio'] == np.max(Top15['self_citation_ratio'])).dropna().index)[0]

    result = (country_name, max_self_citation)

    return result

# Creating a column that estimates the population using Energy Supply and Energy Supply per capita; and then,
# finding out the third most populous country according to this estimate.

def third_country():

    Top15 = total_data()

    Top15['estimated_population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']

    third_population = Top15['estimated_population'].sort_values(ascending = False).iloc[2]

    country_name = list(Top15.where(Top15['estimated_population'] == third_population).dropna().index)[0]

    return country_name

# Creating a column that estimates the number of citable documents per person; and then, finding out the
# correlation between the number of citable documents per capita and the energy supply per capita;
# using Pearson's R.

def correlation():

    Top15 = total_data()

    Top15['estimated_population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['estimated_citation_per_person'] = Top15['Citable documents']/Top15['estimated_population']

    cols = ['Energy Supply per Capita', 'estimated_citation_per_person']

    Top15n = Top15[cols]

    Top15n['estimated_citation_per_person'] = pd.to_numeric(Top15n['estimated_citation_per_person'])
    Top15n['Energy Supply per Capita'] = pd.to_numeric(Top15n['Energy Supply per Capita'])
    
    df = Top15n.corr()

    result = df.loc['estimated_citation_per_person']['Energy Supply per Capita']

    return result

# Creating a new column with a 1 if the country's % Renewable value is at or above the median for
# all countries in the top 15, and a 0 if the country's % Renewable value is below the median; and then,
# returning a series whose index is the country name sorted in ascending order of rank.

def RNW_median():

    Top15 = total_data()

    Top15['median_criteria'] = Top15.apply(lambda x: 1 if x['% Renewable'] >= np.median(Top15['% Renewable']) else 0, axis = 1)

    HighRenew = Top15['median_criteria'].sort_values()

    return HighRenew

# Using a dictionary to group the countries by continent; and then creating a dateframe that
# displays the sample size (the number of countries in each continent bin), and the sum, mean, 
# and the std using the estimated populations of countries in each group.

def groupings():

    Top15 = total_data()

    Top15['estimated_population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']

    Top15n = Top15.reset_index()

    def convertor(x):

        data = x['Country']

        ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
        
        for i in ContinentDict.keys():
            if data == i:
                return ContinentDict[i]
    
    Top15n['Continent'] = Top15n.apply(convertor, axis = 1)

    cols = ['Continent', 'estimated_population']
    Top15n = Top15n[cols]

    Top15n['estimated_population'] = pd.to_numeric(Top15n['estimated_population'])
    
    Result = pd.DataFrame(index = ['Asia', 'Australia', 'Europe', 'North America', 'South America'])
    
    Result['size'] = Top15n.groupby('Continent').count()
    Result['sum'] = Top15n.groupby('Continent').sum()
    Result['mean'] = Top15n.groupby('Continent').mean()
    Result['std'] = Top15n.groupby('Continent').std()

    return Result

# Cutting % Renewable into 5 bins; and then, grouping the Top15 by the Continent, as well as these new % Renewable bins.
# Then, finding out how many countries are in each of these groups.

def groupings_2():

    Top15 = total_data()
    Top15n = Top15.reset_index()

    def convertor(x):

        data = x['Country']

        ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

        for i in ContinentDict.keys():
            if data == i:
                return ContinentDict[i]
    
    Top15n['Continent'] = Top15n.apply(convertor, axis = 1)

    Top15n['Rnw_gp'] = pd.cut(Top15n['% Renewable'], 5)

    result = Top15n.groupby(['Continent', 'Rnw_gp']).size()

    return result

# Converting the Population Estimate series to a string with thousands separator (using commas).

def convertor_str():

    Top15 = total_data()
    Top15['estimated_population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']

    PopEst = Top15['estimated_population']

    for i in range(PopEst.shape[0]):
        PopEst.iloc[i] = '{:,}'.format(PopEst.iloc[i])
    
    return PopEst

f1 = total_data()
print(f1)
print('This was a function results.\n\n')
f2 = data_loss()
print(f2)
print('This was a function results.\n\n')
f3 = avg_GDP()
print(f3)
print('This was a function results.\n\n')
f4 = GDP_change()
print(f4)
print('This was a function results.\n\n')
f5 = mean_ESC()
print(f5)
print('This was a function results.\n\n')
f6 = max_RNW()
print(f6)
print('This was a function results.\n\n')
f7 = max_cit_ratio()
print(f7)
print('This was a function results.\n\n')
f8 = third_country()
print(f8)
print('This was a function results.\n\n')
f9 = correlation()
print(f9)
print('This was a function results.\n\n')
f10 = RNW_median()
print(f10)
print('This was a function results.\n\n')
f11 = groupings()
print(f11)
print('This was a function results.\n\n')
f12 = groupings_2()
print(f12)
print('This was a function results.\n\n')
f13 = convertor_str()
print(f13)
print('This was a function results.\n\n')

print('\nThanks for reviewing')

# Thanks for reviewing  
