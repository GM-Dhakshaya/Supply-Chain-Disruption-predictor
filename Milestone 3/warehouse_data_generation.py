import pandas as pd
import random

# Load the existing news data with sentiment and risk analysis
news_data = pd.read_csv("C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_risk_analysis.csv")

# Function to generate synthetic warehouse data based on sentiment and risk analysis
def generate_warehouse_data(news_data):
    warehouse_data = []

    for index, row in news_data.iterrows():
        # Simulate Warehouse Capacity (e.g., fixed value or random within range)
        warehouse_capacity = random.choice([10000, 15000, 20000])
        
        # Simulate Monthly Incoming (based on sentiment or risk factor)
        if row['sentiment'] > 0.1:  # Positive sentiment
            monthly_incoming = random.randint(5000, 10000)
        elif row['sentiment'] < -0.1:  # Negative sentiment
            monthly_incoming = random.randint(1000, 5000)
        else:  # Neutral sentiment
            monthly_incoming = random.randint(4000, 7000)
        
        # Generate Risk Analysis based on the risk_factor column from the news data
        risk_analysis = row['risk_level']

        # Generate Sentiment based on the sentiment analysis
        sentiment = 'Positive' if row['sentiment'] > 0.1 else 'Negative' if row['sentiment'] < -0.1 else 'Neutral'

        # Monthly Outgoing can be simulated or based on a simple rule
        monthly_outgoing = monthly_incoming - random.randint(1000, 3000)  # Simulated value

        warehouse_data.append({
            'Month': f"Month-{index+1}",  # For simplicity, assigning Month-1, Month-2, etc.
            'Warehouse Capacity': warehouse_capacity,
            'Monthly Incoming': monthly_incoming,
            'Monthly Outgoing': monthly_outgoing,
            'Risk Analysis': risk_analysis,
            'Sentiment': sentiment
        })

    return pd.DataFrame(warehouse_data)

# Generate warehouse data from news data
warehouse_data = generate_warehouse_data(news_data)

# Save the generated warehouse data to CSV
warehouse_data.to_csv("C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv", index=False)

# Display the generated warehouse data
print(warehouse_data.head())
