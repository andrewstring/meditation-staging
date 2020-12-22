from main import app

from main.routes import *

if __name__== "__main__":
    app.run(threaded=True, port=5000)