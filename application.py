from flask import Flask
from flask_mongoengine import MongoEngine
from subprocess import call

from settings import MONGODB_HOST

db = MongoEngine()

def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    app.config.update(config_overrides)

    # setup db
    db.init_app(app)

    # import blueprints
    from user.views import user_app
    from distribution.views import distribution_app
    from retail.views import retail_app
    

    # register blueprints
    app.register_blueprint(user_app)
    app.register_blueprint(distribution_app) #api for all dstribution domain
    app.register_blueprint(retail_app)
    

    return app