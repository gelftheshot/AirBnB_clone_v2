#!/usr/bin/python3
"""
Starts A Flask web application
"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states", defaults={"id": None})
@app.route("/states/<id>")
def states(id):
    """
    Retrieve all states from storage or a specific state by id
    and render them in the template.
    """
    states = storage.all("State")
    if id:
        state = states.get(id)
        return render_template("9-states.html", state=state)
    else:
        return render_template("9-states.html", state=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the database connection after handling an exception.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
