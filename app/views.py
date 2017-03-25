import flask

from app import app
from form import UploadForm

@app.route("/")
def index():
    """
    Define the basic route / and its corresponding request handler
    """
    return flask.render_template('index.html')


@app.route("/upload")
def upload():
    """
    Define the upload route
    """
    form  = UploadForm()
    return flask.render_template('upload.html', form = form)
