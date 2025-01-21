import os
import pandas as pd
import sys

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.fetch_news import fetch_news_data
from src.sentiment_analysis import analyze_news
from src.warehouse_analysis import analyze_warehouse_data
from src.risk_prediction_model import predict_risks
from src.erp_integration import analyze_and_notify

# Paths for data files
NEWS_DATA_PATH = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_data.csv"
SENTIMENT_ANALYSIS_PATH = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/chocolate_news_risk_analysis.csv"
WAREHOUSE_DATA_PATH = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv"
FINAL_ANALYSIS_PATH = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/final_risk_analysis.csv"

def main():
    try:
        print("===== Supply Chain Risk Analysis Pipeline =====")
        
        # Step 1: Fetch News Data
        if not os.path.exists(NEWS_DATA_PATH):
            print("Fetching news data...")
            fetch_news_data(NEWS_DATA_PATH)
            print(f"News data saved to {NEWS_DATA_PATH}")
        else:
            print(f"News data already exists at {NEWS_DATA_PATH}")

        # Step 2: Perform Sentiment Analysis
        print("Performing sentiment analysis...")
        news_df = pd.read_csv(NEWS_DATA_PATH)
        analyzed_news = analyze_news(news_df)
        analyzed_news.to_csv(SENTIMENT_ANALYSIS_PATH, index=False)
        print(f"Sentiment analysis results saved to {SENTIMENT_ANALYSIS_PATH}")
        
        # Step 3: Generate and Analyze Warehouse Data
        if not os.path.exists(WAREHOUSE_DATA_PATH):
            print("Generating warehouse data...")
            analyze_warehouse_data(WAREHOUSE_DATA_PATH)
            print(f"Warehouse data generated and saved to {WAREHOUSE_DATA_PATH}")
        else:
            print(f"Warehouse data already exists at {WAREHOUSE_DATA_PATH}")

        # Step 4: Predict Risks
        print("Predicting risks...")
        warehouse_data = pd.read_csv(WAREHOUSE_DATA_PATH)  # Load the warehouse data here
        # Assuming predict_risks now returns the updated DataFrame
        final_risk_analysis = predict_risks(warehouse_data)  # Pass the DataFrame, not the path
        
        # Ensure that the final analysis is saved
        final_risk_analysis.to_csv(FINAL_ANALYSIS_PATH, index=False)
        print(f"Final risk analysis saved to {FINAL_ANALYSIS_PATH}")

        # Step 5: Run Module 3: Alert Generator with ERP Integration
        print("Running Module 3: Alert Generator with ERP Integration")
        analyze_and_notify(input_file=WAREHOUSE_DATA_PATH)
        print("Module 3 with ERP integration completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Pipeline execution completed.")

if __name__ == "__main__":
    main()