#!/usr/bin/env python
#-*- coding: utf-8 -*-

u"""Ramachandran Module.

Coded by Jean-Charles Carvaillo
carvaillojeancharles@gmail.com
Master 2 Bioinformatics
Copyright 2017, Jean-Charles Carvaillo, All rights reserved.

######################################
# CITATION
######################################

Package Numpy:
Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux.
The NumPy Array: A Structure for Efficient Numerical Computation, Computing
in Science & Engineering, Vol. 13. (2011), pp. 22-30,
DOI:10.1109/MCSE.2011.37

Package Matplotib:
J.D. Hunter. Matplotlib: A 2D Graphics Environment,
Computing in Science & Engineering, Vol. 9, No. 3. (2007), pp. 90-95

"""

######################################
# IMPORT
######################################
from app import db
import numpy as np
import matplotlib.pyplot as plt
import model
import os
import pandas as pd
from sqlalchemy import or_, and_, func
import seaborn as sns
import sys


######################################
# FUNCTION
######################################

def compute_ramachandran_map(pdb_id, unit="radian"):
    """Generate a ramachandran map with a given unit scale
        (radian or degree).

    Arguments
    ---------
    pdb_id : string 
        id of the pdb in the database
    unit : string -- default : "radian"
        the unit in which the ramap is computed

    Returns:
    --------
    string : arary of string 
        paths of Ramachandran maps that have been computed

    """
    #color_ss = {'H': 'red', 'B': 'green', 'C': 'grey', 'P': 'blue'} 
    path = []
    methods =  db.session.query(model.Annotation.method).group_by(model.Annotation.method).all()
    for method in methods:
        # get annotation
        annotation = db.session.query(model.Annotation.result).filter(and_(model.Annotation.pdb_id==pdb_id,
                                                                           model.Annotation.method==method.method)).scalar()
        # transform a string in a list of char
        annotation = list(annotation[1:len(annotation)-1])
        print(annotation)


    #    color = []
    #    for i in range(1,len(annotation)-1):
    #        try:
    #            color.append(color_ss[annotation[i]])
    #        except:
    #            color.append('black')

        # get angles
        angles = db.session.query(model.Angle).filter(model.Angle.pdb_id==pdb_id)
        phi, psi = zip(*[ (angle.phi, angle.psi) for angle in angles.all()])
        phi = phi[1:len(phi)-1]
        psi = psi[1:len(psi)-1]

        if unit == "degree":
            phi = np.rad2deg(phi)
            psi = np.rad2deg(psi)
        # create a dataframe
        try:
            df = pd.DataFrame(dict(phi=phi, psi=psi, color=annotation))
        except:
            continue
        print(df)

        if unit == "degree":
            # conserve and convert radian angle to degree
            x_label_in = "Phi(deg)"
            y_label_in = "Psi(deg)"
            #plt.plot(x, y, ".")
            sns.lmplot('phi', 'psi', data=df, hue='color', fit_reg=False)
            # Sets x axis limits
            plt.xlim(-180, 180)
            # Sets y axis limits
            plt.ylim(-180, 180)
            # Sets ticks markers for x axis
            plt.xticks(np.arange(-180.1, 180.1, 30))
            # Sets ticks makers for y axis
            plt.yticks(np.arange(-180.1, 180.1, 30))
            # Adds x axis label
            plt.xlabel(x_label_in)
            # Adds y axis label
            plt.ylabel(y_label_in)
            plt.arrow(-180, 0, 360, 0)
            plt.arrow(0, -180, 0, 360)

        elif unit == "radian":
            x_label_in = "Phi(rad)"
            y_label_in = "Psi(rad)"
            #plt.plot(x, y, ".")
            sns.lmplot('phi', 'psi', data=df, hue='color', fit_reg=False)
            # Sets x axis limits
            plt.xlim(-3.14, 3.14)
            # Sets y axis limits
            plt.ylim(-3.14, 3.14)
            # Sets ticks markers for x axis
            plt.xticks(np.arange(-3, 3.5, 0.5))
            # Sets ticks makers for y axis
            plt.yticks(np.arange(-3, 3.5, 0.5))
            # Adds x axis label
            plt.xlabel(x_label_in)
            # Adds y axis label
            plt.ylabel(y_label_in)
            plt.arrow(-np.pi, 0, 2*np.pi, 0)
            plt.arrow(0, -np.pi, 0, 2*np.pi)

        # Create a file for plot
        # Creates a figure
        fig = plt.gcf()
        # Changes figure size
        fig.set_size_inches(10.0, 10.0)
        # Saves figures

        if not os.path.exists('temp'):
            os.mkdir('temp')

        fig.savefig('temp/' + pdb_id + '_' + method.method + '.png', dpi=300)
        path.append('temp/' + pdb_id + '_' + method.method + '.png')

    return path


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit("a pdb id should be specified")
    pdb_id = sys.argv[1]
    if len(sys.argv) > 2:
        angle_unit = sys.argv[2]
        if angle_unit not in ["degree", "radian"]:
            sys.exit("you need to specify for the angle unit 'degree'" +
                     " or 'radian'\n")
    else:
        angle_unit = "radian"

    path_map = compute_ramachandran_map(pdb_id, angle_unit)
    print(path_map)

