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


from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurements and stations tables
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Meta = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/names')
def names():
    results = Samples.__table__.columns
    name_list = []
    for result in results:
        name_list.append(result.key)
    name_list.remove('otu_id')
    return jsonify(name_list)


@app.route('/otu')
def otu():
    """List of OTU descriptions."""
    results = session.query(Otu.lowest_taxonomic_unit_found).all()
    otu_list = list(np.ravel(results))
    return jsonify(otu_list)


@app.route('/metadata/<sample>')
def metadata(sample):
    sample = sample.replace("BB_", "")
    result = session.query(Samples_Meta.AGE, Samples_Meta.BBTYPE, Samples_Meta.ETHNICITY, Samples_Meta.GENDER, Samples_Meta.LOCATION, Samples_Meta.SAMPLEID).\
        filter(Samples_Meta.SAMPLEID == sample).one()
    sample_dict = {}
    sample_dict["AGE"] = result[0]
    sample_dict["BBTYPE"] = result[1]
    sample_dict["ETHNICITY"] = result[2]
    sample_dict["GENDER"] = result[3]
    sample_dict["LOCATION"] = result[4]
    sample_dict["SAMPLEID"] = result[5]
    return jsonify(sample_dict) 


@app.route('/wfreq/<sample>')
def wfreq(sample):
    sample = sample.replace("BB_", "")
    result = session.query(Samples_Meta.WFREQ).\
        filter(Samples_Meta.SAMPLEID == sample).one()
    return jsonify(result[0]) 


@app.route('/samples/<sample>')
def samples(sample):
    sample_query = "Samples." + sample
    result = session.query(Samples.otu_id, sample_query).\
        order_by(sample_query + " desc").all()
    otu_ids = [i[0] for i in result]
    sample_values = [i[1] for i in result]
    sample_dict = [{"otu_ids" : otu_ids}, {"sample_values" : sample_values}]
    return jsonify(sample_dict) 


if __name__ == '__main__':
    app.run()