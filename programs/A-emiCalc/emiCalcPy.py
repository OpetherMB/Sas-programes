#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:51:28 2019

@author: nreiminger
"""

#Load libraries
import os, errno
import numpy as np
import traficEmissions
import shutil as sh
import argparse


#Function to create directories
def makeDirectory(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
parser = argparse.ArgumentParser(description="Determine the pollution from trafic information")
parser.add_argument('-p_output', type=str, help='path to where the output should be written')
parser.add_argument('-p_input', type=str, help='path to the input file')

args = parser.parse_args()

inputEmi_path=args.p_input
outputDir=args.p_output

inputEmiCalc_list=sorted([ x  for x in os.listdir(inputEmi_path) if("input_emiCalc" in x)])



#Load current working directory
CWD = os.getcwd()

for i,inputEmi in enumerate(inputEmiCalc_list) :
    dirEtude=outputDir+"/result_"+str(i+1)
    print("calcule pour la route n°   : "+str(i+1))
    print("utilisation de la feuille  : "+inputEmi)
    print("")
    #Building computation dictionary
    with open(inputEmi_path+"/"+inputEmi, "r") as input_emiCalc_file :
        lines_input_emiCalc = input_emiCalc_file.readlines()
        
    computation_dictionary = dict()
    for line in lines_input_emiCalc:
        if(line[0] == "\""):
            line_split=line.replace(" ","").replace("\n","").replace("\t","").split(":")
            computation_dictionary.update({line_split[0]:line_split[1].split("#")[0]})
        else:
            continue
    
    input_emiCalc_file.close()
    
    #road name in simulation
    roadNameSimulation = computation_dictionary.get('"nameRoadSimulation"')
    
    #Method selection
    method = computation_dictionary.get('"method"')
    massUnit = computation_dictionary.get('"massUnit"')
    timeUnit = computation_dictionary.get('"timeUnit"')
    
    #Road information
    dist = float(computation_dictionary.get('"dist"')) 
    sloap = "S"+computation_dictionary.get('"sloap"')
    load = "L"+computation_dictionary.get('"load"')
    load_int = int(computation_dictionary.get('"load"'))
    
    #Vehicles information
    stock = int(computation_dictionary.get('"stock"'))
    w_LV = float(computation_dictionary.get('"w_LV"'))
    w_LCV = float(computation_dictionary.get('"w_LCV"'))
    w_B = float(computation_dictionary.get('"w_B"'))
    w_HDT = float(computation_dictionary.get('"w_HDT"'))
    w_L = float(computation_dictionary.get('"w_L"'))
    
    #Cold start information
    cold = int(computation_dictionary.get('"cold"'))
    trip = int(computation_dictionary.get('"trip"'))
    temp = int(computation_dictionary.get('"temp"'))
    forceCold = computation_dictionary.get('"forceCold"')
    speedFC = int(computation_dictionary.get('"speedFC"'))
    
    with open(CWD+"/data/Emep_Emission_Factors_2016/coldStart_LV_LCV_D.csv", "r") as coldLVDFile :
        lines_coldLVDFile = coldLVDFile.readlines()
    coldLVDFile.close()
    
    A_CHR_LV_D_NOx=float(lines_coldLVDFile[1].split(",")[3])
    A_CHR_LCV_D_NOx=A_CHR_LV_D_NOx
    B_CHR_LV_D_NOx=float(lines_coldLVDFile[1].split(",")[4])
    B_CHR_LCV_D_NOx=B_CHR_LV_D_NOx
    
    A_CHR_LV_D_PM=float(lines_coldLVDFile[2].split(",")[3])
    A_CHR_LCV_D_PM=A_CHR_LV_D_PM
    B_CHR_LV_D_PM=float(lines_coldLVDFile[2].split(",")[4])
    B_CHR_LCV_D_PM=B_CHR_LV_D_PM
    
    with open(CWD+"/data/Emep_Emission_Factors_2016/coldStart_LV_LCV_P.csv", "r") as coldLVPFile :
        lines_coldLVPFile = coldLVPFile.readlines()
    coldLVPFile.close()
    
    A_CHR_LV_P_NOx_5_25=float(lines_coldLVPFile[1].split(",")[3])
    B_CHR_LV_P_NOx_5_25=float(lines_coldLVPFile[1].split(",")[4])
    C_CHR_LV_P_NOx_5_25=float(lines_coldLVPFile[1].split(",")[5])
    
    A_CHR_LV_P_NOx_25_45=float(lines_coldLVPFile[2].split(",")[3])
    B_CHR_LV_P_NOx_25_45=float(lines_coldLVPFile[2].split(",")[4])
    C_CHR_LV_P_NOx_25_45=float(lines_coldLVPFile[2].split(",")[5])
    
    A_CHR_LCV_P_NOx_5_25=float(lines_coldLVPFile[3].split(",")[3])
    B_CHR_LCV_P_NOx_5_25=float(lines_coldLVPFile[3].split(",")[4])
    C_CHR_LCV_P_NOx_5_25=float(lines_coldLVPFile[3].split(",")[5])
    
    A_CHR_LCV_P_NOx_25_45=float(lines_coldLVPFile[4].split(",")[3])
    B_CHR_LCV_P_NOx_25_45=float(lines_coldLVPFile[4].split(",")[4])
    C_CHR_LCV_P_NOx_25_45=float(lines_coldLVPFile[4].split(",")[5])
    
    #Stock information
    with open(CWD+"/data/Stock_CITEPA/stock"+str(stock)+".csv", "r") as stockFile :
        lines_stockFile = stockFile.readlines()
    
    
    w_LV_P = float(lines_stockFile[1].split(",")[1])
    w_LV_D = float(lines_stockFile[2].split(",")[1])
    
    w_LCV_P = float(lines_stockFile[3].split(",")[1])
    w_LCV_D = float(lines_stockFile[4].split(",")[1])
    
    w_HDT_1420 = float(lines_stockFile[5].split(",")[1])
    w_HDT_32 = float(lines_stockFile[6].split(",")[1])
    
    w_LV_E1 = float(lines_stockFile[7].split(",")[1])
    w_LV_E2 = float(lines_stockFile[8].split(",")[1])
    w_LV_E3 = float(lines_stockFile[9].split(",")[1])
    w_LV_E4 = float(lines_stockFile[10].split(",")[1])
    w_LV_E5 = float(lines_stockFile[11].split(",")[1])
    w_LV_E6 = float(lines_stockFile[12].split(",")[1])
    
    w_LCV_E1 = float(lines_stockFile[13].split(",")[1])
    w_LCV_E2 = float(lines_stockFile[14].split(",")[1])
    w_LCV_E3 = float(lines_stockFile[15].split(",")[1])
    w_LCV_E4 = float(lines_stockFile[16].split(",")[1])
    w_LCV_E5 = float(lines_stockFile[17].split(",")[1])
    w_LCV_E6 = float(lines_stockFile[18].split(",")[1])
    
    w_HDT_E1 = float(lines_stockFile[19].split(",")[1])
    w_HDT_E2 = float(lines_stockFile[20].split(",")[1])
    w_HDT_E3 = float(lines_stockFile[21].split(",")[1])
    w_HDT_E4 = float(lines_stockFile[22].split(",")[1])
    w_HDT_E5 = float(lines_stockFile[23].split(",")[1])
    w_HDT_E6 = float(lines_stockFile[24].split(",")[1])
    
    w_L_E1 = float(lines_stockFile[25].split(",")[1])
    w_L_E2 = float(lines_stockFile[26].split(",")[1])
    w_L_E3 = float(lines_stockFile[27].split(",")[1])
    w_L_E4 = float(lines_stockFile[28].split(",")[1])
    w_L_E5 = float(lines_stockFile[29].split(",")[1])
    w_L_E6 = float(lines_stockFile[30].split(",")[1])
    
    stockFile.close()
    
    #Trafic information based on method chosen 
    if method == "daily":
        nb_veh = int(computation_dictionary.get('"nb_veh_d"'))
        v_L = int(computation_dictionary.get('"v_L_d"'))
        v_H = int(computation_dictionary.get('"v_H_d"'))
    elif method == "hourly":
        list_nb_veh = [int(x) for x in computation_dictionary.get('"nb_veh_h"').split(",")]
        list_v_L = [int(x) for x in computation_dictionary.get('"v_L_h"').split(",")]
        list_v_H = [int(x) for x in computation_dictionary.get('"v_H_h"').split(",")]
    else:
        print("!ERROR! Wrong argument for '"'method'"' in" + CWD + "/input_emiCalc")
        raise SystemExit(0)
        
    #Unit calculation
    if massUnit == "t":
        mass = 0.000001
    elif massUnit == "kg":
        mass = 0.001
    elif massUnit == "g":
        mass = 1
    elif massUnit == "mg":
        mass = 1000
    elif massUnit == "µg":
        mass = 1000000
    else:
        print("!ERROR! Wrong argument for '"'massUnit'"' in" + CWD + "/input_emiCalc")
        raise SystemExit(0)
        
    if timeUnit == "y":
        time = 24*365
    elif timeUnit == "d":
        time = 24
    elif timeUnit == "h":
        time = 1
    elif timeUnit == "m":
        time = 1/60
    elif timeUnit == "s":
        time = 1/60/60
    else:
        print("!ERROR! Wrong argument for '"'timeUnit'"' in" + CWD + "/input_emiCalc")
        raise SystemExit(0)
        
    
    if method == "daily" :
        ##################################################################################################################################################################################################################
        ##################################################################################################################################################################################################################
        #######################################################################  NOx 
        #Light diesel vehicles emissions 
        factor_LV_D = traficEmissions.func_L_EF(v_L,"LV","diesel","NOx")
        
        if v_L > 45:
            if forceCold == "no":
                emission_LV_D_hot = (nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_cold = 0
                emission_LV_D_heated = 0
            elif forceCold == "yes":
                CHR=A_CHR_LV_D_NOx-temp*B_CHR_LV_D_NOx
                emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            else:
                print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                raise SystemExit(0)
        else:
            CHR = A_CHR_LV_D_NOx-temp*B_CHR_LV_D_NOx
            emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
        
        emission_LV_D = (emission_LV_D_hot + emission_LV_D_cold + emission_LV_D_heated)*mass*time
        
        
        
        #Light petrol vehicles emissions  
        factor_LV_P = traficEmissions.func_L_EF(v_L,"LV","petrol","NOx")
        
        if v_L > 45:
            if forceCold == "no":
                emission_LV_P_hot = (nb_veh*w_LV/100*w_LV_P)/24*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                emission_LV_P_cold = 0
                emission_LV_P_heated = 0
            elif forceCold == "yes":
                CHR = A_CHR_LV_P_NOx_25_45*speedFC+B_CHR_LV_P_NOx_25_45*temp+C_CHR_LV_P_NOx_25_45
                emission_LV_P_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_P)/24*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                emission_LV_P_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_P)/24*dist*CHR*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                emission_LV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_P)/24*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
            else:
                print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                raise SystemExit(0)
        else:
            if v_L > 25:
                CHR = A_CHR_LV_P_NOx_25_45*v_L+B_CHR_LV_P_NOx_25_45*temp+C_CHR_LV_P_NOx_25_45
            else :
                CHR = A_CHR_LV_P_NOx_5_25*v_L+B_CHR_LV_P_NOx_5_25*temp+C_CHR_LV_P_NOx_5_25
            emission_LV_P_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_P)/24*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
            emission_LV_P_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_P)/24*dist*CHR*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
            emission_LV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_P)/24*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
        
        emission_LV_P = (emission_LV_P_hot + emission_LV_P_cold + emission_LV_P_heated)*mass*time
        
        
        #Light commerical diesel vehicles emissions   
        factor_LCV_D = traficEmissions.func_L_EF(v_L,"LCV","diesel","NOx")
        
        if v_L > 45:
            if forceCold == "no":
                emission_LCV_D_hot = (nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_cold = 0
                emission_LCV_D_heated = 0
            elif forceCold == "yes":
                CHR=A_CHR_LCV_D_NOx-temp*B_CHR_LCV_D_NOx
                emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            else:
                print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                raise SystemExit(0)
        else:
            CHR = A_CHR_LCV_D_NOx-temp*B_CHR_LCV_D_NOx
            emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
        
        emission_LCV_D = (emission_LCV_D_hot + emission_LCV_D_cold + emission_LCV_D_heated)*mass*time
        
        
        #Light commerical petrol vehicles emissions 
        factor_LCV_P = traficEmissions.func_L_EF(v_L,"LCV","petrol","NOx")
        
        if v_L > 45:
            if forceCold == "no":
                emission_LCV_P_hot = (nb_veh*w_LCV/100*w_LCV_P)/24*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                emission_LCV_P_cold = 0
                emission_LCV_P_heated = 0
            elif forceCold == "yes":
                CHR = A_CHR_LCV_P_NOx_25_45*speedFC+B_CHR_LCV_P_NOx_25_45*temp+C_CHR_LCV_P_NOx_25_45
                emission_LCV_P_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_P)/24*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                emission_LCV_P_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_P)/24*dist*CHR*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                emission_LCV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_P)/24*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
            else:
                print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                raise SystemExit(0)
        else:
            if v_L > 25:
                CHR = A_CHR_LCV_P_NOx_25_45*v_L+B_CHR_LCV_P_NOx_25_45*temp+C_CHR_LCV_P_NOx_25_45
            else :
                CHR = A_CHR_LCV_P_NOx_5_25*v_L+B_CHR_LCV_P_NOx_5_25*temp+C_CHR_LCV_P_NOx_5_25
            emission_LCV_P_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_P)/24*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
            emission_LCV_P_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_P)/24*dist*CHR*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
            emission_LCV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_P)/24*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
        
        emission_LCV_P = (emission_LCV_P_hot + emission_LCV_P_cold + emission_LCV_P_heated)*mass*time
        
        
        #Diesel bus emissions 
        factor_B_D = traficEmissions.func_H_EF(v_H,"B","diesel","NOx","B1518",load,sloap)
        emission_B_D_hot = (nb_veh*w_B/100)/24*dist*(factor_B_D[0]*w_HDT_E1+factor_B_D[1]*w_HDT_E2+factor_B_D[2]*w_HDT_E3+factor_B_D[3]*w_HDT_E4+factor_B_D[4]*w_HDT_E5+factor_B_D[5]*w_HDT_E6)
        emission_B_D_cold = 0
        emission_B_D_heated = 0
        
        emission_B_D = (emission_B_D_hot + emission_B_D_cold + emission_B_D_heated)*mass*time
        
        
        #Diesel heavy duty truck 14-20t emissions  
        factor_HDT_1420_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","NOx","HDT1420",load,sloap)
        emission_HDT_1420_D_hot = (nb_veh*w_HDT/100*w_HDT_1420)/24*dist*(factor_HDT_1420_D[0]*w_HDT_E1+factor_HDT_1420_D[1]*w_HDT_E2+factor_HDT_1420_D[2]*w_HDT_E3+factor_HDT_1420_D[3]*w_HDT_E4+factor_HDT_1420_D[4]*w_HDT_E5+factor_HDT_1420_D[5]*w_HDT_E6)
        emission_HDT_1420_D_cold = 0
        emission_HDT_1420_D_heated = 0
        
        emission_HDT_1420_D = (emission_HDT_1420_D_hot + emission_HDT_1420_D_cold + emission_HDT_1420_D_heated)*mass*time
          
            
        #Diesel heavy duty truck 14-20t emissions 
        factor_HDT_32_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","NOx","HDT32",load,sloap)
        emission_HDT_32_D_hot = (nb_veh*w_HDT/100*w_HDT_32)/24*dist*(factor_HDT_32_D[0]*w_HDT_E1+factor_HDT_32_D[1]*w_HDT_E2+factor_HDT_32_D[2]*w_HDT_E3+factor_HDT_32_D[3]*w_HDT_E4+factor_HDT_32_D[4]*w_HDT_E5+factor_HDT_32_D[5]*w_HDT_E6)
        emission_HDT_32_D_cold = 0
        emission_HDT_32_D_heated = 0
        
        emission_HDT_32_D = (emission_HDT_32_D_hot + emission_HDT_32_D_cold + emission_HDT_32_D_heated)*mass*time
        
        
        #Diesel heavy duty truck 14-20t emissions
        factor_L_P = traficEmissions.func_L_EF(v_L,"L","petrol","NOx")
        emission_L_P_hot = (nb_veh*w_L/100)/24*dist*(factor_L_P[0]*w_L_E1+factor_L_P[1]*w_L_E2+factor_L_P[2]*w_L_E3+factor_L_P[3]*w_L_E4+factor_L_P[4]*w_L_E5+factor_L_P[5]*w_L_E6)
        emission_L_P_cold = 0
        emission_L_P_heated = 0
        
        emission_L_P = (emission_L_P_hot + emission_L_P_cold + emission_L_P_heated)*mass*time
        
        
        #Total emissions
        emission_tot_NOx = emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P + emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P
        
        
        
        #Extracting results
        makeDirectory(dirEtude+"/NOx")
        
        with open(dirEtude+"/NOx/hotEmissionsNOx.csv","w") as hotEmissionsNOx :
            hotEmissionsNOx.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            hotEmissionsNOx.write("LV_D," + str((emission_LV_D_hot + emission_LV_D_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("LV_P," + str((emission_LV_P_hot + emission_LV_P_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("LCV_D," + str((emission_LCV_D_hot + emission_LCV_D_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("LCV_P," + str((emission_LCV_P_hot + emission_LCV_P_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("B_D," + str((emission_B_D_hot + emission_B_D_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("HDT_1420_D," + str((emission_HDT_1420_D_hot + emission_HDT_1420_D_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("HDT_32_D," + str((emission_HDT_32_D_hot + emission_HDT_32_D_heated)*mass*time) + "\n")
            hotEmissionsNOx.write("L_P," + str((emission_L_P_hot + emission_L_P_heated)*mass*time) + "\n")    
            hotEmissionsNOx.write("All," + str((emission_LV_D_hot + emission_LV_D_heated + emission_LV_P_hot + emission_LV_P_heated + emission_LCV_D_hot + emission_LCV_D_heated + emission_LCV_P_hot + emission_LCV_P_heated + emission_B_D_hot + emission_B_D_heated + emission_HDT_1420_D_hot + emission_HDT_1420_D_heated + emission_HDT_32_D_hot + emission_HDT_32_D_heated + emission_L_P_hot + emission_L_P_heated)*mass*time) + "\n")
            
        with open(dirEtude+"/NOx/coldEmissionsNOx.csv","w") as coldEmissionsNOx :
            coldEmissionsNOx.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            coldEmissionsNOx.write("LV_D," + str(emission_LV_D_cold*mass*time) + "\n")
            coldEmissionsNOx.write("LV_P," + str(emission_LV_P_cold*mass*time) + "\n")
            coldEmissionsNOx.write("LCV_D," + str(emission_LCV_D_cold*mass*time) + "\n")
            coldEmissionsNOx.write("LCV_P," + str(emission_LCV_P_cold*mass*time) + "\n")
            coldEmissionsNOx.write("B_D," + str(emission_B_D_cold*mass*time) + "\n")
            coldEmissionsNOx.write("HDT_1420_D," + str(emission_HDT_1420_D_cold*mass*time) + "\n")
            coldEmissionsNOx.write("HDT_32_D," + str(emission_HDT_32_D_cold*mass*time) + "\n")
            coldEmissionsNOx.write("L_P," + str(emission_L_P_cold*mass*time) + "\n")    
            coldEmissionsNOx.write("All," + str((emission_LV_D_cold+emission_LV_P_cold+emission_LCV_D_cold+emission_LCV_P_cold+emission_B_D_cold+emission_HDT_1420_D_cold+emission_HDT_32_D_cold+emission_L_P_cold)*mass*time) + "\n")    
        
        with open(dirEtude+"/NOx/totalEmissionsNOx.csv","w") as totalEmissionsNOx :
            totalEmissionsNOx.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            totalEmissionsNOx.write("LV_D," + str(emission_LV_D) + "\n")
            totalEmissionsNOx.write("LV_P," + str(emission_LV_P) + "\n")
            totalEmissionsNOx.write("LCV_D," + str(emission_LCV_D) + "\n")
            totalEmissionsNOx.write("LCV_P," + str(emission_LCV_P) + "\n")
            totalEmissionsNOx.write("B_D," + str(emission_B_D) + "\n")
            totalEmissionsNOx.write("HDT_1420_D," + str(emission_HDT_1420_D) + "\n")
            totalEmissionsNOx.write("HDT_32_D," + str(emission_HDT_32_D) + "\n")
            totalEmissionsNOx.write("L_P," + str(emission_L_P) + "\n")    
            totalEmissionsNOx.write("All," + str(emission_tot_NOx) + "\n")    
        
        ##################################################################################################################################################################################################################
        ##################################################################################################################################################################################################################   
        #######################################################################  PM 
            
        ######################################################### Motor emissions
            
        #Light diesel vehicles emissions 
        factor_LV_D = traficEmissions.func_L_EF(v_L,"LV","diesel","PM")
        
        if v_L > 45:
            if forceCold == "no":
                emission_LV_D_hot = (nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_cold = 0
                emission_LV_D_heated = 0
            elif forceCold == "yes":
                CHR=A_CHR_LV_D_PM-temp*B_CHR_LV_D_PM
                emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            else:
                print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                raise SystemExit(0)
        else:
            CHR = A_CHR_LV_D_PM-temp*B_CHR_LV_D_PM
            emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)/24*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
        
        emission_LV_D = (emission_LV_D_hot + emission_LV_D_cold + emission_LV_D_heated)*mass*time
        
        
        #Light petrol vehicles emissions  
        factor_LV_P = traficEmissions.func_L_EF(v_L,"LV","petrol","PM")
        
        emission_LV_P_hot = (nb_veh*w_LV/100*w_LV_P)/24*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
        emission_LV_P_cold = 0
        emission_LV_P_heated = 0
        
        emission_LV_P = (emission_LV_P_hot + emission_LV_P_cold + emission_LV_P_heated)*mass*time
        
        
        #Light commerical diesel vehicles emissions   
        factor_LCV_D = traficEmissions.func_L_EF(v_L,"LCV","diesel","PM")
        
        if v_L > 45:
            if forceCold == "no":
                emission_LCV_D_hot = (nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_cold = 0
                emission_LCV_D_heated = 0
            elif forceCold == "yes":
                CHR=A_CHR_LCV_D_PM-temp*B_CHR_LCV_D_PM
                emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            else:
                print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                raise SystemExit(0)
        else:
            CHR = A_CHR_LCV_D_PM-temp*B_CHR_LCV_D_PM
            emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)/24*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
        
        emission_LCV_D = (emission_LCV_D_hot + emission_LCV_D_cold + emission_LCV_D_heated)*mass*time
        
        
        #Light commerical petrol vehicles emissions 
        factor_LCV_P = traficEmissions.func_L_EF(v_L,"LCV","petrol","PM")
        
        emission_LCV_P_hot = (nb_veh*w_LCV/100*w_LCV_P)/24*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
        emission_LCV_P_cold = 0
        emission_LCV_P_heated = 0
        
        emission_LCV_P = (emission_LCV_P_hot + emission_LCV_P_cold + emission_LCV_P_heated)*mass*time
        
        
        #Diesel bus emissions 
        factor_B_D = traficEmissions.func_H_EF(v_H,"B","diesel","PM","B1518",load,sloap)
        emission_B_D_hot = (nb_veh*w_B/100)/24*dist*(factor_B_D[0]*w_HDT_E1+factor_B_D[1]*w_HDT_E2+factor_B_D[2]*w_HDT_E3+factor_B_D[3]*w_HDT_E4+factor_B_D[4]*w_HDT_E5+factor_B_D[5]*w_HDT_E6)
        emission_B_D_cold = 0
        emission_B_D_heated = 0
        
        emission_B_D = (emission_B_D_hot + emission_B_D_cold + emission_B_D_heated)*mass*time
        
        
        #Diesel heavy duty truck 14-20t emissions  
        factor_HDT_1420_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","PM","HDT1420",load,sloap)
        emission_HDT_1420_D_hot = (nb_veh*w_HDT/100*w_HDT_1420)/24*dist*(factor_HDT_1420_D[0]*w_HDT_E1+factor_HDT_1420_D[1]*w_HDT_E2+factor_HDT_1420_D[2]*w_HDT_E3+factor_HDT_1420_D[3]*w_HDT_E4+factor_HDT_1420_D[4]*w_HDT_E5+factor_HDT_1420_D[5]*w_HDT_E6)
        emission_HDT_1420_D_cold = 0
        emission_HDT_1420_D_heated = 0
        
        emission_HDT_1420_D = (emission_HDT_1420_D_hot + emission_HDT_1420_D_cold + emission_HDT_1420_D_heated)*mass*time
            
            
        #Diesel heavy duty truck 14-20t emissions 
        factor_HDT_32_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","PM","HDT32",load,sloap)
        emission_HDT_32_D_hot = (nb_veh*w_HDT/100*w_HDT_32)/24*dist*(factor_HDT_32_D[0]*w_HDT_E1+factor_HDT_32_D[1]*w_HDT_E2+factor_HDT_32_D[2]*w_HDT_E3+factor_HDT_32_D[3]*w_HDT_E4+factor_HDT_32_D[4]*w_HDT_E5+factor_HDT_32_D[5]*w_HDT_E6)
        emission_HDT_32_D_cold = 0
        emission_HDT_32_D_heated = 0
        
        emission_HDT_32_D = (emission_HDT_32_D_hot + emission_HDT_32_D_cold + emission_HDT_32_D_heated)*mass*time
        
        #Diesel heavy duty truck 14-20t emissions
        factor_L_P = traficEmissions.func_L_EF(v_L,"L","petrol","PM")
        emission_L_P_hot = (nb_veh*w_L/100)/24*dist*(factor_L_P[0]*w_L_E1+factor_L_P[1]*w_L_E2+factor_L_P[2]*w_L_E3+factor_L_P[3]*w_L_E4+factor_L_P[4]*w_L_E5+factor_L_P[5]*w_L_E6)
        emission_L_P_cold = 0
        emission_L_P_heated = 0
        
        emission_L_P = (emission_L_P_hot + emission_L_P_cold + emission_L_P_heated)*mass*time
        
        
        #Total emissions
        emission_tot_PM = emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P + emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P
        
        
        ######################################################### Other emissions
        with open(CWD+"/data/Emep_Emission_Factors_2016/massFractionTSP.csv", "r") as massFractionTSPFile :
            lines_massFractionTSPFile = massFractionTSPFile.readlines()
        massFractionTSPFile.close()
        FM_TSP_Tyre_PM10=float(lines_massFractionTSPFile[2].split(",")[1])
        FM_TSP_Brake_PM10=float(lines_massFractionTSPFile[2].split(",")[2])
        FM_TSP_Road_PM10=float(lines_massFractionTSPFile[2].split(",")[3])
        FM_TSP_Tyre_PM2_5=float(lines_massFractionTSPFile[3].split(",")[1])
        FM_TSP_Brake_PM2_5=float(lines_massFractionTSPFile[3].split(",")[2])
        FM_TSP_Road_PM2_5=float(lines_massFractionTSPFile[3].split(",")[3])
        
        with open(CWD+"/data/Emep_Emission_Factors_2016/emissionFactorTSP.csv", "r") as emissionFactorTSPFile :
            lines_emissionFactorTSPFile = emissionFactorTSPFile.readlines()
        emissionFactorTSPFile.close()
        EF_TSP_Tyre_L=float(lines_emissionFactorTSPFile[1].split(",")[1])
        EF_TSP_Tyre_LV=float(lines_emissionFactorTSPFile[2].split(",")[1])
        EF_TSP_Tyre_LDT=float(lines_emissionFactorTSPFile[3].split(",")[1])
        EF_TSP_Brake_L=float(lines_emissionFactorTSPFile[1].split(",")[2])
        EF_TSP_Brake_LV=float(lines_emissionFactorTSPFile[2].split(",")[2])
        EF_TSP_Brake_LDT=float(lines_emissionFactorTSPFile[3].split(",")[2])
        EF_TSP_Road_L=float(lines_emissionFactorTSPFile[1].split(",")[3])
        EF_TSP_Road_LV=float(lines_emissionFactorTSPFile[2].split(",")[3])
        EF_TSP_Road_LDT=float(lines_emissionFactorTSPFile[3].split(",")[3])
        EF_TSP_Road_HDT=float(lines_emissionFactorTSPFile[4].split(",")[3])
        
        ######################################################### Tyre emissions
        if v_L > 90:
            St_LV = 0.902
        elif v_L > 40:
            St_LV = -0.00974*v_L+1.78
        else:
            St_LV = 1.39
            
        if v_H > 90:
            St_HV = 0.902
        elif v_H > 40:
            St_HV = -0.00974*v_H+1.78
        else:
            St_HV = 1.39
        
        LCFt = 1.41+(1.38*load_int/100)
        
        tyre_LV_PM10 = nb_veh*w_LV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM10*St_LV/24/100*mass*time
        tyre_LCV_PM10 = nb_veh*w_LCV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM10*St_LV/24/100*mass*time
        tyre_B_PM10 = nb_veh*w_B*dist*EF_TSP_Tyre_LDT*FM_TSP_Tyre_PM10*St_HV/24/100*mass*time
        tyre_HDT1420_PM10 = nb_veh*w_HDT*w_HDT_1420*dist*(3/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM10*St_HV/24/100*mass*time
        tyre_HDT32_PM10 = nb_veh*w_HDT*w_HDT_32*dist*(5/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM10*St_HV/24/100*mass*time
        tyre_L_PM10 = nb_veh*w_L*dist*EF_TSP_Tyre_L*FM_TSP_Tyre_PM10*St_LV/24/100*mass*time
        tyre_all_PM10 = tyre_LV_PM10 + tyre_LCV_PM10 + tyre_B_PM10 + tyre_HDT1420_PM10 + tyre_HDT32_PM10 + tyre_L_PM10
        
        tyre_LV_PM2_5 = nb_veh*w_LV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM2_5*St_LV/24/100*mass*time
        tyre_LCV_PM2_5 = nb_veh*w_LCV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM2_5*St_LV/24/100*mass*time
        tyre_B_PM2_5 = nb_veh*w_B*dist*EF_TSP_Tyre_LDT*FM_TSP_Tyre_PM2_5*St_HV/24/100*mass*time
        tyre_HDT1420_PM2_5 = nb_veh*w_HDT*w_HDT_1420*dist*(3/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM2_5*St_HV/24/100*mass*time
        tyre_HDT32_PM2_5 = nb_veh*w_HDT*w_HDT_32*dist*(5/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM2_5*St_HV/24/100*mass*time
        tyre_L_PM2_5 = nb_veh*w_L*dist*EF_TSP_Tyre_L*FM_TSP_Tyre_PM2_5*St_LV/24/100*mass*time
        tyre_all_PM2_5 = tyre_LV_PM2_5 + tyre_LCV_PM2_5 + tyre_B_PM2_5 + tyre_HDT1420_PM2_5 + tyre_HDT32_PM2_5 + tyre_L_PM2_5
        
        ######################################################### Brake emissions
        if v_L > 90:
            Sb_LV = 0.185
        elif v_L > 40:
            Sb_LV = -0.0270*v_L+2.75
        else:
            Sb_LV = 1.67
            
        if v_H > 90:
            Sb_HV = 0.185
        elif v_H > 40:
            Sb_HV = -0.0270*v_H+2.75
        else:
            Sb_HV = 1.67
        
        LCFb = 1+(0.79*load_int/100)
        
        brake_LV_PM10 = nb_veh*w_LV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM10*Sb_LV/24/100*mass*time
        brake_LCV_PM10 = nb_veh*w_LCV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM10*Sb_LV/24/100*mass*time
        brake_B_PM10 = nb_veh*w_B*dist*EF_TSP_Brake_LDT*FM_TSP_Brake_PM10*Sb_HV/24/100*mass*time
        brake_HDT1420_PM10 = nb_veh*w_HDT*w_HDT_1420*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM10*Sb_HV/24/100*mass*time
        brake_HDT32_PM10 = nb_veh*w_HDT*w_HDT_32*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM10*Sb_HV/24/100*mass*time
        brake_L_PM10 = nb_veh*w_L*dist*EF_TSP_Brake_L*FM_TSP_Brake_PM10*Sb_LV/24/100*mass*time
        brake_all_PM10 = brake_LV_PM10 + brake_LCV_PM10 + brake_B_PM10 + brake_HDT1420_PM10 + brake_HDT32_PM10 + brake_L_PM10
        
        brake_LV_PM2_5 = nb_veh*w_LV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM2_5*Sb_LV/24/100*mass*time
        brake_LCV_PM2_5 = nb_veh*w_LCV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM2_5*Sb_LV/24/100*mass*time
        brake_B_PM2_5 = nb_veh*w_B*dist*EF_TSP_Brake_LDT*FM_TSP_Brake_PM2_5*Sb_HV/24/100*mass*time
        brake_HDT1420_PM2_5 = nb_veh*w_HDT*w_HDT_1420*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM2_5*Sb_HV/24/100*mass*time
        brake_HDT32_PM2_5 = nb_veh*w_HDT*w_HDT_32*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM2_5*Sb_HV/24/100*mass*time
        brake_L_PM2_5 = nb_veh*w_L*dist*EF_TSP_Brake_L*FM_TSP_Brake_PM2_5*Sb_LV/24/100*mass*time
        brake_all_PM2_5 = brake_LV_PM2_5 + brake_LCV_PM2_5 + brake_B_PM2_5 + brake_HDT1420_PM2_5 + brake_HDT32_PM2_5 + brake_L_PM2_5
        
        ######################################################### Road emissions
        road_LV_PM10 = nb_veh*w_LV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM10/24/100*mass*time
        road_LCV_PM10 = nb_veh*w_LCV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM10/24/100*mass*time
        road_B_PM10 = nb_veh*w_B*dist*EF_TSP_Road_LDT*FM_TSP_Road_PM10/24/100*mass*time
        road_HDT1420_PM10 = nb_veh*w_HDT*w_HDT_1420*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM10/24/100*mass*time
        road_HDT32_PM10 = nb_veh*w_HDT*w_HDT_32*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM10/24/100*mass*time
        road_L_PM10 = nb_veh*w_L*dist*EF_TSP_Road_L*FM_TSP_Road_PM10/24/100*mass*time
        road_all_PM10 = road_LV_PM10 + road_LCV_PM10 + road_B_PM10 + road_HDT1420_PM10 + road_HDT32_PM10 + road_L_PM10
        
        road_LV_PM2_5 = nb_veh*w_LV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM2_5/24/100*mass*time
        road_LCV_PM2_5 = nb_veh*w_LCV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM2_5/24/100*mass*time
        road_B_PM2_5 = nb_veh*w_B*dist*EF_TSP_Road_LDT*FM_TSP_Road_PM2_5/24/100*mass*time
        road_HDT1420_PM2_5 = nb_veh*w_HDT*w_HDT_1420*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM2_5/24/100*mass*time
        road_HDT32_PM2_5 = nb_veh*w_HDT*w_HDT_32*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM2_5/24/100*mass*time
        road_L_PM2_5 = nb_veh*w_L*dist*EF_TSP_Road_L*FM_TSP_Road_PM2_5/24/100*mass*time
        road_all_PM2_5 = road_LV_PM2_5 + road_LCV_PM2_5 + road_B_PM2_5 + road_HDT1420_PM2_5 + road_HDT32_PM2_5 + road_L_PM2_5
        
                  
        #Extracting results
        makeDirectory(dirEtude+"/PM")
        
        with open(dirEtude+"/PM/hotEmissionsPM.csv","w") as hotEmissionsPM :
            hotEmissionsPM.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            hotEmissionsPM.write("LV_D," + str((emission_LV_D_hot + emission_LV_D_heated)*mass*time) + "\n")
            hotEmissionsPM.write("LV_P," + str((emission_LV_P_hot + emission_LV_P_heated)*mass*time) + "\n")
            hotEmissionsPM.write("LCV_D," + str((emission_LCV_D_hot + emission_LCV_D_heated)*mass*time) + "\n")
            hotEmissionsPM.write("LCV_P," + str((emission_LCV_P_hot + emission_LCV_P_heated)*mass*time) + "\n")
            hotEmissionsPM.write("B_D," + str((emission_B_D_hot + emission_B_D_heated)*mass*time) + "\n")
            hotEmissionsPM.write("HDT_1420_D," + str((emission_HDT_1420_D_hot + emission_HDT_1420_D_heated)*mass*time) + "\n")
            hotEmissionsPM.write("HDT_32_D," + str((emission_HDT_32_D_hot + emission_HDT_32_D_heated)*mass*time) + "\n")
            hotEmissionsPM.write("L_P," + str((emission_L_P_hot + emission_L_P_heated)*mass*time) + "\n")    
            hotEmissionsPM.write("All," + str((emission_LV_D_hot + emission_LV_D_heated + emission_LV_P_hot + emission_LV_P_heated + emission_LCV_D_hot + emission_LCV_D_heated + emission_LCV_P_hot + emission_LCV_P_heated + emission_B_D_hot + emission_B_D_heated + emission_HDT_1420_D_hot + emission_HDT_1420_D_heated + emission_HDT_32_D_hot + emission_HDT_32_D_heated + emission_L_P_hot + emission_L_P_heated)*mass*time) + "\n")
            
        with open(dirEtude+"/PM/coldEmissionsPM.csv","w") as coldEmissionsPM :
            coldEmissionsPM.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            coldEmissionsPM.write("LV_D," + str(emission_LV_D_cold*mass*time) + "\n")
            coldEmissionsPM.write("LV_P," + str(emission_LV_P_cold*mass*time) + "\n")
            coldEmissionsPM.write("LCV_D," + str(emission_LCV_D_cold*mass*time) + "\n")
            coldEmissionsPM.write("LCV_P," + str(emission_LCV_P_cold*mass*time) + "\n")
            coldEmissionsPM.write("B_D," + str(emission_B_D_cold*mass*time) + "\n")
            coldEmissionsPM.write("HDT_1420_D," + str(emission_HDT_1420_D_cold*mass*time) + "\n")
            coldEmissionsPM.write("HDT_32_D," + str(emission_HDT_32_D_cold*mass*time) + "\n")
            coldEmissionsPM.write("L_P," + str(emission_L_P_cold*mass*time) + "\n")    
            coldEmissionsPM.write("All," + str((emission_LV_D_cold+emission_LV_P_cold+emission_LCV_D_cold+emission_LCV_P_cold+emission_B_D_cold+emission_HDT_1420_D_cold+emission_HDT_32_D_cold+emission_L_P_cold)*mass*time) + "\n")    
        
        with open(dirEtude+"/PM/tbrEmissionsPM10.csv","w") as tbrEmissionsPM :
            tbrEmissionsPM.write("Type [-],Tyre emissions [" + massUnit + "/" + timeUnit + "],Brake emissions [" + massUnit + "/" + timeUnit + "],Road emissions [" + massUnit + "/" + timeUnit + "]\n")
            tbrEmissionsPM.write("LV_D," + str(tyre_LV_PM10*w_LV_D) + "," + str(brake_LV_PM10*w_LV_D) + "," + str(road_LV_PM10*w_LV_D) + "\n")
            tbrEmissionsPM.write("LV_P," + str(tyre_LV_PM10*w_LV_P) + "," + str(brake_LV_PM10*w_LV_P) + "," + str(road_LV_PM10*w_LV_P) + "\n")
            tbrEmissionsPM.write("LCV_D," + str(tyre_LCV_PM10*w_LCV_D) + "," + str(brake_LCV_PM10*w_LCV_D) + "," + str(road_LCV_PM10*w_LCV_D) + "\n")
            tbrEmissionsPM.write("LCV_P," + str(tyre_LCV_PM10*w_LCV_P) + "," + str(brake_LCV_PM10*w_LCV_P) + "," + str(road_LCV_PM10*w_LCV_P) + "\n")
            tbrEmissionsPM.write("B_D," + str(tyre_B_PM10) + "," + str(brake_B_PM10) + "," + str(road_B_PM10) + "\n")
            tbrEmissionsPM.write("HDT_1420_D," + str(tyre_HDT1420_PM10) + "," + str(brake_HDT1420_PM10) + "," + str(road_HDT1420_PM10) + "\n")
            tbrEmissionsPM.write("HDT_32_D," + str(tyre_HDT32_PM10) + "," + str(brake_HDT32_PM10) + "," + str(road_HDT32_PM10) + "\n")
            tbrEmissionsPM.write("L_P," + str(tyre_L_PM10) + "," + str(brake_L_PM10) + "," + str(road_L_PM10) + "\n")
            tbrEmissionsPM.write("All," + str(tyre_all_PM10) + "," + str(brake_all_PM10) + "," + str(road_all_PM10) + "\n")
        
        with open(dirEtude+"/PM/tbrEmissionsPM2_5.csv","w") as tbrEmissionsPM2 :
            tbrEmissionsPM2.write("Type [-],Tyre emissions [" + massUnit + "/" + timeUnit + "],Brake emissions [" + massUnit + "/" + timeUnit + "],Road emissions [" + massUnit + "/" + timeUnit + "]\n")
            tbrEmissionsPM2.write("LV_D," + str(tyre_LV_PM2_5*w_LV_D) + "," + str(brake_LV_PM2_5*w_LV_D) + "," + str(road_LV_PM2_5*w_LV_D) + "\n")
            tbrEmissionsPM2.write("LV_P," + str(tyre_LV_PM2_5*w_LV_P) + "," + str(brake_LV_PM2_5*w_LV_P) + "," + str(road_LV_PM2_5*w_LV_P) + "\n")
            tbrEmissionsPM2.write("LCV_D," + str(tyre_LCV_PM2_5*w_LCV_D) + "," + str(brake_LCV_PM2_5*w_LCV_D) + "," + str(road_LCV_PM2_5*w_LCV_D) + "\n")
            tbrEmissionsPM2.write("LCV_P," + str(tyre_LCV_PM2_5*w_LCV_P) + "," + str(brake_LCV_PM2_5*w_LCV_P) + "," + str(road_LCV_PM2_5*w_LCV_P) + "\n")
            tbrEmissionsPM2.write("B_D," + str(tyre_B_PM2_5) + "," + str(brake_B_PM2_5) + "," + str(road_B_PM2_5) + "\n")
            tbrEmissionsPM2.write("HDT_1420_D," + str(tyre_HDT1420_PM2_5) + "," + str(brake_HDT1420_PM2_5) + "," + str(road_HDT1420_PM2_5) + "\n")
            tbrEmissionsPM2.write("HDT_32_D," + str(tyre_HDT32_PM2_5) + "," + str(brake_HDT32_PM2_5) + "," + str(road_HDT32_PM2_5) + "\n")
            tbrEmissionsPM2.write("L_P," + str(tyre_L_PM2_5) + "," + str(brake_L_PM2_5) + "," + str(road_L_PM2_5) + "\n")
            tbrEmissionsPM2.write("All," + str(tyre_all_PM2_5) + "," + str(brake_all_PM2_5) + "," + str(road_all_PM2_5) + "\n")
            
        with open(dirEtude+"/PM/totalEmissionsPM10.csv","w") as totalEmissionsPM :
            totalEmissionsPM.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            totalEmissionsPM.write("LV_D," + str(emission_LV_D+tyre_LV_PM10*w_LV_D+brake_LV_PM10*w_LV_D+road_LV_PM10*w_LV_D) + "\n")
            totalEmissionsPM.write("LV_P," + str(emission_LV_P+tyre_LV_PM10*w_LV_P+brake_LV_PM10*w_LV_P+road_LV_PM10*w_LV_P) + "\n")
            totalEmissionsPM.write("LCV_D," + str(emission_LCV_D+tyre_LCV_PM10*w_LCV_D+brake_LCV_PM10*w_LCV_D+road_LCV_PM10*w_LCV_D) + "\n")
            totalEmissionsPM.write("LCV_P," + str(emission_LCV_P+tyre_LCV_PM10*w_LCV_P+brake_LCV_PM10*w_LCV_P+road_LCV_PM10*w_LCV_P) + "\n")
            totalEmissionsPM.write("B_D," + str(emission_B_D+tyre_B_PM10+brake_B_PM10+road_B_PM10) + "\n")
            totalEmissionsPM.write("HDT_1420_D," + str(emission_HDT_1420_D+tyre_HDT1420_PM10+brake_HDT1420_PM10+road_HDT1420_PM10) + "\n")
            totalEmissionsPM.write("HDT_32_D," + str(emission_HDT_32_D+tyre_HDT32_PM10+brake_HDT32_PM10+road_HDT32_PM10) + "\n")
            totalEmissionsPM.write("L_P," + str(emission_L_P+tyre_L_PM10+brake_L_PM10+road_L_PM10) + "\n")    
            totalEmissionsPM.write("All," + str(emission_tot_PM+tyre_all_PM10+brake_all_PM10+road_all_PM10) + "\n")      
           
        with open(dirEtude+"/PM/totalEmissionsPM2_5.csv","w") as totalEmissionsPM :
            totalEmissionsPM.write("Type [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            totalEmissionsPM.write("LV_D," + str(emission_LV_D+tyre_LV_PM2_5*w_LV_D+brake_LV_PM2_5*w_LV_D+road_LV_PM2_5*w_LV_D) + "\n")
            totalEmissionsPM.write("LV_P," + str(emission_LV_P+tyre_LV_PM2_5*w_LV_P+brake_LV_PM2_5*w_LV_P+road_LV_PM2_5*w_LV_P) + "\n")
            totalEmissionsPM.write("LCV_D," + str(emission_LCV_D+tyre_LCV_PM2_5*w_LCV_D+brake_LCV_PM2_5*w_LCV_D+road_LCV_PM2_5*w_LCV_D) + "\n")
            totalEmissionsPM.write("LCV_P," + str(emission_LCV_P+tyre_LCV_PM2_5*w_LCV_P+brake_LCV_PM2_5*w_LCV_P+road_LCV_PM2_5*w_LCV_P) + "\n")
            totalEmissionsPM.write("B_D," + str(emission_B_D+tyre_B_PM2_5+brake_B_PM2_5+road_B_PM2_5) + "\n")
            totalEmissionsPM.write("HDT_1420_D," + str(emission_HDT_1420_D+tyre_HDT1420_PM2_5+brake_HDT1420_PM2_5+road_HDT1420_PM2_5) + "\n")
            totalEmissionsPM.write("HDT_32_D," + str(emission_HDT_32_D+tyre_HDT32_PM2_5+brake_HDT32_PM2_5+road_HDT32_PM2_5) + "\n")
            totalEmissionsPM.write("L_P," + str(emission_L_P+tyre_L_PM2_5+brake_L_PM2_5+road_L_PM2_5) + "\n")    
            totalEmissionsPM.write("All," + str(emission_tot_PM+tyre_all_PM2_5+brake_all_PM2_5+road_all_PM2_5) + "\n")      
            
        with open(dirEtude+"/summaryEmission_"+roadNameSimulation+".csv","w") as summaryEmissions :
            summaryEmissions.write("Pollutant [-],Emissions [" + massUnit + "/" + timeUnit + "]\n")
            summaryEmissions.write("NOx," + str(emission_tot_NOx) + "\n") 
            summaryEmissions.write("PM10," + str(emission_tot_PM+tyre_all_PM10+brake_all_PM10+road_all_PM10) + "\n")
            summaryEmissions.write("PM2.5," + str(emission_tot_PM+tyre_all_PM2_5+brake_all_PM2_5+road_all_PM2_5) + "\n")
            
    elif method == "hourly":
        title = "Type,H1,H2,H3,H4,H5,H9,H7,H8,H9,H10,H11,H12,H13,H14,H15,H16,H17,H18,H19,H20,H21,H22,H23,H24,Mean,units : "+str(massUnit)+"/"+str(timeUnit)
        
        for i in range(0,24):
            
            nb_veh = list_nb_veh[i]
            v_L = list_v_L[i]
            v_H = list_v_H[i]
            
    
    
            ##################################################################################################################################################################################################################
            ##################################################################################################################################################################################################################
            #######################################################################  NOx 
            #Light diesel vehicles emissions 
            factor_LV_D = traficEmissions.func_L_EF(v_L,"LV","diesel","NOx")
            
            if v_L > 45:
                if forceCold == "no":
                    emission_LV_D_hot = (nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                    emission_LV_D_cold = 0
                    emission_LV_D_heated = 0
                elif forceCold == "yes":
                    CHR=A_CHR_LV_D_NOx-temp*B_CHR_LV_D_NOx
                    emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                    emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                    emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                else:
                    print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                    raise SystemExit(0)
            else:
                CHR = A_CHR_LV_D_NOx-temp*B_CHR_LV_D_NOx
                emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            
            emission_LV_D = (emission_LV_D_hot + emission_LV_D_cold + emission_LV_D_heated)*mass*time
            
            #Light petrol vehicles emissions  
            factor_LV_P = traficEmissions.func_L_EF(v_L,"LV","petrol","NOx")
            
            if v_L > 45:
                if forceCold == "no":
                    emission_LV_P_hot = (nb_veh*w_LV/100*w_LV_P)*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                    emission_LV_P_cold = 0
                    emission_LV_P_heated = 0
                elif forceCold == "yes":
                    CHR = A_CHR_LV_P_NOx_25_45*speedFC+B_CHR_LV_P_NOx_25_45*temp+C_CHR_LV_P_NOx_25_45
                    emission_LV_P_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_P)*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                    emission_LV_P_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_P)*dist*CHR*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                    emission_LV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_P)*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                else:
                    print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                    raise SystemExit(0)
            else:
                if v_L > 25:
                    CHR = A_CHR_LV_P_NOx_25_45*v_L+B_CHR_LV_P_NOx_25_45*temp+C_CHR_LV_P_NOx_25_45
                else :
                    CHR = A_CHR_LV_P_NOx_5_25*v_L+B_CHR_LV_P_NOx_5_25*temp+C_CHR_LV_P_NOx_5_25
                emission_LV_P_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_P)*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                emission_LV_P_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_P)*dist*CHR*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
                emission_LV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_P)*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
            
            emission_LV_P = (emission_LV_P_hot + emission_LV_P_cold + emission_LV_P_heated)*mass*time
            
            
            #Light commerical diesel vehicles emissions   
            factor_LCV_D = traficEmissions.func_L_EF(v_L,"LCV","diesel","NOx")
            
            if v_L > 45:
                if forceCold == "no":
                    emission_LCV_D_hot = (nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                    emission_LCV_D_cold = 0
                    emission_LCV_D_heated = 0
                elif forceCold == "yes":
                    CHR=A_CHR_LCV_D_NOx-temp*B_CHR_LCV_D_NOx
                    emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                    emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                    emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                else:
                    print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                    raise SystemExit(0)
            else:
                CHR = A_CHR_LCV_D_NOx-temp*B_CHR_LCV_D_NOx
                emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            
            emission_LCV_D = (emission_LCV_D_hot + emission_LCV_D_cold + emission_LCV_D_heated)*mass*time
            
            
            #Light commerical petrol vehicles emissions 
            factor_LCV_P = traficEmissions.func_L_EF(v_L,"LCV","petrol","NOx")
            
            if v_L > 45:
                if forceCold == "no":
                    emission_LCV_P_hot = (nb_veh*w_LCV/100*w_LCV_P)*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                    emission_LCV_P_cold = 0
                    emission_LCV_P_heated = 0
                elif forceCold == "yes":
                    CHR = A_CHR_LCV_P_NOx_25_45*speedFC+B_CHR_LCV_P_NOx_25_45*temp+C_CHR_LCV_P_NOx_25_45
                    emission_LCV_P_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_P)*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                    emission_LCV_P_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_P)*dist*CHR*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                    emission_LCV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_P)*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                else:
                    print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                    raise SystemExit(0)
            else:
                if v_L > 25:
                    CHR = A_CHR_LCV_P_NOx_25_45*v_L+B_CHR_LCV_P_NOx_25_45*temp+C_CHR_LCV_P_NOx_25_45
                else :
                    CHR = A_CHR_LCV_P_NOx_5_25*v_L+B_CHR_LCV_P_NOx_5_25*temp+C_CHR_LCV_P_NOx_5_25
                emission_LCV_P_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_P)*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                emission_LCV_P_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_P)*dist*CHR*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
                emission_LCV_P_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_P)*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
            
            emission_LCV_P = (emission_LCV_P_hot + emission_LCV_P_cold + emission_LCV_P_heated)*mass*time
                    
            #Diesel bus emissions 
            factor_B_D = traficEmissions.func_H_EF(v_H,"B","diesel","NOx","B1518",load,sloap)
            emission_B_D_hot = (nb_veh*w_B/100)*dist*(factor_B_D[0]*w_HDT_E1+factor_B_D[1]*w_HDT_E2+factor_B_D[2]*w_HDT_E3+factor_B_D[3]*w_HDT_E4+factor_B_D[4]*w_HDT_E5+factor_B_D[5]*w_HDT_E6)
            emission_B_D_cold = 0
            emission_B_D_heated = 0
            
            emission_B_D = (emission_B_D_hot + emission_B_D_cold + emission_B_D_heated)*mass*time
                    
            #Diesel heavy duty truck 14-20t emissions  
            factor_HDT_1420_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","NOx","HDT1420",load,sloap)
            emission_HDT_1420_D_hot = (nb_veh*w_HDT/100*w_HDT_1420)*dist*(factor_HDT_1420_D[0]*w_HDT_E1+factor_HDT_1420_D[1]*w_HDT_E2+factor_HDT_1420_D[2]*w_HDT_E3+factor_HDT_1420_D[3]*w_HDT_E4+factor_HDT_1420_D[4]*w_HDT_E5+factor_HDT_1420_D[5]*w_HDT_E6)
            emission_HDT_1420_D_cold = 0
            emission_HDT_1420_D_heated = 0
            
            emission_HDT_1420_D = (emission_HDT_1420_D_hot + emission_HDT_1420_D_cold + emission_HDT_1420_D_heated)*mass*time
                          
            #Diesel heavy duty truck 14-20t emissions 
            factor_HDT_32_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","NOx","HDT32",load,sloap)
            emission_HDT_32_D_hot = (nb_veh*w_HDT/100*w_HDT_32)*dist*(factor_HDT_32_D[0]*w_HDT_E1+factor_HDT_32_D[1]*w_HDT_E2+factor_HDT_32_D[2]*w_HDT_E3+factor_HDT_32_D[3]*w_HDT_E4+factor_HDT_32_D[4]*w_HDT_E5+factor_HDT_32_D[5]*w_HDT_E6)
            emission_HDT_32_D_cold = 0
            emission_HDT_32_D_heated = 0
            
            emission_HDT_32_D = (emission_HDT_32_D_hot + emission_HDT_32_D_cold + emission_HDT_32_D_heated)*mass*time
                    
            #Diesel heavy duty truck 14-20t emissions
            factor_L_P = traficEmissions.func_L_EF(v_L,"L","petrol","NOx")
            emission_L_P_hot = (nb_veh*w_L/100)*dist*(factor_L_P[0]*w_L_E1+factor_L_P[1]*w_L_E2+factor_L_P[2]*w_L_E3+factor_L_P[3]*w_L_E4+factor_L_P[4]*w_L_E5+factor_L_P[5]*w_L_E6)
            emission_L_P_cold = 0
            emission_L_P_heated = 0
            
            emission_L_P = (emission_L_P_hot + emission_L_P_cold + emission_L_P_heated)*mass*time
            
            #Total emissions
            emission_tot_NOx = emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P + emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P
            
            #Hot emissions for writing           
            if (i == 0):
                sum_LV_D_hot = (emission_LV_D_hot+emission_LV_D_heated)*mass*time
                sum_LV_P_hot = (emission_LV_P_hot+emission_LV_P_heated)*mass*time
                sum_LCV_D_hot = (emission_LCV_D_hot+emission_LCV_D_heated)*mass*time
                sum_LCV_P_hot = (emission_LCV_P_hot+emission_LCV_P_heated)*mass*time
                sum_B_D_hot = (emission_B_D_hot+emission_B_D_heated)*mass*time
                sum_HDT_1420_D_hot = (emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time
                sum_HDT_32_D_hot = (emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time
                sum_L_P_hot = (emission_L_P_hot+emission_L_P_heated)*mass*time
                sum_hot = (emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time
                LV_D_hot = "LV_D,"+str((emission_LV_D_hot+emission_LV_D_heated)*mass*time)+","
                LV_P_hot = "LV_P,"+str((emission_LV_P_hot+emission_LV_P_heated)*mass*time)+","
                LCV_D_hot = "LCV_D,"+str((emission_LCV_D_hot+emission_LCV_D_heated)*mass*time)+","
                LCV_P_hot = "LCV_P,"+str((emission_LCV_P_hot+emission_LCV_P_heated)*mass*time)+","
                B_D_hot = "B_D,"+str((emission_B_D_hot+emission_B_D_heated)*mass*time)+","
                HDT_1420_D_hot = "HDT_1420_D,"+str((emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time)+","
                HDT_32_D_hot = "HDT_32_D,"+str((emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time)+","
                L_P_hot = "L_P,"+str((emission_L_P_hot+emission_L_P_heated)*mass*time)+","
                All_hot = "All,"+str((emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time)+","
            else:
                sum_LV_D_hot += (emission_LV_D_hot+emission_LV_D_heated)*mass*time
                sum_LV_P_hot += (emission_LV_P_hot+emission_LV_P_heated)*mass*time
                sum_LCV_D_hot += (emission_LCV_D_hot+emission_LCV_D_heated)*mass*time
                sum_LCV_P_hot += (emission_LCV_P_hot+emission_LCV_P_heated)*mass*time
                sum_B_D_hot += (emission_B_D_hot+emission_B_D_heated)*mass*time
                sum_HDT_1420_D_hot += (emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time
                sum_HDT_32_D_hot += (emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time
                sum_L_P_hot += (emission_L_P_hot+emission_L_P_heated)*mass*time
                sum_hot += (emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time
                LV_D_hot = LV_D_hot+str((emission_LV_D_hot+emission_LV_D_heated)*mass*time)+","
                LV_P_hot = LV_P_hot+str((emission_LV_P_hot+emission_LV_P_heated)*mass*time)+","
                LCV_D_hot = LCV_D_hot+str((emission_LCV_D_hot+emission_LCV_D_heated)*mass*time)+","
                LCV_P_hot = LCV_P_hot+str((emission_LCV_P_hot+emission_LCV_P_heated)*mass*time)+","
                B_D_hot = B_D_hot+str((emission_B_D_hot+emission_B_D_heated)*mass*time)+","
                HDT_1420_D_hot = HDT_1420_D_hot+str((emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time)+","
                HDT_32_D_hot = HDT_32_D_hot+str((emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time)+","
                L_P_hot = L_P_hot+str((emission_L_P_hot+emission_L_P_heated)*mass*time)+","
                All_hot = All_hot+str((emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time)+","
                    
            #Cold emissions for writing
            if (i == 0):
                sum_LV_D_cold = emission_LV_D_cold*mass*time
                sum_LV_P_cold = emission_LV_P_cold*mass*time
                sum_LCV_D_cold = emission_LCV_D_cold*mass*time
                sum_LCV_P_cold = emission_LCV_P_cold*mass*time
                sum_B_D_cold = emission_B_D_cold*mass*time
                sum_HDT_1420_D_cold = emission_HDT_1420_D_cold*mass*time
                sum_HDT_32_D_cold = emission_HDT_32_D_cold*mass*time
                sum_L_P_cold = emission_L_P_cold*mass*time
                sum_cold = (emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold +  emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time
                LV_D_cold = "LV_D,"+str(emission_LV_D_cold*mass*time)+","
                LV_P_cold = "LV_P,"+str(emission_LV_P_cold*mass*time)+","
                LCV_D_cold = "LCV_D,"+str(emission_LCV_D_cold*mass*time)+","
                LCV_P_cold = "LCV_P,"+str(emission_LCV_P_cold*mass*time)+","
                B_D_cold = "B_D,"+str(emission_B_D_cold*mass*time)+","
                HDT_1420_D_cold = "HDT_1420_D,"+str(emission_HDT_1420_D_cold*mass*time)+","
                HDT_32_D_cold = "HDT_32_D,"+str(emission_HDT_32_D_cold*mass*time)+","
                L_P_cold = "L_P,"+str(emission_L_P_cold*mass*time)+","
                All_cold = "All,"+str((emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold + emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time)+","
            else:
                sum_LV_D_cold += emission_LV_D_cold*mass*time
                sum_LV_P_cold += emission_LV_P_cold*mass*time
                sum_LCV_D_cold += emission_LCV_D_cold*mass*time
                sum_LCV_P_cold += emission_LCV_P_cold*mass*time
                sum_B_D_cold += emission_B_D_cold*mass*time
                sum_HDT_1420_D_cold += emission_HDT_1420_D_cold*mass*time
                sum_HDT_32_D_cold += emission_HDT_32_D_cold*mass*time
                sum_L_P_cold += emission_L_P_cold*mass*time
                sum_cold += (emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold +  emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time
                LV_D_cold = LV_D_cold+str(emission_LV_D_cold*mass*time)+","
                LV_P_cold = LV_P_cold+str(emission_LV_P_cold*mass*time)+","
                LCV_D_cold = LCV_D_cold+str(emission_LCV_D_cold*mass*time)+","
                LCV_P_cold = LCV_P_cold+str(emission_LCV_P_cold*mass*time)+","
                B_D_cold = B_D_cold+str(emission_B_D_cold*mass*time)+","
                HDT_1420_D_cold = HDT_1420_D_cold+str(emission_HDT_1420_D_cold*mass*time)+","
                HDT_32_D_cold = HDT_32_D_cold+str(emission_HDT_32_D_cold*mass*time)+","
                L_P_cold = L_P_cold+str(emission_L_P_cold*mass*time)+","
                All_cold = All_cold+str((emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold +  emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time)+","
      
            #Totalemissions for writing
            if (i == 0):
                sum_LV_D = emission_LV_D
                sum_LV_P = emission_LV_P
                sum_LCV_D = emission_LCV_D
                sum_LCV_P = emission_LCV_P
                sum_B_D = emission_B_D
                sum_HDT_1420_D = emission_HDT_1420_D
                sum_HDT_32_D = emission_HDT_32_D
                sum_L_P = emission_L_P
                sum = (emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P +  emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P)
                LV_D = "LV_D,"+str(emission_LV_D)+","
                LV_P = "LV_P,"+str(emission_LV_P)+","
                LCV_D = "LCV_D,"+str(emission_LCV_D)+","
                LCV_P = "LCV_P,"+str(emission_LCV_P)+","
                B_D = "B_D,"+str(emission_B_D)+","
                HDT_1420_D = "HDT_1420_D,"+str(emission_HDT_1420_D)+","
                HDT_32_D = "HDT_32_D,"+str(emission_HDT_32_D)+","
                L_P = "L_P,"+str(emission_L_P)+","
                All = "All_NOx,"+str((emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P + emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P))+","
            else:
                sum_LV_D += emission_LV_D
                sum_LV_P += emission_LV_P
                sum_LCV_D += emission_LCV_D
                sum_LCV_P += emission_LCV_P
                sum_B_D += emission_B_D
                sum_HDT_1420_D += emission_HDT_1420_D
                sum_HDT_32_D += emission_HDT_32_D
                sum_L_P += emission_L_P
                sum += (emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P +  emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P)
                LV_D = LV_D+str(emission_LV_D)+","
                LV_P = LV_P+str(emission_LV_P)+","
                LCV_D = LCV_D+str(emission_LCV_D)+","
                LCV_P = LCV_P+str(emission_LCV_P)+","
                B_D = B_D+str(emission_B_D)+","
                HDT_1420_D = HDT_1420_D+str(emission_HDT_1420_D)+","
                HDT_32_D = HDT_32_D+str(emission_HDT_32_D)+","
                L_P = L_P+str(emission_L_P)+","
                All = All+str((emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P +  emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P))+","
      
        
        mean_LV_D_hot = sum_LV_D_hot / 24
        mean_LV_P_hot = sum_LV_P_hot / 24
        mean_LCV_D_hot = sum_LCV_D_hot / 24
        mean_LCV_P_hot = sum_LCV_P_hot / 24
        mean_B_D_hot = sum_B_D_hot / 24
        mean_HDT_1420_D_hot = sum_HDT_1420_D_hot / 24
        mean_HDT_32_D_hot = sum_HDT_32_D_hot / 24
        mean_L_P_hot = sum_L_P_hot / 24
        mean_All_hot = sum_hot / 24
            
        mean_LV_D_cold = sum_LV_D_cold / 24
        mean_LV_P_cold = sum_LV_P_cold / 24
        mean_LCV_D_cold = sum_LCV_D_cold / 24
        mean_LCV_P_cold = sum_LCV_P_cold / 24
        mean_B_D_cold = sum_B_D_cold / 24
        mean_HDT_1420_D_cold = sum_HDT_1420_D_cold / 24
        mean_HDT_32_D_cold = sum_HDT_32_D_cold / 24
        mean_L_P_cold = sum_L_P_cold / 24
        mean_All_cold = sum_cold / 24
        
        mean_LV_D = sum_LV_D / 24
        mean_LV_P = sum_LV_P / 24
        mean_LCV_D = sum_LCV_D / 24
        mean_LCV_P = sum_LCV_P / 24
        mean_B_D = sum_B_D / 24
        mean_HDT_1420_D = sum_HDT_1420_D / 24
        mean_HDT_32_D = sum_HDT_32_D / 24
        mean_L_P = sum_L_P / 24
        mean_All = sum / 24
        
        makeDirectory(dirEtude+"/NOx")
        
        with open(dirEtude+"/NOx/hotEmissionsNOx.csv","w") as hotEmissionsNOx :
            hotEmissionsNOx.write(title+"\n")
            hotEmissionsNOx.write(LV_D_hot+str(mean_LV_D_hot)+"\n")
            hotEmissionsNOx.write(LV_P_hot+str(mean_LV_P_hot)+"\n")
            hotEmissionsNOx.write(LCV_D_hot+str(mean_LCV_D_hot)+"\n")        
            hotEmissionsNOx.write(LCV_P_hot+str(mean_LCV_P_hot)+"\n")
            hotEmissionsNOx.write(B_D_hot+str(mean_B_D_hot)+"\n")
            hotEmissionsNOx.write(HDT_1420_D_hot+str(mean_HDT_1420_D_hot)+"\n")
            hotEmissionsNOx.write(HDT_32_D_hot+str(mean_HDT_32_D_hot)+"\n")
            hotEmissionsNOx.write(L_P_hot+str(mean_L_P_hot)+"\n")
            hotEmissionsNOx.write(All_hot+str(mean_All_hot)+"\n")
            
        with open(dirEtude+"/NOx/coldEmissionsNOx.csv","w") as coldEmissionsNOx :
            coldEmissionsNOx.write(title+"\n")
            coldEmissionsNOx.write(LV_D_cold+str(mean_LV_D_cold)+"\n")
            coldEmissionsNOx.write(LV_P_cold+str(mean_LV_P_cold)+"\n")
            coldEmissionsNOx.write(LCV_D_cold+str(mean_LCV_D_cold)+"\n")        
            coldEmissionsNOx.write(LCV_P_cold+str(mean_LCV_P_cold)+"\n")
            coldEmissionsNOx.write(B_D_cold+str(mean_B_D_cold)+"\n")
            coldEmissionsNOx.write(HDT_1420_D_cold+str(mean_HDT_1420_D_cold)+"\n")
            coldEmissionsNOx.write(HDT_32_D_cold+str(mean_HDT_32_D_cold)+"\n")
            coldEmissionsNOx.write(L_P_cold+str(mean_L_P_cold)+"\n")
            coldEmissionsNOx.write(All_cold+str(mean_All_cold)+"\n")
            
        with open(dirEtude+"/NOx/totalEmissionsNOx.csv","w") as totEmissionsNOx :
            totEmissionsNOx.write(title+"\n")
            totEmissionsNOx.write(LV_D+str(mean_LV_D)+"\n")
            totEmissionsNOx.write(LV_P+str(mean_LV_P)+"\n")
            totEmissionsNOx.write(LCV_D+str(mean_LCV_D)+"\n")        
            totEmissionsNOx.write(LCV_P+str(mean_LCV_P)+"\n")
            totEmissionsNOx.write(B_D+str(mean_B_D)+"\n")
            totEmissionsNOx.write(HDT_1420_D+str(mean_HDT_1420_D)+"\n")
            totEmissionsNOx.write(HDT_32_D+str(mean_HDT_32_D)+"\n")
            totEmissionsNOx.write(L_P+str(mean_L_P)+"\n")
            totEmissionsNOx.write(All+str(mean_All)+"\n")
            
        
            
    
        for i in range(0,24):
            
            nb_veh = list_nb_veh[i]
            v_L = list_v_L[i]
            v_H = list_v_H[i]
            
            ##################################################################################################################################################################################################################
            ##################################################################################################################################################################################################################
            #######################################################################  PM 
            #Light diesel vehicles emissions 
            factor_LV_D = traficEmissions.func_L_EF(v_L,"LV","diesel","PM")
            
            if v_L > 45:
                if forceCold == "no":
                    emission_LV_D_hot = (nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                    emission_LV_D_cold = 0
                    emission_LV_D_heated = 0
                elif forceCold == "yes":
                    CHR=A_CHR_LV_D_PM-temp*B_CHR_LV_D_PM
                    emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                    emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                    emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                else:
                    print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                    raise SystemExit(0)
            else:
                CHR = A_CHR_LV_D_PM-temp*B_CHR_LV_D_PM
                emission_LV_D_hot = (1-cold/100)*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_cold = trip/100*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*CHR*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
                emission_LV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LV/100*w_LV_D)*dist*(factor_LV_D[0]*w_LV_E1+factor_LV_D[1]*w_LV_E2+factor_LV_D[2]*w_LV_E3+factor_LV_D[3]*w_LV_E4+factor_LV_D[4]*w_LV_E5+factor_LV_D[5]*w_LV_E6)
            
            emission_LV_D = (emission_LV_D_hot + emission_LV_D_cold + emission_LV_D_heated)*mass*time
            
            #Light petrol vehicles emissions  
            factor_LV_P = traficEmissions.func_L_EF(v_L,"LV","petrol","PM")
            
            emission_LV_P_hot = (nb_veh*w_LV/100*w_LV_P)*dist*(factor_LV_P[0]*w_LV_E1+factor_LV_P[1]*w_LV_E2+factor_LV_P[2]*w_LV_E3+factor_LV_P[3]*w_LV_E4+factor_LV_P[4]*w_LV_E5+factor_LV_P[5]*w_LV_E6)
            emission_LV_P_cold = 0
            emission_LV_P_heated = 0
            
            emission_LV_P = (emission_LV_P_hot + emission_LV_P_cold + emission_LV_P_heated)*mass*time
            
            
            #Light commerical diesel vehicles emissions   
            factor_LCV_D = traficEmissions.func_L_EF(v_L,"LCV","diesel","PM")
            
            if v_L > 45:
                if forceCold == "no":
                    emission_LCV_D_hot = (nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                    emission_LCV_D_cold = 0
                    emission_LCV_D_heated = 0
                elif forceCold == "yes":
                    CHR=A_CHR_LCV_D_PM-temp*B_CHR_LCV_D_PM
                    emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                    emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                    emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                else:
                    print("!ERROR! Wrong argument for '"'forceCold'"' in" + CWD + "/input_emiCalc")
                    raise SystemExit(0)
            else:
                CHR = A_CHR_LCV_D_PM-temp*B_CHR_LCV_D_PM
                emission_LCV_D_hot = (1-cold/100)*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_cold = trip/100*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*CHR*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
                emission_LCV_D_heated = (1-trip/100)*cold/100*(nb_veh*w_LCV/100*w_LCV_D)*dist*(factor_LCV_D[0]*w_LCV_E1+factor_LCV_D[1]*w_LCV_E2+factor_LCV_D[2]*w_LCV_E3+factor_LCV_D[3]*w_LCV_E4+factor_LCV_D[4]*w_LCV_E5+factor_LCV_D[5]*w_LCV_E6)
            
            emission_LCV_D = (emission_LCV_D_hot + emission_LCV_D_cold + emission_LCV_D_heated)*mass*time
            
            
            #Light commerical petrol vehicles emissions 
            factor_LCV_P = traficEmissions.func_L_EF(v_L,"LCV","petrol","PM")
            
            emission_LCV_P_hot = (nb_veh*w_LCV/100*w_LCV_P)*dist*(factor_LCV_P[0]*w_LCV_E1+factor_LCV_P[1]*w_LCV_E2+factor_LCV_P[2]*w_LCV_E3+factor_LCV_P[3]*w_LCV_E4+factor_LCV_P[4]*w_LCV_E5+factor_LCV_P[5]*w_LCV_E6)
            emission_LCV_P_cold = 0
            emission_LCV_P_heated = 0
                
            emission_LCV_P = (emission_LCV_P_hot + emission_LCV_P_cold + emission_LCV_P_heated)*mass*time
                    
            #Diesel bus emissions 
            factor_B_D = traficEmissions.func_H_EF(v_H,"B","diesel","PM","B1518",load,sloap)
            emission_B_D_hot = (nb_veh*w_B/100)*dist*(factor_B_D[0]*w_HDT_E1+factor_B_D[1]*w_HDT_E2+factor_B_D[2]*w_HDT_E3+factor_B_D[3]*w_HDT_E4+factor_B_D[4]*w_HDT_E5+factor_B_D[5]*w_HDT_E6)
            emission_B_D_cold = 0
            emission_B_D_heated = 0
            
            emission_B_D = (emission_B_D_hot + emission_B_D_cold + emission_B_D_heated)*mass*time
                    
            #Diesel heavy duty truck 14-20t emissions  
            factor_HDT_1420_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","PM","HDT1420",load,sloap)
            emission_HDT_1420_D_hot = (nb_veh*w_HDT/100*w_HDT_1420)*dist*(factor_HDT_1420_D[0]*w_HDT_E1+factor_HDT_1420_D[1]*w_HDT_E2+factor_HDT_1420_D[2]*w_HDT_E3+factor_HDT_1420_D[3]*w_HDT_E4+factor_HDT_1420_D[4]*w_HDT_E5+factor_HDT_1420_D[5]*w_HDT_E6)
            emission_HDT_1420_D_cold = 0
            emission_HDT_1420_D_heated = 0
            
            emission_HDT_1420_D = (emission_HDT_1420_D_hot + emission_HDT_1420_D_cold + emission_HDT_1420_D_heated)*mass*time
                          
            #Diesel heavy duty truck 14-20t emissions 
            factor_HDT_32_D = traficEmissions.func_H_EF(v_H,"HDT","diesel","PM","HDT32",load,sloap)
            emission_HDT_32_D_hot = (nb_veh*w_HDT/100*w_HDT_32)*dist*(factor_HDT_32_D[0]*w_HDT_E1+factor_HDT_32_D[1]*w_HDT_E2+factor_HDT_32_D[2]*w_HDT_E3+factor_HDT_32_D[3]*w_HDT_E4+factor_HDT_32_D[4]*w_HDT_E5+factor_HDT_32_D[5]*w_HDT_E6)
            emission_HDT_32_D_cold = 0
            emission_HDT_32_D_heated = 0
            
            emission_HDT_32_D = (emission_HDT_32_D_hot + emission_HDT_32_D_cold + emission_HDT_32_D_heated)*mass*time
                    
            #Diesel heavy duty truck 14-20t emissions
            factor_L_P = traficEmissions.func_L_EF(v_L,"L","petrol","PM")
            emission_L_P_hot = (nb_veh*w_L/100)*dist*(factor_L_P[0]*w_L_E1+factor_L_P[1]*w_L_E2+factor_L_P[2]*w_L_E3+factor_L_P[3]*w_L_E4+factor_L_P[4]*w_L_E5+factor_L_P[5]*w_L_E6)
            emission_L_P_cold = 0
            emission_L_P_heated = 0
            
            emission_L_P = (emission_L_P_hot + emission_L_P_cold + emission_L_P_heated)*mass*time
            
            #Total emissions
            emission_tot_PM = emission_LV_D + emission_LV_P + emission_LCV_D + emission_LCV_P + emission_B_D + emission_HDT_1420_D + emission_HDT_32_D + emission_L_P
            
            ######################################################### Other emissions
            with open(CWD+"/data/Emep_Emission_Factors_2016/massFractionTSP.csv", "r") as massFractionTSPFile :
                lines_massFractionTSPFile = massFractionTSPFile.readlines()
            massFractionTSPFile.close()
            FM_TSP_Tyre_PM10=float(lines_massFractionTSPFile[2].split(",")[1])
            FM_TSP_Brake_PM10=float(lines_massFractionTSPFile[2].split(",")[2])
            FM_TSP_Road_PM10=float(lines_massFractionTSPFile[2].split(",")[3])
            FM_TSP_Tyre_PM2_5=float(lines_massFractionTSPFile[3].split(",")[1])
            FM_TSP_Brake_PM2_5=float(lines_massFractionTSPFile[3].split(",")[2])
            FM_TSP_Road_PM2_5=float(lines_massFractionTSPFile[3].split(",")[3])
            
            with open(CWD+"/data/Emep_Emission_Factors_2016/emissionFactorTSP.csv", "r") as emissionFactorTSPFile :
                lines_emissionFactorTSPFile = emissionFactorTSPFile.readlines()
            emissionFactorTSPFile.close()
            EF_TSP_Tyre_L=float(lines_emissionFactorTSPFile[1].split(",")[1])
            EF_TSP_Tyre_LV=float(lines_emissionFactorTSPFile[2].split(",")[1])
            EF_TSP_Tyre_LDT=float(lines_emissionFactorTSPFile[3].split(",")[1])
            EF_TSP_Brake_L=float(lines_emissionFactorTSPFile[1].split(",")[2])
            EF_TSP_Brake_LV=float(lines_emissionFactorTSPFile[2].split(",")[2])
            EF_TSP_Brake_LDT=float(lines_emissionFactorTSPFile[3].split(",")[2])
            EF_TSP_Road_L=float(lines_emissionFactorTSPFile[1].split(",")[3])
            EF_TSP_Road_LV=float(lines_emissionFactorTSPFile[2].split(",")[3])
            EF_TSP_Road_LDT=float(lines_emissionFactorTSPFile[3].split(",")[3])
            EF_TSP_Road_HDT=float(lines_emissionFactorTSPFile[4].split(",")[3])
            
            ######################################################### Tyre emissions
            if v_L > 90:
                St_LV = 0.902
            elif v_L > 40:
                St_LV = -0.00974*v_L+1.78
            else:
                St_LV = 1.39
                
            if v_H > 90:
                St_HV = 0.902
            elif v_H > 40:
                St_HV = -0.00974*v_H+1.78
            else:
                St_HV = 1.39
            
            LCFt = 1.41+(1.38*load_int/100)
            
            tyre_LV_PM10 = nb_veh*w_LV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM10*St_LV/100*mass*time
            tyre_LCV_PM10 = nb_veh*w_LCV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM10*St_LV/100*mass*time
            tyre_B_PM10 = nb_veh*w_B*dist*EF_TSP_Tyre_LDT*FM_TSP_Tyre_PM10*St_HV/100*mass*time
            tyre_HDT1420_PM10 = nb_veh*w_HDT*w_HDT_1420*dist*(3/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM10*St_HV/100*mass*time
            tyre_HDT32_PM10 = nb_veh*w_HDT*w_HDT_32*dist*(5/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM10*St_HV/100*mass*time
            tyre_L_PM10 = nb_veh*w_L*dist*EF_TSP_Tyre_L*FM_TSP_Tyre_PM10*St_LV/100*mass*time
            tyre_all_PM10 = tyre_LV_PM10 + tyre_LCV_PM10 + tyre_B_PM10 + tyre_HDT1420_PM10 + tyre_HDT32_PM10 + tyre_L_PM10
            
            tyre_LV_PM2_5 = nb_veh*w_LV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM2_5*St_LV/100*mass*time
            tyre_LCV_PM2_5 = nb_veh*w_LCV*dist*EF_TSP_Tyre_LV*FM_TSP_Tyre_PM2_5*St_LV/100*mass*time
            tyre_B_PM2_5 = nb_veh*w_B*dist*EF_TSP_Tyre_LDT*FM_TSP_Tyre_PM2_5*St_HV/100*mass*time
            tyre_HDT1420_PM2_5 = nb_veh*w_HDT*w_HDT_1420*dist*(3/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM2_5*St_HV/100*mass*time
            tyre_HDT32_PM2_5 = nb_veh*w_HDT*w_HDT_32*dist*(5/2*LCFt*EF_TSP_Tyre_LV)*FM_TSP_Tyre_PM2_5*St_HV/100*mass*time
            tyre_L_PM2_5 = nb_veh*w_L*dist*EF_TSP_Tyre_L*FM_TSP_Tyre_PM2_5*St_LV/100*mass*time
            tyre_all_PM2_5 = tyre_LV_PM2_5 + tyre_LCV_PM2_5 + tyre_B_PM2_5 + tyre_HDT1420_PM2_5 + tyre_HDT32_PM2_5 + tyre_L_PM2_5
            
            ######################################################### Brake emissions
            if v_L > 90:
                Sb_LV = 0.185
            elif v_L > 40:
                Sb_LV = -0.0270*v_L+2.75
            else:
                Sb_LV = 1.67
                
            if v_H > 90:
                Sb_HV = 0.185
            elif v_H > 40:
                Sb_HV = -0.0270*v_H+2.75
            else:
                Sb_HV = 1.67
            
            LCFb = 1+(0.79*load_int/100)
            
            brake_LV_PM10 = nb_veh*w_LV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM10*Sb_LV/100*mass*time
            brake_LCV_PM10 = nb_veh*w_LCV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM10*Sb_LV/100*mass*time
            brake_B_PM10 = nb_veh*w_B*dist*EF_TSP_Brake_LDT*FM_TSP_Brake_PM10*Sb_HV/100*mass*time
            brake_HDT1420_PM10 = nb_veh*w_HDT*w_HDT_1420*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM10*Sb_HV/100*mass*time
            brake_HDT32_PM10 = nb_veh*w_HDT*w_HDT_32*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM10*Sb_HV/100*mass*time
            brake_L_PM10 = nb_veh*w_L*dist*EF_TSP_Brake_L*FM_TSP_Brake_PM10*Sb_LV/100*mass*time
            brake_all_PM10 = brake_LV_PM10 + brake_LCV_PM10 + brake_B_PM10 + brake_HDT1420_PM10 + brake_HDT32_PM10 + brake_L_PM10
            
            brake_LV_PM2_5 = nb_veh*w_LV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM2_5*Sb_LV/100*mass*time
            brake_LCV_PM2_5 = nb_veh*w_LCV*dist*EF_TSP_Brake_LV*FM_TSP_Brake_PM2_5*Sb_LV/100*mass*time
            brake_B_PM2_5 = nb_veh*w_B*dist*EF_TSP_Brake_LDT*FM_TSP_Brake_PM2_5*Sb_HV/100*mass*time
            brake_HDT1420_PM2_5 = nb_veh*w_HDT*w_HDT_1420*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM2_5*Sb_HV/100*mass*time
            brake_HDT32_PM2_5 = nb_veh*w_HDT*w_HDT_32*dist*(3.13*LCFb*EF_TSP_Brake_LV)*FM_TSP_Brake_PM2_5*Sb_HV/100*mass*time
            brake_L_PM2_5 = nb_veh*w_L*dist*EF_TSP_Brake_L*FM_TSP_Brake_PM2_5*Sb_LV/100*mass*time
            brake_all_PM2_5 = brake_LV_PM2_5 + brake_LCV_PM2_5 + brake_B_PM2_5 + brake_HDT1420_PM2_5 + brake_HDT32_PM2_5 + brake_L_PM2_5
            
            ######################################################### Road emissions
            road_LV_PM10 = nb_veh*w_LV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM10/100*mass*time
            road_LCV_PM10 = nb_veh*w_LCV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM10/100*mass*time
            road_B_PM10 = nb_veh*w_B*dist*EF_TSP_Road_LDT*FM_TSP_Road_PM10/100*mass*time
            road_HDT1420_PM10 = nb_veh*w_HDT*w_HDT_1420*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM10/100*mass*time
            road_HDT32_PM10 = nb_veh*w_HDT*w_HDT_32*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM10/100*mass*time
            road_L_PM10 = nb_veh*w_L*dist*EF_TSP_Road_L*FM_TSP_Road_PM10/100*mass*time
            road_all_PM10 = road_LV_PM10 + road_LCV_PM10 + road_B_PM10 + road_HDT1420_PM10 + road_HDT32_PM10 + road_L_PM10
            
            road_LV_PM2_5 = nb_veh*w_LV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM2_5/100*mass*time
            road_LCV_PM2_5 = nb_veh*w_LCV*dist*EF_TSP_Road_LV*FM_TSP_Road_PM2_5/100*mass*time
            road_B_PM2_5 = nb_veh*w_B*dist*EF_TSP_Road_LDT*FM_TSP_Road_PM2_5/100*mass*time
            road_HDT1420_PM2_5 = nb_veh*w_HDT*w_HDT_1420*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM2_5/100*mass*time
            road_HDT32_PM2_5 = nb_veh*w_HDT*w_HDT_32*dist*EF_TSP_Road_HDT*FM_TSP_Road_PM2_5/100*mass*time
            road_L_PM2_5 = nb_veh*w_L*dist*EF_TSP_Road_L*FM_TSP_Road_PM2_5/100*mass*time
            road_all_PM2_5 = road_LV_PM2_5 + road_LCV_PM2_5 + road_B_PM2_5 + road_HDT1420_PM2_5 + road_HDT32_PM2_5 + road_L_PM2_5
            
            #Hot emissions for writing           
            if (i == 0):
                sum_LV_D_hot = (emission_LV_D_hot+emission_LV_D_heated)*mass*time
                sum_LV_P_hot = (emission_LV_P_hot+emission_LV_P_heated)*mass*time
                sum_LCV_D_hot = (emission_LCV_D_hot+emission_LCV_D_heated)*mass*time
                sum_LCV_P_hot = (emission_LCV_P_hot+emission_LCV_P_heated)*mass*time
                sum_B_D_hot = (emission_B_D_hot+emission_B_D_heated)*mass*time
                sum_HDT_1420_D_hot = (emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time
                sum_HDT_32_D_hot = (emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time
                sum_L_P_hot = (emission_L_P_hot+emission_L_P_heated)*mass*time
                sum_hot = (emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time
                LV_D_hot = "LV_D,"+str((emission_LV_D_hot+emission_LV_D_heated)*mass*time)+","
                LV_P_hot = "LV_P,"+str((emission_LV_P_hot+emission_LV_P_heated)*mass*time)+","
                LCV_D_hot = "LCV_D,"+str((emission_LCV_D_hot+emission_LCV_D_heated)*mass*time)+","
                LCV_P_hot = "LCV_P,"+str((emission_LCV_P_hot+emission_LCV_P_heated)*mass*time)+","
                B_D_hot = "B_D,"+str((emission_B_D_hot+emission_B_D_heated)*mass*time)+","
                HDT_1420_D_hot = "HDT_1420_D,"+str((emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time)+","
                HDT_32_D_hot = "HDT_32_D,"+str((emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time)+","
                L_P_hot = "L_P,"+str((emission_L_P_hot+emission_L_P_heated)*mass*time)+","
                All_hot = "All,"+str((emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time)+","
            else:
                sum_LV_D_hot += (emission_LV_D_hot+emission_LV_D_heated)*mass*time
                sum_LV_P_hot += (emission_LV_P_hot+emission_LV_P_heated)*mass*time
                sum_LCV_D_hot += (emission_LCV_D_hot+emission_LCV_D_heated)*mass*time
                sum_LCV_P_hot += (emission_LCV_P_hot+emission_LCV_P_heated)*mass*time
                sum_B_D_hot += (emission_B_D_hot+emission_B_D_heated)*mass*time
                sum_HDT_1420_D_hot += (emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time
                sum_HDT_32_D_hot += (emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time
                sum_L_P_hot += (emission_L_P_hot+emission_L_P_heated)*mass*time
                sum_hot += (emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time
                LV_D_hot = LV_D_hot+str((emission_LV_D_hot+emission_LV_D_heated)*mass*time)+","
                LV_P_hot = LV_P_hot+str((emission_LV_P_hot+emission_LV_P_heated)*mass*time)+","
                LCV_D_hot = LCV_D_hot+str((emission_LCV_D_hot+emission_LCV_D_heated)*mass*time)+","
                LCV_P_hot = LCV_P_hot+str((emission_LCV_P_hot+emission_LCV_P_heated)*mass*time)+","
                B_D_hot = B_D_hot+str((emission_B_D_hot+emission_B_D_heated)*mass*time)+","
                HDT_1420_D_hot = HDT_1420_D_hot+str((emission_HDT_1420_D_hot+emission_HDT_1420_D_heated)*mass*time)+","
                HDT_32_D_hot = HDT_32_D_hot+str((emission_HDT_32_D_hot+emission_HDT_32_D_heated)*mass*time)+","
                L_P_hot = L_P_hot+str((emission_L_P_hot+emission_L_P_heated)*mass*time)+","
                All_hot = All_hot+str((emission_LV_D_hot + emission_LV_P_hot + emission_LCV_D_hot + emission_LCV_P_hot +  emission_B_D_hot + emission_HDT_1420_D_hot + emission_HDT_32_D_hot + emission_L_P_hot + emission_LV_D_heated + emission_LV_P_heated + emission_LCV_D_heated + emission_LCV_P_heated +  emission_B_D_heated + emission_HDT_1420_D_heated + emission_HDT_32_D_heated + emission_L_P_heated)*mass*time)+","
            
            #Cold emissions for writing
            if (i == 0):
                sum_LV_D_cold = emission_LV_D_cold*mass*time
                sum_LV_P_cold = emission_LV_P_cold*mass*time
                sum_LCV_D_cold = emission_LCV_D_cold*mass*time
                sum_LCV_P_cold = emission_LCV_P_cold*mass*time
                sum_B_D_cold = emission_B_D_cold*mass*time
                sum_HDT_1420_D_cold = emission_HDT_1420_D_cold*mass*time
                sum_HDT_32_D_cold = emission_HDT_32_D_cold*mass*time
                sum_L_P_cold = emission_L_P_cold*mass*time
                sum_cold = (emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold +  emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time
                LV_D_cold = "LV_D,"+str(emission_LV_D_cold*mass*time)+","
                LV_P_cold = "LV_P,"+str(emission_LV_P_cold*mass*time)+","
                LCV_D_cold = "LCV_D,"+str(emission_LCV_D_cold*mass*time)+","
                LCV_P_cold = "LCV_P,"+str(emission_LCV_P_cold*mass*time)+","
                B_D_cold = "B_D,"+str(emission_B_D_cold*mass*time)+","
                HDT_1420_D_cold = "HDT_1420_D,"+str(emission_HDT_1420_D_cold*mass*time)+","
                HDT_32_D_cold = "HDT_32_D,"+str(emission_HDT_32_D_cold*mass*time)+","
                L_P_cold = "L_P,"+str(emission_L_P_cold*mass*time)+","
                All_cold = "All,"+str((emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold + emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time)+","
            else:
                sum_LV_D_cold += emission_LV_D_cold*mass*time
                sum_LV_P_cold += emission_LV_P_cold*mass*time
                sum_LCV_D_cold += emission_LCV_D_cold*mass*time
                sum_LCV_P_cold += emission_LCV_P_cold*mass*time
                sum_B_D_cold += emission_B_D_cold*mass*time
                sum_HDT_1420_D_cold += emission_HDT_1420_D_cold*mass*time
                sum_HDT_32_D_cold += emission_HDT_32_D_cold*mass*time
                sum_L_P_cold += emission_L_P_cold*mass*time
                sum_cold += (emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold +  emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time
                LV_D_cold = LV_D_cold+str(emission_LV_D_cold*mass*time)+","
                LV_P_cold = LV_P_cold+str(emission_LV_P_cold*mass*time)+","
                LCV_D_cold = LCV_D_cold+str(emission_LCV_D_cold*mass*time)+","
                LCV_P_cold = LCV_P_cold+str(emission_LCV_P_cold*mass*time)+","
                B_D_cold = B_D_cold+str(emission_B_D_cold*mass*time)+","
                HDT_1420_D_cold = HDT_1420_D_cold+str(emission_HDT_1420_D_cold*mass*time)+","
                HDT_32_D_cold = HDT_32_D_cold+str(emission_HDT_32_D_cold*mass*time)+","
                L_P_cold = L_P_cold+str(emission_L_P_cold*mass*time)+","
                All_cold = All_cold+str((emission_LV_D_cold + emission_LV_P_cold + emission_LCV_D_cold + emission_LCV_P_cold +  emission_B_D_cold + emission_HDT_1420_D_cold + emission_HDT_32_D_cold + emission_L_P_cold)*mass*time)+","
        
            #PM10 tyre emissions for writing
            if (i == 0):
                sum_LV_D_tyre_PM10 = tyre_LV_PM10*w_LV_D
                sum_LV_P_tyre_PM10 = tyre_LV_PM10*w_LV_P
                sum_LCV_D_tyre_PM10 = tyre_LCV_PM10*w_LV_D
                sum_LCV_P_tyre_PM10 = tyre_LCV_PM10*w_LV_P
                sum_B_D_tyre_PM10 = tyre_B_PM10
                sum_HDT_1420_D_tyre_PM10 = tyre_HDT1420_PM10
                sum_HDT_32_D_tyre_PM10 = tyre_HDT32_PM10
                sum_L_P_tyre_PM10 = tyre_L_PM10
                sum_tyre_PM10 = tyre_LV_PM10+tyre_LCV_PM10+tyre_B_PM10+tyre_HDT1420_PM10+tyre_HDT32_PM10+tyre_L_PM10
                LV_D_tyre_PM10 = "LV_D,"+str(tyre_LV_PM10*w_LV_D)+","
                LV_P_tyre_PM10 = "LV_P,"+str(tyre_LV_PM10*w_LV_P)+","
                LCV_D_tyre_PM10 = "LCV_D,"+str(tyre_LCV_PM10*w_LV_D)+","
                LCV_P_tyre_PM10 = "LCV_P,"+str(tyre_LCV_PM10*w_LV_P)+","
                B_D_tyre_PM10 = "B_D,"+str(tyre_B_PM10)+","
                HDT_1420_D_tyre_PM10 = "HDT_1420_D,"+str(tyre_HDT1420_PM10)+","
                HDT_32_D_tyre_PM10 = "HDT_32_D,"+str(tyre_HDT32_PM10)+","
                L_P_tyre_PM10 = "L_P,"+str(tyre_L_PM10)+","
                All_tyre_PM10 = "All,"+str(tyre_LV_PM10+tyre_LCV_PM10+tyre_B_PM10+tyre_HDT1420_PM10+tyre_HDT32_PM10+tyre_L_PM10)+","
            else:
                sum_LV_D_tyre_PM10 += tyre_LV_PM10*w_LV_D
                sum_LV_P_tyre_PM10 += tyre_LV_PM10*w_LV_P
                sum_LCV_D_tyre_PM10 += tyre_LCV_PM10*w_LV_D
                sum_LCV_P_tyre_PM10 += tyre_LCV_PM10*w_LV_P
                sum_B_D_tyre_PM10 += tyre_B_PM10
                sum_HDT_1420_D_tyre_PM10 += tyre_HDT1420_PM10
                sum_HDT_32_D_tyre_PM10 += tyre_HDT32_PM10
                sum_L_P_tyre_PM10 += tyre_L_PM10
                sum_tyre_PM10 += tyre_LV_PM10+tyre_LCV_PM10+tyre_B_PM10+tyre_HDT1420_PM10+tyre_HDT32_PM10+tyre_L_PM10
                LV_D_tyre_PM10 = LV_D_tyre_PM10+str(tyre_LV_PM10*w_LV_D)+","
                LV_P_tyre_PM10 = LV_P_tyre_PM10+str(tyre_LV_PM10*w_LV_P)+","
                LCV_D_tyre_PM10 = LCV_D_tyre_PM10+str(tyre_LCV_PM10*w_LV_D)+","
                LCV_P_tyre_PM10 = LCV_P_tyre_PM10+str(tyre_LCV_PM10*w_LV_P)+","
                B_D_tyre_PM10 = B_D_tyre_PM10+str(tyre_B_PM10)+","
                HDT_1420_D_tyre_PM10 = HDT_1420_D_tyre_PM10+str(tyre_HDT1420_PM10)+","
                HDT_32_D_tyre_PM10 = HDT_32_D_tyre_PM10+str(tyre_HDT32_PM10)+","
                L_P_tyre_PM10 = L_P_tyre_PM10+str(tyre_L_PM10)+","
                All_tyre_PM10 = All_tyre_PM10+str(tyre_LV_PM10+tyre_LCV_PM10+tyre_B_PM10+tyre_HDT1420_PM10+tyre_HDT32_PM10+tyre_L_PM10)+","
        
            #PM2_5 tyre emissions for writing
            if (i == 0):
                sum_LV_D_tyre_PM2_5 = tyre_LV_PM2_5*w_LV_D
                sum_LV_P_tyre_PM2_5 = tyre_LV_PM2_5*w_LV_P
                sum_LCV_D_tyre_PM2_5 = tyre_LCV_PM2_5*w_LV_D
                sum_LCV_P_tyre_PM2_5 = tyre_LCV_PM2_5*w_LV_P
                sum_B_D_tyre_PM2_5 = tyre_B_PM2_5
                sum_HDT_1420_D_tyre_PM2_5 = tyre_HDT1420_PM2_5
                sum_HDT_32_D_tyre_PM2_5 = tyre_HDT32_PM2_5
                sum_L_P_tyre_PM2_5 = tyre_L_PM2_5
                sum_tyre_PM2_5 = tyre_LV_PM2_5+tyre_LCV_PM2_5+tyre_B_PM2_5+tyre_HDT1420_PM2_5+tyre_HDT32_PM2_5+tyre_L_PM2_5
                LV_D_tyre_PM2_5 = "LV_D,"+str(tyre_LV_PM2_5*w_LV_D)+","
                LV_P_tyre_PM2_5 = "LV_P,"+str(tyre_LV_PM2_5*w_LV_P)+","
                LCV_D_tyre_PM2_5 = "LCV_D,"+str(tyre_LCV_PM2_5*w_LV_D)+","
                LCV_P_tyre_PM2_5 = "LCV_P,"+str(tyre_LCV_PM2_5*w_LV_P)+","
                B_D_tyre_PM2_5 = "B_D,"+str(tyre_B_PM2_5)+","
                HDT_1420_D_tyre_PM2_5 = "HDT_1420_D,"+str(tyre_HDT1420_PM2_5)+","
                HDT_32_D_tyre_PM2_5 = "HDT_32_D,"+str(tyre_HDT32_PM2_5)+","
                L_P_tyre_PM2_5 = "L_P,"+str(tyre_L_PM2_5)+","
                All_tyre_PM2_5 = "All,"+str(tyre_LV_PM2_5+tyre_LCV_PM2_5+tyre_B_PM2_5+tyre_HDT1420_PM2_5+tyre_HDT32_PM2_5+tyre_L_PM2_5)+","
            else:
                sum_LV_D_tyre_PM2_5 += tyre_LV_PM2_5*w_LV_D
                sum_LV_P_tyre_PM2_5 += tyre_LV_PM2_5*w_LV_P
                sum_LCV_D_tyre_PM2_5 += tyre_LCV_PM2_5*w_LV_D
                sum_LCV_P_tyre_PM2_5 += tyre_LCV_PM2_5*w_LV_P
                sum_B_D_tyre_PM2_5 += tyre_B_PM2_5
                sum_HDT_1420_D_tyre_PM2_5 += tyre_HDT1420_PM2_5
                sum_HDT_32_D_tyre_PM2_5 += tyre_HDT32_PM2_5
                sum_L_P_tyre_PM2_5 += tyre_L_PM2_5
                sum_tyre_PM2_5 += tyre_LV_PM2_5+tyre_LCV_PM2_5+tyre_B_PM2_5+tyre_HDT1420_PM2_5+tyre_HDT32_PM2_5+tyre_L_PM2_5
                LV_D_tyre_PM2_5 = LV_D_tyre_PM2_5+str(tyre_LV_PM2_5*w_LV_D)+","
                LV_P_tyre_PM2_5 = LV_P_tyre_PM2_5+str(tyre_LV_PM2_5*w_LV_P)+","
                LCV_D_tyre_PM2_5 = LCV_D_tyre_PM2_5+str(tyre_LCV_PM2_5*w_LV_D)+","
                LCV_P_tyre_PM2_5 = LCV_P_tyre_PM2_5+str(tyre_LCV_PM2_5*w_LV_P)+","
                B_D_tyre_PM2_5 = B_D_tyre_PM2_5+str(tyre_B_PM2_5)+","
                HDT_1420_D_tyre_PM2_5 = HDT_1420_D_tyre_PM2_5+str(tyre_HDT1420_PM2_5)+","
                HDT_32_D_tyre_PM2_5 = HDT_32_D_tyre_PM2_5+str(tyre_HDT32_PM2_5)+","
                L_P_tyre_PM2_5 = L_P_tyre_PM2_5+str(tyre_L_PM2_5)+","
                All_tyre_PM2_5 = All_tyre_PM2_5+str(tyre_LV_PM2_5+tyre_LCV_PM2_5+tyre_B_PM2_5+tyre_HDT1420_PM2_5+tyre_HDT32_PM2_5+tyre_L_PM2_5)+","
                
            #PM10 brake emissions for writing
            if (i == 0):
                sum_LV_D_brake_PM10 = brake_LV_PM10*w_LV_D
                sum_LV_P_brake_PM10 = brake_LV_PM10*w_LV_P
                sum_LCV_D_brake_PM10 = brake_LCV_PM10*w_LV_D
                sum_LCV_P_brake_PM10 = brake_LCV_PM10*w_LV_P
                sum_B_D_brake_PM10 = brake_B_PM10
                sum_HDT_1420_D_brake_PM10 = brake_HDT1420_PM10
                sum_HDT_32_D_brake_PM10 = brake_HDT32_PM10
                sum_L_P_brake_PM10 = brake_L_PM10
                sum_brake_PM10 = brake_LV_PM10+brake_LCV_PM10+brake_B_PM10+brake_HDT1420_PM10+brake_HDT32_PM10+brake_L_PM10
                LV_D_brake_PM10 = "LV_D,"+str(brake_LV_PM10*w_LV_D)+","
                LV_P_brake_PM10 = "LV_P,"+str(brake_LV_PM10*w_LV_P)+","
                LCV_D_brake_PM10 = "LCV_D,"+str(brake_LCV_PM10*w_LV_D)+","
                LCV_P_brake_PM10 = "LCV_P,"+str(brake_LCV_PM10*w_LV_P)+","
                B_D_brake_PM10 = "B_D,"+str(brake_B_PM10)+","
                HDT_1420_D_brake_PM10 = "HDT_1420_D,"+str(brake_HDT1420_PM10)+","
                HDT_32_D_brake_PM10 = "HDT_32_D,"+str(brake_HDT32_PM10)+","
                L_P_brake_PM10 = "L_P,"+str(brake_L_PM10)+","
                All_brake_PM10 = "All,"+str(brake_LV_PM10+brake_LCV_PM10+brake_B_PM10+brake_HDT1420_PM10+brake_HDT32_PM10+brake_L_PM10)+","
            else:
                sum_LV_D_brake_PM10 += brake_LV_PM10*w_LV_D
                sum_LV_P_brake_PM10 += brake_LV_PM10*w_LV_P
                sum_LCV_D_brake_PM10 += brake_LCV_PM10*w_LV_D
                sum_LCV_P_brake_PM10 += brake_LCV_PM10*w_LV_P
                sum_B_D_brake_PM10 += brake_B_PM10
                sum_HDT_1420_D_brake_PM10 += brake_HDT1420_PM10
                sum_HDT_32_D_brake_PM10 += brake_HDT32_PM10
                sum_L_P_brake_PM10 += brake_L_PM10
                sum_brake_PM10 += brake_LV_PM10+brake_LCV_PM10+brake_B_PM10+brake_HDT1420_PM10+brake_HDT32_PM10+brake_L_PM10
                LV_D_brake_PM10 = LV_D_brake_PM10+str(brake_LV_PM10*w_LV_D)+","
                LV_P_brake_PM10 = LV_P_brake_PM10+str(brake_LV_PM10*w_LV_P)+","
                LCV_D_brake_PM10 = LCV_D_brake_PM10+str(brake_LCV_PM10*w_LV_D)+","
                LCV_P_brake_PM10 = LCV_P_brake_PM10+str(brake_LCV_PM10*w_LV_P)+","
                B_D_brake_PM10 = B_D_brake_PM10+str(brake_B_PM10)+","
                HDT_1420_D_brake_PM10 = HDT_1420_D_brake_PM10+str(brake_HDT1420_PM10)+","
                HDT_32_D_brake_PM10 = HDT_32_D_brake_PM10+str(brake_HDT32_PM10)+","
                L_P_brake_PM10 = L_P_brake_PM10+str(brake_L_PM10)+","
                All_brake_PM10 = All_brake_PM10+str(brake_LV_PM10+brake_LCV_PM10+brake_B_PM10+brake_HDT1420_PM10+brake_HDT32_PM10+brake_L_PM10)+","
        
            #PM2_5 brake emissions for writing
            if (i == 0):
                sum_LV_D_brake_PM2_5 = brake_LV_PM2_5*w_LV_D
                sum_LV_P_brake_PM2_5 = brake_LV_PM2_5*w_LV_P
                sum_LCV_D_brake_PM2_5 = brake_LCV_PM2_5*w_LV_D
                sum_LCV_P_brake_PM2_5 = brake_LCV_PM2_5*w_LV_P
                sum_B_D_brake_PM2_5 = brake_B_PM2_5
                sum_HDT_1420_D_brake_PM2_5 = brake_HDT1420_PM2_5
                sum_HDT_32_D_brake_PM2_5 = brake_HDT32_PM2_5
                sum_L_P_brake_PM2_5 = brake_L_PM2_5
                sum_brake_PM2_5 = brake_LV_PM2_5+brake_LCV_PM2_5+brake_B_PM2_5+brake_HDT1420_PM2_5+brake_HDT32_PM2_5+brake_L_PM2_5
                LV_D_brake_PM2_5 = "LV_D,"+str(brake_LV_PM2_5*w_LV_D)+","
                LV_P_brake_PM2_5 = "LV_P,"+str(brake_LV_PM2_5*w_LV_P)+","
                LCV_D_brake_PM2_5 = "LCV_D,"+str(brake_LCV_PM2_5*w_LV_D)+","
                LCV_P_brake_PM2_5 = "LCV_P,"+str(brake_LCV_PM2_5*w_LV_P)+","
                B_D_brake_PM2_5 = "B_D,"+str(brake_B_PM2_5)+","
                HDT_1420_D_brake_PM2_5 = "HDT_1420_D,"+str(brake_HDT1420_PM2_5)+","
                HDT_32_D_brake_PM2_5 = "HDT_32_D,"+str(brake_HDT32_PM2_5)+","
                L_P_brake_PM2_5 = "L_P,"+str(brake_L_PM2_5)+","
                All_brake_PM2_5 = "All,"+str(brake_LV_PM2_5+brake_LCV_PM2_5+brake_B_PM2_5+brake_HDT1420_PM2_5+brake_HDT32_PM2_5+brake_L_PM2_5)+","
            else:
                sum_LV_D_brake_PM2_5 += brake_LV_PM2_5*w_LV_D
                sum_LV_P_brake_PM2_5 += brake_LV_PM2_5*w_LV_P
                sum_LCV_D_brake_PM2_5 += brake_LCV_PM2_5*w_LV_D
                sum_LCV_P_brake_PM2_5 += brake_LCV_PM2_5*w_LV_P
                sum_B_D_brake_PM2_5 += brake_B_PM2_5
                sum_HDT_1420_D_brake_PM2_5 += brake_HDT1420_PM2_5
                sum_HDT_32_D_brake_PM2_5 += brake_HDT32_PM2_5
                sum_L_P_brake_PM2_5 += brake_L_PM2_5
                sum_brake_PM2_5 += brake_LV_PM2_5+brake_LCV_PM2_5+brake_B_PM2_5+brake_HDT1420_PM2_5+brake_HDT32_PM2_5+brake_L_PM2_5
                LV_D_brake_PM2_5 = LV_D_brake_PM2_5+str(brake_LV_PM2_5*w_LV_D)+","
                LV_P_brake_PM2_5 = LV_P_brake_PM2_5+str(brake_LV_PM2_5*w_LV_P)+","
                LCV_D_brake_PM2_5 = LCV_D_brake_PM2_5+str(brake_LCV_PM2_5*w_LV_D)+","
                LCV_P_brake_PM2_5 = LCV_P_brake_PM2_5+str(brake_LCV_PM2_5*w_LV_P)+","
                B_D_brake_PM2_5 = B_D_brake_PM2_5+str(brake_B_PM2_5)+","
                HDT_1420_D_brake_PM2_5 = HDT_1420_D_brake_PM2_5+str(brake_HDT1420_PM2_5)+","
                HDT_32_D_brake_PM2_5 = HDT_32_D_brake_PM2_5+str(brake_HDT32_PM2_5)+","
                L_P_brake_PM2_5 = L_P_brake_PM2_5+str(brake_L_PM2_5)+","
                All_brake_PM2_5 = All_brake_PM2_5+str(brake_LV_PM2_5+brake_LCV_PM2_5+brake_B_PM2_5+brake_HDT1420_PM2_5+brake_HDT32_PM2_5+brake_L_PM2_5)+","
        
            #PM10 road emissions for writing
            if (i == 0):
                sum_LV_D_road_PM10 = road_LV_PM10*w_LV_D
                sum_LV_P_road_PM10 = road_LV_PM10*w_LV_P
                sum_LCV_D_road_PM10 = road_LCV_PM10*w_LV_D
                sum_LCV_P_road_PM10 = road_LCV_PM10*w_LV_P
                sum_B_D_road_PM10 = road_B_PM10
                sum_HDT_1420_D_road_PM10 = road_HDT1420_PM10
                sum_HDT_32_D_road_PM10 = road_HDT32_PM10
                sum_L_P_road_PM10 = road_L_PM10
                sum_road_PM10 = road_LV_PM10+road_LCV_PM10+road_B_PM10+road_HDT1420_PM10+road_HDT32_PM10+road_L_PM10
                LV_D_road_PM10 = "LV_D,"+str(road_LV_PM10*w_LV_D)+","
                LV_P_road_PM10 = "LV_P,"+str(road_LV_PM10*w_LV_P)+","
                LCV_D_road_PM10 = "LCV_D,"+str(road_LCV_PM10*w_LV_D)+","
                LCV_P_road_PM10 = "LCV_P,"+str(road_LCV_PM10*w_LV_P)+","
                B_D_road_PM10 = "B_D,"+str(road_B_PM10)+","
                HDT_1420_D_road_PM10 = "HDT_1420_D,"+str(road_HDT1420_PM10)+","
                HDT_32_D_road_PM10 = "HDT_32_D,"+str(road_HDT32_PM10)+","
                L_P_road_PM10 = "L_P,"+str(road_L_PM10)+","
                All_road_PM10 = "All,"+str(road_LV_PM10+road_LCV_PM10+road_B_PM10+road_HDT1420_PM10+road_HDT32_PM10+road_L_PM10)+","
            else:
                sum_LV_D_road_PM10 += road_LV_PM10*w_LV_D
                sum_LV_P_road_PM10 += road_LV_PM10*w_LV_P
                sum_LCV_D_road_PM10 += road_LCV_PM10*w_LV_D
                sum_LCV_P_road_PM10 += road_LCV_PM10*w_LV_P
                sum_B_D_road_PM10 += road_B_PM10
                sum_HDT_1420_D_road_PM10 += road_HDT1420_PM10
                sum_HDT_32_D_road_PM10 += road_HDT32_PM10
                sum_L_P_road_PM10 += road_L_PM10
                sum_road_PM10 += road_LV_PM10+road_LCV_PM10+road_B_PM10+road_HDT1420_PM10+road_HDT32_PM10+road_L_PM10
                LV_D_road_PM10 = LV_D_road_PM10+str(road_LV_PM10*w_LV_D)+","
                LV_P_road_PM10 = LV_P_road_PM10+str(road_LV_PM10*w_LV_P)+","
                LCV_D_road_PM10 = LCV_D_road_PM10+str(road_LCV_PM10*w_LV_D)+","
                LCV_P_road_PM10 = LCV_P_road_PM10+str(road_LCV_PM10*w_LV_P)+","
                B_D_road_PM10 = B_D_road_PM10+str(road_B_PM10)+","
                HDT_1420_D_road_PM10 = HDT_1420_D_road_PM10+str(road_HDT1420_PM10)+","
                HDT_32_D_road_PM10 = HDT_32_D_road_PM10+str(road_HDT32_PM10)+","
                L_P_road_PM10 = L_P_road_PM10+str(road_L_PM10)+","
                All_road_PM10 = All_road_PM10+str(road_LV_PM10+road_LCV_PM10+road_B_PM10+road_HDT1420_PM10+road_HDT32_PM10+road_L_PM10)+","
        
            #PM2_5 road emissions for writing
            if (i == 0):
                sum_LV_D_road_PM2_5 = road_LV_PM2_5*w_LV_D
                sum_LV_P_road_PM2_5 = road_LV_PM2_5*w_LV_P
                sum_LCV_D_road_PM2_5 = road_LCV_PM2_5*w_LV_D
                sum_LCV_P_road_PM2_5 = road_LCV_PM2_5*w_LV_P
                sum_B_D_road_PM2_5 = road_B_PM2_5
                sum_HDT_1420_D_road_PM2_5 = road_HDT1420_PM2_5
                sum_HDT_32_D_road_PM2_5 = road_HDT32_PM2_5
                sum_L_P_road_PM2_5 = road_L_PM2_5
                sum_road_PM2_5 = road_LV_PM2_5+road_LCV_PM2_5+road_B_PM2_5+road_HDT1420_PM2_5+road_HDT32_PM2_5+road_L_PM2_5
                LV_D_road_PM2_5 = "LV_D,"+str(road_LV_PM2_5*w_LV_D)+","
                LV_P_road_PM2_5 = "LV_P,"+str(road_LV_PM2_5*w_LV_P)+","
                LCV_D_road_PM2_5 = "LCV_D,"+str(road_LCV_PM2_5*w_LV_D)+","
                LCV_P_road_PM2_5 = "LCV_P,"+str(road_LCV_PM2_5*w_LV_P)+","
                B_D_road_PM2_5 = "B_D,"+str(road_B_PM2_5)+","
                HDT_1420_D_road_PM2_5 = "HDT_1420_D,"+str(road_HDT1420_PM2_5)+","
                HDT_32_D_road_PM2_5 = "HDT_32_D,"+str(road_HDT32_PM2_5)+","
                L_P_road_PM2_5 = "L_P,"+str(road_L_PM2_5)+","
                All_road_PM2_5 = "All,"+str(road_LV_PM2_5+road_LCV_PM2_5+road_B_PM2_5+road_HDT1420_PM2_5+road_HDT32_PM2_5+road_L_PM2_5)+","
            else:
                sum_LV_D_road_PM2_5 += road_LV_PM2_5*w_LV_D
                sum_LV_P_road_PM2_5 += road_LV_PM2_5*w_LV_P
                sum_LCV_D_road_PM2_5 += road_LCV_PM2_5*w_LV_D
                sum_LCV_P_road_PM2_5 += road_LCV_PM2_5*w_LV_P
                sum_B_D_road_PM2_5 += road_B_PM2_5
                sum_HDT_1420_D_road_PM2_5 += road_HDT1420_PM2_5
                sum_HDT_32_D_road_PM2_5 += road_HDT32_PM2_5
                sum_L_P_road_PM2_5 += road_L_PM2_5
                sum_road_PM2_5 += road_LV_PM2_5+road_LCV_PM2_5+road_B_PM2_5+road_HDT1420_PM2_5+road_HDT32_PM2_5+road_L_PM2_5
                LV_D_road_PM2_5 = LV_D_road_PM2_5+str(road_LV_PM2_5*w_LV_D)+","
                LV_P_road_PM2_5 = LV_P_road_PM2_5+str(road_LV_PM2_5*w_LV_P)+","
                LCV_D_road_PM2_5 = LCV_D_road_PM2_5+str(road_LCV_PM2_5*w_LV_D)+","
                LCV_P_road_PM2_5 = LCV_P_road_PM2_5+str(road_LCV_PM2_5*w_LV_P)+","
                B_D_road_PM2_5 = B_D_road_PM2_5+str(road_B_PM2_5)+","
                HDT_1420_D_road_PM2_5 = HDT_1420_D_road_PM2_5+str(road_HDT1420_PM2_5)+","
                HDT_32_D_road_PM2_5 = HDT_32_D_road_PM2_5+str(road_HDT32_PM2_5)+","
                L_P_road_PM2_5 = L_P_road_PM2_5+str(road_L_PM2_5)+","
                All_road_PM2_5 = All_road_PM2_5+str(road_LV_PM2_5+road_LCV_PM2_5+road_B_PM2_5+road_HDT1420_PM2_5+road_HDT32_PM2_5+road_L_PM2_5)+","
        
        mean_LV_D_hot = sum_LV_D_hot / 24
        mean_LV_P_hot = sum_LV_P_hot / 24
        mean_LCV_D_hot = sum_LCV_D_hot / 24
        mean_LCV_P_hot = sum_LCV_P_hot / 24
        mean_B_D_hot = sum_B_D_hot / 24
        mean_HDT_1420_D_hot = sum_HDT_1420_D_hot / 24
        mean_HDT_32_D_hot = sum_HDT_32_D_hot / 24
        mean_L_P_hot = sum_L_P_hot / 24
        mean_All_hot = sum_hot / 24
            
        mean_LV_D_cold = sum_LV_D_cold / 24
        mean_LV_P_cold = sum_LV_P_cold / 24
        mean_LCV_D_cold = sum_LCV_D_cold / 24
        mean_LCV_P_cold = sum_LCV_P_cold / 24
        mean_B_D_cold = sum_B_D_cold / 24
        mean_HDT_1420_D_cold = sum_HDT_1420_D_cold / 24
        mean_HDT_32_D_cold = sum_HDT_32_D_cold / 24
        mean_L_P_cold = sum_L_P_cold / 24
        mean_All_cold = sum_cold / 24    
        
        mean_LV_D_tyre_PM10 = sum_LV_D_tyre_PM10 / 24
        mean_LV_P_tyre_PM10 = sum_LV_P_tyre_PM10 / 24
        mean_LCV_D_tyre_PM10 = sum_LCV_D_tyre_PM10 / 24
        mean_LCV_P_tyre_PM10 = sum_LCV_P_tyre_PM10 / 24
        mean_B_D_tyre_PM10 = sum_B_D_tyre_PM10 / 24
        mean_HDT_1420_D_tyre_PM10 = sum_HDT_1420_D_tyre_PM10 / 24
        mean_HDT_32_D_tyre_PM10 = sum_HDT_32_D_tyre_PM10 / 24
        mean_L_P_tyre_PM10 = sum_L_P_tyre_PM10 / 24
        mean_All_tyre_PM10 = sum_tyre_PM10 / 24 
        
        mean_LV_D_tyre_PM2_5 = sum_LV_D_tyre_PM2_5 / 24
        mean_LV_P_tyre_PM2_5 = sum_LV_P_tyre_PM2_5 / 24
        mean_LCV_D_tyre_PM2_5 = sum_LCV_D_tyre_PM2_5 / 24
        mean_LCV_P_tyre_PM2_5 = sum_LCV_P_tyre_PM2_5 / 24
        mean_B_D_tyre_PM2_5 = sum_B_D_tyre_PM2_5 / 24
        mean_HDT_1420_D_tyre_PM2_5 = sum_HDT_1420_D_tyre_PM2_5 / 24
        mean_HDT_32_D_tyre_PM2_5 = sum_HDT_32_D_tyre_PM2_5 / 24
        mean_L_P_tyre_PM2_5 = sum_L_P_tyre_PM2_5 / 24
        mean_All_tyre_PM2_5 = sum_tyre_PM2_5 / 24 
        
        mean_LV_D_brake_PM10 = sum_LV_D_brake_PM10 / 24
        mean_LV_P_brake_PM10 = sum_LV_P_brake_PM10 / 24
        mean_LCV_D_brake_PM10 = sum_LCV_D_brake_PM10 / 24
        mean_LCV_P_brake_PM10 = sum_LCV_P_brake_PM10 / 24
        mean_B_D_brake_PM10 = sum_B_D_brake_PM10 / 24
        mean_HDT_1420_D_brake_PM10 = sum_HDT_1420_D_brake_PM10 / 24
        mean_HDT_32_D_brake_PM10 = sum_HDT_32_D_brake_PM10 / 24
        mean_L_P_brake_PM10 = sum_L_P_brake_PM10 / 24
        mean_All_brake_PM10 = sum_brake_PM10 / 24 
        
        mean_LV_D_brake_PM2_5 = sum_LV_D_brake_PM2_5 / 24
        mean_LV_P_brake_PM2_5 = sum_LV_P_brake_PM2_5 / 24
        mean_LCV_D_brake_PM2_5 = sum_LCV_D_brake_PM2_5 / 24
        mean_LCV_P_brake_PM2_5 = sum_LCV_P_brake_PM2_5 / 24
        mean_B_D_brake_PM2_5 = sum_B_D_brake_PM2_5 / 24
        mean_HDT_1420_D_brake_PM2_5 = sum_HDT_1420_D_brake_PM2_5 / 24
        mean_HDT_32_D_brake_PM2_5 = sum_HDT_32_D_brake_PM2_5 / 24
        mean_L_P_brake_PM2_5 = sum_L_P_brake_PM2_5 / 24
        mean_All_brake_PM2_5 = sum_brake_PM2_5 / 24 
        
        mean_LV_D_road_PM10 = sum_LV_D_road_PM10 / 24
        mean_LV_P_road_PM10 = sum_LV_P_road_PM10 / 24
        mean_LCV_D_road_PM10 = sum_LCV_D_road_PM10 / 24
        mean_LCV_P_road_PM10 = sum_LCV_P_road_PM10 / 24
        mean_B_D_road_PM10 = sum_B_D_road_PM10 / 24
        mean_HDT_1420_D_road_PM10 = sum_HDT_1420_D_road_PM10 / 24
        mean_HDT_32_D_road_PM10 = sum_HDT_32_D_road_PM10 / 24
        mean_L_P_road_PM10 = sum_L_P_road_PM10 / 24
        mean_All_road_PM10 = sum_road_PM10 / 24 
        
        mean_LV_D_road_PM2_5 = sum_LV_D_road_PM2_5 / 24
        mean_LV_P_road_PM2_5 = sum_LV_P_road_PM2_5 / 24
        mean_LCV_D_road_PM2_5 = sum_LCV_D_road_PM2_5 / 24
        mean_LCV_P_road_PM2_5 = sum_LCV_P_road_PM2_5 / 24
        mean_B_D_road_PM2_5 = sum_B_D_road_PM2_5 / 24
        mean_HDT_1420_D_road_PM2_5 = sum_HDT_1420_D_road_PM2_5 / 24
        mean_HDT_32_D_road_PM2_5 = sum_HDT_32_D_road_PM2_5 / 24
        mean_L_P_road_PM2_5 = sum_L_P_road_PM2_5 / 24
        mean_All_road_PM2_5 = sum_road_PM2_5 / 24
        
        makeDirectory(dirEtude+"/PM")
        
        with open(dirEtude+"/PM/hotEmissionsPM.csv","w") as hotEmissionsPM :
            hotEmissionsPM.write(title+"\n")
            hotEmissionsPM.write(LV_D_hot+str(mean_LV_D_hot)+"\n")
            hotEmissionsPM.write(LV_P_hot+str(mean_LV_P_hot)+"\n")
            hotEmissionsPM.write(LCV_D_hot+str(mean_LCV_D_hot)+"\n")        
            hotEmissionsPM.write(LCV_P_hot+str(mean_LCV_P_hot)+"\n")
            hotEmissionsPM.write(B_D_hot+str(mean_B_D_hot)+"\n")
            hotEmissionsPM.write(HDT_1420_D_hot+str(mean_HDT_1420_D_hot)+"\n")
            hotEmissionsPM.write(HDT_32_D_hot+str(mean_HDT_32_D_hot)+"\n")
            hotEmissionsPM.write(L_P_hot+str(mean_L_P_hot)+"\n")
            hotEmissionsPM.write(All_hot+str(mean_All_hot)+"\n")
            
        with open(dirEtude+"/PM/coldEmissionsPM.csv","w") as coldEmissionsPM :
            coldEmissionsPM.write(title+"\n")
            coldEmissionsPM.write(LV_D_cold+str(mean_LV_D_cold)+"\n")
            coldEmissionsPM.write(LV_P_cold+str(mean_LV_P_cold)+"\n")
            coldEmissionsPM.write(LCV_D_cold+str(mean_LCV_D_cold)+"\n")        
            coldEmissionsPM.write(LCV_P_cold+str(mean_LCV_P_cold)+"\n")
            coldEmissionsPM.write(B_D_cold+str(mean_B_D_cold)+"\n")
            coldEmissionsPM.write(HDT_1420_D_cold+str(mean_HDT_1420_D_cold)+"\n")
            coldEmissionsPM.write(HDT_32_D_cold+str(mean_HDT_32_D_cold)+"\n")
            coldEmissionsPM.write(L_P_cold+str(mean_L_P_cold)+"\n")
            coldEmissionsPM.write(All_cold+str(mean_All_cold)+"\n")
            
        with open(dirEtude+"/PM/tyreEmissionsPM10.csv","w") as tyreEmissionsPM :
            tyreEmissionsPM.write(title+"\n")
            tyreEmissionsPM.write(LV_D_tyre_PM10+str(mean_LV_D_tyre_PM10)+"\n")
            tyreEmissionsPM.write(LV_P_tyre_PM10+str(mean_LV_P_tyre_PM10)+"\n")
            tyreEmissionsPM.write(LCV_D_tyre_PM10+str(mean_LCV_D_tyre_PM10)+"\n")        
            tyreEmissionsPM.write(LCV_P_tyre_PM10+str(mean_LCV_P_tyre_PM10)+"\n")
            tyreEmissionsPM.write(B_D_tyre_PM10+str(mean_B_D_tyre_PM10)+"\n")
            tyreEmissionsPM.write(HDT_1420_D_tyre_PM10+str(mean_HDT_1420_D_tyre_PM10)+"\n")
            tyreEmissionsPM.write(HDT_32_D_tyre_PM10+str(mean_HDT_32_D_tyre_PM10)+"\n")
            tyreEmissionsPM.write(L_P_tyre_PM10+str(mean_L_P_tyre_PM10)+"\n")
            tyreEmissionsPM.write(All_tyre_PM10+str(mean_All_tyre_PM10)+"\n")
            
        with open(dirEtude+"/PM/tyreEmissionsPM2_5.csv","w") as tyreEmissionsPM2 :
            tyreEmissionsPM2.write(title+"\n")
            tyreEmissionsPM2.write(LV_D_tyre_PM2_5+str(mean_LV_D_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(LV_P_tyre_PM2_5+str(mean_LV_P_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(LCV_D_tyre_PM2_5+str(mean_LCV_D_tyre_PM2_5)+"\n")        
            tyreEmissionsPM2.write(LCV_P_tyre_PM2_5+str(mean_LCV_P_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(B_D_tyre_PM2_5+str(mean_B_D_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(HDT_1420_D_tyre_PM2_5+str(mean_HDT_1420_D_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(HDT_32_D_tyre_PM2_5+str(mean_HDT_32_D_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(L_P_tyre_PM2_5+str(mean_L_P_tyre_PM2_5)+"\n")
            tyreEmissionsPM2.write(All_tyre_PM2_5+str(mean_All_tyre_PM2_5)+"\n")
            
        with open(dirEtude+"/PM/brakeEmissionsPM10.csv","w") as brakeEmissionsPM :
            brakeEmissionsPM.write(title+"\n")
            brakeEmissionsPM.write(LV_D_brake_PM10+str(mean_LV_D_brake_PM10)+"\n")
            brakeEmissionsPM.write(LV_P_brake_PM10+str(mean_LV_P_brake_PM10)+"\n")
            brakeEmissionsPM.write(LCV_D_brake_PM10+str(mean_LCV_D_brake_PM10)+"\n")        
            brakeEmissionsPM.write(LCV_P_brake_PM10+str(mean_LCV_P_brake_PM10)+"\n")
            brakeEmissionsPM.write(B_D_brake_PM10+str(mean_B_D_brake_PM10)+"\n")
            brakeEmissionsPM.write(HDT_1420_D_brake_PM10+str(mean_HDT_1420_D_brake_PM10)+"\n")
            brakeEmissionsPM.write(HDT_32_D_brake_PM10+str(mean_HDT_32_D_brake_PM10)+"\n")
            brakeEmissionsPM.write(L_P_brake_PM10+str(mean_L_P_brake_PM10)+"\n")
            brakeEmissionsPM.write(All_brake_PM10+str(mean_All_brake_PM10)+"\n")
            
        with open(dirEtude+"/PM/brakeEmissionsPM2_5.csv","w") as brakeEmissionsPM2 :
            brakeEmissionsPM2.write(title+"\n")
            brakeEmissionsPM2.write(LV_D_brake_PM2_5+str(mean_LV_D_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(LV_P_brake_PM2_5+str(mean_LV_P_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(LCV_D_brake_PM2_5+str(mean_LCV_D_brake_PM2_5)+"\n")        
            brakeEmissionsPM2.write(LCV_P_brake_PM2_5+str(mean_LCV_P_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(B_D_brake_PM2_5+str(mean_B_D_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(HDT_1420_D_brake_PM2_5+str(mean_HDT_1420_D_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(HDT_32_D_brake_PM2_5+str(mean_HDT_32_D_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(L_P_brake_PM2_5+str(mean_L_P_brake_PM2_5)+"\n")
            brakeEmissionsPM2.write(All_brake_PM2_5+str(mean_All_brake_PM2_5)+"\n")
            
        with open(dirEtude+"/PM/roadEmissionsPM10.csv","w") as roadEmissionsPM :
            roadEmissionsPM.write(title+"\n")
            roadEmissionsPM.write(LV_D_road_PM10+str(mean_LV_D_road_PM10)+"\n")
            roadEmissionsPM.write(LV_P_road_PM10+str(mean_LV_P_road_PM10)+"\n")
            roadEmissionsPM.write(LCV_D_road_PM10+str(mean_LCV_D_road_PM10)+"\n")        
            roadEmissionsPM.write(LCV_P_road_PM10+str(mean_LCV_P_road_PM10)+"\n")
            roadEmissionsPM.write(B_D_road_PM10+str(mean_B_D_road_PM10)+"\n")
            roadEmissionsPM.write(HDT_1420_D_road_PM10+str(mean_HDT_1420_D_road_PM10)+"\n")
            roadEmissionsPM.write(HDT_32_D_road_PM10+str(mean_HDT_32_D_road_PM10)+"\n")
            roadEmissionsPM.write(L_P_road_PM10+str(mean_L_P_road_PM10)+"\n")
            roadEmissionsPM.write(All_road_PM10+str(mean_All_road_PM10)+"\n")
            
        with open(dirEtude+"/PM/roadEmissionsPM2_5.csv","w") as roadEmissionsPM2 :
            roadEmissionsPM2.write(title+"\n")
            roadEmissionsPM2.write(LV_D_road_PM2_5+str(mean_LV_D_road_PM2_5)+"\n")
            roadEmissionsPM2.write(LV_P_road_PM2_5+str(mean_LV_P_road_PM2_5)+"\n")
            roadEmissionsPM2.write(LCV_D_road_PM2_5+str(mean_LCV_D_road_PM2_5)+"\n")        
            roadEmissionsPM2.write(LCV_P_road_PM2_5+str(mean_LCV_P_road_PM2_5)+"\n")
            roadEmissionsPM2.write(B_D_road_PM2_5+str(mean_B_D_road_PM2_5)+"\n")
            roadEmissionsPM2.write(HDT_1420_D_road_PM2_5+str(mean_HDT_1420_D_road_PM2_5)+"\n")
            roadEmissionsPM2.write(HDT_32_D_road_PM2_5+str(mean_HDT_32_D_road_PM2_5)+"\n")
            roadEmissionsPM2.write(L_P_road_PM2_5+str(mean_L_P_road_PM2_5)+"\n")
            roadEmissionsPM2.write(All_road_PM2_5+str(mean_All_road_PM2_5)+"\n")
            
        with open(dirEtude+"/PM/hotEmissionsPM.csv", "r") as hotEmissionsPM :
            lines_hotPM = hotEmissionsPM.readlines()
        hotEmissionsPM.close()
        
        with open(dirEtude+"/PM/coldEmissionsPM.csv", "r") as coldEmissionsPM :
            lines_coldPM = coldEmissionsPM.readlines()
        coldEmissionsPM.close()
        
        with open(dirEtude+"/PM/tyreEmissionsPM10.csv", "r") as tyreEmissionsPM10 :
            lines_tyrePM10 = tyreEmissionsPM10.readlines()
        tyreEmissionsPM10.close()
         
        with open(dirEtude+"/PM/tyreEmissionsPM2_5.csv", "r") as tyreEmissionsPM2_5 :
            lines_tyrePM2_5 = tyreEmissionsPM2_5.readlines()
        tyreEmissionsPM2_5.close()
        
        with open(dirEtude+"/PM/brakeEmissionsPM10.csv", "r") as brakeEmissionsPM10 :
            lines_brakePM10 = brakeEmissionsPM10.readlines()
        brakeEmissionsPM10.close()
         
        with open(dirEtude+"/PM/brakeEmissionsPM2_5.csv", "r") as brakeEmissionsPM2_5 :
            lines_brakePM2_5 = brakeEmissionsPM2_5.readlines()
        brakeEmissionsPM2_5.close()
        
        with open(dirEtude+"/PM/roadEmissionsPM10.csv", "r") as roadEmissionsPM10 :
            lines_roadPM10 = roadEmissionsPM10.readlines()
        roadEmissionsPM10.close()
         
        with open(dirEtude+"/PM/roadEmissionsPM2_5.csv", "r") as roadEmissionsPM2_5 :
            lines_roadPM2_5 = roadEmissionsPM2_5.readlines()
        roadEmissionsPM2_5.close()
        
        matrix_totEmissionPM10=np.zeros((9,25))
        for i in range(1,10):
            for j in range(1,26):
                matrix_totEmissionPM10[i-1,j-1]=float(lines_hotPM[i].split(",")[j])+float(lines_coldPM[i].split(",")[j])+float(lines_tyrePM10[i].split(",")[j])+float(lines_brakePM10[i].split(",")[j])+float(lines_roadPM10[i].split(",")[j])
        
        typeList = ["LV_D_PM10","LV_P_PM10","LCV_D_PM10","LCV_P_PM10","B_D_PM10","HDT_1420_D_PM10","HDT_32_D_PM10","L_P_PM10","All_PM10"]
        for i in range(0,len(typeList)):
            for j in range (0,24+1):
                typeList[i]=str(typeList[i])+","+str(matrix_totEmissionPM10[i][j])
                
        with open(dirEtude+"/PM/totalEmissionsPM10.csv","w") as totalEmissionsPM :
            totalEmissionsPM.write(title+"\n")
            for i in range(0,9):
                totalEmissionsPM.write(typeList[i]+"\n")
        
        matrix_totEmissionPM2_5=np.zeros((9,25))
        for i in range(1,10):
            for j in range(1,26):
                matrix_totEmissionPM2_5[i-1,j-1]=float(lines_hotPM[i].split(",")[j])+float(lines_coldPM[i].split(",")[j])+float(lines_tyrePM2_5[i].split(",")[j])+float(lines_brakePM2_5[i].split(",")[j])+float(lines_roadPM2_5[i].split(",")[j])
        
        typeList2 = ["LV_D_PM2_5","LV_P_PM2_5","LCV_D_PM2_5","LCV_P_PM2_5","B_D_PM2_5","HDT_1420_D_PM2_5","HDT_32_D_PM2_5","L_P_PM2_5","All_PM2_5"]
        for i in range(0,len(typeList2)):
            for j in range (0,24+1):
                typeList2[i]=str(typeList2[i])+","+str(matrix_totEmissionPM2_5[i][j])
    
        with open(dirEtude+"/PM/totalEmissionsPM2_5.csv","w") as totalEmissionsPM2 :
            totalEmissionsPM2.write(title+"\n")
            for i in range(0,9):
                totalEmissionsPM2.write(typeList[i]+"\n")   
    
        with open(dirEtude+"/NOx/totalEmissionsNOx.csv", "r") as totEmissionsNOx :
            lines_totEmissionsNOx = totEmissionsNOx.readlines()
        totEmissionsNOx.close()
            
        with open(dirEtude+"/summaryEmission.csv","w") as summaryEmissions :
            summaryEmissions.write(title + "\n")
            summaryEmissions.write(lines_totEmissionsNOx[9]) 
            summaryEmissions.write(typeList[8] + "\n")
            summaryEmissions.write(typeList2[8])
       
        
    else:
        print("!ERROR! Wrong argument for '"'method'"' in" + CWD + "/input_emiCalc")
        raise SystemExit(0)