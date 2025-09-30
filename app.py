

from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
import os

app = Flask(__name__)
model = joblib.load('model.joblib')

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../cardio-webpage'), 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Collect all patient info
    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0
    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    name = data.get('name', 'Unknown')
    age = safe_int(data.get('age', 0))
    sex = safe_int(data.get('sex', 0))
    Chest_Pain_Severity = safe_float(data.get('Chest_Pain_Severity', 0))
    Breathing_Difficulty_Severity = safe_float(data.get('Breathing_Difficulty_Severity', 0))
    Headache = safe_int(data.get('Headache', 0))
    Fatigue = safe_int(data.get('Fatigue', 0))
    Fever = safe_int(data.get('Fever', 0))
    Dizziness = safe_int(data.get('Dizziness', 0))
    Cough = safe_int(data.get('Cough', 0))
    Swelling = safe_int(data.get('Swelling', 0))
    Weight_Loss = safe_int(data.get('Weight_Loss', 0))
    Sleep_Trouble = safe_int(data.get('Sleep_Trouble', 0))
    Weight_kg = safe_float(data.get('Weight_kg', 0))
    Blood_Pressure = safe_float(data.get('Blood_Pressure', 0))
    Cholesterol = safe_float(data.get('Cholesterol', 0))

    # Features for model (Sex after Age)
    features = [
        sex, Chest_Pain_Severity, Breathing_Difficulty_Severity, Headache, Fatigue, Fever, Dizziness, Cough, Swelling, Weight_Loss, Sleep_Trouble,
        Weight_kg, Blood_Pressure, Cholesterol, age
    ]
    X = np.array(features).reshape(1, -1)
    # Get new health questions
    bp = int(data.get('bp', 0))
    chol = int(data.get('chol', 0))
    family = int(data.get('family', 0))
    diabetes = int(data.get('diabetes', 0))
    depression = int(data.get('depression', 0))
    arthritis = int(data.get('arthritis', 0))
    skin_cancer = int(data.get('skin_cancer', 0))
    other_cancer = int(data.get('other_cancer', 0))

    # Get new symptom questions
    chest_pain = int(data.get('chest_pain', 0))
    short_breath = int(data.get('short_breath', 0))
    swelling = int(data.get('swelling', 0))
    palpitations = int(data.get('palpitations', 0))
    dizziness = int(data.get('dizziness', 0))
    fatigue = int(data.get('fatigue', 0))
    nausea = int(data.get('nausea', 0))
    sweating = int(data.get('sweating', 0))
    pain_neck = int(data.get('pain_neck', 0))
    weight_gain = int(data.get('weight_gain', 0))

    # Features for model (add new features if retrained)
    # If model expects only old features, use: X = np.array(features[:9]).reshape(1, -1)
    try:
        risk = model.predict(X)[0]
        proba = model.predict_proba(X)[0][1]
    except Exception:
        # fallback for old model
        X = np.array(features[:9]).reshape(1, -1)
        risk = model.predict(X)[0]
        proba = model.predict_proba(X)[0][1]

    # Advice based on risk
    if risk == 1:
        advice = ['ECG', 'Lipid Profile', 'Cardiologist Referral']
        level = 'High'
    else:
        advice = ['Routine Checkup']
        level = 'Low'
    # Echo back all question/answer pairs from the POST data for frontend display
    answers = {}
    # Only include the questions that were sent by the frontend (excluding name, age, sex)
    for k, v in data.items():
        if k not in ['name', 'age', 'sex']:
            answers[k] = v

    report = {
        'name': name,
        'sex': 'Male' if sex == 1 else 'Female',
        'age': age,
        'risk_level': level,
        'risk_probability': round(float(proba), 2),
        'recommended_tests': advice,
        'answers': answers
    }
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)