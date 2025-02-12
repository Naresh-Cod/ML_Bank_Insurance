import pickle
import numpy as np
import os

# Load Model
MODEL_PATH = 'model/insurance_model.pkl'
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
else:
    model = None
    print("⚠️ Warning: Model file not found!")

def predict_insurance(data):
    if model is None:
        raise Exception("Model not found!")

    # Encode Inputs
    sex = 1 if data['sex'] == 'female' else 0
    smoker = 1 if data['smoker'] == 'yes' else 0
    region_map = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}
    region = region_map.get(data['region'], -1)

    if region == -1:
        raise ValueError("Invalid region")

    # Convert to Numpy Array
    input_data = np.array([[data['age'], sex, data['bmi'], data['children'], smoker, region]])
    
    # Prediction
    return model.predict(input_data)[0]
