from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("chocolate_supply_chain_dataset.csv")
print(data.head())

# Encode target variables (Likelihood)
label_encoder_likelihood = LabelEncoder()
data['Likelihood_encoded'] = label_encoder_likelihood.fit_transform(data['Likelihood'])

# Map Likelihood_encoded to the range -1 to +1
data['Likelihood_encoded'] = data['Likelihood_encoded'].apply(lambda x: 1 if x == 1 else -1)

# Split the data into train and test sets
train_data, eval_data = train_test_split(data, test_size=0.2, random_state=42)

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_data(examples):
    return tokenizer(examples["Description of the Risk"], padding="max_length", truncation=True)

# Tokenize the text column
train_encodings = tokenizer(list(train_data['Description of the Risk']), padding=True, truncation=True, max_length=128)
eval_encodings = tokenizer(list(eval_data['Description of the Risk']), padding=True, truncation=True, max_length=128)

class SupplyChainDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float32)  # Change to float32
        return item

# Create train and eval datasets
train_dataset = SupplyChainDataset(train_encodings, train_data['Likelihood_encoded'].values)
eval_dataset = SupplyChainDataset(eval_encodings, eval_data['Likelihood_encoded'].values)

# Load the pre-trained BERT model for regression
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=1)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch", 
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir="./logs",
)

# Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Evaluate the model
eval_results = trainer.evaluate(eval_dataset=eval_dataset)
print(f"Evaluation results: {eval_results}")

# Save the model and tokenizer
model.save_pretrained("./saved_model")
tokenizer.save_pretrained("./saved_model")

# Example input text
new_data = ["Unexpected supplier bankruptcy in the chocolate supply chain"]

# Tokenize the new data
new_encodings = tokenizer(new_data, padding=True, truncation=True, max_length=128, return_tensors="pt")

# Make predictions using the trained model
with torch.no_grad():
    outputs = model(**new_encodings)

# Get the predicted value
predicted_value = outputs.logits.item()
print(f"Predicted likelihood: {predicted_value}")
