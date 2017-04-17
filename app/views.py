#!/usr/bin/env python
#-*- coding: utf-8 -*-

import flask
import ramachandran
import annot
import model
from app import app, pdb_set, db
from form import UploadForm, SearchByPDBidForm, SearchFilesForm, SearchByKeyWD
from sqlalchemy import or_, and_, func


@app.route("/")
def index():
    """Define the basic route / and its corresponding request handler."""
    return flask.render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    """"Define the upload route."""
    form = UploadForm()
    if form.validate_on_submit():

        # check if the file already exist in the db
        # try to get by PK and receive None if it does not exist :
        PDBid = form.pdb_file.data.filename.split('.')[0][-4:]
        # ex : filename = pdb1234.pdb
        #         PDBid = 1234
        if not model.PDBFile.query.get(PDBid):
            # insert data contains in pdb into db :
            filename = pdb_set.save(storage=form.pdb_file.data)
            # The uploaded file to save

            path = pdb_set.path(filename)

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

        return "success"
    return flask.render_template('upload.html', form=form)


def positionsPrinter(length):
    """Get position numbers aligned with the sequence.

    Parameters
    -----------
    length : int
        length of the sequence that is considered.
    """
    numbers = range(10, length + 1, 10)
    pos = "{:<9d}".format(1)
    for number in numbers:
        pos += "{:<10d}".format(number)
    return pos + "\n"


@app.route("/results/<string:PDBid>/<string:unit>")
def resultsForOnePDB(PDBid, unit):
    """Define the detailed results route.

    Arguments
    ---------
    PDBid : string
        id of a PDB in the dadabase
    unint : string ('degree' or 'radian')
        the unit in which the result have to be computed

    """
    pdb = model.PDBFile.query.get(PDBid)
    # boundaries = model.Chain.query.get(PDBid)
    pos = positionsPrinter(len(pdb.seq))
    ramapaths = ramachandran.compute_ramachandran_map(pdb.id, unit)

    return flask.render_template(
        'resultsForOnePDB.html',
        ramap=ramapaths, PDB=pdb, positions=pos
    )

@app.route("/<path:path>")
def get_file(path):
    """Serve file at the given path.

    Arguments
    ---------
    path : string
        the path where the file is.
        the top level dir is the one of the appliation
    """
    print (path)
    return flask.send_file(path)


@app.route("/about")
def about():
    """Define the about route."""
    nb_pdbs = db.session.query(func.count(model.PDBFile.id)).scalar()

    # count the number of proline in the db
    num_P = 0
    for annotation in model.Annotation.query.all():
        num_P += annotation.result.count('P')

    # compute mean resolution of pdbs in the db
    mean_resol = db.session.query(func.avg(model.PDBFile.resolution)).scalar()

    # compute mean length of protein's sequence contains in the db
    mean_len = db.session.query(func.avg(func.length(model.PDBFile.seq))).scalar()

    return flask.render_template(
        'about.html',
        num_pdb=nb_pdbs, num_P=num_P,
        mean_resol=mean_resol, mean_len=mean_len
    )


@app.route('/search_by_pdb_id', methods=['POST'])
def search_by_pdb_id():
    idForm = SearchByPDBidForm()

    if idForm.validate_on_submit():
        # Creates a list of PDB IDs for which a assignation is wanted
        PDBid_list = idForm.PDBid.data.split()
        PDBfiles_list = [model.PDBFile.query.get(id) for id in PDBid_list if model.PDBFile.query.get(id) is not None]
        if not PDBfiles_list:
            return 'no such pdb was founded, you can upload it'
        elif len(PDBfiles_list) == 1:
            return 'there is one result'
        else:
            colnames, data = searchable_tables(PDBfiles_list)
            return flask.render_template("resultsForSeveralPDB.html",colnames = colnames, rows = data )
    return flask.redirect(flask.url_for("search"), code=302)

def searchable_tables(PDBfiles_list) :
    """
    """
    data = []
    for PDB in PDBfiles_list :
        row = [
            PDB.id,
            PDB.head,
            len(PDB.seq),
            PDB.resolution
        ]
        data.append(row)
    print (data)
    colnames  = ['PDB', 'Title', 'Length', 'Resolution']
    return colnames, data


@app.route('/search_files', methods=['POST'])
def search_files():
    filesForm = SearchFilesForm()

    if filesForm.validate_on_submit():

        # User's values retreiving (if any)
        # or default values definitions
        if not filesForm.resMin.data:
            resMin = db.session.query(db.func.min(model.PDBFile.resolution)).scalar()
        else:
            resMin = filesForm.resMin.data

        if not filesForm.resMax.data:
            resMax = db.session.query(db.func.max(model.PDBFile.resolution)).scalar()
        else:
            resMax = filesForm.resMax.data
        print (resMin, resMax)

        if not filesForm.sizeMin.data:
            sizeMin = 15
        else:
            sizeMin = filesForm.sizeMin.data

        if not filesForm.sizeMax.data:
            sizeMax = 10000
        else:
            sizeMax = filesForm.sizeMax.data
        print (sizeMin, sizeMax)

        # Retrive corresponding pdbs :

        PDBfiles_list = model.PDBFile.query.filter(and_(
            model.PDBFile.resolution >= resMin,
            model.PDBFile.resolution <= resMax,
            func.length(model.PDBFile.seq) >= sizeMin,
            func.length(model.PDBFile.seq) <= sizeMax,
        )).all()
        print (PDBfiles_list)
        if not PDBfiles_list:
            return 'no such pdb was founded, you can upload it'
        elif len(PDBfiles_list) == 1:
            return 'there is one result'
        else:
            colnames, data = searchable_tables(PDBfiles_list)
            return flask.render_template("resultsForSeveralPDB.html",colnames = colnames,  rows = data )

    return flask.redirect(flask.url_for("search"), code=302)


@app.route('/search_by_kw', methods=['POST'])
def search_by_kw():
    keywdForm = SearchByKeyWD()
    if keywdForm.validate_on_submit():
        keywd = keywdForm.keywd.data
        print(keywd)

        keywds_list = keywd.split()
        # was extracted from header :
        # keywords, name, head,  deposition_date,  release_date,
        # structure_method, resolution, structure_reference, journal_reference,
        # author, compound

        PDBfiles_list = []
        for kw in keywds_list:
            PDBfiles_list.extend(
                model.PDBFile.query.filter(or_(
                    model.PDBFile.keywords.contains(kw),
                    model.PDBFile.name.contains(kw),
                    model.PDBFile.head.contains(kw),
                    model.PDBFile.deposition_date.contains(kw),
                    model.PDBFile.release_date.contains(kw),
                    model.PDBFile.structure_method.contains(kw),
                    model.PDBFile.resolution.contains(kw),
                    model.PDBFile.structure_reference.contains(kw),
                    model.PDBFile.journal_reference.contains(kw),
                    model.PDBFile.author.contains(kw),
                    model.PDBFile.compound.contains(kw)
                )).all()
            )
        print (PDBfiles_list)

        if not PDBfiles_list:
            return 'no such pdb was founded, you can upload it'
        elif len(PDBfiles_list) == 1:
            return 'there is one result'
        else:
            colnames, data = searchable_tables(PDBfiles_list)
            return flask.render_template("resultsForSeveralPDB.html",colnames = colnames,  rows = data )

    return flask.redirect(flask.url_for("search"), code=302)


@app.route('/search', methods=['GET'])
def search():
    """Define the search route."""
    idForm = SearchByPDBidForm()
    filesForm = SearchFilesForm()
    keywdForm = SearchByKeyWD()
    return flask.render_template(
        'search.html',
        SearchByPDBidForm=idForm,
        SearchFilesForm=filesForm,
        SearchByKeyWDForm=keywdForm
    )
