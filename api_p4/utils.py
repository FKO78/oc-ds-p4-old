import pandas as pd 
import numpy as np # linear algebra
import datetime 

def from_hdays(date=datetime.date.today()): 
    res = []
    for d in FERIES: 
        delta = abs(date - datetime.datetime.strptime(d,'%Y-%m-%d').date() ) 
        res.append(delta.days )
    return min(res) 

def delay_estimation(dt_flight="2016-04-10", origin='San Fancisco', dest='Los Angeles', h_dep=10, h_arr=14): 

    input =  [] 
    
    try: 
        d_flight = datetime.datetime.strptime(dt_flight, '%Y-%m-%d').date() 
    except ValueError: 
        return print("Erreur dans le format de date") 

    if d_flight.year <> 2016: 
        return print("La date doit être en 2016")

    try:
        origin = trips[trips.ORIGIN_CITY_NAME.str.contains(origin, case=False)].ORIGIN_CITY_NAME.unique()[0]
        dest = trips[trips.DEST_CITY_NAME.str.contains(dest, case=False)].DEST_CITY_NAME.unique()[0]
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

    return origin, dest, dict_regr.predict(input_scaled) 