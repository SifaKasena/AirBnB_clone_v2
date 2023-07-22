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


@app.route('/states', strict_slashes=False)
def state():
    """Displays a HTML page with list of states"""
    states = storage.all(State)
    return render_template('9-states.html',
                           states=states,
                           render_for='states_list')


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """
    Displays a HTML page with list of cities under a given state

    Args:
        id: The id of a state to display list of cities
    """
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html',
                                   states=state,
                                   render_for='cities_list')
    return render_template('9-states.html',
                           states=state,
                           render_for='404')


@app.teardown_appcontext
def teardown(self):
    """Teardown ORM session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
