class Config(object):

    #-----
    # general configuration :
    DEBUG = False
    TESTING = False

    #-----
    # configuration of Flask-Uploads
    TOP_LEVEL_DIR = '.'
    UPLOADED_PDB_DEST = TOP_LEVEL_DIR + '/up'
    
    # configaration of Flask-SQLAlchemy
    # which db :
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'

class TestingConfig(Config):
    TESTING = True
