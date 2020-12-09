#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 09:00:15 2019

@author: nreiminger
"""
import os
CWD = os.getcwd()


#Function to calculate emissions factors for LV, LCV, L-Category (whitout load and sloap)
def func_L_EF(V,category,fuel,pollutant):
    with open(CWD+"/data/Emep_Emission_Factors_2016/" + category + "/" + fuel + "/" + pollutant + ".csv", "r") as EFFile :
        lines_EFFile = EFFile.readlines()        
        EF = []        
        for i in range(0,6):
            alpha = float(lines_EFFile[i+1].split(",")[5])
            beta = float(lines_EFFile[i+1].split(",")[6])
            gamma = float(lines_EFFile[i+1].split(",")[7])
            delta = float(lines_EFFile[i+1].split(",")[8])
            epsilon = float(lines_EFFile[i+1].split(",")[9])
            zeta = float(lines_EFFile[i+1].split(",")[10])
            eta = float(lines_EFFile[i+1].split(",")[11])
            RF = float(lines_EFFile[i+1].split(",")[12])            
            EF.append((alpha*V*V + beta*V + gamma + delta/V)/(epsilon*V*V + zeta*V + eta)*(1-RF))                      
    EFFile.close()            
    return(EF[0],EF[1],EF[2],EF[3],EF[4],EF[5])
    
#Function to calculate emissions factors for Buses and HDT (with load and sloap)
def func_H_EF(V,category,fuel,pollutant,variety,load,sloap):
    with open(CWD+"/data/Emep_Emission_Factors_2016/" + category + "/" + fuel + "/" + variety + "/" + load + "/" + sloap + "/" + pollutant + ".csv", "r") as EFFile :
        lines_EFFile = EFFile.readlines()
        EF = []        
        for i in range(0,6):
            alpha = float(lines_EFFile[i+1].split(",")[5])
            beta = float(lines_EFFile[i+1].split(",")[6])
            gamma = float(lines_EFFile[i+1].split(",")[7])
            delta = float(lines_EFFile[i+1].split(",")[8])
            epsilon = float(lines_EFFile[i+1].split(",")[9])
            zeta = float(lines_EFFile[i+1].split(",")[10])
            eta = float(lines_EFFile[i+1].split(",")[11])
            RF = float(lines_EFFile[i+1].split(",")[12])            
            EF.append((alpha*V*V + beta*V + gamma + delta/V)/(epsilon*V*V + zeta*V + eta)*(1-RF))            
    EFFile.close()                       
    return(EF[0],EF[1],EF[2],EF[3],EF[4],EF[5])