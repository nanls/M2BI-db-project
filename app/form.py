"""
Define the forms used in the views.

Forms are defined using FlaskForm class of Flask-WTF module.
They have several fields defined, and a CSRF token hidden field that is created
automatically.
"""
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

import app


class UploadForm(FlaskForm):
    """
    Form for pdb upload.
    """
    pdb_file = FileField('PDB file', validators=[
        FileRequired(),
        FileAllowed( app.pdb_set, '.pdb and .ent only!')
    ])
    
    
    submit = SubmitField('Upload file', render_kw={"class": "btn btn-info btn-lg", "id": "submit-button"})

    
