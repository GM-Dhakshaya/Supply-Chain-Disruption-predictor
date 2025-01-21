import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def predictive_model(file_path):
    # Load the data
    data = pd.read_csv('C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv')

    # Feature selection
    features = ['Warehouse Capacity', 'Monthly Incoming', 'Monthly Outgoing', 'Sentiment']
    X = data[features]
    y = data['Risk Analysis']  # Target variable (Risk Analysis: Low, Medium, High)

    # Convert categorical data to numerical
    X.loc[:, 'Sentiment'] = X['Sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1})

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict and evaluate the model
    y_pred = model.predict(X_test)
    print("Model Evaluation: \n", classification_report(y_test, y_pred))

    return model


# Example to test the function
if __name__ == "__main__":
    sample_file = "C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv"  # Replace with actual data path
    model = predictive_model(sample_file)
