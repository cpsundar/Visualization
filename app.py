import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/bellybutton.sqlite"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# @app.route("/data")
# def data():
#     """Return the homepage."""
#     data = []
#     return jsonify(data)

@app.route("/names")
def names():
    
    """Return a list of sample names."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    return jsonify(list(df.columns)[2:])

@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    #stmt = db.session.query(Samples).order_by(sample).limit(10).all()
    #stmt = f"db.session.query(Samples).order_by(Samples.{str(sample)}.desc()).limit(10).statement"
    #stmt = db.session.query(Samples).order_by(Samples.str(940).desc()).limit(10).statement
    #stmt = db.session.query(Samples.otu_id, Samples.otu_label, Samples.940).order_by(Samples.940.desc()).limit(10).all()
    #results = db.session.query(Samples).statement
    stmt = db.session.query(Samples).statement
    
    print(f"SQL:{stmt}")
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    # sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]].sort_values(sample,ascending=False).head(10)
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]].sort_values(sample,ascending=False)
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    print(f"sample data:{data}")
    return jsonify(data)


if __name__ == "__main__":
    app.debug = True
    app.run()