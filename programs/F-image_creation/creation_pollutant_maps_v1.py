#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:13:16 2020

@author: jurado
"""

import argparse
import os, errno
import shutil
import numpy as np
import colormap as cm
from PIL import Image

def ExpansionHistogram(x,minPol,maxPol,hsl_range_min,hsl_range_max):
    if(x>maxPol):
        x=maxPol
    """ La fonction renvoie un chiffre situé entre 0 (rouge) et 240(bleu foncé) suivant le code hsl (hue saturation light)"""
    return (hsl_range_max-hsl_range_min)-(x-minPol)*(hsl_range_max-hsl_range_min)/(maxPol-minPol)+hsl_range_min

def listIntoRgbImage(list_,n,m,pas_x,pas_y,min_val_x,min_val_y):
    """
    Transforme la liste map_cim en une matrice
    """
    matrix =np.asarray(Image.new('RGB',(m,n),(70,70,70))).copy()
    
    for elem in list_ :
        
        j=int((elem[0]-min_val_x)/pas_x)
        i=int((elem[1]-min_val_y)/pas_y)
        
        matrix[m-i-1,j-1]=np.asarray(elem[2])*255
    
    return Image.fromarray(matrix)


path_script_absolute = os.path.abspath(os.path.dirname(__file__))
#print(path_script_absolute)
parser = argparse.ArgumentParser(description="Creates mesh for every specified directions and speeds")
parser.add_argument('-p_scale', type=str, help='path to the file containing the scale for the images')
parser.add_argument('-p_treated_data', type=str, help='path to the directory containing the csv files to be transformed into images')
args = parser.parse_args()

path_scale_file=args.p_scale.replace(" ","")
path_treated_data_directory=args.p_treated_data.replace(" ","")

with open(path_scale_file, "r") as scale_file :
    lines_scale_file=scale_file.readlines()

scale_dictionary=dict()
for line in lines_scale_file:
    if(line[0]=="\""):
        line_split=line.replace(" ","").replace("\n","").split(":")
        scale_dictionary.update({line_split[0]:line_split[1]})
    else:
        continue


### Extract scales for the images for each polutant from config file

scale_NO2=[ float(x) for x in scale_dictionary.get('"scale_NO2"').split(",")]
scale_NOx=[ float(x) for x in scale_dictionary.get('"scale_NOx"').split(",")]
scale_PM10=[ float(x) for x in scale_dictionary.get('"scale_PM10"').split(",")]
scale_PM2_5=[ float(x) for x in scale_dictionary.get('"scale_PM2-5"').split(",")]
scale_hsv=[ float(x) for x in scale_dictionary.get('"scale_hsv"').split(",")]

pollutant_directories=sorted(os.listdir(path_treated_data_directory))

for pollutant in pollutant_directories :
    
    path_pollutant_directories=os.path.join(path_treated_data_directory,pollutant)
    
    print(pollutant)
    
    map_csv_format_list=sorted(os.listdir(path_pollutant_directories))
    
    for map_csv_format in map_csv_format_list :
        
        path_map_in=os.path.join(path_pollutant_directories,map_csv_format)
        path_map_out=os.path.join(path_pollutant_directories,map_csv_format).replace(".csv",".png")
        
        if("NO2" in pollutant):
            scale=scale_NO2
        elif("NOx" in pollutant):
            scale=scale_NOx
        elif("PM10" in pollutant):
            scale=scale_PM10
        elif("PM2.5" in pollutant):
            scale=scale_PM2_5
        else:
            continue
        
        with open(path_map_in,"r") as map_raw:
            map_raw_lines=map_raw.readlines()[1:]
        
        map_raw_lines=[[float(x.split(",")[0]),float(x.split(",")[1]),cm.hsv2rgb((ExpansionHistogram(float(x.split(",")[2]),scale[0],scale[1],scale_hsv[0],scale_hsv[1])),100,100,normalised=False)] for x in map_raw_lines]
        
        max_val_x=float(max(map_raw_lines,key = lambda x: float(x[0]))[0])
        min_val_x=float(min(map_raw_lines,key = lambda x: float(x[0]))[0])
        max_val_y=float(max(map_raw_lines,key = lambda x: float(x[1]))[1])
        min_val_y=float(min(map_raw_lines,key = lambda x: float(x[1]))[1])
        
        pas_x=10e+5
        pas_y=10e+5
        
        for i in range(0,len(map_raw_lines)-1):
            
            pas_x_intermediaire=abs(float(map_raw_lines[i+1][0])-float(map_raw_lines[i][0]))
            pas_y_intermediaire=abs(float(map_raw_lines[i+1][1])-float(map_raw_lines[i][1]))
            
            if(pas_x>pas_x_intermediaire and pas_x_intermediaire>0):
                pas_x=pas_x_intermediaire
            if(pas_y>pas_y_intermediaire and pas_y_intermediaire>0):
                pas_y=pas_y_intermediaire
        
        m=int((max_val_x-min_val_x)/pas_x)
        n=int((max_val_y-min_val_y)/pas_y)
        
        print(m,n)
        
        
        
        
        map_image=listIntoRgbImage(map_raw_lines,n,m,pas_x,pas_y,min_val_x,min_val_y)
        map_image=map_image.resize((400,400))
        
        map_image.show()
        break
        print(map_raw_lines[0])
        
        #hexColorConcentration=cm.rgb2hex(rgbColorConcentration[0],rgbColorConcentration[1],rgbColorConcentration[2],normalised=True)
        
        print("   -",map_csv_format)
        print("   -",scale)
        
































