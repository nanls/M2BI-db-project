#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


def dsspAnnot(pdb):
    """Retrieve the annotation made by DSSPPII.

    Parameters
    ----------
        pdb: string
            the name of the pdb file.

    Returns
    -------
    string :
        a string containing the corresponding annotation for every
        residue contained in the pdb file.
        Annotation can be: H, B, E, G, I, T, S, P, " "
        with:
            H: alpha helix
            B: bridge
            E: extended (beta sheet)
            G: 3-10 helix
            I: pi helix
            T: turn
            S: bend (high curvature region)
            P: PPII
            " ": coil
    """
    pdb_id = pdb[-8:-4]
    # example: if pdb = 'doc/truc/4dmi.pdb' ==> pdb[-8:-4] = '4dmi'
    os.system("perl tools/DSSPPII/dssppII.pl "+pdb+" > temp/"+pdb_id+".dssp")
    flag = 0
    annot = ""
    with open("temp/"+pdb_id+".dssp", "r") as filin:
        for line in filin:
            if line[0:3] == "  #":
                flag = 1
            elif flag == 1:
                annot += line[16]
        print(annot)
    os.system("rm temp/"+pdb_id+".dssp")
    return(annot)


def prossAnnot(pdb):
    """Retrieve the annotation made by PROSS.

    Parameters
    ----------
        pdb: string
        the name of the pdb file.

    Returns
    -------
    string :
        a string containing the corresponding annotation for every
        residue contained in the pdb file.
        Annotation can be: H, E, T, P, -
        with:
        E: beta sheet
        T: turn
        H: helix
        P: polyproline
        -: coil
    """
    pdb_id = pdb[-8:-4]
    # example: if pdb = 'doc/truc/4dmi.pdb' ==> pdb[-8:-4] = '4dmi'
    # .pross file is the PROSS.py output, .pross2 file is the
    # extract_PROSSSEQ2D.pl output
    os.system("tools/PROSS/PROSS.py " + pdb + " > temp/" + pdb_id + ".pross")
    os.system("tools/PROSS/extract_PROSS2SEQ2D.pl temp/" + pdb_id +
              ".pross > temp/" + pdb_id + ".pross2")
    flag = 0
    annot = ""
    with open("temp/"+pdb_id+".pross2", "r") as filin:
        for line in filin:
            if line[0] == ">" and line[-7:-1] == " pross":
                flag = 1
            elif flag == 1:
                annot += line[:-1]
        print(annot)
    os.system("rm temp/"+pdb_id+".pross")
    os.system("rm temp/"+pdb_id+".pross2")
    return(annot)


if __name__ == '__main__':

    # error management:
    if len(sys.argv) != 2:
        sys.exit("ERROR: one argument is needed (pdb file)")
    s_file = sys.argv[1]
    if s_file[-4:] != ".pdb" or s_file[:-4] != ".ent":
        sys.exit("ERROR: reference file must be a pdb file")

    dssp = dsspAnnot(s_file)
    pross = prossAnnot(s_file)
