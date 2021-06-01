# libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment analysis of tweets about US Airlines")

# creating a sidebar
st.sidebar.title("Sentiment analysis of tweets about US Airlines")

st.markdown("This application is a  dashboard to analyze the sentiment of Tweets.")


st.sidebar.markdown("This application is a  dashboard to analyze the sentiment of Tweets.")

# give path to the URL
DATA_URL=("C:/Users/smitt/Downloads/Sentiment-analysis-of-tweets-about-US-Airlines-master/Tweets.csv")

# if input of the below function dosen't change then cache the data
# loading data
@st.cache(persist=True) #using decorator and cache will be stored on disk
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created']) #changing the col to proper format
    return data #new dataframe
data = load_data()


# view the data when checkbox is not selected
# by default it is hidden

st.sidebar.subheader("View DataFrame")
if not st.sidebar.checkbox("Hide",True,key='0'):
    st.write(data)

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment' , ('positive','neutral','negative'))


# query the tweets from dataframe
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=2).iat[0,0]) #airline_sentient has neg,pos tweets
#n=1 for showing one random tweet from text coln , iat[0] is 0th row and 0th col

# making bar and hist charts
st.sidebar.markdown('### Number of tweets by sentiment')

# dropdown list
select = st.sidebar.selectbox('Visualization type',['Histogram','Pie chart'],key='1')#key is 1 so the widget selectbox dosent confuse itself with other widget

sentiment_count = data['airline_sentiment'].value_counts() #number of pos,neg etc values
# st.write(sentiment_count)

# creating new data frame for the sentimnets and it's values
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index,'Tweets':sentiment_count.values})

# user can hide the plot by using checkbox
if not st.sidebar.checkbox("Hide",True):#by default it is checked
    st.markdown("### Number of tweets by sentiment")
    if select=="Histogram":
        fig = px.bar(sentiment_count,x='Sentiment',y='Tweets',color='Tweets',height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)


# plotting the map
st.sidebar.subheader("When and where are users tweeting from ?")
# creating slider
hour =st.sidebar.slider("Hour of day",0,23) #12 am to 11 pm
#for number input
# hour =st.sidebar.slider("Hour of day",min_value=1,max_value=23) #12 am to 11 pm

# return data user has selected for that hour. creating new df
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close",True,key='1'):
    st.markdown("### tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data",False):
        st.write(modified_data)

# break airline tweets by sentiments
st.sidebar.subheader("Breakdown airline tweets by sentiment")
# multiple airline selection by using widget choice
choice = st.sidebar.multiselect('Pick a airline',('US Airways , United','American','Southwest','Delta','Virgin America'),key='0')


# now for mutliselect widget there should be no error if user selects no airline.
if len(choice)>0:
    # creating new DataFrame
    choice_data = data[data.airline.isin(choice)]
    fig__choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
    facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'} , height=600 , width=800)
    st.plotly_chart(fig__choice)

