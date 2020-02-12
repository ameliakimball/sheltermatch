# sheltermatch
This repo contains all the workings of the flask app for Sheltermatch, a tool to predict the adoptability of dogs at specific animal shelters, and at selected relocation cities. 

This folder is the live version, which also lives on an AWS EC2 instance and is available at 
http://processingdata.co/input

## requirements

the app requires Python 3 (for trivial reasons: e.g. f statments), functions will fail returning server errors 

required packages are: 

`pip install flask numpy pandas requests sklearn gunicorn`

## folder structure 

### application/ contains:

-draft_logit_reg.sav : the .sav pickled model file.  
-run.py: a script that instantiates a local server for debugging.   
-pet_functions.py : a python script of functions called by the app. 
-shelters.csv : a list of the shelters servied from the sql database (to be served to the user with their api query). 

### application/flaskexample contains: 
-views.py: the "guts" of the app, this is top level code that calls the functions in pet_functions.py and instantiates what to do from input to output screens on the ap.   
-templates/ : the html templates used for the input and output   
-static/: a folder with css/, fonts/ and js/ for the website. *Note that /etc/nginx/sites-enabled points to the static folder*, and therefore any change to this folder structure risks losing website formatting, or breaking the website entirely.   
