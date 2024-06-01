import numpy as nu
import pandas as pd
import matplotlib.pyplot as polt
import seaborn as sbn
sbn.set(style='whitegrid')
import textwrap
from wordcloud import WordCloud, STOPWORDS

stat = pd.read_csv('DataScientist.csv')
print(stat.head())

# Data Pre-Processing
# Rows and Columns Dropping

stat.drop(['Unnamed: 0', 'Competitors', 'Founded', 'Sector'], axis=1, inplace=True)
stat = stat.set_index(['index'])

# Replace data with a value of -1 with a value of NaN
stat = stat.replace([-1, -1.0, '-1'], nu.nan)
print(stat.isnull().sum(axis=0))

# Fill in the rows where there are NaN values in the column 'Easy Apply'
stat['Easy Apply'].fillna('FALSE', inplace=True)
# Rows with NaN values should be dropped
stat.dropna(axis=0, inplace=True)
print(stat)

# The process of cleaning columns
# "Salary" Column Values Cleaning

stat['Salary Estimate'] = stat['Salary Estimate'].str.replace('(', '').str.replace(')', '').str.replace(
    'Glassdoor est.', '').str.replace('Employer est.', '')

stat['Min Salary'], stat['Max Salary'] = stat['Salary Estimate'].str.split('-').str
stat['Min Salary'] = stat['Min Salary'].str.strip(' ').str.strip('$').str.strip('K').fillna(0).astype(int)
stat['Max Salary'] = stat['Max Salary'].str.replace('Per Hour', '')
stat['Max Salary'] = stat['Max Salary'].str.strip(' ').str.strip('$').str.strip('K').fillna(0).astype(int)
print(stat[['Salary Estimate', 'Min Salary', 'Max Salary']])

fig, ax = polt.subplots(1, 2, figsize=(16, 4))
sbn.distplot(ax=ax[0], a=stat['Min Salary'])

sbn.distplot(ax=ax[1], a=stat['Max Salary'])
polt.show()

#"Revenue" Column values cleaning

stat['Revenue'].replace(['Unknown / Non-Applicable'], nu.nan, inplace=True)
print(stat[['Revenue']])

# ## "Job Titles" Cloumn Values Cleaning
# comment_words
com_words = ''
stopwords = set(STOPWORDS)

for vale in stat['Job Title']:
    vale = str(vale)
    tokens = vale.split()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    com_words += " ".join(tokens) + " "

wordcloud = WordCloud(background_color='pink', height=211, width=907,
                      stopwords=stopwords, max_font_size=211).generate(com_words)

fig, ax = polt.subplots(figsize=(19, 19))
ax.grid(False)
ax.imshow((wordcloud))
fig.tight_layout(pad=1)
print(polt.show())

# Data scientists are not the only jobs available for recruitment, as indicated by the figure above. Since we want to explore only data scientist jobs, we remove data from Job title columns that do not contain data scientist or data science.

stat = stat[stat['Job Title'].str.contains('Data Science|Data Scientist')]
print(stat)

# # Visualization and Analysis
# # Rating

viewdata = stat.groupby('Rating')['Job Title'].count().reset_index()
viewdata.sort_values('Job Title', ascending=False).head()

fig, ax = polt.subplots(figsize = (25, 10))
#sns.barplot(ax = ax, data = dataview, x = 'Rating', y = 'Job Title', order = dataview.sort_values('Job Title', ascending = False).Rating)
sbn.barplot(stat = viewdata, x = 'Rating', y = 'Job Title', palette = 'deep', ax = ax)
ax.set_ylabel('Count Jobs')
for index,viewdata in enumerate(viewdata['Job Title'].astype(int)):
        ax.text(x=index-0.1 , y =viewdata , s= f"{viewdata}" , fontdict=dict(fontsize=10))
print(polt.show())

# Rating Vs Industry

viewdata_up = stat.groupby('Industry')['Rating'].mean().reset_index()
viewdata_up = viewdata_up.sort_values('Rating', ascending=False).head(10)

viewdata_dow = stat.groupby('Industry')['Rating'].mean().reset_index()
viewdata_dow = viewdata_dow.sort_values('Rating', ascending=True).head(10)

print(viewdata_up, '\n')
print(viewdata_dow)

max_width = 17
ratingdata = [viewdata_up, viewdata_dow]
titledata = ['Top 10', 'Bottom 10']
fig, ax = polt.subplots(2, 1, figsize=(26, 14))
fig.subplots_adjust(hspace=0.5)
for i in range(0, 2):
    sbn.barplot(ax=ax[i], data=ratingdata[i], x='Industry', y='Rating', color='aqua', label='Rating')
    ax[i].set_title(titledata[i] + ' Average Rating Company in Each Industry', fontsize=20)
    ax[i].set_ylabel('Rating', fontsize=20)
    ax[i].set_xlabel('Industry', fontsize=20)
    ax[i].set_xticklabels(textwrap.fill(x.get_text(), max_width) for x in ax[i].get_xticklabels())
    ax[i].set_yticks(nu.arange(0, 5, step=0.5))
    for index, ratingdata[i] in enumerate(nu.round(ratingdata[i]['Rating'], 2)):
        ax[i].text(x=index - 0.1, y=ratingdata[i], s=f"{ratingdata[i]}", fontdict=dict(fontsize=16))
    ax[i].tick_params(labelsize=18)

print(polt.show())

# Rating Vs Location

viewdata_up = stat.groupby('Location')['Rating'].mean().reset_index()
viewdata_up = viewdata_up.sort_values('Rating', ascending=False).head(10)

viewdata_dow = stat.groupby('Location')['Rating'].mean().reset_index()
viewdata_dow = viewdata_dow.sort_values('Rating', ascending=True).head(10)

print(viewdata_up, '\n')
print(viewdata_dow)

max_width = 15
ratingdata = [viewdata_up, viewdata_dow]
titledata = ['Top 10', 'Bottom 10']
fig, ax = polt.subplots(2, 1, figsize=(24, 14))
fig.subplots_adjust(hspace=0.5)
for i in range(0, 2):
    sbn.barplot(ax=ax[i], data=ratingdata[i], x='Location', y='Rating', color='purple', label='Rating')
    ax[i].set_title(titledata[i] + ' Companies Average Rating in Each State', fontsize=20)
    ax[i].set_ylabel('Rating', fontsize=20)
    ax[i].set_xlabel('Location', fontsize=20)
    ax[i].set_xticklabels(textwrap.fill(x.get_text(), max_width) for x in ax[i].get_xticklabels())
    ax[i].set_yticks(nu.arange(0, 5, step=1.0))
    for index, ratingdata[i] in enumerate(nu.round(ratingdata[i]['Rating'], 2)):
        ax[i].text(x=index - 0.1, y=ratingdata[i], s=f"{ratingdata[i]}", fontdict=dict(fontsize=16))
    ax[i].tick_params(labelsize=20)

print(polt.show())

# Easy Apply

viewdata = stat.groupby('Easy Apply')['Job Title'].count().reset_index()
print(viewdata)

fig, ax = polt.subplots()
ax = sbn.barplot(ax=ax, data=viewdata, x='Easy Apply', y='Job Title')
ax.set_title('Data Science Job - Easy Apply')
ax.set_ylabel('Counts of Jobs')
print(polt.show())

# Location

viewdata = stat.groupby('Location')['Job Title'].count().reset_index()
viewdata = viewdata.sort_values('Job Title', ascending=False).head(10)

fig, ax = polt.subplots(figsize=(16, 5))
sbn.barplot(data=viewdata, x='Location', y='Job Title', ax=ax)
ax.set_ylabel('Count Jobs')
ax.set_yticks(nu.arange(0, 200, step=20))
for index, viewdata in enumerate(viewdata['Job Title'].astype(int)):
    ax.text(x=index - 0.1, y=viewdata + 1, s=f"{viewdata}", fontdict=dict(fontsize=10))
print(polt.show())

# Revenue

stat['Revenue'].unique().tolist()

viewdata = stat.copy()
viewdata['Revenue'].replace(['Unknown / Non-Applicable'], nu.nan, inplace=True)
viewdata['Revenue'].dropna(axis=0, inplace=True)
viewdata = viewdata.groupby('Revenue')['Job Title'].count().reset_index()
viewdata.sort_values('Job Title', ascending=False, inplace=True)
print(viewdata)

max_width = 15
fig, ax = polt.subplots(figsize=(16, 4))
sbn.barplot(ax=ax, stat=viewdata, x='Revenue', y='Job Title', palette='deep')
ax.set_title('Count Job Based Revenue')
ax.set_ylabel('Count Jobs')
ax.set_xticklabels(textwrap.fill(x.get_text(), max_width) for x in ax.get_xticklabels())
for index, viewdata in enumerate(viewdata['Job Title'].astype(int)):
    ax.text(x=index - 0.1, y=viewdata + 1, s=f"{viewdata}", fontdict=dict(fontsize=12))
print(polt.show())

# Reference:
# Author: Rifky Ahmad Saputra
# Source: GitHub




