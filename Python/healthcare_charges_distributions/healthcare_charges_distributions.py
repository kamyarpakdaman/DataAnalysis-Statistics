# In this program, we use the data for healthcare diagnoses and charges in the US states to find out what are the
# distributions of charges for a specific diagnosis, 313 - CHEST PAIN, in different states.

import pandas as pd
from matplotlib import pyplot as plt

healthcare = pd.read_csv("healthcare.csv")

states = []
charges = []

for state in sorted(list(set(healthcare['Provider State']))):
    charges_list = list(healthcare[(healthcare['DRG Definition'] == '313 - CHEST PAIN') & (healthcare['Provider State'] == state)][' Average Covered Charges '])
    states.append(state)
    charges.append(charges_list)

plt.figure(figsize = (20, 6))

plt.boxplot(charges)

plt.show()

print('\nThanks for reviewing')

# Thanks for reviewing
