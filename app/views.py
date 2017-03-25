import flask
import ramachandran
from app import app, pdb_set
from form import UploadForm

@app.route("/")
def index():
    """
    Define the basic route / and its corresponding request handler
    """
    return flask.render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    """
    Define the upload route
    """
    form  = UploadForm()
    if form.validate_on_submit():
        
        filename = pdb_set.save(
            storage = form.pdb_file.data, # The uploaded file to save
        )
        print (filename) 
        path = pdb_set.path(filename)
        print (path)
        angles = ramachandran.compute_phi_psi_angles(path, form.angle_unit.data)
        print(angles)
        ramachandran.compute_ramachandran_map(angles, form.angle_unit.data)
        
        return "success"
    return flask.render_template('upload.html', form = form)
