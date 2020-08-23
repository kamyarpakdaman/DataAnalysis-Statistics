# In this program, we'll analyze some parts of the dataset statistically.

# Make sure the name of the file is entered correctly.
dataset <- read.csv("fifa_19.csv")

dim(dataset)
str(dataset)

# All levels for Factor variable of preferred.foot, which is, expectedly,
# right or left. :D
levels(dataset$Preferred.foot)

# Calculating the mean and median values for players' acceleration
accel_mean <- mean(dataset$Acceleration)
accel_med <- median(dataset$Acceleration)

# Calculating the mode value for players' acceleration
accel_freq <- table(dataset$Acceleration)
sort(accel_freq, decreasing = TRUE)

# Creating a new Factor variable which categorizes the players based on their
# acceleration either as High acceleration or Low acceleration
dataset$acceleration_category[dataset$Acceleration >= accel_mean] <- "High acceleration"
dataset$acceleration_category[dataset$Acceleration < accel_mean] <- "Low acceleration"

dataset$acceleration_category <- as.factor(dataset$acceleration_category)

# The frequency of different ages for all players
table(dataset$Age)

# The frequency of different preferred foots for all players
frequency_pfoot <- table(dataset$Preferred.foot)

# Drawing a barplot to display the frequency of different preferred foots
# for all players
barnames <- c("Left footed", "Right footed")
barplot(frequency_pfoot, ylab = "Frequency", xlab = "Preferred foot", names.arg = barnames, main = "Preferred foot frequency")

# Drawing a histogram to display the frequency of different overalls for all
# players
hist(dataset$Overall, ylab = "Frequency", xlab = "Overall ranges", ylim = c(0, 2500), xlim = c(50, 96), main = "Frequency of players' overalls", col = "blue")

# Calculating the range, the quantiles and the IQR for all players' curves
quantile(dataset$Curve)
IQR(dataset$Curve)

# Drawing a baxplot to display dispersity characteristics for players' curves
boxplot(dataset$Curve, main = "Curve dispersity characteristics", col = "green")

# Calculating the standard deviation for players' aggressions
sd(dataset$Aggression)

# Calculating z-scores for different values for players' accelerations
accel_sd <- sd(dataset$Acceleration)
accel_z <- (dataset$Acceleration - accel_mean)/accel_sd

# Drawing a scatterplot to assess the correlation between players' accelerations
# and their overalls; using a random sample of 500 players. Further, we calculate
# the correlation between the two variables, or the Pearson's R. Then we'll find
# the coefficients between players' accelerations and their overalls and draw the
# regression line. Finally, we calculate the R-squared to assess how fir our
# regression line is.

overalls <- dataset$Overall
overalls <- sample(overalls, 500)
accelerations <- dataset$Acceleration
accelerations <- sample(accelerations, 500)
plot(accelerations, overalls, main = "Overalls based on Accelerations")

pearson_r <- cor(accelerations, overalls)

coeffs <- lm(overalls~accelerations)
abline(coeffs)
r_squared <- pearson_r ** 2

# Creating a raw contingency table, and then, a contingency table including the
# proportional percentages, for players weak foot scores (the vertical axis) and skill moves
# score (the horizontal axis). Then, checking the marginal values, which equal to 1.

table(dataset$Weak.Foot, dataset$Skill.Moves)
target_table <- prop.table(table(dataset$Weak.Foot, dataset$Skill.Moves))

rowSums(target_table)
sum(rowSums(target_table))

colSums(target_table)
sum(colSums(target_table))

# Drawing the probability density function diagram for players' overalls, which is approximately
# normal.

overall_mean <- mean(dataset$Overall)
overall_sd <- sd(dataset$Overall)
density <- dnorm(dataset$Overall, mean = overall_mean, sd = overall_sd)
plot(dataset$Overall, density, main = "Players' Overalls pdf diagram", col = "green")

# Calculating the cumulative probability for players' weak foot score. Further, we calculate
# the mean (i. e., the expected score), the variance and the sd for weak foot score.

wf_freq_table <- table(dataset$Weak.Foot)
wf_percent_freq_table <- prop.table(wf_freq_table)
cumsum(wf_percent_freq_table)

df <- as.data.frame(wf_percent_freq_table)
wf_expected_score <- sum(as.numeric(df$Var1) * as.numeric(df$Freq))
wf_variance <- sum((as.numeric(df$Var1) - expected_score)**2)/(nrow(df)-1)
wf_sd <- wf_variance ** 0.5

# Calculating the probability of a player having an overall score of 80 or less.

round((pnorm(80, mean = overall_mean, sd = overall_sd), digits = 2)

# Calculating the 65th percentile for players' overall scores.

qnorm(0.65, mean = overall_mean, sd = overall_sd)

# Creating a sampling distribution for means for the players' curves and drawing the
# density plot for the sampling distribution means, which is normal.

sample_means = NULL
for (i in 1:500) {
     samp <- sample(dataset$Curve, 500)
     sample_means[i] <- mean(samp)
}

curve_sample_mean <- mean(sample_means)
curve_sample_sd <- sd(sample_means)
curve_sampling_distribution_density <- dnorm(sample_means, mean = curve_sample_mean, sd = curve_sample_sd)
plot(sample_means, curve_sampling_distribution_density)

# Creating a sampling distribution for proportions for the players' preferred feet
# and calculating the mean and the sd for the sampling distribution for proportions.
# The proportion of success will be a player's being right footed. Then we draw the
# density plot for the sampling distribution for proportions, which is normal.

for (i in 1:500) {
    samp <- sample(dataset$Preferred.Foot, 500)
    samp_table <- prop.table(table(samp))
    samp_table <- as.data.frame(samp_table)
    samp_prop <- subset(samp_table$Freq, samp_table$samp == "Right")
    sample_means[i] <- samp_prop
}

prop_sample_mean <- mean(sample_means)
prop_sample_sd <- sd(sample_means)
prop_sampling_distribution_density <- dnorm(sample_means, mean = prop_sample_mean, sd = prop_sample_sd)
plot(sample_means, prop_sampling_distribution_density)

# Calculating 0.95 confidence interval for a sample mean of players' overall scores
# assuming we don't have the population sd.

samp <- sample(dataset$Overall, 500)
samp_mean <- mean(samp)
samp_sd <- sd(samp)
estimated_samp_sd <- samp_sd/(500**0.5)
lower_limit <- samp_mean-1.984*estimated_samp_sd
upper_limit <- samp_mean+1.984*estimated_samp_sd

# Calculating 0.95 confidence interval for a sample proportion of players being right footed
# scores assuming we don't have the population proportion.

samp <- sample(dataset$Preferred.Foot, 500)
samp_table <- prop.table(table(samp))
samp_table <- as.data.frame(samp_table)
samp_prop <- subset(samp_table$Freq, samp_table$samp == "Right")
estimated_samp_sd <- ((samp_prop*(1-samp_prop))/500)**0.5
lower_limit <- samp_prop-1.96*estimated_samp_sd
upper_limit <- samp_prop+1.96*estimated_samp_sd

# Significance testing for proportion. Alternative hypothesis: More than 60% of
# players are right footed. Null hypothesis: 60% of players are right footed. At first,
# we assume the null hypothesis is true, so, the proportion of right footed players equalas
# to 0.6. We take a random sample of 500 players and calculate the proportion of
# right footed players. Then we calculate the z-score for the proportion of the
# sample. Finally, with a significance level of 0.05, we reject the null hypothesis
# and conclude with a significance level of 0.05, more than 60% of players are
# right footed. This is a one-tailed test.

samp <- sample(dataset$Preferred.Foot, 500)
samp_table <- prop.table(table(samp))
samp_table <- as.data.frame(samp_table)
samp_prop <- subset(samp_table$Freq, samp_table$samp == "Right")
estimated_sd <- ((0.6*(1-0.6))/500)**0.5
samp_prop_z_score <- (samp_prop - 0.6)/estimated_sd

# Significance testing for mean. Alternative hypothesis: The mean of the players' overall
# isn't equal to 64. Null hypothesis: The mean of the players' overall is equal to 64.
# At first, we assume the null hypothesis is true, so, the mean of players' overall
# equalas to 64. We take a random sample of 500 players and calculate the mean of
# players' overall. Then we calculate the t-score for the mean of the
# sample. Finally, with a significance level of 0.01, we reject the null hypothesis
# and conclude with a significance level of 0.01 that the mean of players' overall isn't
# equal to 64. This is a two-tailed test.

samp <- sample(dataset$Overall, 500)
samp_mean <- mean(samp)
samp_sd <- sd(samp)
t_score <- (samp_mean - 64)/(samp_sd/(500**0.5))

print('Thanks for reviewing')
# Thanks for reviewing
