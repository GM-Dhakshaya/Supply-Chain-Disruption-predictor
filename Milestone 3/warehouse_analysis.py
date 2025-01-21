import pandas as pd
import sqlite3  # Import sqlite3 for ERP simulation

# Function to adjust stock in ERP system
def adjust_stock_in_erp(risk_level, adjustment_quantity, product_name):
    try:
        # Connect to the local ERP system (SQLite)
        conn = sqlite3.connect('C:/Users/tejag/OneDrive/Desktop/Project_SP/data/erp_simulation.db')
        cursor = conn.cursor()

        # Fetch current stock quantity from the ERP database
        cursor.execute("SELECT stock_quantity FROM products WHERE product_name = ?", (product_name,))
        current_quantity = cursor.fetchone()

        if current_quantity:
            current_quantity = current_quantity[0]

            # If risk level is SELL, ensure we don't sell more than available stock
            if risk_level == 'SELL':
                if current_quantity <= 0:
                    print(f"Warning: No stock available to sell for {product_name}.")
                    action = "Stock is empty, cannot sell."
                elif current_quantity < adjustment_quantity:
                    adjustment_quantity = current_quantity  # Sell only the available stock
                    print(f"Warning: Trying to sell {adjustment_quantity} units, but only {current_quantity} units available.")
                    action = f"Selling {adjustment_quantity} units"
                else:
                    action = f"Selling {adjustment_quantity} units"
                    cursor.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_name = ?", 
                                   (adjustment_quantity, product_name))

            # If risk level is BUY, increase stock
            elif risk_level == 'BUY':
                action = f"Buying {adjustment_quantity} units"
                cursor.execute("UPDATE products SET stock_quantity = stock_quantity + ? WHERE product_name = ?", 
                               (adjustment_quantity, product_name))

            # If risk level is MONITOR, no change in stock
            elif risk_level == 'MONITOR':
                action = "Monitoring stock levels (no change)"

            conn.commit()
            print(f"Action: {action} for Product: {product_name}")

            # Fetch the updated stock quantity
            cursor.execute("SELECT stock_quantity FROM products WHERE product_name = ?", (product_name,))
            updated_quantity = cursor.fetchone()[0]
            print(f"Updated stock quantity: {updated_quantity}")

        else:
            print(f"Product {product_name} not found in the ERP database.")

        conn.close()
    except Exception as e:
        print(f"Error adjusting stock in ERP: {e}")

# Function to analyze warehouse data and generate alerts
def analyze_warehouse_data(file_path):
    # Load the warehouse data from CSV
    data = pd.read_csv(file_path)

    # Define thresholds and conditions
    warehouse_capacity_threshold = 0.8  # 80% capacity considered high
    risk_threshold = "High"  # Risk levels: Low, Medium, High
    sentiment_threshold = "Negative"  # Sentiment: Positive, Neutral, Negative

    alerts = []

    # Loop through each row and analyze the data
    for index, row in data.iterrows():
        # Calculate warehouse utilization
        utilization = row['Monthly Incoming'] / row['Warehouse Capacity']

        # Check product name from the row (assume column 'Product Name' exists in the data)
        product_name = row.get('Product Name', 'product_1')  # Default product name if not found

        # Analyze risk factors and sentiment
        if utilization > warehouse_capacity_threshold or row['Risk Analysis'] == risk_threshold:
            if row['Sentiment'] == sentiment_threshold:
                alerts.append((row['Month'], "SELL", f"High utilization ({utilization:.2f}), {row['Risk Analysis']} risk, {row['Sentiment']} sentiment"))
                # Adjust stock based on the alert
                adjust_stock_in_erp('SELL', 50, product_name)  # Example: Selling 50 units
            else:
                alerts.append((row['Month'], "MONITOR", f"High utilization ({utilization:.2f}) with {row['Risk Analysis']} risk"))
                # Monitor stock levels with no action
                adjust_stock_in_erp('MONITOR', 0, product_name)
        elif utilization < 0.4:  # If utilization is very low
            alerts.append((row['Month'], "BUY", f"Low utilization ({utilization:.2f}), consider buying material"))
            # Adjust stock by buying 100 units
            adjust_stock_in_erp('BUY', 100, product_name)

    return alerts

# Main function to run the warehouse analysis and display alerts
if __name__ == "__main__":
    # Specify the file path for generated warehouse data
    warehouse_file = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv"

    # Analyze the warehouse data
    alerts = analyze_warehouse_data(warehouse_file)

    # Display the generated alerts
    if alerts:
        for alert in alerts:
            print(f"Month: {alert[0]}, Action: {alert[1]}, Reason: {alert[2]}")
    else:
        print("No alerts generated.")
