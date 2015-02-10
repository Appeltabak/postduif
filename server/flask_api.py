import sqlite3
from flask import Flask
from flask import jsonify
from flask import request
from decorator import crossdomain
from math import radians, cos, sin, asin, sqrt
import ast
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
           (NOPE)
        Make sure to cast the 'begin' field to a JSON object upon usage in javascript with JSON.parse(str). 
    """
    # relative path to database file.
    con = sqlite3.connect(DATABASE_URI)
    cur = con.cursor()
    cur.execute("SELECT flight.*, duif.speed FROM flight, duif WHERE flight.id = " + str(id) + " AND flight.duif_id = duif.id")
    result = cur.fetchone()
    con.close()
    return jsonify(result)

@app.route("/api/send_msg", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def send_msg():
    """
    Adds message in database.
    Required fields:
        duif_id
        start_time
        msg
        receiver_id
        sender_id
        sealed
    test url: 127.0.0.1:5000/api/send_msg?duif_id=1&start_time=1423524808&msg=test%20bericht&receiver_id=1&sender_id=2&sealed=1
    Not working because the return is in a json format which is dum.
    :return:

    """
    print(request.args)
    if request.args.get('duif_id') is None or request.args.get('start_time') is None or request.args.get('msg') is None or \
            request.args.get('receiver_id') is None or request.args.get('sender_id') is None or \
            request.args.get('sealed') is None:
        return "Error: must provide all fields"
    con = sqlite3.connect(DATABASE_URI)
    #con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT loc FROM user WHERE id = " + request.args.get("receiver_id"))
    latlng_rec = str(cur.fetchone()[0]).split(";")
    cur.execute("SELECT loc FROM user WHERE id = " + request.args.get("sender_id"))
    latlng_send = str(cur.fetchone()[0]).split(';')
    distance = haversine(float(latlng_rec[1]), float(latlng_rec[0]), float(latlng_send[1]), float(latlng_send[0]))
    cur.execute("SELECT speed FROM duif WHERE id = " + request.args.get("duif_id"))
    speed = cur.fetchone()[0]
    time = distance / speed
    end_time = int(request.args.get("start_time")) + time
    print(round(end_time))
    cur.execute("INSERT INTO flight (start_time, end_time, duif_id, msg_id) " +
                "VALUES (" + str(request.args.get('start_time')) + ", " + str(end_time) + ", " + str(request.args.get("duif_id")) + ", " + str(0) + ")")
    con.close()
    return "no errors"

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters. Use 3956 for miles
    return c * r

if __name__ == "__main__":
    app.run(debug=True)
