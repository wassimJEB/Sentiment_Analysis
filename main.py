import streamlit as st
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from TweetScrapping import *

# Fxn
def convert_to_df(sentiment):
	sentiment_dict = {'polarity':sentiment.polarity,'subjectivity':sentiment.subjectivity}
	sentiment_df = pd.DataFrame(sentiment_dict.items(),columns=['metric','value'])
	return sentiment_df

def analyze_token_sentiment(docx):
	analyzer = SentimentIntensityAnalyzer()
	pos_list = []
	neg_list = []
	neu_list = []
	for i in docx.split():
		res = analyzer.polarity_scores(i)['compound']
		if res > 0.1:
			pos_list.append(i)
			pos_list.append(res)

		elif res <= -0.1:
			neg_list.append(i)
			neg_list.append(res)
		else:
			neu_list.append(i)

	result = {'positives':pos_list,'negatives':neg_list,'neutral':neu_list}
	return result




def main():
    st.title("Sentiment Analysis NLP App using  STREAMLIT realized by Wassim JEBALI")
    c = st.selectbox("Choisir une option", ["Tweet scrapping and analysis ", "Sentiment Analysis NLP App using Vader API"])
    if c== "Sentiment Analysis NLP App using Vader API":
        with st.form(key='nlpForm'):
            raw_text = st.text_area("Enter Text Here")
            submit_button = st.form_submit_button(label='Analyze')

            # layout
            col1, col2 = st.columns(2)
            if submit_button:

                with col1:
                    st.info("Results")
                    sentiment = TextBlob(raw_text).sentiment
                    # Emoji
                    if sentiment.polarity > 0:
                        st.markdown("Sentiment:: Positive :smiley: ")
                    elif sentiment.polarity < 0:
                        st.markdown("Sentiment:: Negative :angry: ")
                    else:
                        st.markdown("Sentiment:: Neutral 😐 ")



                with col2:
                    st.info("Token Sentiment")

                    token_sentiments = analyze_token_sentiment(raw_text)
                    st.write(token_sentiments)

    else:
        with st.form(key='nlpForm'):


            raw_text = st.text_area("Enter Keyword/Tag to search about")
            nb = st.text_area("Enter number of tweets")
            button = st.form_submit_button(label='Analyze')



            # layout
            col1, col2 = st.columns(2)
            if button:
                objet = SentimentAnalysis()
                objet.DownloadData(raw_text, nb)

                with col1:
                    st.info("Results")
                    sentiment = TextBlob(raw_text).sentiment
                    # Emoji
                    if sentiment.polarity > 0:
                        st.markdown("Sentiment:: Positive :smiley: ")
                    elif sentiment.polarity < 0:
                        st.markdown("Sentiment:: Negative :angry: ")
                    else:
                        st.markdown("Sentiment:: Neutral 😐 ")

                with col2:
                    st.info("Token Sentiment")

                    token_sentiments = analyze_token_sentiment(raw_text)
                    st.write(token_sentiments)











if __name__ == '__main__':
    main()
