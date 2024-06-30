import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'region', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'region', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country

def data_over_time(df, col):
    # Drop duplicates based on Year and the specified column, then count the number of unique years
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    # Rename columns properly
    nations_over_time.columns = ['Edition', col]
    # Sort by 'Edition'
    nations_over_time = nations_over_time.sort_values('Edition')
    return nations_over_time


def most_successful(df, sport):
    # Drop rows with NaN values in the 'Medal' column
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if a specific sport is provided
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count the number of medals each athlete has won
    medal_counts = temp_df['Name'].value_counts().reset_index().head(15)
    medal_counts.columns = ['Name', 'Medals']  # Rename columns

    # Merge to get additional information about the athletes
    merged_df = medal_counts.merge(df, on='Name', how='left')

    # Select the relevant columns and drop duplicates
    x = merged_df[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, country):
    # Drop rows with NaN values in the 'Medal' column
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if a specific sport is provided

    temp_df = temp_df[temp_df['region'] == country]

    # Count the number of medals each athlete has won
    medal_counts = temp_df['Name'].value_counts().reset_index().head(10)
    medal_counts.columns = ['Name', 'Medals']  # Rename columns

    # Merge to get additional information about the athletes
    merged_df = medal_counts.merge(df, on='Name', how='left')

    # Select the relevant columns and drop duplicates
    x = merged_df[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final





