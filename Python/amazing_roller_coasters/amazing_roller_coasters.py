# In this amazing program, we use some data about roller coasters to create some visualizations.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Loading rankings data. wood and steel refer to the material of roller coasters. In functions 
# we use category argument to refer to the specific dataset. This dataset includes the rankings
# (if available) for some roller coasters (180 in eacg category) in the period of 2013 to 2018.

wood = pd.read_csv('Golden_Ticket_Award_Winners_Wood.csv')
steel = pd.read_csv('Golden_Ticket_Award_Winners_Steel.csv')

# print(wood.head())
# print(steel.head())

# A function to plot rankings over time for 1 roller coaster (specified by its name and park) in a specific category.

def chronological_ranks_roller(name, park, category):
    
    years_ranks = {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0}

    if category == 'wood':
        df = wood.copy()
        df = df[(df.Name == name) & (df.Park == park)]
        df = df.sort_values(by = ['Year of Rank'], axis = 0)
        years = list(df['Year of Rank'])
        ranks = list(df['Rank'])
        
        for i in range(len(years)):
            years_ranks[years[i]] = ranks[i]
        
        final_ranks = list(years_ranks.values())
    
    if category == 'steel':
        df = steel.copy()
        df = df[(df.Name == name) & (df.Park == park)]
        df = df.sort_values(by = ['Year of Rank'], axis = 0)
        years = list(df['Year of Rank'])
        ranks = list(df['Rank'])
        
        for i in range(len(years)):
            years_ranks[years[i]] = ranks[i]
        
        final_ranks = list(years_ranks.values())
    
    plt.figure(figsize = (8, 4))

    x_values = list(range(1, 7))
    
    if category == 'wood':  y_values = [len(wood.index)-rank+1 for rank in final_ranks]
    
    if category == 'steel':  y_values = [len(steel.index)-rank+1 for rank in final_ranks]
    
    plt.plot(x_values, y_values, color = 'darkslateblue')
    plt.ylabel('Ranks')
    plt.title('Ranks for roller coaster {} in park {}'.format(name, park))
    ax = plt.gca()
    ax.set_xticks(x_values)
    ax.set_xticklabels(list(range(2013, 2019)))

    y_ticks = list(range(min(y_values), max(y_values)+1))
    y_tick_labels = [len(wood.index)-rank+1 for rank in y_ticks]

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, right = False,
    top = False, bottom = False)
    plt.show()
    
    return

chronological_ranks_roller('El Toro', 'Six Flags Great Adventure', 'wood')

# A function to plot rankings over time for 2 roller coasters (specified by their names and parks) in a specific category.

def chronological_ranks_2_rollers(name_1, park_1, name_2, park_2, category):

    years_ranks_1 = {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0}
    years_ranks_2 = {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0}

    if category == 'wood':
        df_1 = wood.copy()
        df_1 = df_1[(df_1.Name == name_1) & (df_1.Park == park_1)]
        df_1 = df_1.sort_values(by = ['Year of Rank'], axis = 0)
        years_1 = list(df_1['Year of Rank'])
        ranks_1 = list(df_1['Rank'])
        
        for i in range(len(years_1)):
            years_ranks_1[years_1[i]] = ranks_1[i]
        
        final_ranks_1 = list(years_ranks_1.values())
        
        df_2 = wood.copy()
        df_2 = df_2[(df_2.Name == name_2) & (df_2.Park == park_2)]
        df_2 = df_2.sort_values(by = ['Year of Rank'], axis = 0)
        years_2 = list(df_2['Year of Rank'])
        ranks_2 = list(df_2['Rank'])
        
        for i in range(len(years_2)):
            years_ranks_2[years_2[i]] = ranks_2[i]
        
        final_ranks_2 = list(years_ranks_2.values())
    
    if category == 'steel':
        df_1 = steel.copy()
        df_1 = df_1[(df_1.Name == name_1) & (df_1.Park == park_1)]
        df_1 = df_1.sort_values(by = ['Year of Rank'], axis = 0)
        years_1 = list(df_1['Year of Rank'])
        ranks_1 = list(df_1['Rank'])
        
        for i in range(len(years_1)):
            years_ranks_1[years_1[i]] = ranks_1[i]
        
        final_ranks_1 = list(years_ranks_1.values())
        
        df_2 = steel.copy()
        df_2 = df_2[(df_2.Name == name_2) & (df_2.Park == park_2)]
        df_2 = df_2.sort_values(by = ['Year of Rank'], axis = 0)
        years_2 = list(df_2['Year of Rank'])
        ranks_2 = list(df_2['Rank'])
        
        for i in range(len(years_2)):
            years_ranks_2[years_2[i]] = ranks_2[i]
        
        final_ranks_2 = list(years_ranks_2.values())
    
    plt.figure()

    x_values = list(range(1, 7))
    
    if category == 'wood':
        y_values_1 = [len(wood.index)-rank+1 for rank in final_ranks_1]
        y_values_2 = [len(wood.index)-rank+1 for rank in final_ranks_2]
    
    if category == 'steel':
        y_values_1 = [len(steel.index)-rank+1 for rank in final_ranks_1]
        y_values_2 = [len(steel.index)-rank+1 for rank in final_ranks_2]

    plt.plot(x_values, y_values_1, color = 'darkslateblue')
    plt.plot(x_values, y_values_2, color = 'springgreen')

    plt.ylabel('Ranks')
    plt.title('Ranks for roller coasters {} in park {}\nand {} in park {}'.format(name_1, park_1, name_2, park_2))
    ax = plt.gca()
    ax.set_xticks(x_values)
    ax.set_xticklabels(list(range(2013, 2019)))

    y_ticks = list(range((min(min(y_values_1), min(y_values_2))), (max(max(y_values_1)+1, max(y_values_2)+1))))    
    y_tick_labels = [len(wood.index)-rank+1 for rank in y_ticks]

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, right = False,
    top = False, bottom = False)
    line_1 = mpatches.Patch(color = 'darkslateblue', label = name_1)
    line_2 = mpatches.Patch(color = 'springgreen', label = name_2)
    plt.legend(handles = [line_1, line_2], frameon = True)
    plt.show()
    
    return

chronological_ranks_2_rollers('El Toro', 'Six Flags Great Adventure', 'Phoenix', 'Knoebels Amusement Resort', 'wood')

# A function to plot rankings of all roller coasters which have been ranked n-th or better at least one time, over time.
# For example, when n = 5 and category = 'wood', the function finds roller coasters in wood dataset which have at least
# one record of being ranked 1st, 2nd, 3rd, 4th, or 5th. The it draws bar plots demontrating the rankings of these roller coasters
# from 2013 to 2018.

def chronological_ranks_n_rollers(n, category):
    
    min_y_values = []
    max_y_values = []

    if category == 'wood':

        df = wood.copy()
        df['combined'] = df.apply(lambda x: x['Name']+'@'+x['Park'], axis = 1)
        
        plt.figure(figsize = (15, 6))
        x_values = list(range(1, 7))
        
        for roller_coaster in list(set(df['combined'])):

            ndf = df.copy()
            years_ranks = {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0}
            all_ranks = list(set(ndf[ndf['combined'] == roller_coaster]['Rank']))
            
            if min(all_ranks) <= n:
                ndf = ndf[ndf.combined == roller_coaster]
                ndf = ndf.sort_values(by = ['Year of Rank'], axis = 0)
                years = list(ndf['Year of Rank'])
                ranks = list(ndf['Rank'])
        
                for i in range(len(years)):
                    years_ranks[years[i]] = ranks[i]
                
                final_ranks = list(years_ranks.values())
                y_values = [len(wood.index)-rank+1 for rank in final_ranks]
                min_y_values.append(min(y_values))
                max_y_values.append(max(y_values))
                plt.plot(x_values, y_values, label = roller_coaster.split('@')[0])
    
    if category == 'steel':
        df = steel.copy()
        df['combined'] = df.apply(lambda x: x['Name']+'@'+x['Park'], axis = 1)
        
        plt.figure(figsize = (12, 6))
        x_values = list(range(1, 7))

        for roller_coaster in list(set(df['combined'])):

            ndf = df.copy()
            years_ranks = {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0}
            all_ranks = list(set(ndf[ndf['combined'] == roller_coaster]['Rank']))

            if min(all_ranks) <= n:
                ndf = ndf[ndf.combined == roller_coaster]
                ndf = ndf.sort_values(by = ['Year of Rank'], axis = 0)
                years = list(ndf['Year of Rank'])
                ranks = list(ndf['Rank'])
        
                for i in range(len(years)):
                    years_ranks[years[i]] = ranks[i]
                
                final_ranks = list(years_ranks.values())
                y_values = [len(wood.index)-rank+1 for rank in final_ranks]
                min_y_values.append(min(y_values))
                max_y_values.append(max(y_values))
                plt.plot(x_values, y_values, label = roller_coaster.split('@')[0])
    
    plt.ylabel('Ranks')
    plt.title('Ranks for roller coasters with at least one record of a rank as or better than {}'.format(n))
    ax = plt.gca()
    ax.set_xticks(x_values)
    ax.set_xticklabels(list(range(2013, 2019)))

    y_ticks = list(range(min(min_y_values), max(max_y_values)+1))    
    y_tick_labels = [len(wood.index)-rank+2 for rank in y_ticks]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, right = False,
    top = False, bottom = False)
    plt.legend(loc='upper left', bbox_to_anchor=(0.97, 1), ncol=1)
    
    plt.show()
    
    return

chronological_ranks_n_rollers(5, 'wood')

# Loading roller coaster data. this dataset contains some numeric data about roller coasters such as their heigh and weight.

# captain_coasters = pd.read_csv('roller_coasters.csv')

# print(captain_coasters.head())

# A function to plot a histogram of a specific column.

def hist_drawer(df, field):

    ndf = df.copy()
    ndf = ndf.dropna(subset = [field])
    data = list(ndf[field])

    plt.figure()
    plt.hist(data, color = 'darkslateblue')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, bottom = False)
    plt.title('Distribution of Column {}'.format(field))
    
    plt.show()

    return

hist_drawer(captain_coasters, 'speed')

# A function to plot inversions by coaster at a park here. This function finds all roller coasters in a specific park,
# extracts inversions numbers of all of them, and demonstrates them in a bar chart.

def inversions_in_park(df, park):

    ndf = df.copy()
    ndf = ndf[ndf.park == park]
    roller_coasters_park = list(set(ndf['name']))

    roller_coaster_names = []
    roller_coaster_inversions = []

    for roller_coaster in roller_coasters_park:
        roller_coaster_names.append(roller_coaster)
        num_inversions = int(ndf[ndf.name == roller_coaster]['num_inversions'])
        roller_coaster_inversions.append(num_inversions)
    
    plt.figure(figsize = (12, 7))
    x_values = range(len(roller_coaster_names))
    bars = plt.bar(x_values, roller_coaster_inversions)
    ax = plt.gca()
    ax.set_xticks(x_values)
    ax.set_xticklabels(roller_coaster_names, rotation = -90)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(left = False, bottom = False, labelleft = False)
    for bar in bars:

        if bar.get_height() > 0:
            ax.text(bar.get_x() + bar.get_width()/2, 
                  bar.get_height() - 0.6,
                  int(bar.get_height()),
                  ha = 'center', color = 'w')
    plt.title('Number of Inversions in Roller Coasters of Park {}'.format(park))
    plt.gcf().subplots_adjust(bottom=0.5)
    plt.show()

    return

inversions_in_park(captain_coasters, "Parc Asterix")

# A function to plot a pie chart of operating status for all dataset.

def operation_pie(df):

    ndf_1 = df.copy()
    ndf_2 = df.copy()
    operating = len(list(ndf_1[ndf_1.status == 'status.operating']['name']))
    closed = len(list(ndf_2[ndf_2.status == 'status.closed.definitely']['name']))
    data = [operating, closed]

    plt.figure()
    plt.pie(data, colors = ['springgreen', 'darkslateblue'], labels = ['Operating', 'Closed'], autopct = "%0.1f")
    
    plt.show()

    return

operation_pie(captain_coasters)
  
# A function to create a scatter plot of any two numeric columns. Furthermore, the plot contains degree-1 polynomial
# regression line.

def scatter_numerics(df, field_1, field_2):

    ndf = df.copy()
    ndf = ndf.dropna(subset = [field_1, field_2])
    data_1 = list(ndf[field_1])
    data_2 = list(ndf[field_2])

    z = np.polyfit(data_1, data_2, 1)
    line_function = np.poly1d(z)

    plt.figure()
    plt.plot(data_1, line_function(data_1), color = 'springgreen')
    plt.scatter(data_1, data_2, color = 'darkslateblue')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, bottom = False)
    plt.title('Scatter of Columns {} and {}'.format(field_1, field_2))
    
    plt.show()

    return

scatter_numerics(captain_coasters, 'speed', 'height')

print('\nThanks for reviewing')

# Thanks for reviewing
