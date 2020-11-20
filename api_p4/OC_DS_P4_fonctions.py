import pandas as pd 
import numpy as np # linear algebra
import datetime 

def from_hdays(date=datetime.date.today()): 
    res = []
    for d in FERIES: 
        delta = abs(date - datetime.datetime.strptime(d,'%Y-%m-%d').date() ) 
        res.append(delta.days )
    return min(res) 
    
def delay_estimation(dt_flight="2016-04-10", origin='San Fancisco', dest='Los Angeles', h_dep=10): 

    input =  []
    d_flight = datetime.datetime.strptime(dt_flight, '%Y-%m-%d').date() 

    try:
        origin = trips[trips.ORIGIN_CITY_NAME.str.contains(origin, case=False)].ORIGIN_CITY_NAME.unique()[0]
        dest = trips[trips.DEST_CITY_NAME.str.contains(dest, case=False)].DEST_CITY_NAME.unique()[0]
        group =  trips[(trips.ORIGIN_CITY_NAME == origin) & (trips.DEST_CITY_NAME == dest)].DISTANCE_GROUP.values[0]
    except IndexError: 
         print("Pas de prédiction possible entre", origin.split(',')[0], "et", dest.split(',')[0] )
         return

    input.append(d_flight.month) 
    input.append(CITY_lbl.transform([origin])[0]) 
    input.append(group) #DISTANCE_GROUP 
    input.append(BLK_lbl.transform(list([dict_horaires.get(h_dep, "0001-0559")]))[0]) 
    input.append(abs(from_hdays(d_flight)))  
    input.append(d_flight.weekday()+1) 
    input.append(CITY_lbl.transform([dest])[0]) 
    
    return origin, dest, len(input), dict_regr[len(input)][2].predict([input]) #'{:.0f}'.format(dict_regr[len(input)][2].predict([input])[0]) 