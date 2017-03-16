#!/usr/bin/env python

from argparse import ArgumentParser
import os
import os.path


def is_valid_file(parser, arg):
    """ Check if arg filename is readable
    
    Arguments :
    -----------
    parser : instance of argparse.ArgumentParser
    
    arg : string 
        filename
    
    Return : 
    --------
    an open file handler
    """
    
    if os.path.isfile(arg) and os.access(arg, os.R_OK):
        print("File {0} exists and is readable".format (arg) ) 
        return open(arg, 'r')  # return an open file handle
    else:
        parser.error("Either file is missing or is not readable")
    


parser = ArgumentParser(description="fetch PDBs files using a PICSES list")
parser.add_argument("-l", 
    dest="filename", required=True,
    help="""input file PDB list. The first line is a header. 
    Then, for each line, the fourth characters are PDB ids.""", 
    metavar="FILE",
    type=lambda x: is_valid_file(parser, x)
)
args = parser.parse_args()

with args.filename as f : 
    for line in f : 
        print (line) 
