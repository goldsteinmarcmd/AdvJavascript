from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
import os
from model import session, Sample, meta, otu_variable

#################################################
# Database Setup
#################################################

dbpath = os.path.join('db', 'belly_button_biodiversity.sqlite')
engine = create_engine(f'sqlite:///{dbpath}')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(engine, reflect=True)
## Save reference to the table
#namedata = Base.classes.dataname
#samples = Base.classes.samples
#print(samples)
# Create our session (link) from Python to the DB
session = Session(engine)
#Session.configure(bind=engine)
from flask import Flask, jsonify, render_template

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")


@app.route('/names')
def names():
    '''Returns a json object containing the trace corresponding to the
        desired data.
        '''

    samples = Sample.__table__.columns._data.keys()[1:]


    return jsonify(samples)


@app.route('/otu')
def otu_func():
    otu_desc = session.query(otu_variable)
    otu_desc = {low.otu_id: low.lowest_taxonomic_unit_found for low in otu_desc}
    return jsonify(otu_desc)

@app.route('/meta/<sample>')
def metadata_func(sample):
#    sample = sample.lstrip('BB_')
    metadata = (session.query(meta).filter(meta.SAMPLEID == sample))
    for result in metadata:
        metadata_dict = {
            'AGE': result.AGE,
            'BBTYPE': result.BBTYPE,
            'ETHNICITY': result.ETHNICITY,
            'GENDER': result.GENDER,
            'LOCATION': result.LOCATION,
            'SAMPLEID': result.SAMPLEID,
}
    return jsonify(metadata_dict)

@app.route('/wfreq/<sample>')
def wfreq_func(sample):
    sample = sample.lstrip('BB_')
    metadata = (session.query(meta).filter(meta.SAMPLEID == sample))
    for result in metadata:
        metadata_dict = {
            'WFREQ': result.WFREQ,
}
    return jsonify(metadata_dict)

@app.route('/samples/<sample>')
def otusamples(sample):
    # query for sample value and otu_id
    sample_query = session.query(Sample.otu_id, getattr(Sample, sample))
    

    # ids and sample values lists
    sample_dict = {
        'otu_ids': [otu_func[0] for otu_func in sample_query],
        'sample_values': [otu_func[1] for otu_func in sample_query]
}

    return jsonify(sample_dict)


if __name__ == '__main__':
    app.run(debug=True)



