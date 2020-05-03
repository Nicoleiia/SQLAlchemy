import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>" 
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    one_year = dt.date(2017, 8, 23) - dt.timedelta(365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()

    results = {date: prec for date, prec in precipitation_data}

    return jsonify(results)

@app.route("/api/v1.0/station")
def station():
    
    session = Session(engine)
    
    most_active_stations = session.query(Station.station, func.count(Measurement.station)).\
    filter(Measurement.station == Station.station)
    
    session.close()
    
    stations_dict_list = list(np.ravel(stations_json))
    
    return jsonify(stations_dict_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    temperature_data = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs) ).\
    filter(Measurement.station == top_station).all()
    
    session.close()
    
    tobs_list = list(np.ravel(temperature_data))
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_end_date")
def start_to_end_date():
    
    session = Session(engine)
    
    plotting_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == top_station).\
    filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').all()

    
    start_to_end_list = list(np.ravel(start_to_end_date))
    
    session.close()
    
    start_to_end_data = []
    
    for dte, tmin, tmax, tavg in start_to_end_date:
        ste_dict = {}
        ste_dict["date"] = dte
        ste_dict["min temp"] = tmin
        ste_dict["max temp"] = tmax
        ste_dict["avg temp"] = int(tavg)
        start_to_end_data.append(ste_dict)
        
        return jsonify(start_to_end_list)




if __name__ == '__main__':
    app.run(debug=True)
