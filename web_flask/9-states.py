#!/usr/bin/python3
"""
    return state from the flask file 
"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states")
def states_list():
    """
    Retrieve a list of states from the storage and render them
    in a template.
    """
    states = storage.all("State").values()
    return render_template("9-states.html", states=states)

@app.route("/states/<id>")
def states_list_id(id):
    """
    list of a state object by a certain id
    """
    all_states = storage.all("State").values()
    state = next((state for state in all_states if state.id == id), None)
    return render_template("9-states.html", states=all_states, id=id, state=state)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the database connection after handling an exception.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)