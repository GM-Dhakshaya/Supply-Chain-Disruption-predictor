import requests
from datetime import datetime
from collections import Counter
import json
import matplotlib.pyplot as plt

# API key and URL for fetching articles
api_key = "7f0e4e99-c97d-4557-a3bf-810bf2358fe4"
url = "https://eventregistry.org/api/v1/article/getArticles"

# Parameters for querying articles related to "Korea"
params = {
    "query": '{"$query": {"keyword": "korea"}}',  # $query field specifies the search
    "apiKey": api_key
}

# Fetch the data from the API
response = requests.get(url, params=params)

if response.status_code == 200:
    print("API key is working!\n")
    data = response.json()

    # Debug: print the full response to inspect its structure
    print("Full data structure:", json.dumps(data, indent=4))

    # Check if 'articles' key exists in the response
    if "articles" in data:
        print("\nNumber of articles fetched:", len(data["articles"]))
        if len(data["articles"]) > 0:
            print("\nSample article:")
            print(data["articles"][0])  # Display the first article
        else:
            print("No articles found.")
    else:
        print("No 'articles' key found in the response.")

    # 1. Extract Titles of Articles
    if "articles" in data:
        print("\n1. Article Titles:")
        titles = [article.get("title", "No title") for article in data["articles"]]
        for title in titles:
            print(title)
    else:
        print("\nNo articles available for title extraction.")

    # 2. Filter Articles Published After January 1, 2023
    if "articles" in data:
        print("\n2. Filter Articles Published After January 1, 2023:")
        date_threshold = datetime(2023, 1, 1)
        filtered_articles = [
            article for article in data["articles"]
            if datetime.strptime(article["date"], "%Y-%m-%dT%H:%M:%SZ") > date_threshold
        ]
        print(f"Number of articles after January 1, 2023: {len(filtered_articles)}")
        for article in filtered_articles[:3]:  # Display top 3 articles
            print(f"Title: {article['title']}, Published Date: {article['date']}")

    # 3. Count Articles by Source
    if "articles" in data:
        print("\n3. Article Count by Source:")
        sources = [article.get("source", "Unknown source") for article in data["articles"]]
        source_counts = Counter(sources)
        for source, count in source_counts.items():
            print(f"{source}: {count}")

    # 4. Summarize Articles
    if "articles" in data:
        print("\n4. Article Summaries (First 200 characters):")
        for article in data["articles"][:3]:  # Display top 3 articles
            content = article.get("content", article.get("summary", "No summary available"))
            print(f"Title: {article['title']}")
            print(f"Summary: {content[:200]}...")  # First 200 characters of the summary

    # 5. Save Data to a JSON file
    print("\n5. Saving Data to articles_data.json...")
    with open('articles_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data saved to articles_data.json\n")

    # 6. Visualize Article Count by Source
    if "articles" in data:
        print("6. Visualizing Article Count by Source:")
        plt.bar(source_counts.keys(), source_counts.values())
        plt.xlabel('Source')
        plt.ylabel('Number of Articles')
        plt.title('Article Distribution by Source')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

else:
    print("Error:", response.status_code, response.text)
