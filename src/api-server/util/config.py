import os

# uncomment the line below for mongo database url from environment variable
# mongo_base = os.environ['DATABASE_URL']

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'JWT_CONSTRUCTION_SECRET_KEY_HERE!!!')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'mongod:///'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'mongod:///'
    

class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use mongo in prod
    # DATABASE_URI = mongo_base


config_env = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY