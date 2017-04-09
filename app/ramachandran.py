#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################
# DESCRIPTION
######################################

# Ramachandran Module
# Coded by Jean-Charles Carvaillo
# carvaillojeancharles@gmail.com
# Master 2 Bioinformatics
# Copyright 2017, Jean-Charles Carvaillo, All rights reserved.

######################################
# CITATION
######################################

# Package Numpy:
# Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux.
# The NumPy Array: A Structure for Efficient Numerical Computation, Computing
# in Science & Engineering, Vol. 13. (2011), pp. 22-30,
# DOI:10.1109/MCSE.2011.37

# Package Matplotib:
# J.D. Hunter. Matplotlib: A 2D Graphics Environment,
# Computing in Science & Engineering, Vol. 9, No. 3. (2007), pp. 90-95

# Package Mdtraj:
# Robert T. McGibbon, Kyle A. Beauchamp, Matthew P. Harrigan,
# Christoph Klein, Jason M. Swails, Carlos X. Hernández,
# Christian R. Schwantes, Lee-Ping Wang, Thomas J. Lane, Vijay S. Pande.
# MDTraj: A Modern Open Library for the Analysis of Molecular Dynamics
# Trajectories, Biophysical Journal, Vol. 109, No. 8. (2015), pp. 1528-1532


######################################
# IMPORT
######################################

import glob
import numpy as np
import matplotlib.pyplot as plt
import mdtraj as md
import os
import sys

######################################
# FUNCTION
######################################


def compute_phi_psi_angles(pdb_file, unit="degree"):
    """Method to compute phi and psi angles of a pdb file in an given
        unit (radian or degree).

    Arguments:
        pdb_file: path of the pdb file
        unit: unit of degree for phi and psi angles (degree or radian)

    Returns:
        phi_angles (numpy.ndarray): array which contains all phi angles
        (numpy.float32).
        psi_angles (numpy.ndarray): array which contains all psi angles
        (numpy.float32).
        phi_angles and psi angles are return in a tuple.

    """
    pdb = md.load_pdb(pdb_file)
    phi_angles = md.compute_phi(pdb)
    psi_angles = md.compute_psi(pdb)
    if unit == "degree":
        # conserve and convert radian angle to degree
        phi_angles = np.rad2deg(phi_angles[::][1][0])
        psi_angles = np.rad2deg(psi_angles[::][1][0])

    elif unit == "radian":
        # conserve radian degree
        phi_angles = phi_angles[::][1][0]
        psi_angles = psi_angles[::][1][0]

    # right phi angle with right psi_angles
    # phi angle position n and psi angle position n+1
    return phi_angles[0:-1], psi_angles[1:]


def compute_ramachandran_map(angles, unit="degree"):
    """Method to generate a ramachandran map with a given unit scale
        (radian or degree).

        Arguments:
            angles: tuple which contains
            phi_angles (numpy.ndarray): array which contains all phi angles
            (numpy.float32).
            psi_angles (numpy.ndarray): array which contains all psi angles
            (numpy.float32).
            unit: unit of degree for phi and psi angles (degree or radian)

    """
    x = angles[0]
    y = angles[1]
    if unit == "degree":
        x_label_in = "Phi(deg)"
        y_label_in = "Psi(deg)"
        plt.plot(x, y, ".")
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
        plt.plot(x, y, ".")
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
    fig.savefig('temp/rama.png', dpi=300)

  
if __name__ == "__main__":
    pdb_file = sys.argv[1]
    angle_unit = sys.argv[2]
    if angle_unit not in ["degree", "radian"]:
        sys.exit("you need to specify for the angle unit 'degree'" +
                 " or 'radian'\n")
    try:
        angles = compute_phi_psi_angles(pdb_file, angle_unit)
        print angles
        compute_ramachandran_map(angles, angle_unit)
    except:
        sys.exit("the specified file is not openable or not" +
                 "a pdb file or just not specified\n")

   
