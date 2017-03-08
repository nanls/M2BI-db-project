# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:39:35 2017

@author: jeancharlesc
"""

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

def compute_phi_psi_angles(pdb_file, angle="degree"):
	pdb = md.load_pdb(pdb_file)
	phi_angles = md.compute_phi(pdb)
	psi_angles = md.compute_psi(pdb)
	if angle == "degree":
		# conserve and convert radian angle to degree
		phi_angles = np.rad2deg(phi_angles[::][1][0])
		psi_angles = np.rad2deg(psi_angles[::][1][0])

	elif angle == "radian":
		# conserve radian degree
		phi_angles = phi_angles[::][1][0]
		psi_angles = psi_angles[::][1][0]

	# right phi angle with right psi_angles
	# phi angle position n and psi angle position n+1
	return phi_angles[0:-1], psi_angles[1:]


def compute_ramachandran_map(angles, angle="degree"):
	x = angles[0]
	y = angles[1]
	if angle == "degree":
		x_label_in = "Phi(deg)"
		y_label_in = "Psi(deg)"
		plt.plot(x, y, ".")
		plt.xlim(-180, 180)							# Sets x axis limits
		plt.ylim(-180, 180)							# Sets y axis limits
		plt.xticks(np.arange(-180.1, 180.1, 30))	# Sets ticks markers for x axis
		plt.yticks(np.arange(-180.1, 180.1, 30)) 	# Sets ticks makers for y axis
		plt.xlabel(x_label_in)						# Adds x axis label
		plt.ylabel(y_label_in)						# Adds y axis label
		plt.arrow(-180, 0, 360, 0)
		plt.arrow(0, -180, 0, 360)

	elif angle == "radian":
		x_label_in = "Phi(rad)"
		y_label_in = "Psi(rad)"
		plt.plot(x, y, ".")
		plt.xlim(-3.14, 3.14)						# Sets x axis limits
		plt.ylim(-3.14, 3.14)						# Sets y axis limits
		plt.xticks(np.arange(-3, 3.5, 0.5))			# Sets ticks markers for x axis
		plt.yticks(np.arange(-3, 3.5, 0.5)) 		# Sets ticks makers for y axis
		plt.xlabel(x_label_in)						# Adds x axis label
		plt.ylabel(y_label_in)						# Adds y axis label
		plt.arrow(-np.pi, 0, 2*np.pi, 0)
		plt.arrow(0, -np.pi, 0, 2*np.pi)
	# Show plot
	# plt.show()
	
	# Create a file for plot
	fig = plt.gcf()									# Creates a figure
	fig.set_size_inches(10.0, 10.0)					# Changes figure size
	fig.savefig('rama.png', dpi=300)				# Saves figures

######################################
# Main()
######################################

angles = compute_phi_psi_angles("./1a1yIH", "degree")
compute_ramachandran_map(angles, "degree")