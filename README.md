# AI-Driven Supply Chain Disruption Predictor and Inventory Optimization System

## Milestone 1:
###  1. Introduction

This project integrates real-time supply chain data using various APIs and employs GPT-4 for predictions and analysis in supply chain management.

Task 1: Integrate data APIs with Python to retrieve and process real-time supply chain data.
Task 2: Research GPT-4 (LLM) for applications in supply chain management, such as demand forecasting and trend analysis.
### 2. Task 1: Integrating Data APIs with Python
What are APIs?
APIs (Application Programming Interfaces) enable communication between different software systems. This project uses APIs to gather real-time data on shipping, inventory, global trade, and financials.

### APIs Used:

Event Registry: Real-time news data for market trends.
Freightos: Shipping rates and freight quotes.
MarineTraffic: Ship movement and port traffic.
UN Comtrade: Global trade statistics.
World Bank LPI: Logistics performance indices.
IMF: Global economic data.
NASDAQ Data: Financial data and trends.
Kaggle: Datasets for machine learning.
Dun & Bradstreet: Business and supplier data.
Python Code Example:
import requests

api_key = "your_api_key"
url = "https://api.eventregistry.org/api/v1/article/getArticles"
params = {"query": "supply chain", "apiKey": api_key}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully:", data)
else:
    print("Error fetching data:", response.status_code)
### Key Learnings:

Authentication: Use API keys securely.
Rate Limiting: Be aware of request limits.
Response Formats: Typically JSON or XML.
Error Handling: Handle timeouts and errors gracefully.
### 3. Task 2: Researching and Using GPT-4 for Supply Chain Management
What is GPT-4?
GPT-4 is an advanced language model by OpenAI that performs tasks like content generation, summarization, and prediction. It can be fine-tuned for specific tasks like supply chain management.
Applications in Supply Chain Management:
Demand Forecasting: Predict future demand using historical data.
Supply Chain Optimization: Optimize logistics and inventory.
Trend Analysis: Analyze market trends and disruptions.
Text Mining: Extract insights from unstructured data.
Integrating GPT-4 in Python:
import openai

openai.api_key = 'your_openai_api_key'

response = openai.Completion.create(
    model="gpt-4",
    prompt="Given the latest shipping data, what are the best strategies to optimize our supply chain for Q1?",
    max_tokens=150
)

print(response.choices[0].text.strip())
Key Learnings:

API Access: Obtain an OpenAI API key.
Token Limit: GPT-4 processes a limited amount of text per request.
Fine-Tuning: Tailor GPT-4 for specific tasks like supply chain management.
### 4. Conclusion
This project combines APIs for real-time data retrieval and GPT-4's capabilities for data analysis and predictions to optimize supply chain operations.





---


# MILESTONE 2: Supply Chain Risk Prediction
### Overview
This project focuses on developing a model to predict supply chain disruptions and optimize inventory management. The goal is to analyze the likelihood of disruptions in the chocolate supply chain, specifically for risk factors that affect supply chains globally. Using a combination of machine learning techniques and natural language processing (NLP), the project predicts the likelihood of supply chain disruptions based on descriptive risk factors provided in the input data.

The model uses a pre-trained BERT (Bidirectional Encoder Representations from Transformers) model for sequence classification, which is fine-tuned with custom risk factor data.
## Features
1. **Supply Chain Risk Analysis**:
    - The model predicts the likelihood of a disruption in the chocolate supply chain based on textual descriptions of risks.
It uses a fine-tuned BERT model to assess risks like geopolitical tensions, raw material shortages, and more.

2. **Data Preprocessing**:
    - The system processes and tokenizes risk factor descriptions, encoding them for input to the model.
      
3. **Model Fine-tuning**:
    - The model is trained on a custom dataset, which includes descriptions of risks to the chocolate supply chain.
      
4. **Prediction API**:
    - A Flask-based web API that exposes a RESTful service for making predictions. Clients can send a POST request to predict the likelihood of supply chain disruptions.
---

## Project Goals
- **Risk Assessment for Chocolate Production & Trade**: Identify and evaluate risks affecting chocolate production and trade.
- **Disruption Prediction**: Develop predictive models to forecast supply chain disruptions.
- **Inventory Management**: Simulate and optimize warehouse stock levels using predictive data.
- **Sentiment Analysis**: Understand market sentiment to assess potential impacts on the chocolate supply chain.


- **Chocolate News Analysis**:
  - Fetch real-time news related to chocolate production and trade.
  - Analyze sentiment to identify risks such as production delays, price hikes, or political instability.
  
- **Risk Prediction**:
  - Train a model using historical supply chain data, news sentiment, and market trends to predict potential disruptions in the chocolate supply chain.
  
- **Warehouse Data Simulation**:
  - Simulate warehouse inventory data, adjusting stock levels based on predicted risks.
  - Generate alerts for low stock or excess inventory to optimize stock management.

# Milestone 3: Predictive Disruption Modeling & ERP Integration
This milestone integrates predictive models and ERP simulations to automatically adjust stock levels in response to supply chain disruptions.

- **Predictive Disruption Modeling**:
  - Utilize machine learning models to predict disruptions based on historical data and external factors.
  - Forecast disruptions like supply delays, demand surges, and production issues.

- **ERP Integration**:
  - Simulate ERP system integration to automate stock adjustments based on predicted disruptions.
  - Optimize inventory management and adjust stock levels for future risks.

---

## Requirements
**To run this project, you'll need the following dependencies**:
    
- **pandas**: For data manipulation
- **matplotlib**: For visualizations
- **scikit-learn**: For building machine learning models
- **lightgbm**: For gradient boosting in risk prediction
- **openai**: For sentiment analysis using OpenAI models
- **sqlite3**: For simulating ERP database interactions
- **KaggleHub**: For downloading datasets
- **Pillow (PIL)**: For image handling in case of visual data processing

Install all required libraries with:


pip install -r requirements.txt
---
## How It Works
1. **Input**:
    - The process begins with the retrieval of articles or relevant text data related to the chocolate supply chain, which are either manually entered or retrieved from an external source, such as a news API or a file.

    - This input data, usually stored in a structured format (e.g., JSON or CSV), contains text related to supply chain disruptions, risks, and inventory challenges.

2. **Analysis**:
    - Text Processing: The script reads the description of each entry (e.g., news articles, reports, or supply chain events).

    - Risk Prediction with Pre-trained Model:
        - The text data is fed into the machine learning model (e.g., a pre-trained LLM model such as GPT-3.5-Turbo or another transformer model).
        - The model analyzes the text and identifies any supply chain risks related to the chocolate industry, such as disruptions, geopolitical risks, resource shortages, and transportation bottlenecks.
        - Based on the analysis, the model outputs a prediction score indicating the likelihood or severity of the risk described in the article.
- **Example Risk Analysis**:
        -Input to Model: "A sudden surge in demand has caused supply shortages in the chocolate industry."
        -Output from Model: "The model identifies an inventory disruption risk due to a surge in demand, which could lead to supply shortages in the chocolate supply chain."
- **Sentiment Analysis**:
    -Input to Sentiment Model: "A sudden surge in demand has caused supply shortages in the chocolate industry."
    -Output from Sentiment Model: Negative 
3. **Output**:
-The output from the model includes two key elements:
    -Risk Prediction: A score or text-based analysis of the potential risk in the supply chain based on the description.
    -Sentiment Analysis: The overall sentiment (positive, negative, neutral) of the article or description, which gives an indication of how the situation is being viewed.
    -This information is returned in a structured JSON response, which is either displayed on the console, saved to a file, or passed to another system for further processing.


---
# Milestone-4: Warehouse Alert System with Slack Notification

The program, `alert.py`, analyzes chocolate supply chain data and generates alerts based on utilization, risk levels, and sentiment of the supply chain. It aids stakeholders in taking timely actions (`BUY`, `SELL`, `MONITOR`) to manage disruptions and optimize inventory.

## Program Workflow

### Input Data:
The program reads data from `generated_warehouse_data`. This data includes:
- **Monthly Incoming Stock**: Inventory entering the warehouse.
- **Warehouse Capacity**: Maximum storage limits.
- **Risk Analysis Levels**: High, Medium, or Low risks.
- **Sentiment Analysis**: Positive, Neutral, or Negative sentiment related to supply chain data.

### Slack Notification Process:

1. **Alert Generation**:
   - Alerts are created for each item based on:
     - **Risk**: High, Medium, or Low.
     - **Sentiment**: Positive, Neutral, or Negative.
     - **Utilization**: Warehouse capacity levels.
   - Decisions include:
     - `BUY`: High risk and negative sentiment indicating potential shortages.
     - `SELL`: Low risk and positive sentiment indicating potential excess.
     - `MONITOR`: Mixed signals requiring close observation.

2. **Notification to Slack**:
   - Alerts are prepared with key insights:
     - **Item Name**: Identifies the affected product.
     - **Action**: Specifies `BUY`, `SELL`, or `MONITOR`.
     - **Reason**: Explains the basis of the alert, such as "High risk and negative sentiment—potential shortage detected."
   - Notifications are sent to a specified Slack channel using the Slack API.

---

## Outcome:
1. **Real-Time Alerts**:
   - Alerts are displayed in the terminal and sent instantly to Slack.
2. **Automated Workflow**:
   - Notifications are sent without manual intervention, ensuring quick dissemination.
3. **Actionable Insights**:
   - Alerts guide stakeholders to adjust inventory, prevent shortages, or reduce excess stock.

---

## Example Slack Alert:
![Chocolate Alert Example](alert.jpeg)

---


## Conclusion
This project focuses on the risks and supply chain management of chocolate production. By leveraging learning models, it predicts potential risks like supply chain disruptions and evaluates their impact. The model also assists in identifying key factors affecting the chocolate supply chain to help improve decision-making and mitigate risks effectively.


---



