#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:34:09 2020

@author: nreiminger
"""

print("\n   Starting multiSourceSolverBuilder python program")
print("     ---")

# Loading libraries ###########################################################

print("     Loading libraries...")

import os
import sys
import errno
import solverBuilder as sB

CWD = os.getcwd()

###############################################################################
    
                                                                            #

# Defining functions ##########################################################

#Function to try if the value is an integer
def tryInt(value):
    if(int(value)==value):
        return(int(value))
    else:
        print("   *** ERROR, the subdivision in the x or y-direction is not an integer\n")
        print("   /!\  Program exiting")
        sys.exit()
        
#Function to create directories
def makeDirectory(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise        
    
###############################################################################

                                                                            #

# Reading input file ##########################################################

print("     Reading input file...")

with open(CWD+"/input","r") as input_file :
    input_lines=input_file.readlines()
    
input_dictionary=dict()
for line in input_lines:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").replace("\t","").split(":")
        input_dictionary.update({line_split[0]:line_split[1].split("#")[0]})
    else:
        continue
    
sendingDirectory = input_dictionary.get('"path"').replace("\t","").replace(" ","")
Nmin = int(input_dictionary.get('"Nmin"'))
Nmax = int(input_dictionary.get('"Nmax"'))

###############################################################################

                                                                            #

# Initialization ##############################################################

#makeDirectory(sendingDirectory+"/outputFiles")

###############################################################################

                                                                            #

                                                                            #

                                                                            #

# sourceBuilder ###############################################################
#print("\n   ***")
#print("\n   Starting sourceBuilder python program")
#
## test
##l_x = tryInt((x_max - x_min)/dx)
##l_y = tryInt((y_max - y_min)/dy)
#
#l_x = (x_max - x_min)/dx
#l_y = (y_max - y_min)/dy
#
## function
#print("     Creating inletPol.stl")
##
##N = sb.sourceBuilderFunction(sendingDirectory, dx, dy, x_min, x_max, y_min, y_max, l_x, l_y, injection_height, tolerance)
#
#print("     Number of pollutant sources : "+str(N))
#print("     ---")
#print("   Ending python program")
#

###############################################################################
                                                                       #

# solverBuilder ###############################################################
print("\n   ***")
print("\n   Starting solverBuilder python program")
print("     ---")

print("     Creating newSolver")

for i in range(Nmin,Nmax+1):
    sB.solverBuilderFunction(sendingDirectory, i)

print("     ---")
print("   Ending python program")


###############################################################################

                                                                            #

# solverBuilder ###############################################################

print("\n   ***")
print("\n   Ending multiSourceSolverBuilder")

###############################################################################

