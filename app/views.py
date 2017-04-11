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


def positionsPrinter(length):
    """
    Create a string containing the position numbers in a way that they will be
    aligned with the sequence.
    ARGUMENT:
        length of the sequence to consider.
    """
    numbers = range(0, 10000, 10)
    numbers[0] = 1
    pos = ""
    for i in xrange((length/10)+1):
        if i == 0:
            pos += "{:<9d}".format(numbers[0])
        else:
            pos += "{:<10d}".format(numbers[i])
    return pos + "\n"


@app.route("/results/<PDBid>")
def resultsForOnePDB(PDBid, unit):
    """
    Define the detailed results route
    """
    pdb = model.PDBFile.query.get(PDBid)
    #boundaries = model.Chain.query.get(PDBid)
    sequence = pdb.seq#[boundaries.start:boundaries]
    pos = positionsPrinter(len(sequence))
    # Get the phi and psi angles and compute the Ramachandran map
    angles = model.Angle.query.get(PDBid)
    ramachandran.compute_ramachandran_map((angles.phi, angles.psi), unit)
    # Get the annotations and stores them in a dictionary
    annot = {}
    annotations = model.Annotation.select(model.Annotation.pdb_id= \
        PDBid).execute().all()
    for meth in annotations:
        annot["{<:7s}".format(annotations["method"])] = annotations["result"]
    return flask.render_template('resultsForOnePDB.html', \
        ramap = "temp/"+PDBid+".png", PDBid = PDBid, \
        PDBsum="http://www.rcsb.org/pdb/explore/explore.do?structureId="+PDBid, \
        positions = pos, sequence = sequence, annotations=annot)
