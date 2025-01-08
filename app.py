from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

app = Flask(__name__)

# Load the model and tokenizer (adjust to your model)
model = AutoModelForSequenceClassification.from_pretrained("./saved_model")
tokenizer = AutoTokenizer.from_pretrained("./saved_model")

# Prediction function
def get_prediction(description):
    # Tokenize the input description
    inputs = tokenizer(description, padding=True, truncation=True, max_length=128, return_tensors="pt")
    
    # Get model outputs
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract the predicted value (assuming regression output)
    prediction = outputs.logits.item()
    return prediction

@app.route('/')
def home():
    return "Welcome to the Chocolate Supply Chain Risk Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the JSON data from the POST request
    description = data.get('description')  # Extract 'description' field
    
    if description:
        prediction = get_prediction(description)  # Make a prediction using your model
        return jsonify({'prediction': prediction})  # Return the prediction in JSON format
    else:
        return jsonify({'error': 'Description is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
