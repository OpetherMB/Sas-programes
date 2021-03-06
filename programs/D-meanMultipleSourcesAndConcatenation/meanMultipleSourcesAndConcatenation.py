#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 10:44:26 2020

@author: jurado
"""
import os,errno,sys
import numpy as np
import argparse
import pandas as pd

def makeDir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# fonction permettant de passer des NOx au NO2
def Derwent_Middleton_function(x):
    """
    x est la valeur de NOx
    """
    
    if(x<17.2):
        f=0.723*x
    else:
        A=np.log10(x/1.91)
        f=(2.166-x/1.91*(1.236-3.348*A+1.933*A**2-0.326*A**3))*1.91
    return f

#####################################################################################################################
######### Read arguments passed to the script #######################################################################    
#####################################################################################################################

parser = argparse.ArgumentParser(description="Determine mean pollution for each direction and mean annual pollution")
parser.add_argument('-p_working', type=str, help='path to working directory')
parser.add_argument('-p_output',type=str, help='path to the emission file')

args = parser.parse_args()

working_directory=args.p_working.replace(" ","")
directory_output=args.p_output.replace(" ","")

#####################################################################################################################



#####################################################################################################################
######### Read the input files given by user ########################################################################
#####################################################################################################################

### Create path to access the files given by user ###
preProcessingDict=os.path.join(working_directory,"preProcessingDict")
pollution_fond=os.path.join(working_directory,"pollution_fond")
directory_input=os.path.join(working_directory,"probes")

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

### read the angles given by the user and apply a treatment to be of the format XXX (ex: "000" "020" "120") ###
directions=preProcessing_dictionary.get('"angles"').split(",")

for i in range(0,len(directions)):
    if(int(directions[i]) < 100):
        directions[i]="0"+directions[i]
    if(int(directions[i]) < 10):
        directions[i]="0"+directions[i]
                
vitesse_calculee=float(preProcessing_dictionary.get('"speeds"').split(",")[0])
pollutant_emission=float(preProcessing_dictionary.get('"pollutant_emission"'))
ratio_for_roads=preProcessing_dictionary.get('"ratio_for_roads"').replace("\n","")


### Reading and saving into variables pollution_fond ###
with open(pollution_fond, "r") as pollution_fond_file :
    lines_pollution_fond=pollution_fond_file.readlines()

pollution_fond_dictionary=dict()
for line in lines_pollution_fond:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        pollution_fond_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue

#Valeur de la pollution de fond des différentes espèces chimiques polluant 
NOx=float(pollution_fond_dictionary.get('"NOx"'))
NO2=float(pollution_fond_dictionary.get('"NO2"'))
PM10=float(pollution_fond_dictionary.get('"PM10"'))
PM2_5=float(pollution_fond_dictionary.get('"PM2.5"'))

# Check if the value is not -1, if it is, it means that pollutant must be taken into account
pollutant_list=list()
if(NOx>=0):
    pollutant_list.append(["NOx",NOx])
if(NO2>=0):
    pollutant_list.append(["NO2",NO2])
if(PM10>=0):
    pollutant_list.append(["PM10",PM10])
if(PM2_5>=0):
    pollutant_list.append(["PM2.5",PM2_5])

#####################################################################################################################

### Vérifie les éléments dans working dir et ne garde que les dossiers ayant le string "result"
result_directories=[f for f in sorted(os.listdir(working_directory)) if os.path.isdir(os.path.join(working_directory,f)) and "result" in f ] 
nbSourcePol=len(result_directories)
if(len(result_directories)==0):
    print("* * * ERROR : missing result directories, emiCalc program must run before this one * * *")
    sys.exit()
#####################################################################################################################
######## RECUPERE LES COORDONNNEES DES PROBES #######################################################################
#####################################################################################################################

probCoord=list()

with open(directory_input+"/s1/s1_D_"+str(directions[0])+"_V_"+str(vitesse_calculee), "r") as s:
    s_lines = s.readlines()
    
### trouve la ligne où il y a le string "Time", les probes commencent donc à la ligne d'après
for i in range(0,len(s_lines)):
    if ("Time" in s_lines[i]): # Ce qui sépare les coordonnées des probes à leurs valeurs
        ligne_prob=i+1
        
probCoord.append("x,y,z")
for i in range(0,ligne_prob-2):
    s_lines_col=s_lines[i].split()
    probCoord.append(str(s_lines_col[3].replace("(",""))+","+str(s_lines_col[4])+","+str(str(s_lines_col[5].replace(")",""))))

nbLineValue=len(s_lines)-ligne_prob

#####################################################################################################################
### LIT LES FICHIERS POUR PRENDRE EN COMPTE LES DIVERSES LONGUEUR DE ROUTE
#permet de prendre en compte les différentes longueurs qu'une route peut avoir selon la distance à la route
if(ratio_for_roads=="True"):
    df_ratio_length=pd.read_csv(os.path.join(working_directory,"ratio_road_length.csv"))
    for column in df_ratio_length.columns :
        if("#" in column):
           df_ratio_length=df_ratio_length.drop(column,axis=1)
    df_ratio_length = df_ratio_length.set_index(["angle"])
    print()

### Créer le répertoire de sortie ###
makeDir(directory_output)
print("Writing coordinates of probes")
### Ecrit les coordonnées du fichier dans le répertoire de sortie ###
with open(directory_output+"/"+"probesCoord","w") as data_output:            
    [data_output.write(str(probCoord[i])+"\n") for i in range(0,len(probCoord))]
    
    # boucle sur les directions
    for l,direction in enumerate(directions):
        
        
        print(" ")
        print("      Direction : D_"+str(direction))
        print(" ")
        moyenne_simulation_probes_sum=list()
        
        # boucles sur le nombre de sources de polluant
        for k in range(1,nbSourcePol+1):     
    
            sPolluant="s"+str(k)
            print("             Polluant source number :"+sPolluant)
            
            #prise en compte de ratio 
            if(ratio_for_roads=="True"):
                if(direction=="000"):
                    ratio_road_direction=float(df_ratio_length.at[int(360),"inletPol"+str(k)])
                else:
                    ratio_road_direction=float(df_ratio_length.at[int(direction),"inletPol"+str(k)])
                print("             ratio applied for the direction and polluant source :"+str(ratio_road_direction))
            else:
                ratio_road_direction=1
                print("             no ratio road specified, 1 by default")
            #####################################################################################################################
            ### lecture du fichier de pollution issue d'OpenFoam ################################################################
            #####################################################################################################################
            
            with open(directory_input+"/"+sPolluant+"/"+sPolluant+"_D_"+str(direction)+"_V_"+str(vitesse_calculee), "r") as s :
                s_lines = s.readlines()

            #Initialisation de la liste avec les valeurs de la première ligne    
            line=s_lines[ligne_prob].split()
            line=[float(x) for x in line[1:]] #commence à 1 pour éliminer le premier élément qui est le temps
            
            
            #Sommation pour chaque temps (i) sur chaque probes (j) 
            for i in range(ligne_prob,len(s_lines)-1):
                    line_new=s_lines[i+1].split()
                    line=[line[j]+float(line_new[j+1]) for j in range(0,len(line))] 
            
            #valeur qui sert à séparer les probes localisé au niveau des batiments et les autres
            threshold_negative_value=-100000
            if(l==0 and k==1):
                verifProbes=[False if x<threshold_negative_value else True for x in line]
                with open(directory_output+"/verifProbes","w") as data_output:
                    [data_output.write(str(verifProbes[i])+"\n") for i in range(0,len(line))]

            # Si la probe à une valeur négative c'est qu'en réalité elle est faible est oscille autour de 0
            line=[0.0 if x < 0.0  else x for x in line ]
            nbLines=len(s_lines)-ligne_prob
            
            #################################################################################################################################
            
            #lecture du fichier des emissions des sources
            with open(os.path.join(working_directory,"result_"+str(k),"summaryEmission_inletPol"+str(k)+".csv"),"r") as emission_file:
                    emission_lines=emission_file.readlines()[1:]
            
            
            
            for m,pollutant in enumerate(pollutant_list):
    
                print("                    -pollutant:",pollutant[0])
                moyenne_simulation_probes=list()
                if(k==1):
                    makeDir(os.path.join(directory_output,pollutant[0]))
                
                #Vérifie si la pollution est le NO2, si tel est le cas la formule de derwent et Middleton est appliqué au calcul des NOx
                if(pollutant[0]=="NO2"):
                    coeffPollution=float([x.split(",")[1] for x in emission_lines if("NOx" in x)][0])
                    [moyenne_simulation_probes.append(Derwent_Middleton_function(coeffPollution*ratio_road_direction*line[j]/nbLines/pollutant_emission)) for j in range(0,len(line))]
                else:
                    coeffPollution=float([x.split(",")[1] for x in emission_lines if(pollutant[0] in x)][0])
                    [moyenne_simulation_probes.append(coeffPollution*ratio_road_direction*line[j]/nbLines/pollutant_emission) for j in range(0,len(line))]
                
                
                makeDir(os.path.join(directory_output,pollutant[0],"severalSources",sPolluant))
                
                #ouvre un fichier dans lequel il va écrire la valeur de pollution de chaque source pondérées par leurs emissions
                with open(os.path.join(directory_output,pollutant[0],"severalSources",sPolluant,sPolluant+"_D_"+str(direction)+"_V_"+str(vitesse_calculee)+"_treated"),"w") as data_output:
                    data_output.write("c\n")
                    [data_output.write(str(moyenne_simulation_probes[i])+"\n") for i in range(0,len(line))]
                
                #Créer une liste sommant les pollutions pour de chaque source pour chaque pollution 
                if(k==1):
                    moyenne_simulation_probes_sum.append(moyenne_simulation_probes)
        
                else:
                    moyenne_simulation_probes_sum[m]=np.add(moyenne_simulation_probes,moyenne_simulation_probes_sum[m])

        # ecrit les listes sommant chaque source
        for m,pollutant in enumerate(pollutant_list):
            makeDir(os.path.join(directory_output,pollutant[0],"concatenatedSources"))
            with open(os.path.join(directory_output,pollutant[0],"concatenatedSources","s_D_"+str(direction)+"_V_"+str(vitesse_calculee)+"_treated"),"w") as data_output:            
                data_output.write("c\n")
                [data_output.write(str(moyenne_simulation_probes_sum[m][i])+"\n") for i in range(0,len(line))]
     
