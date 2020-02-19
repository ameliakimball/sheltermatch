# sheltermatch
This repo contains all the workings of the flask app for Sheltermatch, a tool to predict the adoptability of dogs at specific animal shelters, and at selected relocation cities. 

### The app works by loading:   
- a model trained on a SQL database of adopted dogs scraped from the Petfinder API   

- a csv list of recommended shelters (pulled from the top shelters in the SQL database)

### When given a petfinder shelterid as input, the app:  
- pings the petfinder API,  
- returns the full list of dogs at that shelter,  
- calculates the probability of adoption within a month for each dog at the shelter,  
- calculates the probability of adoption for each dog if it were to move to Minneapolis, Denver, or Chicago,  
- returns the ten dogs who are least likely to be adopted within a month, along with the percent likelihood of their adoption within one month in their current shelter, in  Minneapolis, in Denver, and in Chicago
- returns a list of shelters in Minneapolis, Denver, and Chicago. 

This folder is the live version, which also lives on an AWS EC2 instance and is available at 
http://processingdata.co/input

## requirements

1) python version the app requires Python 3 (for trivial reasons: e.g. f statments), if Python 2 is used functions will fail returning server errors 

2) python modules
flask   
numpy  
pandas   
requests  
sklearn   
gunicorn  

`pip install flask numpy pandas requests sklearn gunicorn`

3) API Key and secret. As written, your petfinder API Key and secret must be defined as environment variables. They are called in views.py

4) To instantiate the app it must inheret two things from a separate repo:   
- a .csv list of shelters to display  
- a .sav file pickled model to run on the data retrieved from the API    

These files are listed in their appropriate folder in the folder structure section below. 


## folder structure 


### application/ contains:

- draft_logit_reg.sav : the .sav pickled model file.  
- run.py: a script that instantiates a local server for debugging.   
- pet_functions.py : a python script of functions called by the app. 
- shelters.csv : a list of the shelters servied from the sql database (to be served to the user with their api query). 

### application/flaskexample contains: 
- views.py: the "guts" of the app, this is top level code that calls the functions in pet_functions.py and specifies what happens from input to output screens on the app.   
- templates/ : the html templates used for the input and output   
- static/: a folder with css/, fonts/ and js/ for the website. *Note that /etc/nginx/sites-enabled points to the static folder*, and therefore any change to this folder structure risks losing website formatting, or breaking the website entirely.   
