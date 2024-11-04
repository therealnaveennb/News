import pandas as pd
import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from pymongo import MongoClient, server_api
from dotenv import load_dotenv
from urllib.parse import quote_plus
import json

nltk.download('vader_lexicon')
load_dotenv()
# Function to connect to MongoDB and retrieve data from a collection
def fetch_data_from_mongodb(collection_name):
   # Get MongoDB credentials from environment variables
    mongo_username = quote_plus(os.getenv('MONGO_USERNAME'))
    db_password = quote_plus(os.getenv('MONGO_PASSWORD'))
    db_name = os.getenv('DB_NAME')

    # MongoDB connection URI with escaped username and password
    uri = f"mongodb+srv://{mongo_username}:{db_password}@news-analyzer.0ittn.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=News-analyzer"

    # Create a new client and connect to the MongoDB server
    client = MongoClient(uri, server_api=server_api.ServerApi('1'))

    # Test connection by pinging the MongoDB server
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return
    
    # Retrieve data from the collection and convert it to a DataFrame
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find({}))
    return pd.DataFrame(data)

# Function to calculate sentiment polarity using NLTK's SentimentIntensityAnalyzer
def calculate_polarity(df):
    sia = SIA()
    results = []
    
    # Iterate over each row of lemmatized text to calculate polarity scores
    for line in df['lems']:
        pol_score = sia.polarity_scores(line)
        pol_score['headline'] = line
        results.append(pol_score)
    
    # Convert results into a DataFrame
    polarity_df = pd.DataFrame.from_records(results)
    
    # Add the source of the news articles to the polarity DataFrame
    polarity_df['source'] = df['source']
    
    # Classify the news articles as positive (1), negative (-1), or neutral (0) based on compound score
    polarity_df['label'] = 0
    polarity_df.loc[polarity_df['compound'] > 0.2, 'label'] = 1
    polarity_df.loc[polarity_df['compound'] < -0.2, 'label'] = -1
    
    # Add word count to the DataFrame
    polarity_df['word_count'] = polarity_df['headline'].apply(lambda x: len(str(x).split()))
    
    return polarity_df

# Function to group by source and calculate mean compound scores
def group_by_source(polarity_df):
    grouped_df = polarity_df.groupby('source')['compound'].mean().to_frame()
    return grouped_df

# Function to save the mean polarity to CSV
def save_polarity(polarity_df, file_path='assets/mean_polarity.csv'):
    polarity_df.to_csv(file_path, index_label='source')

# Main function to tie all the steps together
def main():
   
    

    # Fetch data from MongoDB
    news_articles_df = fetch_data_from_mongodb(collection_name="DailyNews")
    print(news_articles_df)
    # Calculate polarity scores
    headlines_polarity = calculate_polarity(news_articles_df)
    save_polarity(headlines_polarity)
    # Group by source and calculate the mean polarity
    mean_polarity_df = group_by_source(headlines_polarity)
    
    # Save the mean polarity DataFrame to a CSV file
    save_polarity(headlines_polarity)

# Allow this script to be used as an importable module or run as a standalone script
if __name__ == "__main__":
    main()
