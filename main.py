from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forms')
def forms():
    return render_template('forms.html')

@app.route('/model_score')
def model_score():
    return render_template('model_score.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    age = request.form.get('Age')
    sex = request.form.get('Sex')
    bmi = request.form.get('Bmi')
    children = request.form.get('Children')
    smoker = request.form.get('Smoker')
    region = request.form.get('Region')
    data=[[age, sex, bmi, children, smoker, region]]


    input=pd.DataFrame(data,columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])
    
    with open("/Users/gauravjangid/PycharmProjects/insurance project/model/best_model.pkl","rb") as file:
        pipeline=pickle.load(file)
        
    pred=pipeline.predict(input)
    return render_template('model_score.html', pred=np.round(pred, 2))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1000)
