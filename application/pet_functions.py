import os
import requests 
import json
import pandas as pd 
import sklearn
import pickle
import numpy as np

KEY = os.environ['PETFINDER_KEY2']
SECRET = os.environ['PETFINDER_SECRET2']

def get_bearer_token(KEY,SECRET):
	data = {
	'grant_type': 'client_credentials',
	'client_id': KEY,
	'client_secret': SECRET
	  }
	response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
	if response.reason != 'OK':
	    print('failed to get token. check credentials')
	    print('response code:', response.status_code)
	    print('response reason:', response.reason)
	else:
	    print('new token received')
	    TOKEN = json.loads(response.text)['access_token']
	    new_header = {
	            'Authorization': 'Bearer {}'.format(TOKEN),}
	return new_header


def get_text_resp(organization, header):
	org = organization
	type = 'dog'
	page = 1
	limit = 100
	status = 'adoptable'
	respdf = pd.DataFrame()
	req_url = f'https://api.petfinder.com/v2/animals?type={type}&limit={limit}&page={page}&status={status}&organization={org}'
	response = requests.get(req_url, headers = header)
	my_dict =json.loads(response.text)
	animals = my_dict.get('animals')
	df = pd.io.json.json_normalize(animals)
	respdf = respdf.append(df)
	return respdf



def clean_dirty_resp(df, vars_of_interest):
	my_df = df 
	my_df = my_df[vars_of_interest]
	#city should be here!
	#other cleaning?
	#uf the columns expected by the model don't exist, create them and fill them with zeros
	return my_df


#applies one hot coding to all discrete variables
#fills in empty columns for all columns expected by the model and not already present in df. 
def one_hot_fill(df, cols_in_mod, cols_to_transform):
	my_df = df 
	X = my_df[['age','size','coat','attributes.special_needs']]
	X = pd.get_dummies(df, columns = cols_to_transform)
	Xcollist = list(X.columns)

	cols_in_mod = cols_in_mod

	for col in cols_in_mod:
	 	if col not in Xcollist:
	 		X.insert(0, col,0)
	return X



def get_petmod_predict(coded_df): #clean_df
	X = coded_df.drop(['name','id'],1)
	filename = 'draft_logit_reg.sav'
	loaded_model = pickle.load(open(filename, 'rb'))
	pred_ys = loaded_model.predict_proba(X)
	coded_df['predicted_probability'] = pred_ys[:,0] 
	coded_df['predicted_percent'] = round(coded_df['predicted_probability']*100)

	Denver = X
	Denver['City_Chicago'] = 0
	Denver['City_StLouis'] = 0
	Denver['City_Indy'] = 0
	Denver['City_Houston'] = 0
	Denver['City_ElPaso'] = 0
	Denver['City_Denver'] = 1
	Denver['City_Minne'] = 0
	pred_y2s = loaded_model.predict_proba(Denver)

	coded_df['predicted_prob_Denver'] = pred_y2s[:,0] 
	coded_df['predicted_percent_Denver'] = round((coded_df['predicted_prob_Denver']*100),0)

	Minne = X
	Minne['City_Chicago'] = 0
	Minne['City_StLouis'] = 0
	Minne['City_Indy'] = 0
	Minne['City_Houston'] = 0
	Minne['City_Denver'] = 0
	Minne['City_ElPaso'] = 0
	Minne['City_Minne'] = 1

	pred_y3s = loaded_model.predict_proba(Minne)

	coded_df['predicted_prob_Minne'] = pred_y3s[:,0] 
	coded_df['predicted_percent_Minne'] = round((coded_df['predicted_prob_Minne']*100),0)
	
	Chicago= X
	Chicago['City_Chicago'] = 1
	Chicago['City_StLouis'] = 0
	Chicago['City_Indy'] = 0
	Chicago['City_Houston'] = 0
	Chicago['City_ElPaso'] = 0
	Chicago['City_Minne'] = 0
	Chicago['City_Minne'] = 0
	pred_y4s = loaded_model.predict_proba(Chicago)

	coded_df['predicted_prob_Chicago'] = pred_y4s[:,0] 
	coded_df['predicted_percent_Chicago'] = round((coded_df['predicted_prob_Chicago']*100),0)

	return coded_df





