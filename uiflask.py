from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np
import pandasql as ps

app= Flask(__name__)
cors= CORS(app)
model= pickle.load(open('RandomForestModel.pkl','rb'))
car= pd.read_csv('filtered_car')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sell')
def sell():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()
    return render_template('sell.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type)

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    company=request.form.get('company')
    car_model=request.form.get('car_models')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=request.form.get('kilo_driven')
    print(company)
    prediction=model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                              data=np.array([car_model,company,year,driven,fuel_type]).reshape(1, 5)))
    return str(np.round(prediction[0],2))

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    price  = request.form.get('Price')
    fuel = request.form.get('fuel')
    comp = request.form.get('company')
    driven = request.form.get('kms')
    year = request.form.get('year')
    copy = pd.DataFrame(car.copy(deep=True))

    if(len(price)!=0):
        price = int(price)
        copy = copy.query("Price <=@price")
    if (len(year) != 0):
        year = int(year)
        copy = copy.query("year >=@year")
    if (len(fuel)!=0):
        copy = copy.query("fuel_type ==@fuel")
    if (len(comp)!=0):
        copy = copy.query("company ==@comp")
    if (len(driven)!=0):
        driven=int(driven)
        copy = copy.query("kms_driven <=@driven")
    car_name=[]
    car_price=[]
    car_brand=[]
    car_driven=[]
    car_fuel=[]
    car_year=[]
    for i in range(len(copy)):
        car_name.append(copy.iloc[i, 0])
        car_price.append(copy.iloc[i, 3])
        car_brand.append(copy.iloc[i, 1])
        car_driven.append(copy.iloc[i, 4])
        car_fuel.append(copy.iloc[i, 5])
        car_year.append(copy.iloc[i, 2])
    print(car_name)
    return render_template('cars.html',car_name=car_name,car_price=car_price,car_brand=car_brand,car_driven=car_driven,car_fuel=car_fuel,car_year=car_year)

if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')
