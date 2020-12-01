# In this program, we use binomial distribution to investigate if our survey results are valid or not.

import numpy as np
import matplotlib.pyplot as plt

# This is the result of a survey about the winner of the presidential elevtion.

survey_responses = ['Ceballos', 'Kerrigan', 'Ceballos', 'Ceballos', 'Ceballos','Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Ceballos', 
'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Ceballos', 'Ceballos', 'Ceballos', 'Ceballos',
'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Ceballos',
'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Ceballos', 'Ceballos', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Kerrigan', 'Ceballos']

# Computing the number of people who voted for Ceballos.

total_ceballos = survey_responses.count('Ceballos')
# print(total_ceballos)
n_survey_responses = len(survey_responses)
percentage_ceballos = total_ceballos/float(n_survey_responses)
print(percentage_ceballos)

# While our survey says around 47% of voters will choose Ceballos, in the real election, 54% of the 10000 town population voted for Ceballos. We want to know if there is something wrong with the poll.

# We create a binomial distribution assuming the actual percentage happens in a survey of our survey size. Then we draw a histogram of our distribution.

possible_surveys = np.random.binomial(n_survey_responses, 0.54, size=10000) / float(n_survey_responses)
# print(possible_surveys)

plt.figure()

plt.hist(possible_surveys, range=(0, 1), bins=20)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(left = False, bottom = False)
plt.xlabel('Possible Ceballos Vote Shares')
plt.savefig('result_1.png')

plt.show()

# Now we calculate the percentage of survey results indicating Ceballos' losing, even though he has won.

ceballos_loss_surveys = np.mean(possible_surveys < 0.5)

# Alright. Around 20% of the time a survey output would predict Ceballos losing, even if he has won.

print(ceballos_loss_surveys)

# Let's assume we had run our survey with 7000 people. How likely were we to make a wrong prediction in that case?

# We create a binomial distribution in the new setting and repeat the previous steps.

large_surveys = np.random.binomial(7000, 0.54, size=10000) / float(7000)
# print(possible_surveys)

plt.figure()

plt.hist(large_surveys, range=(0, 1), bins=10)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(left = False, bottom = False)
plt.xlabel('Possible Ceballos Vote Shares with Large Survey Size')
plt.savefig('result_2.png')

plt.show()

# Now we calculate the percentage of survey results indicating Ceballos' losing, even though he has won, using the large survey size.

ceballos_loss_large_surveys = np.mean(large_surveys < 0.5)

# Cool. The result indicates 0% of the time a large survey output would predict Ceballos losing, even if he has won.

print(ceballos_loss_large_surveys)

print('\nThanks for reviewing')

# Thanks for reviewing
