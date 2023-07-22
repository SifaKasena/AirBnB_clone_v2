#!/usr/bin/python3
"""
This script starts a flask web application listening
on 0.0.0.0, port 5000
Routes:
    - /states_list: displays a list of states in a HTML page
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__, template_folder='templates')


@app.route("/states_list", strict_slashes=False)
def display_states():
    """Displays a HTML page with list of states"""
    states = storage.all()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(self):
    """Teardown ORM session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
