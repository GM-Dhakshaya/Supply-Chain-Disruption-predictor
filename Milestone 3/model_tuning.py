import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('C:/Users/tejag/OneDrive/Desktop/Project_SP/data/generated_warehouse_data.csv')

# Preprocess the data (encoding categorical variables)
data['Sentiment'] = data['Sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1})

# Encode Risk Analysis if necessary
label_encoder = LabelEncoder()
data['Risk Analysis'] = label_encoder.fit_transform(data['Risk Analysis'])

# Handle missing values (if any)
data = data.dropna()

# Feature selection (X) and target variable (y)
X = data[['Warehouse Capacity', 'Monthly Incoming', 'Sentiment']]  # Features
y = data['Risk Analysis']  # Target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# Define the model
model = RandomForestClassifier(random_state=42)

# Hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

# Grid search for hyperparameter tuning
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Print the best parameters
print("Best parameters found: ", grid_search.best_params_)

# Evaluate the tuned model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Print classification report
print("Model Evaluation:")
print(classification_report(y_test, y_pred))
