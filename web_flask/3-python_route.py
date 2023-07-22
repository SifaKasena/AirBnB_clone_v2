#!/usr/bin/python3
"""
This script starts a flask web application listening
on 0.0.0.0, port 5000
Routes:
    - /: display “Hello HBNB!”
    - /hbnb: display “HBNB”
    - /c/<text>: display “C ” followed by the value of
                 the text variable
                 (replace underscore _ symbols with a space)
    - /python/(<text>): display “Python ”, followed by
                        the value of the text variable
                        (replace underscore _ symbols with a space)
                        The default value of text is “is cool”
"""

from flask import Flask


app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """Return Hello HBNB!"""
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return HBNB"""
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """
    Returns C followed by <text>

    Args:
        text: The parameter passed by user in the URL
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text):
    """
    Returns Python followed by <text>

    Args:
        text: The parameter passed by user in the URL
    """
    return "Python {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
