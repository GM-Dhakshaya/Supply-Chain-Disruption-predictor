from slack_sdk import WebClient

client = WebClient(token="xoxb-8354222057619-8354264601811-vFutOLsB1ZxwKwD8qBfF3VcC")

def send_slack_message(channel, message):
    client.chat_postMessage(channel=channel, text=message)

#def analyze_risk_and_sentiment(risk_mean, sentiment_mean):
def analyze_inventory(file_path):
    data = pd.read_csv(file_path)
    inventory_capacity_threshold = 0.8  
    alerts = []

    for _, row in data.iterrows():
    if risk_mean > 0 and sentiment_mean < 0:
        action = "BUY \n High risk with negative sentiment. Potential shortage!\n Increase inventory to full capacity."
    elif risk_mean < 0 and sentiment_mean > 0:
        action = "SELL \n Low risk with positive sentiment. Potential excess!\n Reduce inventory to avoid excess stock."
    elif risk_mean > 0 and sentiment_mean > 0:
        action = "MODERATE \n High risk with positive sentiment. Mixed signals!\n Monitor inventory trends closely."
    else:
        action = "MODERATE \n Low risk with negative sentiment. Stable situation. \n No immediate action required."
    
    send_slack_message("#general", action)
# Helper function to create formatted action messages
data = {
    "Item": [" dark chocolate", ", milk chocolate", "white chocolate"],
    "Quantity": [850, 400, 120],
    "Capacity": [1000, 500, 300],
    "Risk Analysis": ["Medium", "High", "Low"],
    "Sentiment": ["Neutral", "Negative", "Positive"]
}

sample_file = "generated_warehouse_data.csv"
pd.DataFrame(data).to_csv(sample_file, index=False)

alerts = analyze_inventory(sample_file)
def generate_action_message(action_type, risk_description, recommendation):
    return (f"{action_type} \n{risk_description}\n {recommendation}")

# Example usage
analyze_risk_and_sentiment(0.6, -0.3)  # Replace with actual risk and sentiment values

