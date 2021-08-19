#!/usr/bin/env python
# coding: utf-8

# ## In this report:
# We will examine MLB hitting statistics dating back to 1973 (the first year of the DH rule inclusion), to examine what positions hit the best, and why.

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# First, import each .csv file. These files were each SQL queries exported as comma delimited text files, pulled from the 2020 Lahman's database. The Lahman database is regarded as one of the most comprehensive baseball databases in the world. 

# In[ ]:


appearances = pd.read_csv('appearancesAfter1973.csv')
batting = pd.read_csv('battingAfter1973.csv', encoding = 'unicode_escape', engine ='python')
fielding = pd.read_csv('fieldingAfter1973.csv', encoding = 'unicode_escape', engine ='python')
players = pd.read_csv('playerNames.csv')


# We can take a quick look at the general shape of each DataFrame now to get an idea of what each contains.

# In[ ]:


print('appearances', '\n', appearances.head())
print('\n', 'batting', '\n', batting.head())
print('\n', 'fielding', '\n', fielding.head())
print('\n', 'players', '\n', players.head())


# Next we can start to merge these DataFrames on similar columns. Firstly, appearances and batting share playerID, yearID, and teamID columns. 

# In[ ]:


merge1 = pd.merge(appearances, batting, left_on=['playerID', 'yearID', 'teamID'], right_on=['playerID', 'yearID', 'teamID'] )
print(list(merge1))


# We can also drop all of the G_'position name' columns because the fielding and outfield sheets supply each player's position in each year.

# In[ ]:


merge1.drop([col for col in merge1.columns if 'G_' in col], axis=1, inplace=True)


# In[ ]:


merge1.drop(['G'], axis=1,inplace=True)
print(list(merge1))


# We can now continue to merge the sheets together using similar columns.

# In[ ]:


merge2 = pd.merge(merge1, fielding, left_on=['playerID', 'yearID', 'stint'], right_on=['playerID', 'yearID', 'stint'])


# In[ ]:


print(list(merge2))


# In[ ]:


full_df = pd.merge(merge2, players, how= 'left', on='playerID')


# In[ ]:


print(full_df)
print(list(full_df))


# Now we have our sheets all merged into one large DataFrame. We can begin to work on computing relevant statistics from what we are given - such as slugging percentage, batting average, on-base percentage, and fielding percentage. 

# In[ ]:


full_df['AVG'] = full_df['H'] / full_df['AB']
full_df['OBP'] = (full_df['H'] + full_df['BB'] + full_df['HBP']) / (full_df['AB'] + full_df['BB'] + full_df['HBP'] + full_df['SF'])
full_df['SLG'] = (full_df['H'] + full_df['2B'] + (2 * full_df['3B']) + (4 * full_df['HR'])) / full_df['AB']
full_df['OPS'] = full_df['OBP'] + full_df['SLG']
full_df['FLD'] = (full_df['PO'] + full_df['A']) / (full_df['PO'] + full_df['A'] + full_df['E'])
print(full_df)
print(list(full_df))


# Now we have calculated some of the more useful, widely applied statistics to evaluate a player's performance. Next, we will visualize our data to get an understanding of some of the trends.

# In[ ]:


avg_by_pos = full_df.groupby('POS').mean()
avg_by_pos = avg_by_pos.sort_values('AVG')


# In[ ]:





# Create dashboard on streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Baseball Statistics by Position')
h_or_f = st.sidebar.radio('Select Statistic Field' ,('Hitting', 'Fielding'))
if h_or_f == 'Hitting':
    choice = st.sidebar.selectbox('Choose a Statistic', ['AVG','SLG', 'OBP', 'OPS'])
    avg_by_pos = avg_by_pos.sort_values(choice)
    st.header(f'{choice} by Position (since 1973)')
    plt.bar(list(avg_by_pos.index), avg_by_pos[choice])
    plt.xlabel('Position')
    plt.ylabel(choice)
    ymin = min(avg_by_pos[choice]) - 0.1
    ymax = max(avg_by_pos[choice]) + 0.05
    axes = plt.gca()
    axes.set_ylim([ymin, ymax])
    st.pyplot()
else:
    avg_by_pos = avg_by_pos.sort_values('FLD')
    st.header('Fielding Percentage by Position (since 1973)')
    plt.bar(list(avg_by_pos.index), avg_by_pos['FLD'])
    plt.xlabel('Position')
    plt.ylabel('Fielding Percentage')
    ymin = min(avg_by_pos['FLD']) - 0.1
    axes = plt.gca()
    axes.set_ylim([ymin, 1])
    st.pyplot()

