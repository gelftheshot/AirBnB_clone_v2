#!/usr/bin/python3
"""
    intoducing a python flask with greating
"""

from flask import Flask, abort
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """
    Returns a greeting message.
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def just_hbnb():
    """
    return only hbnb
    """
    return "HBNB"


@app.route("/c/<text>")
def c_is_fun(text):
    """
    return c is <text>
    """
    return "C {}".format(text.replace("_", " "))


@app.route("/python")
@app.route("/python/")
@app.route("/python/<text>")
def python_is_cool(text="is cool"):
    """
    return python
    """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<n>")
def is_number(n):
    """
    return if number
    """
    if n.isdigit() or isinstance(n, int):
        return "{} is a number".format(n)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
