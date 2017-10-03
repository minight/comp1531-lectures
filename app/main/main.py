from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import SQLAlchemyAdapter, UserManager

class ConfigClass(object):
    SECRET_KEY = 'lawekjgnaiowuhgiozxcljhialowuhto29y5hiouhkln'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.sqlite'
    DEBUG = True
    USER_ENABLE_EMAIL              = False
    USER_ENABLE_RETYPE_PASSWORD    = False


db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

db.init_app(app)

from . import models

with app.app_context():
    db.create_all()

db_adapter = SQLAlchemyAdapter(db, models.models.User)        # Register the User model
user_manager = UserManager(db_adapter, app,
                           password_validator=lambda x,y: None)

#  from .basic import app as basic_bp
#  app.register_blueprint(basic_bp)

from .users import app as users_bp
app.register_blueprint(users_bp)
