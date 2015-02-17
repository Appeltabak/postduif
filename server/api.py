import sqlite3

from flask import jsonify
from flask import request

from decorator import crossdomain
from controllers import haversine, dict_factory
from . import app


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
              "duif_id": 1,
              "end_time": 1423525314,
              "id": 3,
              "msg_id": 1,
              "receiver_loc": "53.349923;6.6434699",
              "sender_loc": "53.449983;6.6414699",
              "speed": 22,
              "start_time": 1423524808
            }
        receiver_loc and sender_loc can be split width a ';' separator
    """
    # relative path to database file.
    con = sqlite3.connect(app.config['DATABASE_URI'])
    cur = con.cursor()
    cur.row_factory = dict_factory
    cur.execute("SELECT flight.*, duif.speed, receiver.loc AS receiver_loc, sender.loc AS sender_loc "
                "FROM flight "
                "LEFT JOIN duif ON flight.duif_id = duif.id "
                "LEFT JOIN message ON flight.msg_id = message.id "
                "LEFT JOIN user AS receiver ON message.receiver_id = receiver.id "
                "LEFT JOIN user AS sender ON message.sender_id = sender.id "
                "WHERE flight.id = " + id)
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
    test url:
    127.0.0.1:5000/api/send_msg?duif_id=1&start_time=1423524808&msg=test%20bericht&receiver_id=1&sender_id=2&sealed=1

    :return:

    """
    if request.args.get('duif_id') is None or request.args.get('start_time') is None or request.args.get('msg') is None or \
            request.args.get('receiver_id') is None or request.args.get('sender_id') is None or \
            request.args.get('sealed') is None:
        return "Error: must provide all fields"

    # establish connection
    con = sqlite3.connect(app.config['DATABASE_URI'])
    cur = con.cursor()

    # get all variables for the end_time calculation
    cur.execute("SELECT loc FROM user WHERE id = " + request.args.get("receiver_id"))
    latlng_rec = str(cur.fetchone()[0]).split(";")  # array width the receiver location
    cur.execute("SELECT loc FROM user WHERE id = " + request.args.get("sender_id"))
    latlng_send = str(cur.fetchone()[0]).split(';')  # array width the sender location
    distance = haversine(float(latlng_rec[1]), float(latlng_rec[0]), float(latlng_send[1]), float(latlng_send[0]))
    cur.execute("SELECT speed FROM duif WHERE id = " + request.args.get("duif_id"))
    speed = cur.fetchone()[0]
    time = distance / speed
    end_time = round(int(request.args.get("start_time")) + time)

    # insert message into database
    cur.execute("INSERT INTO message (msg, receiver_id, sender_id, sealed, status)" +
                "VALUES ('" + str(request.args.get('msg')) + "', " + str(request.args.get('receiver_id')) + ", " +
                str(request.args.get('sender_id')) + ", " + str(request.args.get('sealed')) + ", " + str("0") + ")")
    con.commit()  # commit the message

    # insert flight into database. Get message id from con.lastrowid
    cur.execute("INSERT INTO flight (start_time, end_time, duif_id, msg_id) " +
                "VALUES (" + str(request.args.get('start_time')) + ", " + str(end_time) + ", " +
                str(request.args.get("duif_id")) + ", " + str(cur.lastrowid) + ")")
    con.commit()  # commit the flight

    con.close()

    return "1"


# if __name__ == "__main__":
#     app.run(debug=True)
