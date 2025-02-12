import os
import pickle
import numpy as np
import pandas as pd
from flask import Blueprint, request, jsonify
from app.utils.auth import check_api_key

api_bp = Blueprint('api', __name__)

# _ Load Model
MODEL_PATH = os.path.join(os.getcwd(), "app", "models", "insurance_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"⚠️ Model file not found at {MODEL_PATH}")

with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

@api_bp.route("/submit_data", methods=["POST"])
def submit_data():
    
    # _ API Key authentication check 
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # _ Ensure all fields exist
        required_fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        if not all(field in request.form for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # _ Extract and Convert Data Safely
        try:
            age = float(request.form.get("age", 0))
            sex = 1 if request.form.get("sex") == "male" else 0
            bmi = float(request.form.get("bmi", 0))
            children = int(request.form.get("children", 0))
            smoker = 1 if request.form.get("smoker") == "yes" else 0
            region = request.form.get("region")
        except ValueError:
            return jsonify({"error": "Invalid input types"}), 400

        # _ Encode Region
        region_map = {"northeast": 0, "northwest": 1, "southeast": 2, "southwest": 3}
        region_encoded = region_map.get(region, -1)

        if region_encoded == -1:
            return jsonify({"error": "Invalid region"}), 400

        # _ Convert to Pandas DataFrame
        input_data = pd.DataFrame([{
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region_encoded
        }])

        # Debugging: Print input data and types
        print("Input Data:", input_data)
        print("Data Types:", input_data.dtypes)

        # _ Ensure All Data is Numeric
        input_data = input_data.astype(float)

        # _ Check for NaN values
        if input_data.isnull().values.any():
            return jsonify({"error": "Input contains NaN values"}), 400

        # _ Make Prediction
        prediction = model.predict(input_data)[0]

        return jsonify({"prediction": f"${prediction:,.2f}"})

    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 400