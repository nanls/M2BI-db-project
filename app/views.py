import flask
import ramachandran
import annot
from app import app, pdb_set, db
from form import UploadForm
from model import Annotation

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
        dssp = annot.dsspAnnot(path)
        pross = annot.prossAnnot(path)
        angles = ramachandran.compute_phi_psi_angles(path, form.angle_unit.data)
        print(angles)
        ramachandran.compute_ramachandran_map(angles, form.angle_unit.data)
        
        
        def insert(filename, dssp, pross):
            """
            Insertion of computed data into database
            Arguments :
            -----------
            filename : string
                name of the pdb file
            dssp : string
                annotation by dssp method
            pross : string
                annotation by pross method
            
            Return :
            --------
            None
            """
            
            dssp_data = model.Annotation(pdb_id=filename[-8:-4], method="dssp", result=dssp)
            #filename = "path/3xal.pdb", filename[-8:-4] = "3xal"
            pross_data = model.Annotation(pdb_id=filename[-8:-4], method="pross", result=pross)
            
            #Add all annotations into db
            db.session.add(dssp_data)
            db.session.add(pross_data)
            db.session.commit()
            return
        
        return "success"
    return flask.render_template('upload.html', form = form)
