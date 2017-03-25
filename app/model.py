"""
Model implementation
"""
from app import db

class PDBFile(db.Model):
    """
    Attributes :
    -----------
    id : 4-character string, primary key
        the 4-character unique identifier of every entry in the Protein Data Bank
    header : varchar
    seq : text
        the corresponding sequence using 1-letter AA code
    resolution : float
    
    
    """
    pdb_id = db.Column(db.String(4), primary_key=True)
    header = db.Column(db.String)
    seq = db.Column(db.Text)
    resolution = db.Column(db.Float)
    
    chains = db.relationship('Chain', backref='pdb', lazy='dynamic')
    annotations = db.relationship('Annotation', backref='pdb', lazy='dynamic')
    angles = db.relationship('Angle', backref='pdb', lazy='dynamic')

    def __init__(self, id, header, seq, resolution):
        """
        constructor of one pdb file : PDBFile

        Arguments :
        ------------
        id : 4-character string
            the 4-character unique identifier of every entry in the Protein Data Bank
        header : string
        seq : text
            the corresponding sequence using 1-letter AA code
        resolution : float
            a measure of the quality of the data that has been collected on
            the crystal containing the protein or nucleic acid
        """
        self.id = id
        self.header = header
        self.seq = seq
        self.resolution = resolution

        
class Chain(db.Model):
    """
    Attributes :
    -----------
    id : 1-character string
    pdb_id : 4-character string
        the 4-character unique identifier of every entry in the Protein Data Bank
    start : integer 
        index of the first chain residue
    stop : integer
        index of the last chain residue (start < stop)
    """
    id = db.Column(db.String(1), primary_key=True)
    pdb_id = db.Column(db.String(4), primary_key=True, db.ForeignKey('pdbfile.id'))
    start = db.Column(db.int)
    stop = db.Column(db.int)
    
    def __init__(self, id, pdb_id, start, stop):
        """
        constructor of one chain instance : Chain
        Arguments :
        ------------
        id : integer
        pdb_id : 4-character string
            the 4-character unique identifier of every entry in the Protein Data Bank
        start : integer 
            index of the first chain residue
        stop : integer
            index of the last chain residue 
            (we assume that start < stop in the PDB file)
        """
        self.id = id
        self.pdb_id = pdb_id
        self.start = start
        self.stop = stop

    
class Annotation(db.Model):
    """
    Attributes :
    -----------
    pdb_id : 4-character string
        the 4-character unique identifier of every entry in the Protein Data Bank
    method : string
        the method used to produce the annotation
    result : string
        the string of annotation
    """
    pdb_id = db.Column(db.String(4),  primary_key=True, db.ForeignKey('pdbfile.id'))
    method = db.Column(db.String, primary_key=True)
    result = db.Column(db.String)
    def __init__(self, pdb_id, method, result):
         """
        constructor of one annotation instance : Annotation
        Arguments :
        ------------
        pdb_id : 4-character string
            the 4-character unique identifier of every entry in the Protein Data Bank
        method : string
            the method used to produce the annotation
        result : string
            the string of annotation
        """
        self.pdb_id = pdb_id
        self.method = method
        self.result = result
        
class Angle(db.Model):
    """
    Attributes :
    ------------
    pdb_id : 4-character string
        the 4-character unique identifier of every entry in the Protein Data Bank
    atom_idx : int
        index of atom following the numerotation of the pdb
    phi : float
        value of the phi angle
    psi : float
        value of the psi angle
    """
    pdb_id = db.Column(db.String(4), primary_key=True, db.ForeignKey('pdbfile.id'))
    atom_idx = db.Column(db.Integer, primary_key=True)
    phi = db.Column(db.Float)
    psi = db.Column(db.Float)

    def __init__(self, pdb_id, atom_idx, phi, psi):
         """
        constructor of one annotation instance : Annotation
        Arguments :
        ------------
        pdb_id : 4-character string
            the 4-character unique identifier of every entry in the Protein Data Bank
        method : string
            the method used to produce the annotation
        result : string
            the string of annotation
        """
        self.pdb_id = pdb_id
        self.method = method
        self.result = result

