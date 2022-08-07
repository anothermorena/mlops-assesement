#1. import required packages
#===========================
import re
import base64
import pickle
import pandas as pd
from PIL import Image
import streamlit as st
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

#2. clean, stem and vectorize tweets
#===================================
def preprocess_tweets(df):
    # Stemming
    ps = PorterStemmer()
    # Initializing Lists
    corpus = []
    for i in range(0, len(df)):
        # Removing characters other than letters
        review = re.sub('[^a-zA-Z]', ' ', str(df['tweets'][i]))
        # Lowering the case all the text
        review = review.lower()
        # Splitting into words
        review = review.split()
        # Applying Stemming
        stemmed = [ps.stem(word) for word in review if not word in stopwords.words('english')]
        # Joining words
        review = ' '.join(stemmed)
        # Appending all tweets to a list after preprocessing
        corpus.append(review)
    
    #apply TF-IDF Vectorization
    tfidf = TfidfVectorizer(max_features=2500)
    X_tfidf = tfidf.fit_transform(corpus).toarray()
    
    #save vectorized tweets to a csv file
    df = pd.DataFrame(X_tfidf, columns = tfidf.get_feature_names())
    df.to_csv("vectorized_tweets.csv", index=False)
    
 

#3. file download
#================
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="predictions.csv">Download Predictions</a>'
    return href

#4. model building
#================
def build_model(input_data):
    # reads in saved logistic regression model
    load_model = pickle.load(open('model.pickle', 'rb'))
    
    # apply model to make predictions
    predictions = load_model.predict(input_data)
    
    # convert predictions to integers
    predictions = predictions.astype(int)
    
    st.header('**Prediction Output**')
    prediction_output = pd.Series(predictions, name='sentiments')
    original_tweets = pd.read_csv('original_tweets_data.csv')
    
    df = pd.concat([original_tweets['tweets'], prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)
  

#5. logo image
#=============
image = Image.open('senitiment_analysis.jpg')
st.image(image, use_column_width=True)

#6. page title and description
#=============
st.markdown("<h2 style='text-align: center;'>Streamlit Twitter Sentiment Analysis</h2>", unsafe_allow_html=True)
st.markdown("""
    # 
    This app allows you to classify or predict posts or tweets as negative, positive, or neutral..

    **Credits**
    - App built in `Python` + `Streamlit` by [Otsogile Onalepelo](https://morena.dev) (aka [Morena](https://github.com/anothermorena))
    ---
    """
)

#7. sidebar
#==========
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['csv'])
    st.sidebar.markdown("""
        [Example input file](https://github.com/anothermorena/mlops-assesement/blob/dashboard/dashboard/tweets_example_file.csv)
    """)

if st.sidebar.button('Predict'):
    load_data = pd.read_csv(uploaded_file)
    load_data.to_csv("original_tweets_data.csv")

    st.header('**Original Input Data**')
    st.write(load_data)

    with st.spinner("Preprocessing Tweets..."):
        preprocess_tweets(load_data)

    # read in vectorized tweets and display them in a dataframe
    st.header('**Preprocessed Tweets**')
    v_tweets = pd.read_csv('vectorized_tweets.csv')
    st.write(v_tweets)

    Xlist = list(pd.read_csv('vectorized_tweets.csv').columns)
    v_tweets_subset = v_tweets[Xlist]
    
    print(v_tweets_subset)

    # apply trained model to make sentiment analysis on query  query
    build_model(v_tweets_subset)
else:
    st.info('Upload input data in the sidebar to start!')
    
 
#8. set a custom footer and hide streamlit's navigation menu on app load
#========================================================================   
footer = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'Made with 💙 by Morena'; 
        visibility: visible;
        display: block;
        position: relative;
        #background-color: red;
        padding: 5px;
        top: 2px;
    }
    </style>
    """
st.markdown(footer, unsafe_allow_html=True) 