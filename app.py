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
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/(start)/(end)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert list of tuples into normal list
    prcps = []
    for x, y in results:
        prcps_dict = {}
        prcps_dict["date"] = x
        prcps_dict["prcp"] = y
        prcps.append(prcps_dict)

    return jsonify(prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    stts = []
    for x, y in results:
        stts_dict = {}
        stts_dict["station"] = x
        stts_dict["name"] = y
        stts.append(stts_dict)

    return jsonify(stts)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = last[0].split("-")
    yearago = dt.datetime(int(date[0]), int(date[1]), int(date[2])) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= yearago).order_by(Measurement.date).all()

    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    ttobs = []
    for x, y in results:
        ttobs_dict = {}
        ttobs_dict["date"] = x
        ttobs_dict["tobs"] = y
        ttobs.append(ttobs_dict)

    return jsonify(ttobs)

@app.route("/api/v1.0/<start>")
def minmax(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(func.max(Measurement.tobs),func.avg(Measurement.tobs),func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    st = start.split("-")
    try:
        newDate = dt.datetime(int(st[0]),int(st[1]),int(st[2]))
    except:
        return("Invalid Date")

    # Create a dictionary from the row data and append to a list of all_passengers
    table = []
    for x, y, z in results:
        qdict = {}
        qdict["min"] = x
        qdict["avg"] = y
        qdict["max"] = z
        table.append(qdict)

    return jsonify(table)

@app.route("/api/v1.0/<start>/<end>")
def minmaxend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(func.max(Measurement.tobs),func.avg(Measurement.tobs),func.min(Measurement.tobs)).filter((Measurement.date >= start) & (Measurement.date <= end)).all()
    
    session.close()

    st = start.split("-")
    st2 = end.split("-")
    try:
        newDate = dt.datetime(int(st[0]),int(st[1]),int(st[2]))
        newDate = dt.datetime(int(st2[0]),int(st2[1]),int(st2[2]))
    except:
        return("Invalid Date")

    # Create a dictionary from the row data and append to a list of all_passengers
    table = []
    for x, y, z in results:
        qdict = {}
        qdict["min"] = x
        qdict["avg"] = y
        qdict["max"] = z
        table.append(qdict)

    return jsonify(table)
if __name__ == '__main__':
    app.run(debug=True)