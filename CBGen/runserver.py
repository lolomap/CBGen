"""
This script runs the CBGen application using a development server.
"""

from os import environ
from CBGen import app
from waitress import serve

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    serve(app, host=HOST, port=PORT)
    # app.run(HOST, PORT, debug=True)
