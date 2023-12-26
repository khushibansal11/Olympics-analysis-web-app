import streamlit as st
import pandas as pd
import preprocessing , helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
reg_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocess(df,reg_df)

st.sidebar.title('Olympic Analysis')
user_menu=st.sidebar.radio(
    "Select an option",
    ("Medal Tally", "Overall Analysis","Country-Wise Analysis","Athlete-Wise Analysis")
)
if user_menu == 'Medal Tally' :
    st.sidebar.header('Medal Tally')
    years,country=helper.year_country_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_modal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Overall Tally in '+str(selected_year))
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+' Overall Performance')
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country +' performance in year '+str(selected_year) + ' Olympics')
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    edition=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    region=df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("sports")
        st.title(sports)

    col4,col5,col6=st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Regions")
        st.title(region)
    with col6:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time=helper.participating_overtime(df,'region')
    fig = px.line(nations_over_time, x="Year", y="region", title='Countries participation over the years')
    st.plotly_chart(fig)
    nations_over_time = helper.participating_overtime(df, 'Event')
    fig = px.line(nations_over_time, x="Year", y="Event", title='participating events over the years')
    st.plotly_chart(fig)

    st.title("No. of events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    successful=helper.most_successful(df,selected_sport)
    st.table(successful)

if user_menu == 'Country-Wise Analysis' :
    st.title('Country wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Sport', country_list)
    final=helper.countrywise_year_tally(df,selected_country)
    st.subheader(selected_country+' Medal Tally over the years')
    fig = px.line(final, x="Year", y="Medal")
    st.plotly_chart(fig)

    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    if(pt.shape[0]!=0):
        st.subheader(selected_country + ' excels in the following sports')
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)

    st.subheader('Most Successful Athlete in '+selected_country)
    temp=helper.countrywise_most_successful(df,selected_country)
    st.table(temp)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)