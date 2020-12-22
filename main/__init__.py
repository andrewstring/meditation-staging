from flask import Flask
from main.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#app initialization
app = Flask(__name__)
app.config.from_object(Config)

#db initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

from main import routes, models