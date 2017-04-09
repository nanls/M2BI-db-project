"""
Model implementation
"""
from app import db
from Bio import PDB

class PDBFile(db.Model):
    """
    Attributes :
    -----------
    id : 4-character string, primary key
        the 4-character unique identifier of every entry in the Protein Data Bank
    seq : text
        the corresponding sequence using 1-letter AA code

    keywords : string

    name : string

    head : string

    deposition_date : string

    release_date : string

    structure_method : string

    resolution : float
        a measure of the quality of the data that has been collected on
        the crystal containing the protein or nucleic acid
    structure_reference : string
        list of references
    journal_reference : string

    author : string

    compound : string
        various information about the crystallized compound
    """
    id = db.Column(db.String(4), primary_key=True)
    seq = db.Column(db.Text)

    resolution = db.Column(db.Text)
    keywords = db.Column(db.Text)
    name = db.Column(db.Text)
    head = db.Column(db.Text)
    deposition_date = db.Column(db.Text)
    release_date = db.Column(db.Text)
    structure_method = db.Column(db.Text)
    resolution = db.Column(db.Float)
    structure_reference = db.Column(db.Text)
    journal_reference = db.Column(db.Text)
    author = db.Column(db.Text)
    compound  = db.Column(db.Text)



    chains = db.relationship('Chain', backref='pdb', lazy='dynamic')
    annotations = db.relationship('Annotation', backref='pdb', lazy='dynamic')
    angles = db.relationship('Angle', backref='pdb', lazy='dynamic')

    def __init__(self, filepath):
        """
        constructor of one pdb file : PDBFile

        Argument :
        ------------
        filepath : string
            path to the pdb file
        """


        #-----
        # init parser :
        parser = PDB.PDBParser()
        struct = parser.get_structure("", filepath)

        #-----
        # extract from header :
        self.keywords = struct.header['keywords']
        self.name = struct.header['name']
        self.head = struct.header['head']
        self.deposition_date = struct.header['deposition_date']
        self.release_date = struct.header['release_date']
        self.structure_method = struct.header['structure_method']
        self.resolution = struct.header['resolution']
        self.structure_reference = struct.header['structure_reference']
        self.journal_reference = struct.header['journal_reference']
        self.author = struct.header['author']
        self.compound = struct.header['compound']

        #-----
        # Get the sequence and the angles

        # extract all polypeptides from the structure :
        ppb = PDB.CaPPBuilder()

        #The sequence of each polypeptide can then easily be obtained from the Polypeptide objects :
        for pp in ppb.build_peptides(struct):
            print (pp)

            seq = pp.get_sequence()
            # The sequence is represented as a Biopython Seq object,
            # and its alphabet is defined by a ProteinAlphabet object.
            print (seq)

            # Get the boundary of the peptide
            # using residu id
            # A residue id is a tuple with three elements:
            # - The hetero-flag
            # - *The sequence identifier in the chain*
            # - The insertion code,
            start = pp[0].get_id()[1]
            print (start)
            end = pp[-1].get_id()[1]
            print (end)


            # Get phi psi angle
            angles = pp.get_phi_psi_list()
            # Some are None because :
            # - Some atoms are missing
            #   -> Phi/Psi cannot be calculated for some residue
            # - No phi for residue 0
            # - No psi for last residue
            print(angles)

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
    pdb_id = db.Column(db.String(4), db.ForeignKey('pdb_file.id'), primary_key=True,)
    start = db.Column(db.Integer())
    stop = db.Column(db.Integer())

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
    pdb_id = db.Column(db.String(4), db.ForeignKey('pdb_file.id'), primary_key=True)
    method = db.Column(db.String, primary_key=True)
    result = db.Column(db.Text)
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
    pdb_id = db.Column(db.String(4), db.ForeignKey('pdb_file.id'), primary_key=True)
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
