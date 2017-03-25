from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

pdb = UploadSet('pdb', ('pdb') )
configure_uploads(app, pdb)

db = SQLAlchemy(app)
