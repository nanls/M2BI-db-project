import flask
import ramachandran
import annot
import model
from app import app, pdb_set, db
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
        pdb_id = filename[0:4]

        # TODO : check if the file is already in the db

        # if not, insert data into db :
        path = pdb_set.path(filename)
        print (path)#TEMP

        current_pdb = model.PDBFile(path)
        dssp_data = model.Annotation(pdb_id=current_pdb.id, method="dssp", result=annot.dsspAnnot(path))
        pross_data = model.Annotation(pdb_id=current_pdb.id, method="pross", result=annot.prossAnnot(path))
        #add angles PHI & PSI
        angles_data = ramachandran.compute_phi_psi_angles(path, form.angle_unit.data) #TEMP
        #TODO : header+name+length...

        #Add all annotations into db
        db.session.add(dssp_data)
        db.session.add(pross_data)
        db.session.add(angles_data)
        db.session.commit()

        #TODO : move next line into a future display function !!!!!!
        #ramachandran.compute_ramachandran_map(angles, form.angle_unit.data) #TEMP

        return "success"
    return flask.render_template('upload.html', form = form)


def insert(filename, path, form):
    """
    Insertion of computed data into database
    Arguments :
    -----------
    filename : string
        name of the pdb file
    path : string
        path of the file
    form : instance of UploadForm()

    Return :
    --------
    None
    """

    return
