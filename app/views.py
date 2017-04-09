import flask
import ramachandran
import annot
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
        dssp = annot.dsspAnnot(path)
        pross = annot.prossAnnot(path)
        angles = ramachandran.compute_phi_psi_angles(path, form.angle_unit.data)
        print(angles)
        ramachandran.compute_ramachandran_map(angles, form.angle_unit.data)
        
        return "success"
    return flask.render_template('upload.html', form = form)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    """
    Define the search route.
    """
    idForm = SearchByPDBidForm()
    filesForm = SearchFilesForm()
    keywdForm = SearchByKeyWD()

    if SearchByPDBidForm.validate_on_submit():
        form = SearchByPDBidForm()
        PDBid = idForm.PDBid.data
        # Creates a list of PDB IDs for which a assignation is wanted
        PDBid = PDBid.split("\n")
        # Lancer sur la page de "résultats lors d’une requête issue de 
        # l’interrogation" (pas encore créée)
    elif SearchFilesForm.validate_on_submit():
        form = SearchFilesForm()
        # Default values definitions
        resMin = 0.0
        resMax = 10000.0
        sizeMin = 15
        sizeMax = 10000
        # User's values retreiving (if any)
        if filesForm.resMin.data != "":
            resMin = filesForm.resMin.data
        if filesForm.resMax.data != "":
            resMax = filesForm.resMax.data
        if filesForm.sizeMin.data != "":
            sizeMin = filesForm.sizeMin.data
        if filesForm.sizeMax.data != "":
            sizeMax = filesForm.sizeMin.data
        # Lancer sur la page de "résultats lors d’une requête issue de 
        # l’interrogation" (pas encore créée)
    elif SearchByKeyWD.validate_on_submit():
        form = SearchByKeyWD()
        keywd = keywdForm.keywd.data
    return flask.render_template('search.html', form = form)


