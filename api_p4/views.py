import pandas as pd 
import numpy as np
import pickle 
from .utils import * 
from flask import Flask, request #, render_template, url_for,  
#import json 

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

with open(app.config['SOURCE_FILE'], 'rb') as file: 
    unpickler = pickle.Unpickler(file)
    dict_regr = unpickler.load()    
    trips = unpickler.load()    
    CITY_lbl = unpickler.load()    
    std_scale = unpickler.load()    
    
SOURCE_FILE = 'OC_DS_P4_run.pkl' 

FERIES = ['2015-01-01', '2015-01-19', '2015-02-16', '2015-05-25', '2015-07-04', '2015-09-07', '2015-10-12', '2015-11-11', '2015-11-26', '2015-12-25', \
          '2016-01-01', '2016-01-18', '2016-02-15', '2016-05-30', '2016-07-04', '2016-09-05', '2016-10-10', '2016-11-11', '2016-11-24', '2016-12-26', \
          '2017-01-02', '2017-01-16', '2017-02-20', '2017-05-29', '2017-07-04', '2017-09-04', '2017-10-09', '2017-11-11', '2017-11-23', '2017-12-25'] 
                 
dict_horaires = { 0:"0001-0559", 6:"0600-0659", 7:"0700-0759", 8:"0800-0859", 9:"0900-0959", \
                 10:"1000-1059", 11:"1100-1159", 12:"1200-1259", 13:"1300-1359", 14:"1400-1459", \
                 15:"1500-1559", 16:"1600-1659", 17:"1700-1759", 18:"1800-1859", 19:"1900-1959", \
                 20:"2000-2059", 21:"2100-2159", 22:"2200-2259", 23:"2300-2359" }

#if __name__ == "__main__":
#    app.run() 

@app.route('/delay/')
def delay():
    origin = request.args.get('origin') 
    dest = request.args.get('dest') 
    dep = request.args.get('dep') 
    arr = request.args.get('arr') 
    day = request.args.get('day') 

    return delay_estimation(day, origin, dest, dep, arr)
