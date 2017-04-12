#!/usr/bin/env python
#-*- coding: utf-8 -*-

import flask
import ramachandran
import annot
import model
from app import app, pdb_set, db
from sqlalchemy import func
import model
from form import UploadForm, SearchByPDBidForm, SearchFilesForm, SearchByKeyWD


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

        # check if the file already exist in the db
        check_pdb = db.session.query(model.PDBFile).filter(model.PDBFile.id==form.pdb_file.data.filename[0:4])
        check_bool = db.session.query(check_pdb.exists()).scalar()

        # insert data contains in pdb into db :
        if not check_bool:
            filename = pdb_set.save(storage = form.pdb_file.data,) # The uploaded file to save
  
            path = pdb_set.path(filename)

            # compute annotation
            current_pdb = model.PDBFile(path)
            dssp_data = model.Annotation(pdb_id=current_pdb.id, method="dssp", result=annot.dsspAnnot(path))
            current_pdb.annotations.append(dssp_data)
            pross_data = model.Annotation(pdb_id=current_pdb.id, method="pross", result=annot.prossAnnot(path))
            current_pdb.annotations.append(pross_data)

            #add all annotations into db
            db.session.add(current_pdb)
            db.session.commit()

        return "success"
    return flask.render_template('upload.html', form = form)


@app.route("/about")
def about():
    """
    Define the about route
    """
    nb_pdbs = db.session.query(func.count(model.PDBFile.id)).scalar()

    # count the number of proline in the db
    num_P = 0
    for annotation in model.Annotation.query.all():
        num_P += annotation.result.count('P')

    # compute mean resolution of pdbs in the db
    mean_resol = db.session.query(func.avg(model.PDBFile.resolution)).scalar()

    # compute mean length of protein's sequence contains in the db
    mean_len = db.session.query(func.avg(func.length(model.PDBFile.seq))).scalar()


    return flask.render_template('about.html', num_pdb = nb_pdbs,
                                 num_P = num_P, mean_resol = mean_resol,
                                 mean_len = mean_len)

@app.route('/search_by_pdb_id', methods = ['POST'])
def search_by_pdb_id():
    idForm = SearchByPDBidForm()

    if idForm.validate_on_submit() :
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
        # Lancer sur la page de "resultats lors d’une requete issue de
        # l’interrogation" (pas encore creee)

        # l’interrogation" (pas encore creee)
        return 'succes search_files'
    return flask.redirect(flask.url_for("search"), code=302)

@app.route('/search_by_kw', methods = ['POST'])
def search_by_kw():
    keywdForm = SearchByKeyWD()
    if keywdForm.validate_on_submit():
        keywd = keywdForm.keywd.data
        return 'success search_by_kw'
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
