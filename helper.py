import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['total'] = medal_tally['total'].astype(int)
    return medal_tally


def year_country_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years , country

def fetch_modal_tally(df,year,country):
    flag = 0
    temp_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    if(year=='Overall' and country=='Overall'):
        medal_df=temp_df
    if(year!='Overall' and country=='Overall'):
        medal_df=temp_df[temp_df['Year']==year]
    if(year=='Overall' and country!='Overall'):
        flag=1
        temp_df=temp_df[temp_df['region']==country]
        medal_df=temp_df.groupby('Year').sum()[['Gold','Bronze','Silver']].sort_values('Year',ascending=True).reset_index()
    if(year!='Overall' and country!='Overall'):
        medal_df=temp_df[(temp_df['region']==country) & (temp_df['Year']==year)]
    if(flag==0):
        medal_df=medal_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_df['total']=medal_df['Gold']+medal_df['Silver']+medal_df['Bronze']

    medal_df['Gold'] = medal_df['Gold'].astype(int)
    medal_df['Bronze'] = medal_df['Bronze'].astype(int)
    medal_df['Silver'] = medal_df['Silver'].astype(int)
    medal_df['total'] = medal_df['total'].astype(int)
    return medal_df

def participating_overtime(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count': col}, inplace=True)
    return nations_over_time

def most_successful(df,sport):
    temp_df=df.dropna(subset='Medal')
    if(sport!='Overall'):
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','region','Sport']].drop_duplicates().reset_index()
    x.rename(columns={'count':'Medals Won'},inplace=True)
    x=x[['Name', 'Medals Won', 'region', 'Sport']]
    return x

def countrywise_year_tally(df,country):
    temp = df.dropna(subset=['Medal'])
    temp = temp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp = temp[temp['region'] == country]
    final = temp.groupby('Year').count()['Medal'].reset_index()
    return final

def country_event_heatmap(df,country):
    temp = df.dropna(subset=['Medal'])
    temp = temp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp = temp[temp['region'] == country]
    pt=temp.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return pt

def countrywise_most_successful(df,country):
    temp_df=df.dropna(subset='Medal')
    temp_df=temp_df[temp_df['region']==country]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates().reset_index()
    x.rename(columns={'count':'Medals Won'},inplace=True)
    x=x[['Name', 'Medals Won','Sport']]
    return x
