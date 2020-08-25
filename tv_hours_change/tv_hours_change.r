# In this program, we will perform some statistical inferences on a dataset.

library(ggplot2)
library(dplyr)
library(statsr)
load("gss.Rdata")

# Below is the research question we want to investigate.

# How has the mean hours spent on watching TV changed from 2000 to 2012 for the US households?

# To perform the exploratory data analysisT at first, let's create a data set including the year and tvhour columns, 
# where the year is either 2000 or 2012.

tvhour0012 <- gss %>%
  filter(year == 2000 | year == 2012) %>%
  select(year, tvhours)

# Now let's see the summary statistics and mean values for the tvhour grouped by the year:

tvhour_mean <- tvhour0012 %>% 
    group_by(year) %>%
    summarise(mean_val = mean(tvhours, na.rm = TRUE))

# Now we create a bar chart for the change in the mean value in 2000 and 2012:

ggplot(data = tvhour_mean, aes(x = c('2000', '2012'), y = mean_val)) + geom_bar(stat = 'identity', fill = 
'steelblue') + geom_text(aes(label = round(mean_val, digits = 2)), vjust = 3, color = 
'white') + theme(axis.text.x = element_text(), axis.text.y = element_blank()) + labs(title = 
"Hours Spent Watching TV, 2000 and 2012") + xlab("Years") + ylab("Mean Watching TV Hours")

# Alright! As we can see, the mean value for hours spent on watching TV has changed from 2.97 hours per day 
# to 3.09 hours per day in our sample.

# To perform the inference, note that we have two mean values from the sample, our sample statistics. At first, we will 
# perform our hypothesis test to see if there is strong evidence that the mean hours spent on watching TV is changed 
# from 2000 to 2012. We assume the conditions for a hypothesis test are met.

# H0: mu(tvhours 2012) - mu(tvhours 2000) = 0
# HA: mu(tvhours 2012) - mu(tvhours 2000) <> 0

# Below, we perform the hypothesis testing:

inference(y = tvhours, x = year, data = tvhour0012, statistic = 'mean',
          type = 'ht', null = 0, alternative = 'twosided', method = 'theoretical')

# As of the result of the hypothesis testing, we get a p-value of 0.2393; hence, with an alpha of 0.05, we cannot reject 
# the H0. Therefore, we can conclude that at a 5% significance level, there isn't strong evidence that the hours spent 
# watching TV has changed from 2000 to 2012.

# Now, let's calculate the 0.95 confidence interval to see if our results from CI and HT match. Again, we assume the conditions
# are met.

inference(y = tvhours, x = year, data = tvhour0012, statistic = 'mean',
          type = 'ci', method = 'theoretical')

# As a result, our confidence interval for the difference of the means at a 95% confidence level would be (-0.3135 , 0.0783). We can see that our null value, 0, lie within the interval; hence, we see that our results from the HT and calculating the CI match, and that we cannot reject our H0, which insists there isn't strong enough evidence that the mean hours spent watching TV is changed from 2000 to 2012.

print('\nThanks for reviewing')

# Thanks for reviewing
