#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 10:44:26 2020

@author: jurado
"""
import os,errno
import numpy as np
import argparse

def makeDir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

parser = argparse.ArgumentParser(description="Determine mean pollution for each direction and mean annual pollution")

parser.add_argument('-p_working', type=str, help='path to working directory')
parser.add_argument('-p_output',type=str, help='path to the emission file')

args = parser.parse_args()

working_directory=args.p_working.replace(" ","")
directory_output=args.p_output.replace(" ","")

preprocessingDict_path=os.path.join(directory_output,"preprocessingDict")
directory_input=os.path.join(working_directory,"probes")


directions=["000","040","080","120","160","200","240","280","320"]
vitesse_calculee=1.5
nbSourcePol=4

coeffPollutionPerPol=[5081.6,1687.1,949.9,660.3]

directory_input="/home/jurado/OpenFOAM/jurado-5.0/run/Etude_AiretD/2019_10_Gare/probes"
directory_output="/home/jurado/OpenFOAM/jurado-5.0/run/Etude_AiretD/2019_10_Gare/probes_treated"

probCoord=list()
### RECUPERE LES COORDONNNEES DES PROBES ###
s = open(directory_input+"/s1/s1_D_"+str(directions[0])+"_V_"+str(vitesse_calculee), "r")
s_lines = s.readlines()
s.close()
### trouve la ligne où il y a le string "Time", les probes commencent donc à la ligne d'après
for i in range(0,len(s_lines)):
    if ("Time" in s_lines[i]): # Ce qui sépare les coordonnées des probes à leurs valeurs
        ligne_prob=i+1
probCoord.append("x,y,z")
for i in range(0,ligne_prob-2):
    s_lines_col=s_lines[i].split()
    probCoord.append(str(s_lines_col[3].replace("(",""))+","+str(s_lines_col[4])+","+str(str(s_lines_col[5].replace(")",""))))

nbLineValue=len(s_lines)-ligne_prob

makeDir(directory_output+"/treated")

print("Writing coordinates of probes")
with open(directory_output+"/treated/"+"probesCoord","w") as data_output:            
    [data_output.write(str(probCoord[i])+"\n") for i in range(0,len(probCoord))]


for l,direction in enumerate(directions):
    
    print(" ")
    print("      Direction : D_"+str(direction))
    print(" ")
    moyenne_simulation_probes_sum=list()
    for k in range(1,nbSourcePol+1):     

        sPolluant="s"+str(k)
        print("             Polluant source number :"+sPolluant)
        moyenne_simulation_probes=list()
            
        with open(directory_input+"/"+sPolluant+"/"+sPolluant+"_D_"+str(direction)+"_V_"+str(vitesse_calculee), "r") as s :
            s_lines = s.readlines()
            s.close()
        
        #Initialisation de la liste avec les valeurs de la première ligne    
        line=s_lines[ligne_prob].split()
        line=[float(x) for x in line[1:]] #commence à 1 pour éliminer le premier élément qui est le temps
        
        #Sommation pour chaque temps (i) sur chaque probes (j) 
        for i in range(ligne_prob,len(s_lines)-1):
                line_new=s_lines[i+1].split()
                line=[line[j]+float(line_new[j+1]) for j in range(0,len(line))] 
                
        if(l==0 and k==1):
            verifProbes=[False if x<-10000 else True for x in line]
            with open(directory_output+"/treated/verifProbes","w") as data_output:
                [data_output.write(str(verifProbes[i])+"\n") for i in range(0,len(line))]
                
        line=[x==0.0 if x < 0  else x for x in line ]
        nbLines=len(s_lines)-ligne_prob
        [moyenne_simulation_probes.append(coeffPollutionPerPol[k-1]*line[j]/nbLines) for j in range(0,len(line))] 
        
        makeDir(directory_output+"/severalSources"+"/"+sPolluant)
        with open(directory_output+"/severalSources"+"/"+sPolluant+"/"+sPolluant+"_D_"+str(direction)+"_V_"+str(vitesse_calculee)+"_treated","w") as data_output:
            [data_output.write(str(moyenne_simulation_probes[i])+"\n") for i in range(0,len(line))]
        
        
        
        
                
        if(k==1):
            moyenne_simulation_probes_sum=moyenne_simulation_probes

        else:
            moyenne_simulation_probes_sum=np.add(moyenne_simulation_probes,moyenne_simulation_probes_sum)
    
    with open(directory_output+"/treated/"+"s_D_"+str(direction)+"_V_"+str(vitesse_calculee)+"_treated","w") as data_output:            
        [data_output.write(str(moyenne_simulation_probes_sum[i])+"\n") for i in range(0,len(line))]
              
        
