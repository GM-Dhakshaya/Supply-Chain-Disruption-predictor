import requests
import pandas as pd
from textblob import TextBlob # type: ignore

# Fetch news data from NewsAPI
def fetch_news_data():
    api_key = "53b903602a6943d89c6e860dde291355"  # Replace with your own key
    url = f"https://newsapi.org/v2/everything?q=chocolate&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()

    if 'articles' in data and len(data['articles']) > 0:
        return data['articles']
    else:
        return []

# Save fetched news data to CSV
def save_news_to_csv(news_data, filename):
    if not news_data:
        print("No data to save.")
        return

    df = pd.DataFrame(news_data)
    df.to_csv('C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_data.csv', index=False)
    print(f"News data saved to {filename}")

if __name__ == "__main__":
    news_data = fetch_news_data()
    save_news_to_csv(news_data, "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_data.csv")
