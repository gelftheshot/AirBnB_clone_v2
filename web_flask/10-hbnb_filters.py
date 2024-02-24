#!/usr/bin/python3
"""
Starts A Flask web application
"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/hbnb_filters")
def hbnb_filters():
    """
    Display a HTML page with a list of states and cities
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template(
        "10-hbnb_filters.html",
        states=states,
        amenities=amenities
    )


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the database connection after handling an exception.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
