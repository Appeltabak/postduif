import sqlite3
from flask import Flask
from flask import jsonify
from decorator import crossdomain
app = Flask(__name__)

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = os.path.join(_basedir, 'database.db')


def dict_factory(cursor, row):
    """Formats sqlite3 output to JSON"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/api/get_flight/<id>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_flight(id):
    """Fetches flight data from sqlite3 based on flight id
    Args:
        id: the id of the flight.

    Returns:
        One JSON formated data object of a single flight.
        example:
        {
            "begin": "{\"lat\":53.349923,\"lng\":6.6434699}",
            "duif_id": 1,
            "end": "{\"lat\":53.232787,\"lng\":6.5709585}",
            "id": 1,
            "speed": 22,
            "start_time": 0
	}
        Make sure to cast the 'begin' field to a JSON object upon usage in javascript with JSON.parse(str). 
    """
    # relative path to database file.
    con = sqlite3.connect(DATABASE_URI)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT flight.*, duif.speed FROM flight, duif WHERE flight.id = " + str(id) + " AND flight.duif_id = duif.id")
    result = cur.fetchone()
    con.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
