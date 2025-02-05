from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os

app = Flask(__name__)

# Trained model load karein
with open('model/insurance_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forms')
def forms():
    return render_template('forms.html') # Updated form

@app.route('/submit_data', methods=['POST'])
def submit_data():
    try:
        # Form se data lena
        age = float(request.form['age'])
        sex = request.form['sex']
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form['smoker']
        region = request.form['region']

        # Encoding for categorical variables
        sex = 1 if sex == 'female' else 0
        smoker = 1 if smoker == 'yes' else 0
        region_map = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}
        region = region_map[region]

        # Prediction ke liye input prepare karein
        input_data = np.array([[age, sex, bmi, children, smoker, region]])
        prediction = model.predict(input_data)[0]

        return jsonify({'prediction': f"${prediction:,.2f}"})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1000)
