"""
Model implementation
"""
from app import db

class PDBFile(db.Model):
    """
    Attributes :
    -----------
    pdb_id : 4-character string
        the 4-character unique identifier of every entry in the Protein Data Bank
    seq : string
        the corresponding sequence using 1-letter AA code
    resolution : float
        a measure of the quality of the data that has been collected on
        the crystal containing the protein or nucleic acid
    """
    pdb_id = db.Column(db.String(4), primary_key=True)
    seq = db.Column(db.Text)
    resolution = db.Column(db.Float)
