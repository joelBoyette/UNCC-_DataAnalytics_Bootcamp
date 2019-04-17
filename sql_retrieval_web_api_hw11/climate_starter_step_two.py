

import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

# # Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # strip date into day,month, year
    date =  [func.strftime("%d", Measurement.date),
            func.strftime("%m", Measurement.date),
            func.strftime("%Y", Measurement.date)]

    # find last date in measurement table 
    last_date = session.query(*date).order_by(Measurement.date.desc()).first()

    #put into day/month/year
    day = int(last_date[0])
    month = int(last_date[1])
    year = int(last_date[2])

    #convert to datetime for timedelta calculation
    last_date_datetime = dt.date(year,month,day)

    #find date 12 months from last date
    beg_date_12_months =  last_date_datetime - dt.timedelta(days=365)
    
    results = session.query(Measurement.date,Measurement.prcp).\
            filter(Measurement.date >= beg_date_12_months).all()
    
    prcp_12month = []
    
    for precipitation in results:
        prcp_12month_dict = {}
        prcp_12month_dict["Date"] = precipitation.date
        prcp_12month_dict["Precipitation"] = precipitation.prcp
        prcp_12month.append(prcp_12month_dict)
    
    return jsonify(prcp_12month)
    

@app.route("/api/v1.0/stations")
def stations():

    # strip date into day,month, year
    date =  [func.strftime("%d", Measurement.date),
            func.strftime("%m", Measurement.date),
            func.strftime("%Y", Measurement.date)]

    # find last date in measurement table 
    last_date = session.query(*date).order_by(Measurement.date.desc()).first()

    #put into day/month/year
    day = int(last_date[0])
    month = int(last_date[1])
    year = int(last_date[2])

    #convert to datetime for timedelta calculation
    last_date_datetime = dt.date(year,month,day)

    #find date 12 months from last date
    beg_date_12_months =  last_date_datetime - dt.timedelta(days=365)

    sel = [Measurement.date, Measurement.station, Station.station, Station.name]
    
    results = session.query(*sel).filter(Measurement.station == Station.station).\
                filter(Measurement.date >= beg_date_12_months).distinct()

    station_list = []
    
    for station in results:
        
        station_dict = {}

        if station not in station_dict:
            
            station_dict["Station"] = station.name
            station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # strip date into day,month, year
    date =   [func.strftime("%d", Measurement.date),
            func.strftime("%m", Measurement.date),
            func.strftime("%Y", Measurement.date)]

    # find last date in measurement table 
    last_date = session.query(*date).order_by(Measurement.date.desc()).first()

    #put into day/month/year
    day = int(last_date[0])
    month = int(last_date[1])
    year = int(last_date[2])

    #convert to datetime for timedelta calculation
    last_date_datetime = dt.date(year,month,day)

    #find date 12 months from last date
    beg_date_12_months =  last_date_datetime - dt.timedelta(days=365)
    
    results = session.query(Measurement.date,Measurement.tobs).\
            filter(Measurement.date >= beg_date_12_months).all()
    
    tobs_12month = []
    
    for item in results:
        tobs_12month_dict = {}
        tobs_12month_dict["Date"] = item.date
        tobs_12month_dict["tobs"] = item.tobs
        tobs_12month.append(tobs_12month_dict)
    
    return jsonify(tobs_12month)

@app.route("/api/v1.0/<start_date>")
def weather_stats_start(start_date):

    results = session.query(func.min(Measurement.tobs).label('min_tobs'),func.avg(Measurement.tobs).label('avg_tobs'),func.max(Measurement.tobs).label('max_tobs')).\
                            filter(Measurement.date >= start_date).all()
    item_list = []

    for item in results:
        item_dict = {}
        item_dict['TMIN'] = item.min_tobs
        item_dict['TAVG'] = item.avg_tobs
        item_dict['TMAX'] = item.max_tobs
        item_list.append(item_dict)


    return jsonify(item_list)


@app.route("/api/v1.0/<start_date>/<end_date>")
def weather_stats_start_end(start_date,end_date):

    results = session.query(func.min(Measurement.tobs).label('min_tobs'),func.avg(Measurement.tobs).label('avg_tobs'),func.max(Measurement.tobs).label('max_tobs')).\
                            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    item_list = []

    for item in results:
        item_dict = {}
        item_dict['TMIN'] = item.min_tobs
        item_dict['TAVG'] = item.avg_tobs
        item_dict['TMAX'] = item.max_tobs
        item_list.append(item_dict)

    return jsonify(item_list)

if __name__ == '__main__':
    app.run(debug=True)
















