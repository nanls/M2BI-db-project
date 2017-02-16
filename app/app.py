from flask import Flask
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
pdb = UploadSet('pdb', ('pdb') )
configure_uploads(app, pdb)
