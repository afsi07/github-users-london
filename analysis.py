import pandas as pd
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the CSV files
users_df = pd.read_csv('users.csv')
repos_df = pd.read_csv('repositories.csv')

# 1. Top 5 users in London with the highest number of followers
top_followers = users_df.nlargest(5, 'followers')['login'].tolist()
print("Top 5 users by followers:", ", ".join(top_followers))

# 2. 5 earliest registered users
earliest_users = users_df.nsmallest(5, 'created_at')['login'].tolist()
print("5 earliest registered users:", ", ".join(earliest_users))

# 3. 3 most popular licenses
popular_licenses = repos_df['license_name'].value_counts().nlargest(3).index.tolist()
print("Top 3 licenses:", ", ".join(popular_licenses))

# 4. Majority company
company_mode = users_df['company'].mode()[0]
print("Majority company:", company_mode)

# 5. Most popular language
popular_language = repos_df['language'].mode()[0]
print("Most popular language:", popular_language)

# 6. Second most popular language for users after 2020
recent_users = users_df[users_df['created_at'] > '2020']
second_language = repos_df[repos_df['login'].isin(recent_users['login'])]['language'].value_counts().nlargest(2).index[-1]
print("Second most popular language after 2020:", second_language)

# 7. Language with the highest average stars
language_stars = repos_df.groupby('language')['stargazers_count'].mean().idxmax()
print("Language with highest avg stars:", language_stars)

# 8. Top 5 users by leader strength
users_df['leader_strength'] = users_df['followers'] / (1 + users_df['following'])
top_leader_strength = users_df.nlargest(5, 'leader_strength')['login'].tolist()
print("Top 5 by leader strength:", ", ".join(top_leader_strength))

# 9. Correlation between followers and repos
followers_repos_corr, _ = pearsonr(users_df['followers'], users_df['public_repos'])
print("Correlation between followers and repos:", round(followers_repos_corr, 3))

# 10. Regression: followers on repos
reg = LinearRegression().fit(users_df[['public_repos']], users_df['followers'])
slope = reg.coef_[0]
print("Regression slope of followers on repos:", round(slope, 3))

# 11. Correlation between projects and wiki enabled
projects_wiki_corr, _ = pearsonr(repos_df['has_projects'], repos_df['has_wiki'])
print("Correlation between projects and wiki enabled:", round(projects_wiki_corr, 3))

# 12. Average following for hireable vs. non-hireable users
hireable_following = users_df[users_df['hireable'] == True]['following'].mean()
non_hireable_following = users_df[users_df['hireable'] == False]['following'].mean()
hireable_diff = hireable_following - non_hireable_following
print("Average following diff (hireable - non-hireable):", round(hireable_diff, 3))

# 13. Correlation between bio word length amd followers

import pandas as pd
import statsmodels.api as sm

# Load the users data from the CSV file
users_df = pd.read_csv('users.csv')

# Filter out users without bios
users_with_bios = users_df[users_df['bio'].notna()]

# Calculate the length of the bio in words
#users_with_bios['bio_word_count'] = users_with_bios['bio'].str.split(" ").str.len()

# The error was here: users_with_bio was used instead of users_with_bios
users_with_bios['bio_word_count'] = users_with_bios['bio'].apply(lambda x: len(x.split()))


# Prepare the data for regression
X = users_with_bios['bio_word_count']  # Independent variable
y = users_with_bios['followers']        # Dependent variable

# Add a constant to the independent variable for the regression
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Get the regression slope (coefficient for bio_word_count)
slope = model.params['bio_word_count']

# Print the slope rounded to three decimal places
print(f'Regression slope of followers on bio word count: {slope:.3f}')

# 14. Top 5 users creating most repos on weekends
repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
repos_df['is_weekend'] = repos_df['created_at'].dt.weekday >= 5
weekend_repos = repos_df[repos_df['is_weekend']].groupby('login').size().nlargest(5).index.tolist()
print("Top 5 users by weekend repos:", ", ".join(weekend_repos))

# 15. Hireable users sharing emails more often
hireable_email_rate = users_df[users_df['hireable'] == True]['email'].notna().mean()
non_hireable_email_rate = users_df[users_df['hireable'] == False]['email'].notna().mean()
email_diff = hireable_email_rate - non_hireable_email_rate
print("Email sharing diff (hireable - non-hireable):", round(email_diff, 3))

# 16. Most common surname
users_df['surname'] = users_df['name'].fillna('').apply(lambda x: x.split()[-1] if x else '')
common_surname = users_df['surname'].mode()[0]
print("Most common surname:", common_surname)
