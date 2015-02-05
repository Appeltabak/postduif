import sqlite3
from flask import Flask
from flask import jsonify
from decorator import crossdomain
app = Flask(__name__)

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
          "begin_lat": 53.232787,
          "begin_long": 6.5709585,
          "end_lat": 53,
          "end_long": 6,
          "id": 1,
          "speed": 22,
          "start_time": 1422917121
        }
	"""
	con = sqlite3.connect("database.db") #relative path to database file.
	con.row_factory = dict_factory
	cur = con.cursor()
	cur.execute("SELECT * FROM flight WHERE id = " + str(id))
	result = cur.fetchone()
	con.close()
	return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)