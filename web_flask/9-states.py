#!/usr/bin/python3
"""
Starts A Flask web application
"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states")
def states():
    """
    Retrieve all states from storage and render them in the template.
    """
    states = storage.all("State").values()
    return render_template("9-states.html", state=states)


@app.route("/states/<id>")
def states_id(id):
    """
    Retrieve a state by its ID and render the corresponding template.
    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the database connection after handling an exception.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
