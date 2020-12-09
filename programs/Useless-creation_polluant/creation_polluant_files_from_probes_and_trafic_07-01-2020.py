#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:43:39 2019

@author: jurado
"""

import os,errno
import numpy as np
import pandas as pd
import argparse
import colormap as cm
from PIL import Image

# fonction permettant de passer des NOx au NO2
def Derwent_Middleton_function(x):
    """
    x est la valeur de NOx
    """
    A=np.log10(x/1.91)
    if(x<17.2):
        f=0.723*x
    else:
        f=(2.166-x/1.91*(1.236-3.348*A+1.933*A**2-0.326*A**3))*1.91
    return f

def makeDirectory(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

#########################################################################################################################################
#                                                     Arguments du programme                                                            #
#########################################################################################################################################


parser = argparse.ArgumentParser(description="Determine mean pollution for each direction and mean annual pollution")

parser.add_argument('-p_pol_fond',type=str, help='path to background pollution file')
parser.add_argument('-p_emission',type=str, help='path to the emission file')
parser.add_argument('-p_simu',type=str, help='path to probes from simulations')
parser.add_argument('-p_output',type=str, help='path for the results')

args = parser.parse_args()

path_fond_pollution=args.p_pol_fond
path_emissions=args.p_emission
path_simulations=args.p_simu
path_output_simulations=args.p_output


#Lecture du fichier contenant les informations sur la pollution de fond
with open(path_fond_pollution,"r") as input_file :
    input_lines=input_file.readlines()

input_dictionary=dict()

for line in input_lines:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").replace("\t","").split(":")
        input_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue

#Valeur de la pollution de fond des différentes espèces chimiques polluant 
NOx=float(input_dictionary.get('"NOx"'))
NO2=float(input_dictionary.get('"NO2"'))
PM10=float(input_dictionary.get('"PM10"'))
PM2_5=float(input_dictionary.get('"PM2.5"'))

#Liste des simulations
simulation_names=sorted(os.listdir(path_simulations))

#Liste des sources de pollution - Pour l'instant qu'une seule source est supporté
emission_names=sorted([f for f in os.listdir(path_emissions) if os.path.isfile(os.path.join(path_emissions,f))])

list_df_emission=list()
key="Pollutant [-]"

for i,emission_name in enumerate(emission_names):
    if(i==0):
        df_polluant=pd.read_csv(os.path.join(path_emissions,emission_name),sep=",")
        df_polluant["Emissions [µg/s]"].astype(float)
        pd.DataFrame({"NO2":"NO2","length": 1.3}, index=[3])
        df_polluant.rename(columns={"Emissions [µg/s]":emission_name.split("_")[1].replace(".csv","")+" [µg/s]"},inplace=True)
    else:
        df_old=pd.read_csv(os.path.join(path_emissions,emission_name),sep=",")
        df_old["Emissions [µg/s]"].astype(float)
        df_old.rename(columns={"Emissions [µg/s]":emission_name.split("_")[1].replace(".csv","")+" [µg/s]"},inplace=True)
        df_polluant=pd.merge(df_polluant,df_old,on=key)

#df_normalised=df_main.iloc[:,1:].div(df_main.iloc[:,1:].max(axis=1), axis=0)
#print(df_normalised)

for simulation_name in simulation_names:
    print(os.path.join(path_simulations,simulation_name))
    print('determining polluants for file "'+simulation_name+'" :')
    df_simu=pd.read_csv(os.path.join(path_simulations,simulation_name),sep=",",dtype="float64")
    
    
    
    for index,polluant in df_polluant.iterrows(): 
        df_copy=df_simu.copy()
        #data=df_simu.iloc[:,3:] 
        if(float(input_dictionary.get('"'+polluant.iloc[0]+'"'))>=0):
            print("\t-> "+str(polluant.iloc[0])+" * emission: "+str(polluant.iloc[1])+" * fond: "+input_dictionary.get('"'+polluant.iloc[0]+'"'))
            #df_lama=df_simu.drop(['x','y','z'], axis=1)
            print(df_copy.iloc[:,3:])
            df_copy.iloc[:,3:] *= float(polluant.iloc[1])
            df_copy.iloc[:,3:] += float(input_dictionary.get('"'+polluant.iloc[0]+'"'))
            print(df_copy.iloc[:,3:])
            #print(df_simu.iloc[:,3:])
            hauteur=float(simulation_name.split("_")[1].replace(".csv","").replace("m",""))
            if(hauteur<100 and hauteur > 10):
                hauteur="0"+str(hauteur)
            elif(hauteur<10 and hauteur >0):
                hauteur="00"+str(hauteur)
            
            if(polluant.iloc[0]=="NOx"):
                print("\t-> "+str("NO2")+" * emission: "+str(polluant.iloc[1])+" * fond: "+input_dictionary.get('"NO2"'))
                
                df_no2=df_simu.copy()
                for i in range(3,len(df_no2.columns)):
                    name=df_no2.columns[i]
                    df_no2[name]=df_no2[name].apply(lambda x : Derwent_Middleton_function(x))
                    df_no2[name] *= float(polluant.iloc[1])
                    df_no2[name] += float(input_dictionary.get('"NO2"'))
                makeDirectory(os.path.join(path_output_simulations,"NO2"))
                df_no2.to_csv(os.path.join(path_output_simulations,"NO2",str(polluant.iloc[0]).replace("x","2")+"_"+hauteur+"m.csv"),index=False)
            
            makeDirectory(os.path.join(path_output_simulations,str(polluant.iloc[0])))
            df_copy.to_csv(os.path.join(path_output_simulations,str(polluant.iloc[0]),str(polluant.iloc[0])+"_"+hauteur+"m.csv"),index=False)
    print("") 
            
                
                

        
    