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

#if __name__ == "__main__":
#    app.run() 

@app.route('/delay/')
def delay():

    origin = request.args.get('origin') 
    dest = request.args.get('dest') 
    dep = request.args.get('dep') 
    arr = request.args.get('arr') 
    day = request.args.get('day') 

    return delay_estimation(origin=origin, dest=dest, h_dep=dep, h_arr=arr, dt_flight=day, pickfile=app.config['SOURCE_FILE'])
