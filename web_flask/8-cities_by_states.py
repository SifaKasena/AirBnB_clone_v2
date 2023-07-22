#!/usr/bin/python3
"""
This script starts a flask web application listening
on 0.0.0.0, port 5000
Routes:
    - /cities_by_states: displays a list of cities by states in a HTML page
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__, template_folder='templates')


@app.route("/cities_by_states", strict_slashes=False)
def display_states():
    """Displays a HTML page with list of cities by states"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(self):
    """Teardown ORM session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
