from flask import Flask, jsonify, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json


data = pd.read_csv("diabetes.csv")
app = Flask(__name__, static_url_path='', static_folder='static')

correlation = data.corr()
X=data.drop("Outcome",axis=1)
Y=data['Outcome']
X_train,X_test,Y_train,Y_test =train_test_split(X,Y,test_size=0.2)


model=LogisticRegression(max_iter=1000)
model.fit(X_train,Y_train)


model_json = model.coef_.tolist()
with open('model.json', 'w') as json_file:
    json.dump(model_json, json_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # Get input values from the form
        pregnancies = float(data['pregnancies'])
        glucose = float(data['glucose'])
        blood_pressure = float(data['blood_pressure'])
        skin_thickness = float(data['skin_thickness'])
        insulin = float(data['insulin'])
        bmi = float(data['bmi'])
        diabetes_pedigree_function = float(data['diabetes_pedigree_function'])
        age = float(data['age'])

        # Sample input data (replace this with the actual input from the user)
        input_data = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]

        # Load the serialized model from JSON
        with open('model.json', 'r') as json_file:
            model_coef = json.load(json_file)

        # Make prediction using the loaded coefficients
        user_prediction = predict_diabetes(input_data, model_coef)

        return jsonify({'prediction': user_prediction})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

def predict_diabetes(input_data, model_coef):
    try:
        # Ensure input_data[0] contains numerical values
        input_values = []
        for x in input_data:
            input_values.append(x)
        print(input_values)
        # Ensure model_coef contains numerical coefficients
        model_coefs = []
        for coef in model_coef:
            model_coefs.append(coef)
        print(model_coef)
        # Perform the prediction calculation
        raw_prediction = sum(x * coef for x, coef in zip(input_values, model_coefs[0]))
        print(raw_prediction)
        # Apply a threshold for simplicity (you can adjust this based on your model)
        threshold = 0.5
        user_prediction = 1 if raw_prediction > threshold else 0
        print(user_prediction)
        return user_prediction
    except Exception as e:
        print(f"Error in predict_diabetes: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
