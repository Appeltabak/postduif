import sqlite3
from flask import Flask
from flask import jsonify
from decorator import crossdomain
app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/")
def hello():
	return "data"

@app.route("/api/get_flight/<id>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_flight(id):
	con = sqlite3.connect("database.db")
	con.row_factory = dict_factory
	cur = con.cursor()
	cur.execute("SELECT * FROM flight WHERE id = " + str(id))
	result = cur.fetchone()
	con.close()
	return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)