import model
from app import db
import annot

from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir('data/') if isfile(join('data/', f))]

for fname in onlyfiles:

    # check if the file already exist in the db
    # try to get by PK and receive None if it does not exist :
    PDBid = fname.split('.')[0][-4:]
    # ex : filename = pdb1234.pdb
    #         PDBid = 1234

    current_pdb = model.PDBFile.query.get(PDBid)
    if not current_pdb:
        # insert data contains in pdb into db :

        path = join('data/', fname)

        # compute annotation
        current_pdb = model.PDBFile(path)
        dssp_data = model.Annotation(
            pdb_id=current_pdb.id,
            method="dssp",
            result=annot.dsspAnnot(path)
        )
        current_pdb.annotations.append(dssp_data)
        pross_data = model.Annotation(
            pdb_id=current_pdb.id,
            method="pross",
            result=annot.prossAnnot(path)
        )
        current_pdb.annotations.append(pross_data)

        # Add all annotations into db
        db.session.add(current_pdb)
        db.session.commit()
