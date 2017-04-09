"""
Define the forms used in the views.

Forms are defined using FlaskForm class of Flask-WTF module.
They have several fields defined, and a CSRF token hidden field that is created
automatically.
"""
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, RadioField, TextAreaField, DecimalField, IntegerField
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

    angle_unit = RadioField('Angle units', choices=[('degree','degree (default)'),('radian','radian')])

    
class SearchByPDBidForm(FlaskForm):
	"""
	Form for search in database by a PDB ID.
	"""
	PDBid = TextAreaField('PDB ID or list of PDB IDs separated by carriage return')
	submit = SubmitField('Search', render_kw={"class": "btn btn-info btn-lg", "id": "submit-button"})


class SearchFilesForm(FlaskForm):
	"""
	Form for display PDB in database according to resolution and/or 
	criteria.
	"""
	# Resolution?
	resMin = DecimalField('Minimum resolution', places = 2, rounding = None)
	resMax = DecimalField('Maximum resolution', places = 2, rounding = None)
	# Size?
	sizeMin = IntegerField('Minimum size')
	sizeMax = IntegerField('Maximum size')
	submit = SubmitField('Display list of PDB id in database', render_kw={"class": "btn btn-info btn-lg", "id": "submit-button"})


class SearchByKeyWD(FlaskForm):
	"""
	Form for search by keyword in the database.
	"""
	keywd = TextAreaField('Ex: integrin, Homo sapiens...')
	submit = SubmitField('Search', render_kw={"class": "btn btn-info btn-lg", "id": "submit-button"})

