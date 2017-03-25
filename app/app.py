from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

pdb_set = UploadSet('pdb', ('pdb') )
configure_uploads(app, pdb_set)

db = SQLAlchemy(app)
