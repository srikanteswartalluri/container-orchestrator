# flask packages
from flask import Flask, app
from flask_restful import Api
from flask_mongoengine import MongoEngine

# custom imports
from util.routes import create_routes

# default mongodb configuration
default_config = {'MONGODB_SETTINGS': {
    'db': 'co_db',
    'host': 'co_repo',
    'port': 27017,
    'username': 'root',
    'password': 'root123',
    'authentication_source': 'admin'}}


def intialise_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    :param config: Configuration dictionary
    :return: app
    """
    # init flask
    app_instance = Flask(__name__)

    # configure app
    config = default_config if config is None else config
    app_instance.config.update(config)
    #app_instance.config.from_object(config_env[env])

    # init api and routes
    api = Api(app=app_instance)
    create_routes(api=api)

    # init mongoengine
    db = MongoEngine(app=app_instance)

    return app_instance


if __name__ == '__main__':
    # Main entry point when run in stand-alone mode. Ignore this in case of 'flask run'
    app = intialise_app()
    app.run(debug=True)