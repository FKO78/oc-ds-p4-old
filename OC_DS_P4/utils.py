import pandas as pd 
import numpy as np # linear algebra
import datetime 
import pickle 

FERIES = ['2015-01-01', '2015-01-19', '2015-02-16', '2015-05-25', '2015-07-04', '2015-09-07', '2015-10-12', '2015-11-11', '2015-11-26', '2015-12-25', \
          '2016-01-01', '2016-01-18', '2016-02-15', '2016-05-30', '2016-07-04', '2016-09-05', '2016-10-10', '2016-11-11', '2016-11-24', '2016-12-26', \
          '2017-01-02', '2017-01-16', '2017-02-20', '2017-05-29', '2017-07-04', '2017-09-04', '2017-10-09', '2017-11-11', '2017-11-23', '2017-12-25'] 
                 
dict_horaires = { 0:"0001-0559", 6:"0600-0659", 7:"0700-0759", 8:"0800-0859", 9:"0900-0959", \
                 10:"1000-1059", 11:"1100-1159", 12:"1200-1259", 13:"1300-1359", 14:"1400-1459", \
                 15:"1500-1559", 16:"1600-1659", 17:"1700-1759", 18:"1800-1859", 19:"1900-1959", \
                 20:"2000-2059", 21:"2100-2159", 22:"2200-2259", 23:"2300-2359" }

def from_hdays(date=datetime.date.today()): 
    res = []
    for d in FERIES: 
        delta = abs(date - datetime.datetime.strptime(d,'%Y-%m-%d').date() ) 
        res.append(delta.days )
    return min(res) 

def get_group(dist):
    return ceil((dist+1) / 250) if dist <2500 else 11

def delay_estimation(dt_flight="2016-04-10", origin='San Fancisco', dest='Los Angeles', h_dep=10, h_arr=14, pickfile="OC_DS_P4_run.pkl"): 

    input =  [] 
    
    with open(app.config['SOURCE_FILE'], 'rb') as file: 
        unpickler = pickle.Unpickler(file)
        dict_regr = unpickler.load()    
        trips = unpickler.load()    
        CITY_lbl = unpickler.load()    
        std_scale = unpickler.load()    
        cities = unpickler.load()
    
    try: 
        d_flight = datetime.datetime.strptime(dt_flight, '%Y-%m-%d').date() 
    except ValueError: 
        return "Erreur dans le format de date {}".format(dt_flight)  

    if d_flight.year != 2016: 
        return "La date doit être en 2016 {}".format(d_flight)

    try:
        origin = cities[cities.name.str.contains(origin, case=False)].name.value[0]
        dest = cities[cities.name.str.contains(dest, case=False)].name.value[0]
        group =  trips[(trips.ORIGIN_CITY_NAME == origin) & (trips.DEST_CITY_NAME == dest)].DISTANCE_GROUP.values[0]
    except IndexError: 
         return print("Pas de prédiction possible entre", origin.split(',')[0], "et", dest.split(',')[0] )

# ['MONTH', 'ORIGIN_CITY', 'DEP_TIME_BLK', 'ARR_TIME_BLK', 'DISTANCE_GROUP', 'FROM_HDAYS', 'DAY_OF_WEEK', 'DEST_CITY']
 
    input.append(d_flight.month) 
    input.append(CITY_lbl.transform([origin])[0]) 
    input.append(h_dep) 
    input.append(h_arr) 
    input.append(group) #DISTANCE_GROUP 
    input.append(abs(from_hdays(d_flight)))  
    input.append(d_flight.weekday()+1) 
    input.append(CITY_lbl.transform([dest])[0]) 

    input_scaled = std_scale.transform([input])

    return origin, dest #, dict_regr.predict(input_scaled) 