#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:03:30 2019

@author: jurado
"""

import os, errno
import numpy
import pandas as pd
import scipy.integrate as integrate
from math import *
import argparse

def makeDir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

parser = argparse.ArgumentParser(description="Determine mean pollution for earch direction and mean annual pollution")


parser.add_argument('-p_config',type=str, help='path to config file')
parser.add_argument('-p_freq',type=str, help='path to frequency file')
parser.add_argument('-p_sigmo',type=str, help='path to sigmoid file')
parser.add_argument('-p_working',type=str, help='path to working directory')
parser.add_argument('-p_probes_treated',type=str, help='path to working directory')

args = parser.parse_args()

p_config=args.p_config.replace(" ","")
p_freq=args.p_freq.replace(" ","")
p_sigmo=args.p_sigmo.replace(" ","")
p_working=args.p_working.replace(" ","")
p_probes_treated=args.p_probes_treated.replace(" ","")   

p_preProcessing=os.path.join(p_working,"preProcessingDict")
p_pollution_fond=os.path.join(p_working,"pollution_fond")

########################### Lecture fu fichier config ###########################
#################################################################################   

with open(p_config,"r") as config_file :
    lines_config=config_file.readlines()

config_dictionary=dict()
for line in lines_config:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        config_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue

     
v_seuil_min=float(config_dictionary.get('"v_seuil_min"')) #vitesse limite pour laquelle on considère que la turbulence du vent est compensé par la turbulence des voitures et/ou de la température
v_seuil_max=float(config_dictionary.get('"v_seuil_max"'))#vitesse pour laquelle on considère que la pollution devient négligeable 
ratio_for_max_speed=float(config_dictionary.get('"ratio_for_max_speed"'))
v_infinity=v_seuil_max*ratio_for_max_speed
#################################################################################


########################### Lecture du fichier preProcessing ###########################
########################################################################################

with open(p_preProcessing,"r") as preProcessingDict_file :
    lines_preProcessingDict=preProcessingDict_file.readlines()

preProcessingDict_dictionary=dict()
for line in lines_preProcessingDict:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        preProcessingDict_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue
    
directions_original=preProcessingDict_dictionary.get('"angles"').split(",")

for i in range(len(directions_original)):
    if(int(directions_original[i]) < 100):
        directions_original[i]="0"+directions_original[i]
    if(int(directions_original[i]) < 10):
        directions_original[i]="0"+directions_original[i]

vitesse_calculee=float(preProcessingDict_dictionary.get('"speeds"').split(",")[0])
pas=int(preProcessingDict_dictionary.get('"pas_angle"'))
#################################################################################


########################### Lecture du fichier de pollution de fond ###########################
###############################################################################################

with open(p_pollution_fond, "r") as pollution_fond_file :
    lines_pollution_fond=pollution_fond_file.readlines()
    
pollution_fond_dictionary=dict()
for line in lines_pollution_fond:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        pollution_fond_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue
#################################################################################


print("nombre de directions: ",len(directions_original))

#Liste les différents polluants déterminé par meanMultipleSourcesAndConcatenation
polluant_directories=[f for f in sorted(os.listdir(p_probes_treated)) if os.path.isdir(os.path.join(p_probes_treated,f)) ] 


### RECUPERE LES COORDONNNEES DES PROBES ###
with open(os.path.join(p_probes_treated,"probesCoord"), "r") as probes :
    probesCoord = [x.replace("\n","") for x in probes.readlines()]
    
with open(os.path.join(p_probes_treated,"verifProbes"), "r") as verif :
    verifProbes = [x.replace("\n","") for x in verif.readlines()]

for polluant in polluant_directories:
    print(" ")
    print("calcul pour le polluant:",polluant)
    directory=os.path.join(p_probes_treated,polluant,"concatenatedSources")
    
    pollution_fond=float(pollution_fond_dictionary.get('"'+polluant+'"'))

    ################################################################################# Vérifie si la direction 0 a été donnée et auquel cas la transforme en 360 #################################################################################
    directions=directions_original
    for i in range(0,len(directions_original)):
        if(directions_original[i]=="0" or directions_original[i]=="00" or directions_original[i]=="000" or directions_original[i]=="360"):  
            try:
                os.rename(directory+"/s_D_0_V_"+str(vitesse_calculee)+"_treated",directory+"/s_D_"+str(360)+"_V_"+str(vitesse_calculee)+"_treated")
            except:
                try:
                    os.rename(directory+"/s_D_00_V_"+str(vitesse_calculee)+"_treated",directory+"/s_D_"+str(360)+"_V_"+str(vitesse_calculee)+"_treated")
                except:
                    try:
                        os.rename(directory+"/s_D_000_V_"+str(vitesse_calculee)+"_treated",directory+"/s_D_"+str(360)+"_V_"+str(vitesse_calculee)+"_treated")
                    except:
                        os.rename(directory+"/s_D_360_V_"+str(vitesse_calculee)+"_treated",directory+"/s_D_"+str(360)+"_V_"+str(vitesse_calculee)+"_treated")
                        
            directions[i]="360"
    
    directions.sort()
    ###################################################################################################################################################################################################################################################
    
    
    #Creating directory to store
    makeDir(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_moyennes_par_direction"))
    makeDir(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_maximales_par_direction"))      
    makeDir(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_moyennes_annuelles"))
    makeDir(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_maximales_annuelles"))
    
    ### LIST NEEDED TO STOCK RESULTS ###
    resultCmoy=list()
    resultCmoyYear=list()
    sumFreqMoyYear=list()
    sumFreqMaxYear=list()
    listCmax=list()
    moyMoyFreqYear=list()
    moyMaxFreqYear=list()
    l=0
    
    
    
    
    print("Calcul de la concentration moyenne :")
    
    ### LIT LES FICHIERS AVEC LES PARAMETRES POUR LES DIRECTIONS (valeurs des coeff des sigmoides et fréquences d'apparition) ### 
    frequencesVent=open(p_freq,"r")
    lines_frequenceVent=frequencesVent.readlines()
    frequencesVent.close()
    paramSigm=open(p_sigmo,"r")
    paramSigm_lines=paramSigm.readlines()
    paramSigm.close()
    
    ### LIT LES FICHIERS POUR PRENDRE EN COMPTE LES DIVERSES LONGUEUR DE ROUTE
    #permet de prendre en compte les différentes longueurs qu'une route peut avoir selon la distance à la route
#    df_ratio_length=pd.read_csv(os.path.join(p_working,"ratio_road_length.csv"))
#    for column in df_ratio_length.columns :
#        if("#" in column):
#           df_ratio_length=df_ratio_length.drop(column,axis=1)
#    df_ratio_length = df_ratio_length.set_index(["angle"])
    
           
    for l,direction in enumerate(directions):
    
        print(" ")
        print("      direction : D_"+str(direction)+" #############################################################")
        print(" ")
        
        ### ECRIT LES ENTETES AVEC LES DIRECTIONS ###
        if(l==0):
            resultCmoy.append("D_"+str(direction))
            listCmax.append("D_"+str(direction))
            sumFreqMoyYear.append(str("Somme à l'année de la moyenne"))
            sumFreqMaxYear.append(str("Somme à l'année du Max"))
        else:
            resultCmoy[0]=str(resultCmoy[0])+","+"D_"+str(direction)
            listCmax[0]=str(listCmax[0])+","+"D_"+str(direction)
        
    
    
        ############################################################################################################################################
        ##########################         READING AND CORRECTING WIND FREQUENCY FOR GIVEN DIRECTION AND STEP         ##############################
        ############################################################################################################################################
        
        ### CHERCHE LES PARAMETRES POUR LA SIGMOIDE POUR LA DIRECTION DE LA BOUCLE ###        
    
        for i in range(1,len(paramSigm_lines)):
                    if (str(direction) in paramSigm_lines[i]):
                        ligne_param=i
        
        
        paramSigm_list=paramSigm_lines[ligne_param].split(",")
        alpha=float(paramSigm_list[1])
        Beta1=float(paramSigm_list[2])
        gamma1=float(paramSigm_list[4])
        Beta2=float(paramSigm_list[3])
        gamma2=float(paramSigm_list[5])
        
        ### CHERCHE LA FREQUENCE DU VENT POUR LA DIRECTION DE LA BOUCLE ###  
        freqInterSup=0
        freqInterInf=0    
        directionTot=len(lines_frequenceVent)
    
        for i in range(0,len(lines_frequenceVent)):
    
            if (str(direction) in lines_frequenceVent[i]):            
                ### CALCUL MOYENNE S ADAPTE AU SELON LE PAS DE L ANGLE CHOISI POUR L ETUDE                
                freq=float(lines_frequenceVent[i].split(",")[1])
                print("        * fréquence du vent : "+str(freq))
                print("")
                if(pas>20):
                    for j in range(1,int(pas/20)):
                        lineFreqSup = i+j
                        lineFreqInf = i-j
                        
                        if ( lineFreqSup > directionTot-1): # Prend en compte qu'on est dans un cercle
                            lineFreqSup=lineFreqSup-directionTot
                        if (lineFreqInf < 0):
                            lineFreqInf=directionTot-abs(lineFreqInf)
                        freqInterSup=freqInterSup+float(lines_frequenceVent[lineFreqSup].split(",")[1])
                        freqInterInf=freqInterInf+float(lines_frequenceVent[lineFreqInf].split(",")[1])
    
                        print("         vent réparti: "+str(lines_frequenceVent[lineFreqInf].split(",")[0])+"-"+str(lines_frequenceVent[lineFreqSup].split(",")[0]))
                    linePreviousDir=i-int(pas/20)
                    lineNextDir=i+int(pas/20)
    
                    if ( linePreviousDir < 0):
                        linePreviousDir=directionTot-abs(linePreviousDir)
                    if ( lineNextDir > directionTot-1):
                        lineNextDir=lineNextDir-directionTot
    
                    freq=freq+freqInterInf*freq/(freq+float(lines_frequenceVent[linePreviousDir].split(",")[1]))+freqInterSup*freq/(freq+float(lines_frequenceVent[lineNextDir].split(",")[1]))
                    
                    print("        * fréquence réajustée: "+str(freq))
                    print("        * vent connu adjacent supérieur: "+str(lines_frequenceVent[linePreviousDir].split(",")[0]))
                    print("        * vent connu adjacent inférieur: "+str(lines_frequenceVent[lineNextDir].split(",")[0]))
        
        
        
        ############################################################################################################################################
        moyenne_simulation_probes=list()
        
        with open(directory+"/s_D_"+str(direction)+"_V_"+str(vitesse_calculee)+"_treated", "r") as s :
            moyenne_simulation_probes = [float(x) for x in s.readlines()[1:]]
    
        
#        print("        -\ ratio de la route : ",df_ratio_length.loc[float(direction)][0])
        print("")
        #débit massique surface qui correspond à c*v avec c la concentration en un point et v la vitesse à 10 d'une simu
        ### Calculs des intégrales de la fréquence des vitesses par direction sur la gamme [0,vmin], [vmin,vmax], [vmax,ratio*vmax]
        integrale_frequence_full=integrate.quad(lambda x: alpha*(-1+1/(1+Beta1*exp(-1*gamma1*(x)))+1/(1+Beta2*exp(gamma2*(x)))),0,v_infinity)[0]
        integrale_frequence_low_speed=integrate.quad(lambda x: alpha*(-1+1/(1+Beta1*exp(-1*gamma1*(x)))+1/(1+Beta2*exp(gamma2*(x)))),0,v_seuil_min)[0]
        integrale_frequence_mid_speed=integrate.quad(lambda x: alpha*(-1+1/(1+Beta1*exp(-1*gamma1*(x)))+1/(1+Beta2*exp(gamma2*(x)))),v_seuil_min,v_seuil_max)[0]    
        integrale_frequence_high_speed=integrate.quad(lambda x: alpha*(-1+1/(1+Beta1*exp(-1*gamma1*(x)))+1/(1+Beta2*exp(gamma2*(x)))),v_seuil_max,v_infinity)[0]
        
#        road_length=df_ratio_length.loc[float(direction)][0]
        
        integrale_frequence_mid_speed_inverse_speed=integrate.quad(lambda x: 1/x*alpha*(-1+1/(1+Beta1*exp(-1*gamma1*(x)))+1/(1+Beta2*exp(gamma2*(x)))),v_seuil_min,v_seuil_max)[0]
        
        print("        -} part des fréquences entre 0 et la vitesse min                     : ",round(integrale_frequence_low_speed/integrale_frequence_full*100),"%")
        print("        -} part des fréquences entre la vitesse min et la vitesse max        : ",round(integrale_frequence_mid_speed/integrale_frequence_full*100),"%")
        print("        -} part des fréquences entre la vitesse max et "+str(ratio_for_max_speed)+" fois la vitesse max : ",round(integrale_frequence_high_speed/integrale_frequence_full*100),"%")
        print("")
        
        for j,concentration in enumerate(moyenne_simulation_probes):
  
            #print(str(j+1)+" "+str(typeFunction[j+1].split(",")[col_dir])+" "+str(coeff[j+1].split(",")[col_dir]))
            if(j==round(len(moyenne_simulation_probes)/4,0) or j==round(len(moyenne_simulation_probes)/2,0) or j==round(len(moyenne_simulation_probes)*3/4,0) or j==round(len(moyenne_simulation_probes)*4/4-1,0)):
                print("            -> avancement sur les probes : "+str(round(j/len(moyenne_simulation_probes)*100,0))+" %")
            
            if (concentration>0):
                dms_ref=vitesse_calculee*concentration
                Cmax=dms_ref/v_seuil_min
                Cmin=dms_ref/v_seuil_max
                integrale_frequence_low_speed_concentration = Cmax*integrale_frequence_low_speed
                integrale_frequence_high_speed_concentration = Cmin*integrale_frequence_high_speed
                integrale_frequence_mid_speed_concentration=dms_ref*integrale_frequence_mid_speed_inverse_speed
                integral_tot = integrale_frequence_low_speed_concentration+integrale_frequence_mid_speed_concentration+integrale_frequence_high_speed_concentration

                
                
                #Récupère le ratio associé à la route pour augmenter la concentration 
                C=integral_tot/integrale_frequence_full#*road_length
                Cmax=Cmax#*road_length
            else:
                C=0
                Cmax=0
                
            if(l==0):
                resultCmoy.append(str(C+pollution_fond))
                listCmax.append(str(Cmax+pollution_fond))
                sumFreqMoyYear.append(C*freq)
                sumFreqMaxYear.append(Cmax*freq)
            else:
                resultCmoy[j+1]=str(resultCmoy[j+1])+","+str(C+pollution_fond)
                listCmax[j+1]=str(listCmax[j+1])+","+str(Cmax+pollution_fond)
                sumFreqMoyYear[j+1]=sumFreqMoyYear[j+1]+C*freq
                sumFreqMaxYear[j+1]=sumFreqMaxYear[j+1]+Cmax*freq
            
    
#    print(resultCmoy[0])
#    print(resultCmoy[1])
#    print(listCmax[0])
#    print(listCmax[1])
#    print(verifProbes[0])
#    print(verifProbes[1])
    moyMoyFreqYear=sumFreqMoyYear
    moyMaxFreqYear=sumFreqMaxYear
    
    moyMoyFreqYear[0]="Cmoy"
    moyMaxFreqYear[0]="Cmax"
    for i in range(0, len(moyMoyFreqYear)-1):
        moyMoyFreqYear[i+1]=moyMoyFreqYear[i+1]/100+pollution_fond
        moyMaxFreqYear[i+1]=moyMaxFreqYear[i+1]/100+pollution_fond   
        
        
    ### ECRIT LES DONNEES Cmoyen ET Cmax ###
        ### ECRIT LES ENTETES
    l=0 
    for i in range(1,len(resultCmoy)):
    
        if(probesCoord[i].split(",")[2] != probesCoord[i-1].split(",")[2]):
            if(l>0):
                cmoy_output.close()
                cmax_output.close()
                cmoyMoyYear_output.close()
                cmoyMaxYear_output.close() 
            z=probesCoord[i].split(",")[2]
            cmoy_output=open(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_moyennes_par_direction","Cmoy_par_direction_"+str(z)+"m.csv"),"w")
            cmax_output=open(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_maximales_par_direction","Cmax_par_direction_"+str(z)+"m.csv"),"w")
            cmoyMoyYear_output=open(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_moyennes_annuelles","Cmoy_annuelles_"+str(z)+"m.csv"),"w")
            cmoyMaxYear_output=open(os.path.join(p_probes_treated,polluant,"concentrations_ponderees","concentrations_maximales_annuelles","Cmax_annuelles_"+str(z)+"m.csv"),"w")
                
            cmoy_output.write(str(probesCoord[0])+","+str(resultCmoy[0])+"\n")
            cmax_output.write(str(probesCoord[0])+","+str(listCmax[0])+"\n")
            cmoyMoyYear_output.write(str(probesCoord[0])+","+str(moyMoyFreqYear[0])+"\n")
            cmoyMaxYear_output.write(str(probesCoord[0])+","+str(moyMaxFreqYear[0])+"\n") 
            
            l=l+1
            
        if(verifProbes[i-1]=="True"): # Verifie que le point n'est pas issu d'un batiment (qu'il valait moins de -1e+200)
            cmoy_output.write(str(probesCoord[i])+","+str(resultCmoy[i])+"\n")
            cmax_output.write(str(i)+","+str(probesCoord[i])+","+str(listCmax[i])+"\n")
            cmoyMoyYear_output.write(str(probesCoord[i])+","+str(moyMoyFreqYear[i])+"\n")
            cmoyMaxYear_output.write(str(probesCoord[i])+","+str(moyMaxFreqYear[i])+"\n")
            
    cmoy_output.close()
    cmax_output.close()
    cmoyMoyYear_output.close()
    cmoyMaxYear_output.close()
    print(" ")
print("Fin du Script")    
        
        

