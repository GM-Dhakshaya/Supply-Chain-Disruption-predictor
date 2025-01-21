import pandas as pd
from textblob import TextBlob

# Sentiment analysis function
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

# Risk level classification based on sentiment
def classify_risk(sentiment):
    if sentiment > 0.1:
        return 'Low Risk'
    elif sentiment < -0.1:
        return 'High Risk'
    else:
        return 'Medium Risk'

# Categorize articles based on keywords (e.g., flood, strike)
def categorize_risk_factor(text):
    risk_keywords = ['flood', 'strike', 'shortage', 'disruption', 'price surge']
    for keyword in risk_keywords:
        if keyword in text.lower():
            return keyword.capitalize()
    return 'None'
# Function to load news data from CSV
def load_news_data(filename):
    return pd.read_csv(filename)

# Load and inspect the data
news_data = load_news_data("C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_data.csv")
print(news_data.head())


# Analyze sentiment and risk factor
def analyze_news(df):
    df['sentiment'] = df['content'].apply(analyze_sentiment)
    df['risk_level'] = df['sentiment'].apply(classify_risk)
    df['risk_factor'] = df['content'].apply(categorize_risk_factor)
    return df

# Save updated data to a new CSV
def save_analyzed_data(df, filename):
    df.to_csv('C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_risk_analysis.csv', index=False)
    print(f"News data with sentiment and risk levels saved to {filename}")

if __name__ == "__main__":
    # Load news data
    news_data = load_news_data("C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_data.csv")

    # Analyze sentiment and classify risk
    analyzed_data = analyze_news(news_data)

    # Save the analyzed data
    save_analyzed_data(analyzed_data, "data/chocolate_news_risk_analysis.csv")
