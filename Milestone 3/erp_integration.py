import sqlite3
import pandas as pd
import logging
from datetime import datetime

# Define constants
DATABASE_PATH = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/erp_simulation.db"
ALERT_FILE_PATH = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/inventory_alert.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_database():
    """
    Ensure the ERP database and alerts table are set up.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                alert_type TEXT,
                recommendation TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        logging.info("Database setup completed.")
    except Exception as e:
        logging.error(f"Error setting up the database: {e}")
    finally:
        conn.close()

def update_erp_database(product_name, alert_type, recommendation):
    """
    Updates the ERP database with inventory alerts.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (product_name, alert_type, recommendation)
            VALUES (?, ?, ?)
        ''', (product_name, alert_type, recommendation))
        conn.commit()
        logging.info(f"Alert saved for product '{product_name}': {alert_type}")
    except Exception as e:
        logging.error(f"Error updating the database: {e}")
    finally:
        conn.close()

def map_scores(data):
    """
    Map risk and sentiment values to numerical scores.
    """
    risk_mapping = {'Neutral': 0, 'Positive': 1, 'Negative': -1}
    sentiment_mapping = {'low': -1, 'medium': 0, 'high': 1}

    data['Risk_Score'] = data['Risk Analysis'].map(risk_mapping)
    data['Sentiment_Score'] = data['Sentiment'].map(sentiment_mapping)
    return data

def calculate_means(data):
    """
    Calculate mean scores for risk and sentiment.
    """
    sentiment_mean = data['Sentiment_Score'].mean()
    risk_mean = data['Risk_Score'].mean()
    return risk_mean, sentiment_mean

def generate_alert(risk_mean, sentiment_mean):
    """
    Generate alerts based on risk and sentiment mean values.
    """
    if risk_mean > 0 and sentiment_mean < 0:
        return "BUY \n High risk with negative sentiment. Potential shortage!\n Increase inventory to full capacity","Increase inventory to full capacity."
    elif risk_mean < 0 and sentiment_mean > 0:
        return "SELL \n Low risk with positive sentiment. Potential excess!\n Reduce inventory to avoid excess stock.", "Reduce inventory to avoid excess stock."
    elif risk_mean > 0 and sentiment_mean > 0:
        return " MODERATE \n High risk with positive sentiment. Mixed signals!\n Monitor inventory trends closely.", "Monitor inventory trends closely."
    else:
        return " MODERATE \n Low risk with negative sentiment. Stable situation. \n No immediate action required.", "No immediate action required."

def analyze_and_notify(input_file, product_name='product_1'):
    """
    Analyze warehouse data, calculate risks, and generate inventory alerts.
    """
    try:
        # Load data
        data = pd.read_csv(input_file)
        data = map_scores(data)

        # Calculate mean values
        risk_mean, sentiment_mean = calculate_means(data)

        # Generate alert
        alert, recommendation = generate_alert(risk_mean, sentiment_mean)

        # Save alert
        update_erp_database(product_name, alert, recommendation)
        with open(ALERT_FILE_PATH, "w") as f:
            f.write(f"{datetime.now()}\n{alert}\n{recommendation}")
        
        logging.info("Alert generated and saved successfully.")
    except Exception as e:
        logging.error(f"Error in analysis and notification: {e}")

# Example usage
if __name__ == "__main__":
    setup_database()
    input_file = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv"
    analyze_and_notify(input_file, "Chocolate")
