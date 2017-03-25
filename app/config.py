class Config(object):

    #-----
    # general configuration :
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'

class TestingConfig(Config):
    TESTING = True
