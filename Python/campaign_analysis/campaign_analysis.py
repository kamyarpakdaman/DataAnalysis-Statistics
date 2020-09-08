# In this program, we are going to perform some analyses on a dataset for an ad campaign.

import pandas as pd

ad_clicks = pd.read_csv('campaign_info.csv')

# print(ad_clicks.head())

# Calculating the number of views from each 'utm_source' through counting the 'user_id's.
q2 = ad_clicks.groupby('utm_source')['user_id'].count().reset_index()

# print(q2)

# If the ad_click_timestamp is not null, then someone must have clicked on the ad.
# We create the new column 'is_clicked' to better access the clicked ads.

ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

# print(ad_clicks.head())

# In the following 3 steps, we find out the percentage of people who have clicked
# on the ads in each utm_source.

clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()

# print(clicks_by_source)

clicks_pivot = clicks_by_source.pivot(columns = 'is_click', index = 'utm_source', values = 'user_id')

clicks_pivot['percent_clicked'] = (100*(clicks_pivot[True]/(clicks_pivot[True] + clicks_pivot[False]))).round(2)

# print(clicks_pivot)

# Calculating the number of people viewing the ads A and B.

a_or_b = ad_clicks.groupby('experimental_group').user_id.count()

# print(a_or_b)

# Checking how many people clicked on ad A and how many clicked on ad B.

ad_segment = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()

# print(ad_segment)

# Now, using a pivot table to find out the percentage of people who have clicked on the ads.

ad_segment_pivot = ad_segment.pivot(columns = 'is_click', index = 'experimental_group', values = 'user_id')

ad_segment_pivot['percent_clicked'] = (100*(ad_segment_pivot[True]/(ad_segment_pivot[True] + ad_segment_pivot[False]))).round(2)

# print(ad_segment_pivot)

# Investigating if total clicks have changed by day of week.

# print(ad_clicks)

clicks_days = ad_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()

# print(clicks_days)

clicks_days_pivot = clicks_days.pivot( columns = 'is_click', index = 'day', values = 'user_id')

# print(clicks_days_pivot)

clicks_days_pivot['total_percent_clicked'] = (100*(clicks_days_pivot[True]/(clicks_days_pivot[True] + clicks_days_pivot[False]))).round(2)

clicks_days_pivot.reset_index(inplace = True)

# print(clicks_days_pivot)

# Investigating if clicks on ad A have changed by day of week.

a_clicks = ad_clicks[ad_clicks['experimental_group'] == 'A']

# print(a_clicks)

a_clicks_days = a_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()

# print(a_clicks_days)

a_clicks_days_pivot = a_clicks_days.pivot( columns = 'is_click', index = 'day', values = 'user_id')

# print(a_clicks_days_pivot)

a_clicks_days_pivot['a_percent_clicked'] = (100*(a_clicks_days_pivot[True]/(a_clicks_days_pivot[True] + a_clicks_days_pivot[False]))).round(2)

a_clicks_days_pivot.reset_index(inplace = True)

# print(a_clicks_days_pivot)

# Investigating if clicks on ad B have changed by day of week.

b_clicks = ad_clicks[ad_clicks['experimental_group'] == 'B']

# print(b_clicks)

b_clicks_days = b_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()

# print(b_clicks_days)

b_clicks_days_pivot = b_clicks_days.pivot( columns = 'is_click', index = 'day', values = 'user_id')

# print(b_clicks_days_pivot)

b_clicks_days_pivot['b_percent_clicked'] = (100*(b_clicks_days_pivot[True]/(b_clicks_days_pivot[True] + b_clicks_days_pivot[False]))).round(2)

b_clicks_days_pivot.reset_index(inplace = True)

# print(b_clicks_days_pivot)

# Merging the three sets of results, for ad A, ad B, and total clicks.

ab_merge = pd.merge(a_clicks_days_pivot, b_clicks_days_pivot, how = 'inner', left_on = 'day', right_on = 'day')

total_results = pd.merge(clicks_days_pivot, ab_merge, how = 'inner', left_on = 'day', right_on = 'day')

total_results = total_results[['day', 'a_percent_clicked', 'b_percent_clicked', 'total_percent_clicked']]

# print(total_results)

print('\nThanks for reviewing')

# Thanks for reviewing
