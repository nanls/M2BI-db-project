#!/usr/bin/env python

from argparse import ArgumentParser
import os

import Bio.PDB


def is_valid_file(parser, arg):
    """Check if arg filename is readable.

    Arguments :
    -----------
    parser : instance of argparse.ArgumentParser

    arg : string
        filename

    Return :
    --------
    an open file handler
    """
    # https://docs.python.org/3/library/os.html#os.access
    # if it's a file and it's readable :
    if os.path.isfile(arg) and os.access(arg, os.R_OK):
        print("File {0} exists and is readable".format(arg))
        return open(arg, 'r')  # return an open file handle
    else:
        parser.error("Either file is missing or is not readable")


parser = ArgumentParser(description="fetch PDBs files using a PICSES list")
parser.add_argument(
    "-l",
    dest="filename", required=True,
    help="""input file PDB list. The first line is a header.
    Then, for each line, the fourth characters are PDB ids.""",
    metavar="FILE",
    type=lambda x: is_valid_file(parser, x)
)
args = parser.parse_args()


pdbl = Bio.PDB.PDBList()

with args.filename as f:
    next(f)  # Do not take header into account
    for line in f:
        pdb_id = line[:4]
        print (pdb_id)
        try:
            # try retrieving the file the normal way :
            pdbl.retrieve_pdb_file(pdb_id, pdir='data', file_format='pdb')
        except IOError:
            try:
                # try retrieving the file as obsolete :
                pdbl.retrieve_pdb_file(pdb_id, pdir='data', obsolete=True)
            except IOError:
                # the file couldn't be fetched at all :
                print("the file couldn't be fetched at all.")
