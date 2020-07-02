import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud  import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets of US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets of US Airlines")
st.markdown("This application of streamlit is to analyze sentiments of tweets.")
st.sidebar.markdown("This application of streamlit is to analyze sentiments of tweets.")

DATA_URL=("./Tweets.csv")
@st.cache(persist=True)
def load_data():
	data=pd.read_csv(DATA_URL)
	data['tweet_created']=pd.to_datetime(data['tweet_created'])
	return data


data=load_data()
st.sidebar.subheader("Show Random Tweet")
random_tweet=st.sidebar.radio('Sentiment',('positive','neutral','negative'))

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of Tweets by Sentiments")
select=st.sidebar.selectbox('Visualiaztion Type',['Histogram','Pie-chart'],key='1')
sentiment_count=data['airline_sentiment'].value_counts()
sentiment_count=pd.DataFrame({'sentiment': sentiment_count.index,'Tweets' : sentiment_count.values})

if not st.sidebar.checkbox("Hide",True):
	st.markdown("## Number of Tweets by Sentiment")
	if select == "Histogram":
		fig=px.bar(sentiment_count,x='sentiment',y='Tweets',color='Tweets',height=500)
		st.plotly_chart(fig)
	else:
		fig=px.pie(sentiment_count,values='Tweets',names='sentiment')
		st.plotly_chart(fig)

st.sidebar.subheader("When and Where The Users Tweeting From")
hour=st.sidebar.slider("Hour of Day", 0,23)

modified_data=data[data['tweet_created'].dt.hour==hour]
if not st.sidebar.checkbox("close",True,key='1'):
	st.markdown("### Tweets Locations Based on Time of The Day")
	st.markdown("%i Tweets Between %i:00 and %i:00" %(len(modified_data),hour,(hour+1)%24))
	st.map(modified_data)

	if st.sidebar.checkbox("Show Raw Data",False):
		st.write(modified_data)

st.sidebar.subheader("Breakdown Airline Tweets by Sentiment")
choice=st.sidebar.multiselect('Pick Airlines',['US Airways','United','American','Southwest','Delta','Virgin America'],key='0')

if len(choice) > 0:
	choice_data = data[data.airline.isin(choice)]
	fig_choice=px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',
		color='airline_sentiment',facet_col='airline_sentiment',labels={'airline_sentiment':'Tweets'},height=600,width=800)
	st.plotly_chart(fig_choice)

st.sidebar.header("Word CLoud")
word_sentiment=st.sidebar.radio('Display word cloud for what sentiment?',('positive','neutral','negative'))

if not st.sidebar.checkbox("close",True,key='3'):
	st.header('Word Cloud for %s sentiment' %(word_sentiment))
	df=data[data['airline_sentiment']==word_sentiment]
	words=' '.join(df['text'])
	processed_words=' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
	wordCloud=WordCloud(stopwords=STOPWORDS,background_color='white',height=640,width=800).generate(processed_words)
	plt.imshow(wordCloud)
	plt.xticks([])
	plt.yticks([])
	st.pyplot()