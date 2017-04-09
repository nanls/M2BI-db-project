class Config(object):

    #-----
    # general configuration :
    DEBUG = False
    TESTING = False

    #-----
    # configuration of Flask-Uploads
    TOP_LEVEL_DIR = '.'
    UPLOADED_PDB_DEST = TOP_LEVEL_DIR + '/up'
    
    # configuration of Flask-SQLAlchemy
    # which db :
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

class ProductionConfig(Config):
    pass #empty because this database will not be really in production on a server

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'

class TestingConfig(Config):
    TESTING = True
