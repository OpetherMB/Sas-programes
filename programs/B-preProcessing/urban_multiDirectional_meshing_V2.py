# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#!/usr/bin/python


### IMPORTING LIBRARY ###

from math import *
import shutil
import os, errno, sys
import subprocess
import time
from decimal import Decimal
import argparse

#custom libraries
from preProcessingTurbulenceComputation import *
import getBoundaries

### DEFINING COPY DIRECTORIES METHOD ###
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
        
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)




### GETTING PATH OF THE SCRIPT DIRECTORY ###


### GETTING PATH OF THE SCRIPT DIRECTORY ###

path_script_absolute = os.path.abspath(os.path.dirname(__file__))
#print(path_script_absolute)
parser = argparse.ArgumentParser(description="Creates mesh for every specified directions and speeds")
parser.add_argument('-p_working', type=str, help='path to working directory')
parser.add_argument('-p_config', type=str, help='path to config file')
parser.add_argument('-np_mesh', type=int, default=10, help='number of processor for meshing')
parser.add_argument('-snappy_enable', type=str, default="false", help='enable snappy option')

args = parser.parse_args()

dirEtude=args.p_working.replace(" ","")
preProcessingDict=args.p_working.replace(" ","")+"/preProcessingDict"
computationDict=args.p_config.replace(" ","")
nbProcConstruct=args.np_mesh
snappy_enable=args.snappy_enable.replace(" ","")

print(dirEtude)
###############################################
### Reading the config files and closing it ###
###############################################

### Reading and saving into variables computationDict ###

with open(computationDict, "r") as computationDict_file :
    lines_computationDict=computationDict_file.readlines()

computation_dictionary=dict()
for line in lines_computationDict:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        computation_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue

print(computation_dictionary)

meshingMaxSize=float(computation_dictionary.get('"biggest_mesh_size"'))
refinementRoad=computation_dictionary.get('"refinement_road"').split(",")
refinementBlock=computation_dictionary.get('"refinement_block"').split(",")
refinementGround=computation_dictionary.get('"refinement_ground"').split(",")
nbLayer=int(computation_dictionary.get('"nb_refinement_layer"'))
zRef=float(computation_dictionary.get('"z_reference"'))
K=float(computation_dictionary.get('"von_karman_constant"'))


### Reading and saving into variables preProcessingDict ###
with open(preProcessingDict, "r") as preProcessing_file :
    lines_preProcessing=preProcessing_file.readlines()

preProcessing_dictionary=dict()
for line in lines_preProcessing:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        preProcessing_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue

angle_list=preProcessing_dictionary.get('"angles"').split(",")

z0Inlet=float(preProcessing_dictionary.get('"roughness_length_inlet"'))
z0Ground=float(preProcessing_dictionary.get('"roughness_length_ground"'))
z0Block=float(preProcessing_dictionary.get('"roughness_length_block"'))

#L'addition ici sert à avoir un point qui ne soit pas au niveau d'une interface d'une cellule. 

valeurs_polluant_list=preProcessing_dictionary.get('"pollutant_emission"').split(",")
vitesses_list=preProcessing_dictionary.get('"speeds"').split(",")

xminProbes=int(preProcessing_dictionary.get('"xmin_probes"'))
xmaxProbes=int(preProcessing_dictionary.get('"xmax_probes"'))
yminProbes=int(preProcessing_dictionary.get('"ymin_probes"'))
ymaxProbes=int(preProcessing_dictionary.get('"ymax_probes"'))
zlistProbes=[float(x) for x in preProcessing_dictionary.get('"zlist_probes"').split(",")]
pasXProbes=int(preProcessing_dictionary.get('"pasX_probes"'))
pasYProbes=int(preProcessing_dictionary.get('"pasY_probes"'))
angleProbes=int(preProcessing_dictionary.get('"angle_probes"'))
transXprobes=int(preProcessing_dictionary.get('"translation_x_probes"'))
transYprobes=int(preProcessing_dictionary.get('"translation_y_probes"'))


ground_center=[float(x) for x in preProcessing_dictionary.get('"ground_center"').split(",")]
rectangle_length=[float(x) for x in preProcessing_dictionary.get('"rectangle_length"').split(",")]


### Treatment of some variables of config files to adapt them to the code ###
rad90 = float(0.01745329251*90)
nb_vitesses=len(vitesses_list)
nb_specified_polluant=len(valeurs_polluant_list)
valeurs_polluant_list[nb_specified_polluant-1]=valeurs_polluant_list[nb_specified_polluant-1].replace("\n","")
vitesses_list[nb_vitesses-1]=vitesses_list[nb_vitesses-1].replace("\n","")
angle_list[len(angle_list)-1]=angle_list[len(angle_list)-1].replace("\n","")


filesInStudyDir=os.listdir(dirEtude)

### Check if he will use one set of stl for all directions or a set for each directions

if any("wallGround" in s for s in filesInStudyDir):
    if any("wallBlock" in s for s in filesInStudyDir):
        if any("inletPol" in s for s in filesInStudyDir):
            if any("D_" in s for s in filesInStudyDir): 
                print("Le choix n'a pas pu être fait entre mailler un set de stl pour toutes les directions ou un set de stl pour chaque direction ")
                sys.exit()
            else:
                print("choix de mailler toutes les directions avec un set de stl")
                multiSetStl=False #variable qui sert à savoir si on a un set pour toutes les directions
                for angle in angle_list :
                    try:
                        os.makedirs(dirEtude+"/D_"+str(angle))
                    except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
                    for element in os.listdir(dirEtude):
                        if element.endswith('.stl') or element.endswith('.obj'):
                            shutil.copyfile(str(dirEtude+"/"+element),str(dirEtude+"/D_"+str(angle)+"/"+element))
                
elif(any("D_" in s for s in filesInStudyDir)):
    print("choix de mailler pour chaque direction avec un set de stl")
    multiSetStl=True
else:
    print("il n'y a pas les fichiers wallBlock, wallGround, inletPolX ou les répertoire D_XXX pour effectuer le maillage")
    sys.exit()
    
    
### Copie le preProcess et computation utilisé pour cette étude

#copy(path_script_absolute+"/preProcessingDict",dirEtude+"/preProcessingDict")
#copy(path_script_absolute+"/computationDict",dirEtude+"/computationDict")

print(filesInStudyDir)

for angle in angle_list:
    
    directory=dirEtude+"/"+"D_"+str(angle)
    
    print("")
    print("COMMENCEMENT DU SCRIPT POUR LE DOSSIER: "+directory)
    print("Pour un angle de: "+str(angle))
    ### Determine the number of inletPol stl given, check if it match the number of sources and if only one value is given, apply it to every sources ###
    
    nb_inlet_polluant=0
    listFiles=os.listdir(dirEtude+"/"+"D_"+str(angle))
    
    for file in listFiles:
        if("inletPol" in file):
            nb_inlet_polluant+=1
    
    wallground_files_list=list()
    for elem in listFiles:
        if("wallGround" in elem):
            wallground_files_list.append(elem)
    
    if(nb_specified_polluant==nb_inlet_polluant):
        print("nombre de polluant égale aux nombres de sources")
    elif(nb_specified_polluant==1):
        print("la même valeur de polluant va être appliqué à toutes les sources: ",valeurs_polluant_list[0])
        for i in range(1,nb_inlet_polluant):
            valeurs_polluant_list.append(valeurs_polluant_list[0])
    elif(nb_specified_polluant<nb_inlet_polluant):
        print("le nombre de sources de polluant ne correspond pas aux nombres de valeurs spécifiées pour ces polluants")
        sys.exit()
    else:
        print("le nombres de sources de polluant est inférieure aux nombre de valeurs spécifiées pour cette directions")
    
    
    ### Choix des boundaries, si multiSetStl est vrai alors on détermine les boundaries du stl wallGround ###
    ### si multiSetStl est faux alors on détermine les boundaries du wallGround et on calcule le nouveau wallGround en fonction de la rotation pour la bonne direction ###
    
    
    angleRadian=0.01745329251*float(angle)
    if(rectangle_length[0]==0 or rectangle_length[1]==0):
        zmaxAndZmin=getBoundaries.getHeightBuildingAndZmaxAndZmin(directory,wallground_files_list,meshingMaxSize,nbLayer,refinementGround)
        if(multiSetStl==True):
            geometricBoundaries=getBoundaries.getGroundBoundariesSteadyDirection(directory,angle)
            x0=geometricBoundaries[0]
            y0=geometricBoundaries[1]
            x1=geometricBoundaries[2]
            y1=geometricBoundaries[3]
            x2=geometricBoundaries[4]
            y2=geometricBoundaries[5]
            x3=geometricBoundaries[6]
            y3=geometricBoundaries[7]
            
            zmin_inlet=float(zmaxAndZmin[0])
            zmin_ground=float(zmaxAndZmin[0])-0.05
            zmax=float(zmaxAndZmin[1])-0.05
            
            pointInMeshX=float((x3+x1)/2+0.005987814115)
            pointInMeshY=float((y3+y1)/2+0.015468746312)
            pointInMeshZ=float(zmaxAndZmin[2]*1.8+0.0310572052)
        else:
            groundBoundary=getBoundaries.getGroundBoundaries(dirEtude)
            transX=float(groundBoundary[4])
            transY=float(groundBoundary[5])
            xmin=float(groundBoundary[0])
            xmax=float(groundBoundary[1])
            ymin=float(groundBoundary[2])
            ymax=float(groundBoundary[3])
            zmin_inlet=float(zmaxAndZmin[0])
            zmin_ground=float(zmaxAndZmin[0])-0.05
            zmax=float(zmaxAndZmin[1])-0.05
            pointInMeshX=float((xmax+xmin)/2+0.005987814115)
            pointInMeshY=float((ymax+ymin)/2+0.015468746312)
            pointInMeshZ=float(zmaxAndZmin[2]*1.8+0.0310572052)
            
            if(angle==0 or angle==360):
                x0=xmin
                y0=ymin   
                x1=xmax
                y1=ymin
                x2=xmax
                y2=ymax
                x3=xmin
                y3=ymax    
            ### Correcting if there is an angle ###    
            else:
                x0=(xmin-transX)*cos(angleRadian)+(ymin-transY)*sin(angleRadian)+transX
                y0=-(xmin-transX)*sin(angleRadian)+(ymin-transY)*cos(angleRadian)+transY
                x1=(xmax-transX)*cos(angleRadian)+(ymin-transY)*sin(angleRadian)+transX
                y1=-(xmax-transX)*sin(angleRadian)+(ymin-transY)*cos(angleRadian)+transY
                x2=(xmax-transX)*cos(angleRadian)+(ymax-transY)*sin(angleRadian)+transX
                y2=-(xmax-transX)*sin(angleRadian)+(ymax-transY)*cos(angleRadian)+transY
                x3=(xmin-transX)*cos(angleRadian)+(ymax-transY)*sin(angleRadian)+transX
                y3=-(xmin-transX)*sin(angleRadian)+(ymax-transY)*cos(angleRadian)+transY  
    else:
        transX=ground_center[0]
        transY=ground_center[1]
        zmin_inlet=ground_center[2]
        
        zmax,hmax,zmin_ground=getBoundaries.getHeightBuildingZmax(directory,zmin_inlet,wallground_files_list,meshingMaxSize,nbLayer,refinementGround)
        
        zmax=zmax-0.05
        zmin_ground=zmin_ground-0.05
        
        
        xmin=ground_center[0]-rectangle_length[0]/2
        xmax=ground_center[0]+rectangle_length[0]/2
        ymin=ground_center[1]-rectangle_length[1]/2
        ymax=ground_center[1]+rectangle_length[1]/2
        
        pointInMeshX=float((xmax+xmin)/2+0.005987814115)
        pointInMeshY=float((ymax+ymin)/2+0.015468746312)
        pointInMeshZ=float((hmax)*1.8+zmin_inlet+0.0310572052)
                    
        if(angle==0 or angle==360):
            x0=xmin
            y0=ymin   
            x1=xmax
            y1=ymin
            x2=xmax
            y2=ymax
            x3=xmin
            y3=ymax    
        ### Correcting if there is an angle ###    
        else:
            x0=(xmin-transX)*cos(angleRadian)+(ymin-transY)*sin(angleRadian)+transX
            y0=-(xmin-transX)*sin(angleRadian)+(ymin-transY)*cos(angleRadian)+transY
            x1=(xmax-transX)*cos(angleRadian)+(ymin-transY)*sin(angleRadian)+transX
            y1=-(xmax-transX)*sin(angleRadian)+(ymin-transY)*cos(angleRadian)+transY
            x2=(xmax-transX)*cos(angleRadian)+(ymax-transY)*sin(angleRadian)+transX
            y2=-(xmax-transX)*sin(angleRadian)+(ymax-transY)*cos(angleRadian)+transY
            x3=(xmin-transX)*cos(angleRadian)+(ymax-transY)*sin(angleRadian)+transX
            y3=-(xmin-transX)*sin(angleRadian)+(ymax-transY)*cos(angleRadian)+transY  
    

    
                        ##################################################  
    ##################  ### ### ### MODIFYING SYSTEM DIRECTORY ### ### ### #####################################################################################
                        ##################################################
    
    print("création du dossier system")  
    
    copy(path_script_absolute+"/system/",directory+"/system") # copie le dossier constant dans le répertoire cible
    os.remove(directory+"/system"+"/surfaceFeatureExtractDict") # supprime les fichiers qui vont être remplacé par la suite par les bons
    os.remove(directory+"/system"+"/snappyHexMeshDict")
    
    
    ##########################################################
    ### ### ### CHANGING SURFACEFEATUREEXTRACTDICT ### ### ###
    ##########################################################
    
    print("  - création du fichier surfaceFeatureExtractDict")  
    
    surfaceFeactureDictInput=path_script_absolute+"/system/surfaceFeatureExtractDict" 
    surfaceFeactureDictOutput=directory+"/system/surfaceFeatureExtractDict"
    
    surfaceFeatureDict_file_input = open(surfaceFeactureDictInput, "r")
    lines_surfaceFeatureDictInput=surfaceFeatureDict_file_input.readlines()
    surfaceFeatureDict_file_input.close()

 

    lines_surfaceFeatureDictOutput=list()
    
    for i in range(0,15):
        lines_surfaceFeatureDictOutput.append(lines_surfaceFeatureDictInput[i])
    
    for i in range(0,nb_inlet_polluant):
        lines_surfaceFeatureDictOutput.append("\n"+"inletPol"+str(i+1)+".stl"+"\n") 
        lines_surfaceFeatureDictOutput.append("{"+"\n")
        lines_surfaceFeatureDictOutput.append("    extractionMethod    extractFromSurface;"+"\n")
        lines_surfaceFeatureDictOutput.append("    extractFromSurfaceCoeffs"+"\n")
        lines_surfaceFeatureDictOutput.append("{"+"\n")
        lines_surfaceFeatureDictOutput.append("        includedAngle   120;"+"\n")
        lines_surfaceFeatureDictOutput.append("        geometricTestOnly       yes;"+"\n")
        lines_surfaceFeatureDictOutput.append("}"+"\n")
        lines_surfaceFeatureDictOutput.append("        writeObj                yes;"+"\n")
        lines_surfaceFeatureDictOutput.append("}"+"\n")
    
    for i,wallground in enumerate(wallground_files_list):
        lines_surfaceFeatureDictOutput.append("\n"+wallground+"\n") 
        lines_surfaceFeatureDictOutput.append("{"+"\n")
        lines_surfaceFeatureDictOutput.append("    extractionMethod    extractFromSurface;"+"\n")
        lines_surfaceFeatureDictOutput.append("    extractFromSurfaceCoeffs"+"\n")
        lines_surfaceFeatureDictOutput.append("{"+"\n")
        lines_surfaceFeatureDictOutput.append("        includedAngle   120;"+"\n")
        lines_surfaceFeatureDictOutput.append("        geometricTestOnly       yes;"+"\n")
        lines_surfaceFeatureDictOutput.append("}"+"\n")
        lines_surfaceFeatureDictOutput.append("        writeObj                yes;"+"\n")
        lines_surfaceFeatureDictOutput.append("}"+"\n")        
    
    
    for i in range(16,len(lines_surfaceFeatureDictInput)):
        lines_surfaceFeatureDictOutput.append(lines_surfaceFeatureDictInput[i])   
    
    surfaceFeatureDict_file_output=open(surfaceFeactureDictOutput, "w")
    
    for i in range(0,len(lines_surfaceFeatureDictOutput)):
        surfaceFeatureDict_file_output.write(str(lines_surfaceFeatureDictOutput[i]))    
    surfaceFeatureDict_file_output.close()
    
    ###################################################
    ### ### ### CHANGING SNAPPYHEXXMESHDICT ### ### ###
    ###################################################
    
    print("  - création du fichier snappyHexMeshDict")  
    
    snappyHexMeshDictInput=path_script_absolute+"/system/snappyHexMeshDict" 
    snappyHexMeshDictOutput=directory+"/system/snappyHexMeshDict"
    
    snappyHexMeshDict_file_input = open(snappyHexMeshDictInput, "r")
    lines_snappyHexMeshDictInput=snappyHexMeshDict_file_input.readlines()
    snappyHexMeshDict_file_input.close()

    for i,line in enumerate(lines_snappyHexMeshDictInput):
        
        if("geometry\n" in line):
            geometry_nb_line=i+2
        elif("features\n" in line):
            features_nb_line=i+2
        elif("refinementSurfaces\n" in line):
            refinementSurfaces_nb_line=i+2
        elif("refinementRegions" in line):
            refinementRegions_nb_line=i+2
        elif("snap            true;" in line):
            snap_nb_line=i
        elif("nCellsBetweenLevels" in line):
            nCellsBetweenLevels_nb_line=i
        elif("locationInMesh (ToBeDef ToBeDef ToBeDef);" in line):
            locationInMesh_nb_line=i    
    
    lines_snappyHexMeshDictOutput=list()
    lines_snappyHexMeshDictInput[snap_nb_line]="snap            "+str(snappy_enable)+";\n"  
    lines_snappyHexMeshDictInput[nCellsBetweenLevels_nb_line]="    nCellsBetweenLevels "+str(nbLayer)+";\n"
    lines_snappyHexMeshDictInput[locationInMesh_nb_line]="    locationInMesh ("+str(pointInMeshX)+" "+str(pointInMeshY)+" "+str(pointInMeshZ)+");\n"
    
    #locate the line of the specified keywords
            
    for i in range(0,geometry_nb_line):
        lines_snappyHexMeshDictOutput.append(lines_snappyHexMeshDictInput[i])
    
    for i in range(0,nb_inlet_polluant):
        lines_snappyHexMeshDictOutput.append("    inletPol"+str(i+1)+".stl"+"\n")
        lines_snappyHexMeshDictOutput.append("    {"+"\n")
        lines_snappyHexMeshDictOutput.append("    type triSurfaceMesh;"+"\n")
        lines_snappyHexMeshDictOutput.append("    name  inletPol"+str(i+1)+";\n")
        lines_snappyHexMeshDictOutput.append("    }"+"\n")

    for i,wallground in enumerate(wallground_files_list):
        lines_snappyHexMeshDictOutput.append("    "+wallground+"\n")
        lines_snappyHexMeshDictOutput.append("    {"+"\n")
        lines_snappyHexMeshDictOutput.append("    type triSurfaceMesh;"+"\n")
        lines_snappyHexMeshDictOutput.append("    name  "+wallground.split(".")[0]+";\n")
        lines_snappyHexMeshDictOutput.append("    }"+"\n")
   
    for i in range(geometry_nb_line,features_nb_line):
        lines_snappyHexMeshDictOutput.append(lines_snappyHexMeshDictInput[i])
        
    for i in range(0,nb_inlet_polluant):
        lines_snappyHexMeshDictOutput.append("	{"+"\n")
        lines_snappyHexMeshDictOutput.append("            file \"inletPol"+str(i+1)+".eMesh\";"+"\n")
        lines_snappyHexMeshDictOutput.append("            level 0;\n")
        lines_snappyHexMeshDictOutput.append("        }"+"\n")

    for i,wallground in enumerate(wallground_files_list):
        lines_snappyHexMeshDictOutput.append("	{"+"\n")
        lines_snappyHexMeshDictOutput.append("            file \""+wallground.split(".")[0]+".eMesh\";"+"\n")
        lines_snappyHexMeshDictOutput.append("            level 0;\n")
        lines_snappyHexMeshDictOutput.append("        }"+"\n")  
    
    for i in range(features_nb_line,refinementSurfaces_nb_line):
        lines_snappyHexMeshDictOutput.append(lines_snappyHexMeshDictInput[i])
    
    for i in range(0,nb_inlet_polluant):
    
        lines_snappyHexMeshDictOutput.append("        inletPol"+str(i+1)+"\n")
        lines_snappyHexMeshDictOutput.append("        {"+"\n")
        lines_snappyHexMeshDictOutput.append("            level (0 0);\n")
        lines_snappyHexMeshDictOutput.append("        }\n")

    for i,wallground in enumerate(wallground_files_list):

        lines_snappyHexMeshDictOutput.append("        "+wallground.split(".")[0]+"\n")
        lines_snappyHexMeshDictOutput.append("        {"+"\n")
        lines_snappyHexMeshDictOutput.append("            level (0 0);\n")
        lines_snappyHexMeshDictOutput.append("        }\n")
        
    for i in range(refinementSurfaces_nb_line,refinementRegions_nb_line):
        lines_snappyHexMeshDictOutput.append(lines_snappyHexMeshDictInput[i])
    
    lines_snappyHexMeshDictOutput.append("    wallBlock"+"\n")
    lines_snappyHexMeshDictOutput.append("        {"+"\n")
    lines_snappyHexMeshDictOutput.append("           mode distance;"+"\n")
    lines_snappyHexMeshDictOutput.append("            levels ("+"\n")
    for refinement_for_block in refinementBlock :
        lines_snappyHexMeshDictOutput.append("		    "+refinement_for_block.replace(";"," ")+"\n")
    lines_snappyHexMeshDictOutput.append("        );"+"\n")
    lines_snappyHexMeshDictOutput.append("        }"+"\n")

    for i,wallground in enumerate(wallground_files_list):
        lines_snappyHexMeshDictOutput.append("    "+wallground.split(".")[0]+"\n")
        lines_snappyHexMeshDictOutput.append("        {"+"\n")
        lines_snappyHexMeshDictOutput.append("           mode distance;"+"\n")
        lines_snappyHexMeshDictOutput.append("            levels ("+"\n")
        for refinement_for_ground in refinementGround :
            lines_snappyHexMeshDictOutput.append("		    "+refinement_for_ground.replace(";"," ")+"\n")
        lines_snappyHexMeshDictOutput.append("        );"+"\n\n")    
        lines_snappyHexMeshDictOutput.append("        }"+"\n")

    for i in range(0,nb_inlet_polluant):
        lines_snappyHexMeshDictOutput.append("    inletPol"+str(i+1)+"\n")
        lines_snappyHexMeshDictOutput.append("        {"+"\n")
        lines_snappyHexMeshDictOutput.append("           mode distance;"+"\n")
        lines_snappyHexMeshDictOutput.append("            levels ("+"\n")
        for refinement_for_road in refinementRoad :
            lines_snappyHexMeshDictOutput.append("		    "+refinement_for_road.replace(";"," ")+"\n")
        lines_snappyHexMeshDictOutput.append("        );"+"\n\n")
        lines_snappyHexMeshDictOutput.append("        }"+"\n")
    
    for i in range(refinementRegions_nb_line,len(lines_snappyHexMeshDictInput)):
        lines_snappyHexMeshDictOutput.append(lines_snappyHexMeshDictInput[i])
    
    snappyHexMesh_file_output=open(snappyHexMeshDictOutput, "w")
    
    for i in range(0,len(lines_snappyHexMeshDictOutput)):
        snappyHexMesh_file_output.write(str(lines_snappyHexMeshDictOutput[i]))   
    snappyHexMesh_file_output.close()
    
    #################################################
    ### ### ### CHANGING DECOMPOSEPARDICT ### ### ###
    #################################################  
    
    print("  - changement des fichiers decomposePar") 
    
    ### DecomposeParDict for meshing ###
    
    decomposeParConstruct_file=open(str(directory+"/system/decomposeParDict.construct"),"r")
    lines_decomposeParConstruct=decomposeParConstruct_file.readlines()
    decomposeParConstruct_file.close()  
    lines_decomposeParConstruct[17]="numberOfSubdomains "+str(nbProcConstruct)+";\n"
    decomposeParConstruct_file=open(str(directory+"/system/decomposeParDict.construct"),"w")
    for j in range(0,len(lines_decomposeParConstruct)):
        decomposeParConstruct_file.write(lines_decomposeParConstruct[j])
    decomposeParConstruct_file.close()

    #######################################
    ### ### ### CHANGING PROBES ### ### ###
    #######################################
    
    print("  - création du fichier probes")  
    
    probesInput=path_script_absolute+"/system/probes" 
    probesOutput=directory+"/system/probes"
    
    probes_file_input = open(probesInput, "r")
    lines_probesInput=probes_file_input.readlines()
    probes_file_input.close()
    
    lines_probesOutput=list()
    string_nb_inlet_polluant="            s1"
    for i in range(1,nb_inlet_polluant):
        string_nb_inlet_polluant=string_nb_inlet_polluant+" s"+str(i+1)
    string_nb_inlet_polluant=string_nb_inlet_polluant+" U\n"
    
    lines_probesInput[25]=string_nb_inlet_polluant
    
    for i in range(0,30):
        lines_probesOutput.append(lines_probesInput[i])
    
    #Translation et Rotation
    lines_probesOutput=lines_probesOutput+getBoundaries.probes_rotation_translation(xminProbes,xmaxProbes,yminProbes,ymaxProbes,zlistProbes,transXprobes,transYprobes,pasXProbes,pasYProbes,angleProbes)    
        
    for i in range(30,len(lines_probesInput)):
        lines_probesOutput.append(lines_probesInput[i])
    
    probes_file_output=open(probesOutput, "w")
    for i in range(0,len(lines_probesOutput)):
        probes_file_output.write(str(lines_probesOutput[i]))   
    probes_file_output.close() 
    
    #######################################
    ### ### ### CHANGING TOPOSETDICT ### ### ###
    #######################################    
    
    print("  - création du fichier topoSetDict")

    topoSetInput=path_script_absolute+"/system/topoSetDict" 
    topoSetOutput=directory+"/system/topoSetDict"
    
    topoSet_file_input = open(topoSetInput, "r")
    lines_topoSetInput=topoSet_file_input.readlines()
    topoSet_file_input.close()    
    
    lines_topoSetOutput=list()
    
    for i in range(0,15):
        lines_topoSetOutput.append(lines_topoSetInput[i])
    
    lines_topoSetOutput.append("actions\n")   
    lines_topoSetOutput.append("(\n")
    for i in range(0,nb_inlet_polluant):
   
    
        lines_topoSetOutput.append("    {\n")
        lines_topoSetOutput.append("        name    leSet"+str(i+1)+";\n")
        lines_topoSetOutput.append("        type    cellSet;\n")
        lines_topoSetOutput.append("        action  new;\n")
        lines_topoSetOutput.append("        source  surfaceToCell;\n")
        lines_topoSetOutput.append("        sourceInfo\n")
        lines_topoSetOutput.append("        {\n")
        lines_topoSetOutput.append('    	           file "constant/triSurface/inletPol'+str(i+1)+'.stl";\n')
        lines_topoSetOutput.append("    		       outsidePoints (("+str(pointInMeshX)+" "+str(pointInMeshY)+" "+str(pointInMeshZ)+"));\n")
        lines_topoSetOutput.append("    		       includeCut true;\n")
        lines_topoSetOutput.append("    	           includeInside true;\n")
        lines_topoSetOutput.append("    		       includeOutside false;\n")
        lines_topoSetOutput.append("    		       nearDistance -1;\n")
        lines_topoSetOutput.append("    	           curvature -100;\n")
        lines_topoSetOutput.append("        }\n")
        lines_topoSetOutput.append("}\n")
        lines_topoSetOutput.append("{\n")
        lines_topoSetOutput.append("    name	sourcePolVol"+str(i+1)+";\n")
        lines_topoSetOutput.append("    type cellZoneSet;\n")  
        lines_topoSetOutput.append("    action new;\n")  
        lines_topoSetOutput.append("    source setToCellZone;\n")  
        lines_topoSetOutput.append("    sourceInfo\n")  
        lines_topoSetOutput.append("    {\n")  
        lines_topoSetOutput.append("        set leSet"+str(i+1)+";\n")  
        lines_topoSetOutput.append("    }\n")  
        lines_topoSetOutput.append("}\n\n")  
          
        
    lines_topoSetOutput.append(");\n")    
    for i in range(15,len(lines_topoSetInput)):
        lines_topoSetOutput.append(lines_topoSetInput[i])
    
    topoSet_file_output=open(topoSetOutput, "w")
    for i in range(0,len(lines_topoSetOutput)):
        topoSet_file_output.write(str(lines_topoSetOutput[i]))   
    topoSet_file_output.close()      
    
    ###########################################
    ### ### ### CHANGING fvSolution ### ### ###
    ###########################################
    
    print("  - création du fichier fvSolution")  
    
    fvsolutionInput=path_script_absolute+"/system/fvSolution" 
    fvsolutionOutput=directory+"/system/fvSolution"
    
    fvsolution_file_input = open(fvsolutionInput, "r")
    lines_fvsolutionInput=fvsolution_file_input.readlines()
    fvsolution_file_input.close()
    
    lines_fvsolutionOutput=list()
    
    string_number_polluant="s1"
    for i in range(1,nb_inlet_polluant):
        string_number_polluant=string_number_polluant+"|s"+str(i+1)
    
    lines_fvsolutionOutput=lines_fvsolutionInput
    lines_fvsolutionOutput[49]='    "('+string_number_polluant+')"\n'
    lines_fvsolutionOutput[57]='    "('+string_number_polluant+')Final"\n'
    
    fvsolution_file_output=open(fvsolutionOutput, "w")
    
    for i in range(0,len(lines_fvsolutionOutput)):
        fvsolution_file_output.write(str(lines_fvsolutionOutput[i]))   
    fvsolution_file_output.close()     
    
    ##########################################
    ### ### ### CHANGING fvSchemes ### ### ###
    ##########################################
    
    print("  - création du fichier fvSchemes")  
    
    fvschemesInput=path_script_absolute+"/system/fvSchemes" 
    fvschemesOutput=directory+"/system/fvSchemes"
    
    fvschemes_file_input = open(fvschemesInput, "r")
    lines_fvschemesInput=fvschemes_file_input.readlines()
    fvschemes_file_input.close()
    
    lines_fvschemesOutput=list()
    
    for i in range(0,38):
        lines_fvschemesOutput.append(lines_fvschemesInput[i])
    
    for i in range(0,nb_inlet_polluant):
        lines_fvschemesOutput.append("    div(phi,s"+str(i+1)+")      Gauss linearUpwind grad(s"+str(i+1)+");\n")
    
    for i in range(38,len(lines_fvschemesInput)):
        lines_fvschemesOutput.append(lines_fvschemesInput[i])
    
    fvschemes_file_output=open(fvschemesOutput, "w")
    
    for i in range(0,len(lines_fvschemesOutput)):
        fvschemes_file_output.write(str(lines_fvschemesOutput[i]))   
    fvschemes_file_output.close()   
                        ######################################################  
    ################### ### ### ### END MODIFYING SYSTEM DIRECTORY ### ### ### ######################################################################
                        ######################################################
                     
                        #############################################
    ##################  ### ### ### MODIFYING 0 DIRECTORY ### ### ### ########################################################################
                        #############################################
    
    print("création du dossier 0")  
    
    try:
        os.makedirs(directory+"/0")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    #########################################################
    ### Copying Include and Modifying ABLConditionsDomain ###
    #########################################################   
    
    print("  - copie du répertoire Include") 
    
    includeInput=path_script_absolute+"/0/include/" 
    includeOutput=directory+"/0/include/"
    copy(includeInput,includeOutput)
    
    ABLConditionsDomain_file=open(includeOutput+"ABLConditionsDomain","r")
    ABLConditionsDomain_lines=ABLConditionsDomain_file.readlines()
    ABLConditionsDomain_file.close()
    ABLConditionsDomain_lines[8]="z0Ground                   uniform "+str(z0Ground)+";\n"
    ABLConditionsDomain_lines[9]="z0Block                    uniform "+str(z0Block)+";\n"    
    
    ABLConditionsDomain_file=open(includeOutput+"ABLConditionsDomain","w")  
    [ABLConditionsDomain_file.write(item) for item in ABLConditionsDomain_lines]
    ABLConditionsDomain_file.close()
    
    ######################
    ### WRITINGEpsilon ###
    ######################
    
    print("  - création du fichier espilon")
    epsilonInput=path_script_absolute+"/0/epsilon" 
    epsilonOutput=directory+"/0/epsilon"
    epsilon_file_input = open(epsilonInput, "r")
    
    lines_epsilonInput=epsilon_file_input.readlines()
    epsilon_file_input.close()
    
    lines_epsilonOutput = list()
    
    for i in range(0,25):
        lines_epsilonOutput.append(lines_epsilonInput[i]) 

    for i in range(0,nb_inlet_polluant):
        lines_epsilonOutput.append("    inletPol"+str(i+1)+"\n")
        lines_epsilonOutput.append("    {"+"\n")
        lines_epsilonOutput.append("        type            epsilonWallFunction;"+"\n")
        lines_epsilonOutput.append("        Cmu             0.09;"+"\n")
        lines_epsilonOutput.append("        kappa           0.4;"+"\n")
        lines_epsilonOutput.append("        E               9.8;"+"\n")
        lines_epsilonOutput.append("        value           $internalField;"+"\n")   
        lines_epsilonOutput.append("    }"+"\n")
  
    for i in range(25,len(lines_epsilonInput)):
        lines_epsilonOutput.append(lines_epsilonInput[i])  
    
    
    
    epsilon_file_output=open(epsilonOutput, "w")
    
    for i in range(0,len(lines_epsilonOutput)):
        epsilon_file_output.write(str(lines_epsilonOutput[i]))
    
    epsilon_file_output.close()
    
    #################
    ### WRITING k ###
    #################
    print("  - création du fichier k")  
    kInput=path_script_absolute+"/0/k" 
    kOutput=directory+"/0/k"
    k_file_input = open(kInput, "r")
    
    lines_kInput=k_file_input.readlines()
    k_file_input.close()
    
    lines_kOutput = list()
    
    for i in range(0,25):
        lines_kOutput.append(lines_kInput[i]) 

    for i in range(0,nb_inlet_polluant):
        lines_kOutput.append("    inletPol"+str(i+1)+"\n")
        lines_kOutput.append("    {"+"\n")
        lines_kOutput.append("        type            kqRWallFunction;"+"\n")
        lines_kOutput.append("        value           uniform 0.0;"+"\n")   
        lines_kOutput.append("    }"+"\n")
   
    for i in range(25,len(lines_kInput)):
        lines_kOutput.append(lines_kInput[i])  
    
    
    
    k_file_output=open(kOutput, "w")
    
    for i in range(0,len(lines_kOutput)):
        k_file_output.write(str(lines_kOutput[i]))
    
    k_file_output.close()
    
    ###################
    ### WRITING nut ###
    ###################
    print("  - création du fichier nut")  
    nutInput=path_script_absolute+"/0/nut" 
    nutOutput=directory+"/0/nut"
    nut_file_input = open(nutInput, "r")
    
    lines_nutInput=nut_file_input.readlines()
    nut_file_input.close()
    lines_nutOutput = list()    

    for i in range(0,24):
        lines_nutOutput.append(lines_nutInput[i])

    for i in range(0,nb_inlet_polluant):
        lines_nutOutput.append("    inletPol"+str(i+1)+"\n")
        lines_nutOutput.append("    {"+"\n")
        lines_nutOutput.append("        type            nutkAtmRoughWallFunction;"+"\n")
        lines_nutOutput.append("        z0              $z0Ground;"+"\n")
        lines_nutOutput.append("        value           uniform 0.0;"+"\n")
        lines_nutOutput.append("    }"+"\n")
 
    for i in range(24,len(lines_nutInput)):
        lines_nutOutput.append(lines_nutInput[i])   
    
    nut_file_output=open(nutOutput, "w")
    
    for i in range(0,len(lines_nutOutput)):
        nut_file_output.write(str(lines_nutOutput[i]))
    
    nut_file_output.close()    
    
    #################
    ### WRITING P ###
    #################
    print("  - création du fichier P")  
    pInput=path_script_absolute+"/0/p" 
    pOutput=directory+"/0/p"
    p_file_input = open(pInput, "r")
    
    lines_pInput=p_file_input.readlines()
    p_file_input.close()
    lines_pOutput = list()
    
    for i in range(0,22):
        lines_pOutput.append(lines_pInput[i])

    for i in range(0,nb_inlet_polluant):
        lines_pOutput.append("    inletPol"+str(i+1)+"\n")
        lines_pOutput.append("    {"+"\n")
        lines_pOutput.append("        type            zeroGradient;"+"\n")
        lines_pOutput.append("    }"+"\n")
 
    for i in range(22,len(lines_pInput)):
        lines_pOutput.append(lines_pInput[i])   
    
    p_file_output=open(pOutput, "w")
    
    for i in range(0,len(lines_pOutput)):
        p_file_output.write(str(lines_pOutput[i]))
    
    p_file_output.close()
    
    #################
    ### WRITING s ###
    #################
    print("  - création du fichier s")
    
    for j in range(0,nb_inlet_polluant):
        
        sInput=path_script_absolute+"/0/s" 
        sOutput=directory+"/0/s"+str(j+1)
        s_file_input = open(sInput, "r")
        
        lines_sInput=s_file_input.readlines()
        s_file_input.close()
        
        lines_sOutput = list()
    
        for i in range(0,22):
            lines_sOutput.append(lines_sInput[i]) 
       
        for i in range(0,nb_inlet_polluant):
            lines_sOutput.append("    inletPol"+str(i+1)+"\n")
            lines_sOutput.append("    {"+"\n")
            lines_sOutput.append("        type            zeroGradient;"+"\n")
            lines_sOutput.append("    }"+"\n")
               
        for i in range(22,len(lines_sInput)):
            lines_sOutput.append(lines_sInput[i])  
     
        
        
        s_file_output=open(sOutput, "w")
        
        for i in range(0,len(lines_sOutput)):
            s_file_output.write(str(lines_sOutput[i]))
        
        s_file_output.close()
    
    #################
    ### WRITING U ###
    #################
    print("  - création du fichier U")  
    UInput=path_script_absolute+"/0/U" 
    UOutput=directory+"/0/U"
    U_file_input = open(UInput, "r")
    
    lines_UInput=U_file_input.readlines()
    U_file_input.close()
    
    lines_UOutput = list()
    
    for i in range(0,24):
        lines_UOutput.append(lines_UInput[i]) 

    for i in range(0,nb_inlet_polluant):
        lines_UOutput.append("    inletPol"+str(i+1)+"\n")
        lines_UOutput.append("    {"+"\n")
        lines_UOutput.append("        type            uniformFixedValue;"+"\n")
        lines_UOutput.append("        uniformValue    (0 0 0);"+"\n") 
        lines_UOutput.append("        value           uniform (0 0 0);"+"\n") 
        lines_UOutput.append("    }"+"\n")

    for i in range(24,len(lines_UInput)):
        lines_UOutput.append(lines_UInput[i])  
    
    
    
    U_file_output=open(UOutput, "w")
    
    for i in range(0,len(lines_UOutput)):
        U_file_output.write(str(lines_UOutput[i]))
    
    U_file_output.close()        
                        
                        #################################################### 
    ##################  ### ### ### MODIFYING CONSTANT DIRECTORY ### ### ### ########################################################################
                        ####################################################                    
    print("création du dossier constant")                    
    copy(path_script_absolute+"/constant/",directory+"/constant") # copie le dossier constant dans le répertoire cible
    
    ### CREATING TRISURFACE ###
    print("  - création du dossier triSurface")  
    try:
        os.makedirs(directory+"/constant/triSurface")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    ### FILLING TRISURFACE ###
            
    for element in os.listdir(directory):
        if element.endswith('.stl') or element.endswith('.obj'):
            shutil.copyfile(str(directory+"/"+element),str(directory+"/constant/triSurface/"+element))
            os.remove(str(directory+"/"+element))
                 
    ##########################################    
    ### ### ### MODYFING BLOCKMESH ### ### ###
    ##########################################
    
    print("  - création du fichier blockMeshDict")
    
    blockMesh=path_script_absolute+"/constant/polyMesh/blockMeshDict" 
    blockMeshOutput=directory+"/constant/polyMesh/blockMeshDict"
    
    blockMesh_file_input = open(blockMesh, "r")
    blockMesh_file_output = open(blockMeshOutput, "w")
    
    lines_blockMesh=blockMesh_file_input.readlines()
    blockMesh_file_input.close()
    
    lineVertex0="(" +str(x0)+"   "+ str(y0)+ "   "+ str(zmin_ground) +") // 0" +"\n"
    lineVertex1="(" +str(x1)+"   "+ str(y1)+ "   "+ str(zmin_ground) +") // 1" +"\n"
    lineVertex2="(" +str(x2)+"   "+ str(y2)+ "   "+ str(zmin_ground) +") // 2" +"\n"
    lineVertex3="(" +str(x3)+"   "+ str(y3)+ "   "+ str(zmin_ground) +") // 3" +"\n"
    lineVertex4="(" +str(x0)+"   "+ str(y0)+ "   "+ str(zmax) +") // 4" +"\n"
    lineVertex5="(" +str(x1)+"   "+ str(y1)+ "   "+ str(zmax) +") // 5" +"\n"
    lineVertex6="(" +str(x2)+"   "+ str(y2)+ "   "+ str(zmax) +") // 6" +"\n"
    lineVertex7="(" +str(x3)+"   "+ str(y3)+ "   "+ str(zmax) +") // 7" +"\n"
    
    lines_blockMesh[20]=lineVertex0
    lines_blockMesh[21]=lineVertex1
    lines_blockMesh[22]=lineVertex2
    lines_blockMesh[23]=lineVertex3
    lines_blockMesh[24]=lineVertex4
    lines_blockMesh[25]=lineVertex5
    lines_blockMesh[26]=lineVertex6
    lines_blockMesh[27]=lineVertex7
    
    
    mailleDx=round(getBoundaries.calculateDistance(x0,y0,x1,y1)/meshingMaxSize)
    mailleDy=round(getBoundaries.calculateDistance(x0,y0,x3,y3)/meshingMaxSize)
    mailleDz=round((zmax-zmin_ground)/meshingMaxSize)
    
    maillageBlockMesh="hex (0 1 2 3 4 5 6 7) ("+ str(mailleDx) +" "+ str(mailleDy) +" "+ str(mailleDz)  +") simpleGrading (1 1 1) \n"
    lines_blockMesh[32]=maillageBlockMesh
    
    for i in range(0,len(lines_blockMesh)):
        blockMesh_file_output.write(str(lines_blockMesh[i]))
    blockMesh_file_output.close()
    
        
    ############################################    
    ### ### ### MODIFYING FVOPTIONS  ### ### ###
    ############################################

    print("  - création du fichier fvOptions")
    
    fvOptionsInput=path_script_absolute+"/constant/fvOptions" 
    fvOptionsOutput=directory+"/constant/fvOptions"
    
    fvOptions_file_input = open(fvOptionsInput, "r")
    lines_fvOptionsInput=fvOptions_file_input.readlines()
    fvOptions_file_input.close()    
    
    lines_fvOptionsOutput=list()
    
    for i in range(0,16):
        lines_fvOptionsOutput.append(lines_fvOptionsInput[i])
    
    for i in range(0,nb_inlet_polluant):

        lines_fvOptionsOutput.append("massSource"+str(i+1)+"\n")
        lines_fvOptionsOutput.append("{\n")
        lines_fvOptionsOutput.append("    type            scalarSemiImplicitSource;\n")
        lines_fvOptionsOutput.append("    active          true;\n")
        lines_fvOptionsOutput.append("    scalarSemiImplicitSourceCoeffs\n")
        lines_fvOptionsOutput.append("    {\n")
        lines_fvOptionsOutput.append("        timeStart       0;\n")
        lines_fvOptionsOutput.append("        duration        10000;\n")
        lines_fvOptionsOutput.append("        selectionMode   cellZone;\n")
        lines_fvOptionsOutput.append("        cellZone	      sourcePolVol"+str(i+1)+";\n")
        lines_fvOptionsOutput.append("        volumeMode      absolute;\n")
        lines_fvOptionsOutput.append("        injectionRateSuSp\n")
        lines_fvOptionsOutput.append("        {\n")
        lines_fvOptionsOutput.append("	  	      s"+str(i+1)+"	       ("+str(valeurs_polluant_list[i])+" 0);\n")
        lines_fvOptionsOutput.append("        }\n")
        lines_fvOptionsOutput.append("    }\n")
        lines_fvOptionsOutput.append("}\n\n")

        
    for i in range(16,len(lines_fvOptionsInput)):
        lines_fvOptionsOutput.append(lines_fvOptionsInput[i])
    
    fvOptions_file_output=open(fvOptionsOutput, "w")
    for i in range(0,len(lines_fvOptionsOutput)):
        fvOptions_file_output.write(str(lines_fvOptionsOutput[i]))   
    fvOptions_file_output.close()    

    #################################################  
    ### ### ### END MODIFYING FVOPTIONS   ### ### ###
    ################################################# 
    
    ###################################################################    
    ### ### ### COPYING ALLRUNPARALLELMESHING + RUNNING IT  ### ### ###
    ###################################################################    
    os.rename(directory+"/system/controlDict.construct",directory+"/system/controlDict")     
    os.rename(directory+"/system/decomposeParDict.construct",directory+"/system/decomposeParDict")  

    print("  - changement du fichier allrunParallelMeshing") 
    
    shutil.copyfile(path_script_absolute+"/allrunParallelMeshing",directory+"/allrunParallelMeshing")
    #Lecture all run Parallel Meshing
    allrunParallelMeshingFile=open(directory+"/allrunParallelMeshing","r")
    allrunParallelMeshing_lines=allrunParallelMeshingFile.readlines()
    allrunParallelMeshingFile.close()
    
    allrunParallelMeshing_lines[12]="mpirun -np "+str(nbProcConstruct)+" snappyHexMesh -parallel >> log.5_SnappyHexMesh\n"
    if(snappy_enable=="true"):
        value=2
    else:
        value=1
    allrunParallelMeshing_lines[14]="cp -r "+str(value)+"/polyMesh constant/ \n"
    allrunParallelMeshing_lines[16]="rm -r "+str(value)+" \n"
    allrunParallelMeshing_lines[23]="	cp -a "+str(value)+"/polyMesh/. constant/polyMesh/ \n"
    allrunParallelMeshing_lines[24]="	rm -r "+str(value)+" \n"
    

    allrunParallelMeshingFile=open(directory+"/allrunParallelMeshing","w")
    print(directory)
    for i in range(0,len(allrunParallelMeshing_lines)):
        allrunParallelMeshingFile.write(str(allrunParallelMeshing_lines[i]))
    allrunParallelMeshingFile.close()

    print("           maillage en cours...")
    with cd(str(directory)):
        if(multiSetStl==False):
            if(rectangle_length[0]==0 or rectangle_length[1]==0):
                if(angle !=0 or angle !=360):
            
                    surfaceTransformPointDict_file=open(directory+"/surfaceTransformPointDict","w")
                    os.system(str("chmod u+x "+directory+"/surfaceTransformPointDict"))
                    surfaceTransformPointDict_file.write("#!/bin/bash\n")
                    surfaceTransformPointDict_file.write("#cd ${0%/*} || exit 1\n\n")
                    surfaceTransformPointDict_file.write(". $WM_PROJECT_DIR/bin/tools/RunFunctions\n")
                    surfaceTransformPointDict_file.write("application='getApplication'\n")
                    surfaceTransformPointDict_file.write("source /opt/openfoam5/etc/bashrc\n\n")
                    surfaceTransformPointDict_file.write("surfaceTransformPoints -translate '("+str(-transX)+" "+str(-transY)+" 0)' "+directory+"/constant/triSurface/wallGround.stl"+" "+directory+"/constant/triSurface/wallGround.stl"+"\n")
                    surfaceTransformPointDict_file.write("surfaceTransformPoints -rotate '((1 0 0)("+str(round(-1*cos( - angleRadian),9))+" "+str(round(-1*sin( - angleRadian),9))+" 0))' "+directory+"/constant/triSurface/wallGround.stl"+" "+directory+"/constant/triSurface/wallGround.stl"+"\n")
                    surfaceTransformPointDict_file.write("surfaceTransformPoints -translate '("+str(transX)+" "+str(transY)+" 0)' "+directory+"/constant/triSurface/wallGround.stl"+" "+directory+"/constant/triSurface/wallGround.stl"+"\n")
                    surfaceTransformPointDict_file.close()
                    subprocess.call("./surfaceTransformPointDict")
                    
        os.system("chmod u+x allrunParallelMeshing")
        subprocess.call("./allrunParallelMeshing")
    print("           ...fin du maillage")
    
    os.rename(directory+"/system/controlDict",directory+"/system/controlDict.construct")
    os.rename(directory+"/system/controlDict.final",directory+"/system/controlDict")
    os.rename(directory+"/system/decomposeParDict",directory+"/system/decomposeParDict.construct")
    os.rename(directory+"/system/decomposeParDict.run",directory+"/system/decomposeParDict")
    #######################################################################    
    ### ### ### END COPYING ALLRUNPARALLELMESHING + RUNNING IT  ### ### ###
    #######################################################################   
    
    ##########################################    
    ### ### ### MODYFING BOUNDARY  ### ### ###
    ##########################################
    
    print("  - changement du fichier boundary")
    boundary=directory+"/constant/polyMesh/boundary"
    boundary_file=open(boundary,"r")
    lines_boundary=boundary_file.readlines()
    boundary_file.close()
    os.remove(str(directory+"/constant/polyMesh/boundary"))
    
    save_line = list()
    for i in range(0,len(lines_boundary)):
        if("inletPol" in lines_boundary[i]):
            lines_boundary[i+2]="        type            wall;\n"
            save_line.append(i+3)
    
#    for i in range(0,len(save_line)):
#        del(lines_boundary[save_line[i]])
        
    boundary_file_output=open(boundary,"w")
    for i in range(0,len(lines_boundary)):
        boundary_file_output.write(str(lines_boundary[i]))
    boundary_file_output.close()
    
    #############################################    
    ### ### ### END MODYFING BOUNDARY ### ### ###
    #############################################
    
    
                        #################################################
    ##################  ### ### ### END OF MODYFYING CONSTANT ### ### ### ########################################################################
                        #################################################
    
                        #######################################################
    ##################  ### ### ### CREATING VELOCITIES DIRECTORIES ### ### ### ########################################################################
                        #######################################################
    
    print("création des dossiers vitesses")  
    

    for i in range(0,nb_vitesses):
        
        uStar=K*float(vitesses_list[i])/log((10+z0Inlet)/z0Inlet)
        uRef=round(uStar/K*log((zRef+z0Inlet)/z0Inlet),5)

        #Decimal sert à passer en notation scientifique et le '%.4E' permet de récupérer les 4 premières valeurs      
        kInternal='%.4E' % Decimal(turbulenceComputationRichards(z0Inlet,zRef,zmax,uRef)[0])
        epsilonInternal='%.4E' % Decimal(turbulenceComputationRichards(z0Inlet,zRef,zmax,uRef)[1]) 
        
        nomDirV=str(vitesses_list[i])
        print("  - création du dossier"+"/V_"+str(nomDirV))
        ### CREATING VELOCITIES DIRECTORIES
        try:
            os.makedirs(str(directory+"/V_"+str(vitesses_list[i])))
        except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                    
        ### CHANGING ABLConditionsInlet File ###    
        copy(str(directory+"/0/"),str(directory+"/V_"+nomDirV+"/0"))
        
        ABLConditionsInlet_file=open(str(directory+"/V_"+nomDirV+"/0/include/ABLConditionsInlet"),"r")
        lines_ABLConditionsInlet=ABLConditionsInlet_file.readlines()
        ABLConditionsInlet_file.close()
        os.remove(str(directory+"/V_"+nomDirV+"/0/include/ABLConditionsInlet"))
        
        initialConditions_file=open(str(directory+"/V_"+nomDirV+"/0/include/initialConditions"),"r")
        lines_initialConditions=initialConditions_file.readlines()
        initialConditions_file.close()
        os.remove(str(directory+"/V_"+nomDirV+"/0/include/initialConditions"))

        ###CHANGING TURBULENCE###
        print("       changement de la turbulence k et epsilon : "+"/V_"+str(vitesses_list[i]))
        
        lines_ABLConditionsInlet[8]="Uref                 "+str(uRef)+";\n"
        lines_ABLConditionsInlet[9]="Zref                 "+str(zRef+zmin_inlet)+";\n"
        lines_ABLConditionsInlet[12]="z0                   "+str(z0Inlet)+";\n"
        lines_ABLConditionsInlet[13]="zGround              "+str(zmin_inlet)+";\n"
        
        lines_initialConditions[10]="turbulentKE          "+str(kInternal)+";\n"
        lines_initialConditions[11]="turbulentEpsilon     "+str(epsilonInternal)+";\n"        
     
        ### CHANGING INTERNAL FIELD DEPENDING ON ANGLE ### /!\ EFFICIENCY COULD BE IMPROVED IF DONE IN 0 BECAUSE HERE IT IS DONE nb_velocities TIMES INSTEAD OF ONCE BUT EASIER SINCE IT REWRITE 0 file 
        if(angle != 0 or angle !=360):
            print("       changement orientation inlet et outlet à cause de l'angle pour: "+"/V_"+str(vitesses_list[i]))
            lines_ABLConditionsInlet[11]="flowDir              ("+ str(round(-1*cos(rad90 - angleRadian),5)) +" "+ str(round(-1*sin(rad90 - angleRadian),5))+" 0"+");\n"
            lines_initialConditions[8]="flowVelocity         (" + str(round(-1*cos(rad90 - angleRadian),5)) +" "+ str(round(-1*sin(rad90 - angleRadian),5))+" 0"+");\n"
        
        ABLConditionsInlet_file=open(str(directory+"/V_"+nomDirV+"/0/include/ABLConditionsInlet"),"w")             
        initialConditions_file=open(str(directory+"/V_"+nomDirV+"/0/include/initialConditions"),"w")
        
        for j in range(0,len(lines_ABLConditionsInlet)):
            ABLConditionsInlet_file.write(str(lines_ABLConditionsInlet[j]))
        ABLConditionsInlet_file.close()
        
        for j in range(0,len(lines_initialConditions)):
            initialConditions_file.write(str(lines_initialConditions[j]))
        initialConditions_file.close() 
        
        ### COPYING CONSTANT AND SYSTEM INTO VELOCITIES DIRECTORIES ###
        copy(directory+"/constant/",directory+"/V_"+nomDirV+"/constant")
        copy(directory+"/system/",directory+"/V_"+nomDirV+"/system")
        if (2.5 < float(vitesses_list[i]) and float(vitesses_list[i]) < 4.0):
            control_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict"),"r")
            lines_control=control_file.readlines()
            control_file.close()  
            lines_control[25]="endTime         600;\n"
            control_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict"),"w")
            for j in range(0,len(lines_control)):
                control_file.write(lines_control[j])
            control_file.close()
            
            control_Probes_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict.probes"),"r")
            lines_controlProbes=control_Probes_file.readlines()
            control_Probes_file.close()  
            lines_controlProbes[21]="startTime       600;\n"            
            lines_controlProbes[25]="endTime         700;\n"
            control_Probes_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict.probes"),"w")
            for j in range(0,len(lines_control)):
                control_Probes_file.write(lines_controlProbes[j])
            control_Probes_file.close()
            
        if (4.0 <= float(vitesses_list[i])):
            control_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict"),"r")
            lines_control=control_file.readlines()
            control_file.close()  
            lines_control[25]="endTime         400;\n"
            control_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict"),"w")
            for j in range(0,len(lines_control)):
                control_file.write(lines_control[j])
            control_file.close()
            
            control_Probes_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict.probes"),"r")
            lines_controlProbes=control_Probes_file.readlines()
            control_Probes_file.close()  
            lines_controlProbes[21]="startTime       400;\n"            
            lines_controlProbes[25]="endTime         500;\n"
            control_Probes_file=open(str(directory+"/V_"+nomDirV+"/system/controlDict.probes"),"w")
            for j in range(0,len(lines_controlProbes)):
                control_Probes_file.write(lines_controlProbes[j])
            control_Probes_file.close() 
    
    shutil.rmtree(directory+"/constant/")
    shutil.rmtree(directory+"/system/")
    shutil.rmtree(directory+"/0/")
    
    print(" ")
    print(" ")
    
    if(int(angle) < 100):
        os.rename(dirEtude+"/"+"D_"+str(angle),dirEtude+"/"+"D_0"+str(angle))
    if(int(angle) < 10):
        os.rename(dirEtude+"/"+"D_0"+str(angle),dirEtude+"/"+"D_00"+str(angle))
        
print("FIN DU SCRIPT")
