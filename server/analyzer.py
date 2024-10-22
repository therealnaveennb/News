import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')
# Function to read the cleaned CSV file
def read_cleaned_data(file_path='assets/news_articles_clean.csv'):
    return pd.read_csv(file_path)

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
def save_mean_polarity(grouped_df, file_path='assets/mean_polarity.csv'):
    grouped_df.to_csv(file_path, index_label='source')

# Main function to tie all the steps together
def main():
    # Read the cleaned data
    news_articles_df = read_cleaned_data()
    
    # Calculate polarity scores
    headlines_polarity = calculate_polarity(news_articles_df)
    
    # Group by source and calculate the mean polarity
    mean_polarity_df = group_by_source(headlines_polarity)
    
    # Save the mean polarity DataFrame to a CSV file
    save_mean_polarity(mean_polarity_df)

# Allow this script to be used as an importable module or run as a standalone script
if __name__ == "__main__":
    main()
