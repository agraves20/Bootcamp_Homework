import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, inspect, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
Base = declarative_base()
import pandas as pd
from warnings import filterwarnings
import pymysql
filterwarnings('ignore', category=pymysql.Warning)
import os
from dateutil import parser
from datetime import datetime 
import datetime as dt
import time
import dateutil
import argparse
import numpy as np


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///new_database.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurements and stations tables
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)


def valid_date(date):
    try:
        return dt.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: " + date
        raise argparse.ArgumentTypeError(msg)

def calc_temps(start_date, end_date):
    start_date = valid_date(start_date)
    end_date = valid_date(end_date)

    temps = session.query(Measurements.tobs).\
    filter(Measurements.date >= start_date).\
    filter(Measurements.date <= end_date)

    df4 = pd.read_sql_query(temps.statement, temps.session.bind)
    return df4.describe()

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

        f"/api/v1.0/precipitation - List of Date/Precipitation for Last Year<br/>"

        f"/api/v1.0/stations - List of Stations<br/>"

        f"/api/v1.0/tobs- List of Temp Observations for Last Year<br/>"

        f"/api/v1.0/tempstats/<start> and /api/v1.0/tempstats/<start>/<end> - Temp Info for Requested Timeframe<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation for the last year."""

    results = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date > dt.date(2016, 8, 23)).all()
    # Convert list of tuples into normal list

    precipitation_list = []
    for result in results:
        row = {}
        row["date"] = results[0]
        row["prcp"] = results[1]
        precipitation_list.append(row)

    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Stations.station).all()

    station_list = list(np.ravel(results))
    return jsonify(station_list)
    
@app.route("/api/v1.0/tobs")
def temperature():
    """Return a list of temperature observations for the last year."""

    results = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date > dt.date(2016, 8, 23)).all()
    # Convert list of tuples into normal list
    temperature_list = []
    for result in results:
        row = {}
        row["date"] = results[0]
        row["tobs"] = results[1]
        temperature_list.append(row)

    return jsonify(temperature_list) 


@app.route("/api/v1.0/tempstats/<start>")
@app.route("/api/v1.0/tempstats/<start>/<end>")
def tempstats(start, end = dt.datetime.now().strftime("%Y-%m-%d")):
    #start = valid_date(start)
    #end = valid_date(end)

    data = calc_temps(start, end)

    results = {}
    results["min"] = data['tobs']['min']
    results["max"] = data['tobs']['max']
    results["avg"] = data['tobs']['mean']

    return jsonify(results)


if __name__ == '__main__':
    app.run()