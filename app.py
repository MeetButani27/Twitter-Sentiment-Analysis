from attr import has
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from helper import preprocessing_data, graph_sentiment, analyse_mention, analyse_hastag, download_data

st.set_page_config(
     page_title = "Twitter Sentiment analysis",
     page_icon = "🧊",
     layout = "wide", 
     initial_sidebar_state = "expanded",
     menu_items = {
         'Get Help': 'https://github.com/everydaycodings/Data-Analysis-Web-App',
         'Report a bug': "https://github.com/everydaycodings/Data-Analysis-Web-App/issues/new",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)

number_of_tweets = 0

def about():
    st.title("About")
    st.write("Through this project we are excited to bring you a powerful tool to help you understand how people feel about a particular topic on Twitter. Our project uses advanced natural language processing algorithms to analyze tweets and provide an overall sentiment score. We understand that social media can be a powerful tool for businesses, individuals, and organizations to reach their target audience. However, it can be challenging to determine how people are responding to your content or product.")
    st.write("Our Twitter Sentiment Analysis project solves this problem by providing a comprehensive analysis of tweets related to your topic of interest. Our user-friendly interface makes it easy to input a keyword or hashtag and receive a detailed sentiment analysis report. The report includes the number of positive, negative, and neutral tweets, as well as a breakdown of the most commonly used words in tweets.")
    st.write("We believe that our Twitter Sentiment Analysis project will help businesses, individuals, and organizations make data-driven decisions and improve their social media strategy. Thank you for considering our project, and we hope it proves to be a valuable tool for you!")
    st.write(" ")
    image = Image.open("twitter.png")
    # st.image(image, width=40, caption="", use_column_width=True)
    st.image(image, width=700)  

def mention_chart(mention):
    st.subheader("Top 10 @Mentions in {} tweets".format(number_of_tweets))
    st.bar_chart(mention)

def hastags_chart(hastag):
    st.subheader("Top 10 Hastags used in {} tweets".format(number_of_tweets))
    st.bar_chart(hastag)

def usedlinks_chart(data):
    st.subheader("Top 10 Used Links for {} tweets".format(number_of_tweets))
    st.bar_chart(data["links"].value_counts().head(10).reset_index())

def all_tweets(data):
    st.subheader("All Tweets containing top 10 links used")
    filtered_data = data[data["links"].isin(data["links"].value_counts().head(10).reset_index()["index"].values)]
    st.write(filtered_data)

def sentiment_bar(analyse):
    st.subheader("Twitter Sentment Analysis chart")
    st.bar_chart(analyse)

def sentiment_pie(text):
  positive_count = (text['Polarity'] > 0).sum()
  negative_count = (text['Polarity'] < 0).sum()
  neutral_count = (text['Polarity'] == 0).sum()

  fig, ax = plt.subplots(figsize=(4,4))
  ax.pie([positive_count, negative_count, neutral_count], labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%", startangle=90)
  ax.set_facecolor(st.get_option("theme.backgroundColor"))
  ax.set_title("Sentiment Distribution")
  st.subheader("Sentiment analysis Pie chart")
  st.pyplot(fig)

def display_data(data, analyse, mention, hastag):
    st.write(" ")
    st.write(" ")
    st.header("Extracted and Preprocessed Dataset")
    st.write(data)
    download_data(data, label="twitter_sentiment_filtered")
    st.write(" ")
        

    col1,col2,col3 = st.columns(3)
    with col2:
        st.markdown("### Data Visualization")


    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    with col1:
        mention_chart(mention)
        st.write(" ")
    with col2:
        hastags_chart(hastag)
        st.write(" ")
    with col3:
        usedlinks_chart(data)
        st.write(" ")
    with col4:
        sentiment_bar(analyse)
        st.write(" ")
    with col5:
        all_tweets(data)
        st.write(" ")
    with col6:
        sentiment_pie(data)
        st.write(" ")
    

menu = {
    "Home": '',
    "Top 10 @Mentions": '',
    "Top 10 Hastags": '',
    "Top 10 Used Links": '',
    "All fetched Tweets": '',
    "Sentiment analysis": '',
    "Sentiment distribution": '',
    "About": ''
}


def main():
    function_option = st.sidebar.selectbox("Select The Funtionality: ", ["Search By #Tag and Words", "Search By Username"])
    menu_choice = st.sidebar.radio("Select your choice:", tuple(menu.keys()))

    if menu_choice != "About":
        st.title("Twitter Sentiment Analysis")
        
        if function_option == "Search By #Tag and Words":
            word_query = st.text_input("Enter the Hastag or any word")

        if function_option == "Search By Username":
            word_query = st.text_input("Enter the Username ( Don't include @ )")

        global number_of_tweets
        number_of_tweets = st.slider("How many tweets You want to collect from {}".format(word_query), min_value=100, max_value=1000)
        
        def fetch_clean_data():
            global data,analyse,mention,hastag
            data = preprocessing_data(word_query, number_of_tweets, function_option)
            analyse = graph_sentiment(data)
            mention = analyse_mention(data)
            hastag = analyse_hastag(data)

    
    if menu_choice=="Home":
        if st.button("Analysis Sentiment"):
            fetch_clean_data()
            display_data(data, analyse, mention, hastag)

    elif menu_choice=="Top 10 @Mentions":
        fetch_clean_data()
        mention_chart(mention)

    elif menu_choice=="Top 10 Hastags":
        fetch_clean_data()
        hastags_chart(hastag)
    
    elif menu_choice=="Top 10 Used Links":
        fetch_clean_data()
        usedlinks_chart(data)

    elif menu_choice=="All fetched Tweets":
        fetch_clean_data()
        all_tweets(data)

    elif menu_choice=="Sentiment analysis":
        fetch_clean_data()
        sentiment_bar(analyse)

    elif menu_choice=="Sentiment distribution":
        fetch_clean_data()
        sentiment_pie(data)

    elif menu_choice=="About":
        about()


if __name__ == "__main__":
    main()