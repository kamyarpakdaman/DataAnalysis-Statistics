# In this program, we're going to analyze the funnel from visit to purchase
# for a website.

from datetime import datetime as dt
import pandas as pd
from functools import reduce

visits = pd.read_csv('visits.csv')
cart = pd.read_csv('cart.csv')
checkout = pd.read_csv('checkout.csv')
purchase = pd.read_csv('purchase.csv')

# print(visits.head())
# print(cart.head())
# print(checkout.head())
# print(purchase.head())

# Cleaning the dates

visits['Visit_time'] = visits['visit_time'].apply(lambda row: dt.strptime(row, "%m/%d/%Y %H:%M"))
cart['Cart_time'] = cart['cart_time'].apply(lambda row: dt.strptime(row, "%m/%d/%Y %H:%M"))
checkout['Checkout_time'] = checkout['checkout_time'].apply(lambda row: dt.strptime(row, "%m/%d/%Y %H:%M"))
purchase['Purchase_time'] = purchase['purchase_time'].apply(lambda row: dt.strptime(row, "%m/%d/%Y %H:%M"))

# Merging the tables for drawing the desired info.

visits_to_cart = pd.merge(visits, cart, how = 'left', left_on = 'user_id', right_on = 'user_id')

# print(visits_to_cart.head())

visits_to_cart_cr = round(100*(visits_to_cart.Cart_time.count()) / (visits_to_cart.Visit_time.count()), 2)

print(visits_to_cart_cr)

cart_to_checkout = pd.merge(cart, checkout, how = 'left', left_on = 'user_id', right_on = 'user_id')

# print(cart_to_checkout.head())

cart_to_checkout_cr = round(100*(cart_to_checkout.Checkout_time.count()) / (cart_to_checkout.Cart_time.count()), 2)

print(cart_to_checkout_cr)

checkout_to_purchase = pd.merge(checkout, purchase, how = 'left', left_on = 'user_id', right_on = 'user_id')

# print(checkout_to_purchase.head())

checkout_to_purchase_cr = round(100*(checkout_to_purchase.Purchase_time.count()) / (checkout_to_purchase.Checkout_time.count()), 2)

print(checkout_to_purchase_cr)

# We can see that the visits to cart step has the weakest conversion rate.

# Calculating the average time from visit to purchase.

dfs = [visits, cart, checkout, purchase]

all_data = reduce(lambda  left,right: pd.merge(left, right, on=['user_id'], how='left'), dfs)

all_data['time_to_purchase'] = all_data.Purchase_time - all_data.Visit_time

# print(all_data.head())

avg_time_to_purchase = all_data.time_to_purchase.mean()

print(avg_time_to_purchase)

print('\nThanks for reviewing')

# Thanks for reviewing
