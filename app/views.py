#!/usr/bin/env python
#-*- coding: utf-8 -*-

import flask
import ramachandran
import annot
from app import app, pdb_set, db
from sqlalchemy import func
import model
from form import UploadForm, SearchByPDBidForm, SearchFilesForm, SearchByKeyWD
from sqlalchemy import or_, and_, func

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
        angles = ramachandran.compute_phi_psi_angles(path, form.angle_unit.data) #TEMP
        print(angles) #TEMP
        ramachandran.compute_ramachandran_map(angles, form.angle_unit.data) #TEMP

        insert(filename)

        return "success"
    return flask.render_template('upload.html', form = form)


def positionsPrinter(length):
    """
    Create a string containing the position numbers in a way that they will be
    aligned with the sequence.
    ARGUMENT:
        length of the sequence to consider.
    """
    numbers = range(10, length + 1, 10)
    pos = "{:<9d}".format(1)
    for number in numbers:
        pos += "{:<10d}".format(number)
    return pos + "\n"

@app.route("/results/<string:PDBid>/<string:unit>")
def resultsForOnePDB(PDBid, unit):
    """
    Define the detailed results route
    """
    pdb = model.PDBFile.query.get(PDBid)
    #boundaries = model.Chain.query.get(PDBid)
    sequence = pdb.seq#[boundaries.start:boundaries]
    pos = positionsPrinter(len(sequence))
    # Get the phi and psi angles and compute the Ramachandran map
    angles_phi, angles_psi = zip(*[ (angle.phi, angle.psi) for angle in  pdb.angles.all()])
    # unzip list of tuple of (phi ,psi) for each angle
    print ( angles_phi, angles_psi )

    path = ramachandran.compute_ramachandran_map((angles_phi, angles_psi), unit)
    # Get the annotations and stores them in a dictionary
    annot = {}
    annotations = pdb.annotations
    for meth in annotations:
        annot["{<:7s}".format(annotations["method"])] = annotations["result"]
    return flask.render_template('resultsForOnePDB.html', \
        ramap = path, PDBid = PDBid, \
        PDBsum="http://www.rcsb.org/pdb/explore/explore.do?structureId="+PDBid, \
        positions = pos, sequence = sequence, annotations=annot)


@app.route("/about")
def about():
    """
    Define the about route
    """
    nb_pdbs = db.session.query(func.count(model.PDBFile.id)).scalar()
    print(nb_pdbs)

    num_P = 0
    for annotation in model.Annotation.query.all():
        num_P += annotation.result.count('P')
    print (num_P)

    mean_resol = db.session.query(func.avg(model.PDBFile.resolution)).scalar()
    print(mean_resol)

    mean_len = db.session.query(func.avg(func.length(model.PDBFile.seq))).scalar()
    print(mean_len)


    return flask.render_template('about.html', num_pdb = nb_pdbs,
                                 num_P = num_P, mean_resol = mean_resol,
                                 mean_len = mean_len)

@app.route('/search_by_pdb_id', methods = ['POST'])
def search_by_pdb_id():
    idForm = SearchByPDBidForm()
    print (idForm)
    print (idForm.errors)

    if idForm.validate_on_submit() :
        print ('OKKAYYYYYYYYYYYYYYYYYYYYYY')
        # Creates a list of PDB IDs for which a assignation is wanted
        PDBid_list = idForm.PDBid.data.split()
        PDBfiles_list = [model.PDBFile.query.get(id) for id in PDBid_list if model.PDBFile.query.get(id) is not None]
        if not PDBfiles_list :
            return 'no such pdb was founded, you can upload it'
        elif len(PDBfiles_list)== 1 :
            return 'there is one result'
        else:
            return 'several result -> make searchable array'
    return flask.redirect(flask.url_for("search"), code=302)

@app.route('/search_files', methods = ['POST'])
def search_files():
    filesForm = SearchFilesForm()

    if filesForm.validate_on_submit():
        print (filesForm.resMin.data)

        # User's values retreiving (if any)
        # or default values definitions
        if not filesForm.resMin.data:
            resMin = db.session.query(db.func.min(model.PDBFile.resolution)).scalar()
        else :
            resMin = filesForm.resMin.data

        if not filesForm.resMax.data:
            resMax = db.session.query(db.func.max(model.PDBFile.resolution)).scalar()
        else :
            resMax = filesForm.resMax.data
        print (resMin, resMax)

        if not filesForm.sizeMin.data:
            sizeMin = 15
        else :
            sizeMin = filesForm.sizeMin.data

        if not filesForm.sizeMax.data:
            sizeMax = 10000
        else :
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
        if not PDBfiles_list :
            return 'no such pdb was founded, you can upload it'
        elif len(PDBfiles_list)== 1 :
            return 'there is one result'
        else:
            return 'several result -> make searchable array'

    return flask.redirect(flask.url_for("search"), code=302)

@app.route('/search_by_kw', methods = ['POST'])
def search_by_kw():
    keywdForm = SearchByKeyWD()
    if keywdForm.validate_on_submit():
        keywd = keywdForm.keywd.data
        print(keywd)

        keywds_list = keywd.split()
        # was extracted from header :
        #keywords, name, head,  deposition_date,  release_date, structure_method
        #resolution, structure_reference, journal_reference, author, compound

        PDBfiles_list = []
        for kw in keywds_list :
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

        if not PDBfiles_list :
            return 'no such pdb was founded, you can upload it'
        elif len(PDBfiles_list)== 1 :
            return 'there is one result'
        else:
            return 'several result -> make searchable array'
    return flask.redirect(flask.url_for("search"), code=302)

@app.route('/search', methods = ['GET'])
def search():
    """
    Define the search route.
    """
    idForm = SearchByPDBidForm()
    filesForm = SearchFilesForm()
    keywdForm = SearchByKeyWD()
    return flask.render_template('search.html', SearchByPDBidForm = idForm, SearchFilesForm = filesForm, SearchByKeyWDForm = keywdForm)


def insert(filename):
    """
    Insertion of computed data into database
    Arguments :
    -----------
    filename : string
        name of the pdb file
    Return :
    --------
    None
    """
    #TODO !!!!!!!!!!! add angles PHI & PSI AND header+name+length...
    dssp_data = model.Annotation(pdb_id=filename[-8:-4], method="dssp", result=annot.dsspAnnot(path))
    #filename = "path/3xal.pdb", filename[-8:-4] = "3xal"
    pross_data = model.Annotation(pdb_id=filename[-8:-4], method="pross", result=annot.prossAnnot(path))

    #Add all annotations into db
    db.session.add(dssp_data)
    db.session.add(pross_data)
    db.session.commit()
    return
