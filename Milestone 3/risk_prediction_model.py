import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Updated adjust_stock_in_erp function with a fixed product_name ('product_1')
def adjust_stock_in_erp(risk_level, adjustment_quantity):
    try:
        # Fixed product name
        product_name = 'product_1'

        # Connect to the local ERP system (SQLite)
        conn = sqlite3.connect('C:/Users/tejag/OneDrive/Desktop/Project_SP/data/erp_simulation.db')
        cursor = conn.cursor()

        # Create the products table if it doesn't exist
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                stock_quantity INTEGER NOT NULL
            )
        ''')

        # Check if the table is empty, and insert a product if it is
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            # Table is empty, so insert the first product
            cursor.execute(''' 
                INSERT INTO products (product_name, stock_quantity)
                VALUES ('product_1', 100)  -- Example product with initial stock
            ''')
            conn.commit()
            print(f"Product '{product_name}' inserted with initial stock quantity of 100.")

        # Fetch current stock quantity from the ERP database for the fixed product_name
        cursor.execute("SELECT stock_quantity FROM products WHERE product_name = ?", (product_name,))
        current_quantity = cursor.fetchone()

        if current_quantity:
            current_quantity = current_quantity[0]

            if risk_level == 'SELL' and current_quantity < adjustment_quantity:
                adjustment_quantity = current_quantity  # Sell only available stock
                print(f"Warning: Trying to sell {adjustment_quantity} units, but only {current_quantity} units available.")

            if risk_level == 'BUY':
                action = f"Buying {adjustment_quantity} units"
                cursor.execute("UPDATE products SET stock_quantity = stock_quantity + ? WHERE product_name = ?", 
                               (adjustment_quantity, product_name))
            elif risk_level == 'SELL':
                action = f"Selling {adjustment_quantity} units"
                cursor.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_name = ?", 
                               (adjustment_quantity, product_name))
            elif risk_level == 'MONITOR':
                action = "Monitoring stock levels (no change)"

            conn.commit()
            print(f"Action: sell {action} for Product: {product_name}")

            # Fetch the updated stock quantity
            cursor.execute("SELECT stock_quantity FROM products WHERE product_name = ?", (product_name,))
            updated_quantity = cursor.fetchone()[0]
            print(f"Updated stock quantity: {updated_quantity}")

        else:
            print(f"Product '{product_name}' not found in the ERP database.")

        conn.close()
    except Exception as e:
        print(f"Error adjusting stock in ERP: {e}")

# Your original predict_risks function, modified to include stock adjustments without product_name
def predict_risks(data):
    # Step 1: Preprocess the data (encoding categorical variables, handling missing values)
    data['Sentiment'] = data['Sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1})

    label_encoder = LabelEncoder()
    data['Risk Analysis'] = label_encoder.fit_transform(data['Risk Analysis'])
    data = data.dropna()

    # Step 2: Feature selection (X) and target variable (y)
    X = data[['Warehouse Capacity', 'Monthly Incoming', 'Sentiment']]  # Features
    y = data['Risk Analysis']  # Target (Risk Analysis: Low=0, Medium=1, High=2)

    # Step 3: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Step 4: Train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 5: Predict on the test set
    y_pred = model.predict(X_test)

    # Step 6: Evaluate the model
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))

    # Step 7: Feature Importance (optional)
    feature_importances = model.feature_importances_
    plt.barh(X.columns, feature_importances)
    plt.xlabel('Feature Importance')
    plt.title('Feature Importance for Risk Prediction')
    plt.show()

    # Step 8: Adjust stock based on the predicted risks
    for idx, prediction in enumerate(y_pred):
        risk_level = 'BUY' if prediction == 2 else 'SELL' if prediction == 1 else 'MONITOR'
        
        # Assuming the adjustment quantity is based on the predicted risk level (you can adjust logic here)
        adjustment_quantity = 100 if risk_level == 'BUY' else 50 if risk_level == 'SELL' else 0
        
        # Call the ERP system to adjust stock
        adjust_stock_in_erp(risk_level, adjustment_quantity)

        # Add the stock adjustment action to the DataFrame (to be saved or passed further)
        data.at[idx, 'Stock_Adjustment'] = f'{risk_level}: {adjustment_quantity} units'

    return data
