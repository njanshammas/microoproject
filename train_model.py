
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib


# Load custom synthetic dataset
file_path = 'custom_synthetic_dataset.csv'
df = pd.read_csv(file_path)



# Use all features matching frontend/backend
features = [
    'Sex',
    'Chest_Pain_Severity',
    'Breathing_Difficulty_Severity',
    'Headache_Severity',
    'Fatigue_Severity',
    'Fever_Severity',
    'Dizziness_Severity',
    'Cough_Severity',
    'Swelling_Severity',
    'Weight_Loss_Severity',
    'Sleep_Trouble_Severity',
    'Weight_kg',
    'Blood_Pressure',
    'Cholesterol',
    'Age'
]

# Encode only the target column
df['Heart_Disease'] = df['Heart_Disease'].map({'Yes': 1, 'No': 0})




X = df[features]
y = df['Heart_Disease']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)
# Save model
joblib.dump(model, 'model.joblib')
print('Model trained and saved as model.joblib')