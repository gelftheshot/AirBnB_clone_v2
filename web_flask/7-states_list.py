#!/usr/bin/python3
"""
Starts A Flask web application
"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states_list")
def states_list():
    """
    Retrieve a list of states from the storage and render them
    in a template.
    """
    states = storage.all("State").values()
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(self):
    """
    Closes the database connection.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
