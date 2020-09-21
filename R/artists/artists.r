# In this program, we make some simple modifications to a dataframe in R.

library(dplyr)
library(readr)

artists <- read_csv('artists.csv')
head(artists)

# Selecting columns

chosen_cols <- artists %>% 
  select(-country,-year_founded,-albums)
head(chosen_cols)  

# Filtering rows

popular_not_hip_hop <- chosen_cols %>% 
  filter(spotify_monthly_listeners > 20000000, genre != 'Hip Hop') 
head(popular_not_hip_hop)

# Arranging rows

youtube_desc <- popular_not_hip_hop %>% 
  arrange(desc(youtube_subscribers))
head(youtube_desc)

# A combination of all above

artists <- artists %>%
select(-country,-year_founded,-albums) %>% 
filter(spotify_monthly_listeners>20000000,!(genre=='Hip Hop')) %>%
arrange(desc(youtube_subscribers))
head(artists)

print('Thanks for reviewing')
# Thanks for reviewing
