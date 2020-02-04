import os
import numpy as np
import json
import pickle
from flask import render_template
from flask import request 
from flaskexample import app
import pandas as pd
import requests
from pet_functions import get_bearer_token
from pet_functions import get_text_resp
from pet_functions import clean_dirty_resp
from pet_functions import one_hot_fill
from pet_functions import get_petmod_predict


KEY = os.environ['PETFINDER_KEY2']
SECRET = os.environ['PETFINDER_SECRET2']

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Dog lover, go to the input page to test the app' },
       )

@app.route('/input')
def cesareans_input():
    return render_template("input.html")

@app.route('/output')
def cesareans_output():
  shelter_id = request.args.get('shelter_id')
  my_header = get_bearer_token(KEY = KEY, SECRET = SECRET)
  dirty_df = get_text_resp(organization = shelter_id, header = my_header)
  clean_df = clean_dirty_resp(df= dirty_df, vars_of_interest =['age','size', 'coat','attributes.special_needs','name','id'])
  coded_df = one_hot_fill(df = clean_df,
                          cols_in_mod = ['age_Adult', 'age_Baby', 'age_Senior', 
                          'age_Young', 'City_Chicago', 'City_Denver', 
                          'City_ElPaso', 'City_Houston', 'City_Indy', 
                          'City_Minne', 'City_StLouis', 'size_Extra Large',
                          'size_Large', 'size_Medium', 'size_Small',
                          'coat_Curly', 'coat_Hairless', 'coat_Long',
                          'coat_Medium', 'coat_Short', 'coat_Wire',
                          'attributes.special_needs_False',
                          'attributes.special_needs_True'],
                          cols_to_transform = ['age','size', 'coat',
                          'attributes.special_needs'])
  predict_df = get_petmod_predict(coded_df = coded_df)
  new_df = predict_df.sort_values(by='predicted_percent',ascending = True).reset_index(drop=True)
  shelter_df = pd.read_csv('shelters.csv', sep= ';')
  print(shelter_df)
  return render_template("output.html", my_df = new_df, my_range = range(0,10),range2 = range(0,9), shelt_df =shelter_df)
