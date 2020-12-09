#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:45:57 2020

@author: nreiminger
"""

############################################################################
#                                                                          #
#  This function build a 3DAIR-USFD-1.5 solver with N pollutant transport  #
#                                                                          #
############################################################################

#Load libraries
import os
import errno
import shutil as sh

CWD = os.getcwd()

#Function to create directories
def makeDirectory(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
   
            
###############################################################################
###############################################################################
###############################################################################
            
def solverBuilderFunction(sendingDirectory, N):
    
    WD = sendingDirectory+"/"
    baseSolver = "3DAIR-USFD-1.5"
    newSolver = baseSolver+"-"+str(N)+"s"
    
    
    sh.copytree(CWD+"/baseFiles/"+baseSolver, WD+newSolver)
    
  ### Modifying file Make/files
    with open(WD+newSolver+'/Make/files', 'r') as file:
        lines = file.readlines()
        
    lines[0] = newSolver+".C\n"
    lines[3] = "EXE = $(FOAM_USER_APPBIN)/"+newSolver
    
    with open(WD+newSolver+'/Make/files', 'w') as file:
        file.writelines(lines)
        
  ### Modifying file 3DAIR-USFD-1.5.C
    os.rename(WD+newSolver+"/3DAIR-USFD-1.5.C", WD+newSolver+"/"+newSolver+".C")
    
    list=[]
    with open(WD+newSolver+'/'+newSolver+'.C', 'r') as file:
        lines = file.readlines()
    
    for i in range (0,101):         #Writing the first part of the file
        list.append(lines[i])
        
    for i in range (1,N+1):         #Writing the solvers
        list.append('\t\t\t#include "s'+str(i)+'Eqn.H"\n')

    for i in range (102,120):       #Writing the last part of the file
        list.append(lines[i])

    with open(WD+newSolver+'/'+newSolver+'.C', 'w') as file:
        file.writelines(list)
    
  ### Modifying file createFields.H
    list=[]
    with open(WD+newSolver+'/'+'/createFields.H', 'r') as file:
        lines = file.readlines()
    
    for i in range (0,28):         #Writing the first part of the file
        list.append(lines[i])
        
    for i in range (1,N+1):         #Writing the volumeScalarFields
        list.append('Info<< "Reading field s'+str(i)+'" <<endl;\n')
        list.append('volScalarField s'+str(i)+'\n')
        list.append('(\n')
        list.append('    IOobject\n')
        list.append('    (\n')
        list.append('         "s'+str(i)+'",\n')
        list.append('         runTime.timeName(),\n')
        list.append('         mesh,\n')
        list.append('         IOobject::MUST_READ,\n')
        list.append('         IOobject::AUTO_WRITE\n')
        list.append('    ),\n')
        list.append('    mesh\n')
        list.append(');\n')
        list.append('\n')
            
    for i in range (42,83):         #Writing the first part of the file
        list.append(lines[i])  
        
    with open(WD+newSolver+'/createFields.H', 'w') as file:
        file.writelines(list)

  ### Creating sEqn files
    for i in range(1,N+1):
        file = open(WD+newSolver+'/s'+str(i)+'Eqn.H','w+')
        file.write("fvScalarMatrix s"+str(i)+"Eqn\n")
        file.write("(\n")
        file.write("fvm::ddt(s"+str(i)+")\n")
        file.write("+ fvm::div(phi, s"+str(i)+")\n")
        file.write("- fvm::laplacian(Ds+turbulence->nut()/Sct, s"+str(i)+")\n")
        file.write("==\n")
        file.write("fvOptions(s"+str(i)+")\n")
        file.write(");\n")
        file.write("\n")
        file.write("s"+str(i)+"Eqn.relax();\n")
        file.write("fvOptions.constrain(s"+str(i)+"Eqn);\n")
        file.write("s"+str(i)+"Eqn.solve();\n")
        file.write("fvOptions.correct(s"+str(i)+");\n")
    
    return(lines)




