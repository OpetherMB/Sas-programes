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
from PIL import Image, ImageDraw, ImageFont


#Function to create directories
def makeDirectory(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def get_concat_v_blank(im1,im2,im3,color=(255,255,255,255)):
    #séparation entre l'image de pollution et la légende
    separation_image=0.01
    #ratio de la hauteur de la légende par rapport au logo
    ratio_legende_logo_h=0.15
    #ratio de la largeur de la légende par rapport au logo
    ratio_legende_logo_l=0.1
    im2_alpha=im2.copy()
    im2_alpha=im2_alpha.convert("RGBA")
    im2_alpha.putalpha(128)
    datas = im2_alpha.getdata()
    
    newData = []
    for item in datas:
        if(item[0]==255 and item[1]==255 and item[2]==255):
            newData.append((255,255,255,128))
        else:
            newData.append(item)
    im2_alpha.putdata(newData)
    
    
    dst=Image.new('RGBA',(max(im1.width,im2.width),im1.height + int(im1.height*separation_image) + im2.height),color)
    dst.paste(im1,(0,0))
    dst.paste(im2_alpha,(0,int(im1.height-im2.height)))
#    dst.paste(im2,(0,im1.height+int(im1.height*separation_image)))
    dst.paste(im3,(int(im2.width*(1+ratio_legende_logo_l)),im1.height+int(im1.height*separation_image)+int(im2.height*ratio_legende_logo_h)))
    
    draw = ImageDraw.Draw(dst)
    for i in range(0,5):
        draw.text(xy=(int(im2.width*(1+ratio_legende_logo_l*0.8))+int(i*im3.width/4),im1.height+int(im1.height*separation_image)+int(im2.height*ratio_legende_logo_h)+int(im3.height*1.05)),text=str(20+i*5),fill=(0,0,0))
    
    return dst

def customColorBar(height,width,scale_hsv,alpha_bar_line=0.01,number_of_lines=5):
    array_color_bar = np.zeros([width,height,3],dtype=np.uint8)
    
    if(width*alpha_bar_line*2>1):
        bar_width_border=int(width*alpha_bar_line*2)
    else:
        bar_width_border=1*2
    
    if(width*alpha_bar_line>1):
        bar_width_line=int(width*alpha_bar_line)
    else:
        bar_width_line=1
    compartiment=height/(number_of_lines-1)
    
    for j in range(0,height):
        for i in range(0,width):
            pixel_rgb=cm.hsv2rgb(ExpansionHistogram(j,0,height,scale_hsv[0],scale_hsv[1]),100,80,normalised=False)
            for z in range(0,3):
                if(i<bar_width_border or i>width-1-bar_width_border):
                    array_color_bar[i][j][z]=0
                    
                elif(j<bar_width_border or j%compartiment > compartiment-bar_width_line or j%compartiment < bar_width_line or j>height-bar_width_border-1):
                    array_color_bar[i][j][z]=0
                else:
                    array_color_bar[i][j][z]=int(round(pixel_rgb[z]*255))
                
    image_color_bar=Image.fromarray(array_color_bar,'RGBA')
    
    return image_color_bar

def ExpansionHistogram(x,minPol,maxPol,hsl_range_min,hsl_range_max):
    """
    
    Permet de faire la bijection de la pollution min - max vers les couleurs de hsl 
    
    """
    
    if(x>maxPol):
        x=maxPol
    """ La fonction renvoie un chiffre situé entre 0 (rouge) et 240(bleu foncé) suivant le code hsl (hue saturation light)"""
    return (hsl_range_max-hsl_range_min)-(x-minPol)*(hsl_range_max-hsl_range_min)/(maxPol-minPol)+hsl_range_min

def listIntoRgbMatrix(map_coordinates,map_values,n,m,pas_x,pas_y,min_val_x,min_val_y,color_building):
    """
    
    Créer une matrice de la couleur des batiments puis rajoute par dessus la pollution des probes
    Cette fonction le fait pour toutes les directions qui lui sont demandées 
    
    """
    
    matrix_list=list()
    
    matrix_base=Image.new('RGB',(m,n),color_building)
    
    for i in range(0,len(map_values[0])):
        matrix_list.append(np.copy(np.asarray(matrix_base)))
        
    for coordinate,values in zip(map_coordinates,map_values):
        
        k=int((coordinate[0]-min_val_x)/pas_x)
        l=int((coordinate[1]-min_val_y)/pas_y)
        
        for j,value in enumerate(values):
                
            matrix_list[j][n-l-1,k]=value
    
    return matrix_list


path_script_absolute = os.path.abspath(os.path.dirname(__file__))


### Récupère les données fournie par l'utilisateur
parser = argparse.ArgumentParser(description="Creates mesh for every specified directions and speeds")
parser.add_argument('-p_scale', type=str, help='path to the file containing the scale for the images')
parser.add_argument('-p_treated_data', type=str, help='path to the directory containing the csv files to be transformed into images')
parser.add_argument('-p_logo',type=str,help='path to the logo of air&d')
args = parser.parse_args()

path_scale_file=args.p_scale.replace(" ","")
path_treated_data_directory=args.p_treated_data.replace(" ","")
path_logo=args.p_logo.replace(" ","")
image_logo=Image.open(path_logo)

### récupère les données dans le fichier 
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

### Extract the color for the buildings
color_building= tuple([ int(x) for x in scale_dictionary.get('"color_building"').split(",")])

### Extract the format and size of the output image
format_image=scale_dictionary.get('"format_image"')
size_image=[ int(x) for x in scale_dictionary.get('"image_size"').split(",")]

### Récupère les divers dossiers avec les polluants dedans
pollutant_directories=[x for x in sorted(os.listdir(path_treated_data_directory)) if(os.path.isdir(os.path.join(path_treated_data_directory,x)))]



Image_tier_horizontal=int(round(1/3*size_image[1]))
Image_2tier_horizontal=int(round(2/3*size_image[1]))
Image_tier_vertical=int(round(Image_tier_horizontal*145/388))

image_logo=image_logo.resize((Image_tier_horizontal,Image_tier_vertical))
image_color_bar=customColorBar(int(Image_tier_horizontal*1.8),int(Image_tier_vertical*0.3),scale_hsv)
#print(image_logo.shape)
print("résolution de l'image:",size_image)




for pollutant in pollutant_directories :
    
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
    
    
    path_pollutant_directories=os.path.join(path_treated_data_directory,pollutant,"concentrations_ponderees")
    print("")
    print("")
    print("Création des images pour le polluant :",pollutant)
    print("échelle pour le polluant:",scale)
    print("")    
    mean_directories=sorted([x for x in os.listdir(path_pollutant_directories) if("moyennes" in x) ])
    
    
    
    for mean in mean_directories:
        #récupère les fichiers du type NO2_2m, NO2_4m, etc.
        
        print("   *",mean)
        path_mean_file=os.path.join(path_pollutant_directories,mean)
        map_csv_format_list=[f for f in sorted(os.listdir(path_mean_file)) if os.path.isfile(os.path.join(path_mean_file,f))]

        
        for map_csv_format in map_csv_format_list :
            
            print("      -",map_csv_format)
            path_map_in=os.path.join(path_mean_file,map_csv_format)
            
            makeDirectory(os.path.join(path_treated_data_directory,pollutant,"cartes_de_pollution"))
            path_map_out=os.path.join(path_treated_data_directory,pollutant,"cartes_de_pollution",map_csv_format).replace(".csv","")
            
            
            
            with open(path_map_in,"r") as map_raw:
                map_raw_lines=map_raw.readlines()
            
            map_coordinates=[[float(x.split(",")[0]),float(x.split(",")[1])] for x in map_raw_lines[1:]]
            
            map_values=[[np.asarray(cm.hsv2rgb((ExpansionHistogram(float(y),scale[0],scale[1],scale_hsv[0],scale_hsv[1])),100,80,normalised=False))*255 for y in x.split(",")[3:] ] for x in map_raw_lines[1:]]
            
            ### Récupère les limites du rectangle des probes
            max_val_x=float(max(map_coordinates,key = lambda x: float(x[0]))[0])
            min_val_x=float(min(map_coordinates,key = lambda x: float(x[0]))[0])
            max_val_y=float(max(map_coordinates,key = lambda x: float(x[1]))[1])
            min_val_y=float(min(map_coordinates,key = lambda x: float(x[1]))[1])
            
            #initialisation du pas à une valeur très haute jamais atteinte
            pas_x=10e+5
            pas_y=10e+5
            
            ### Récupère le pas entre deux probes consécutives
            for i in range(0,len(map_coordinates)-1):
                
                pas_x_intermediaire=abs(float(map_coordinates[i+1][0])-float(map_coordinates[i][0]))
                pas_y_intermediaire=abs(float(map_coordinates[i+1][1])-float(map_coordinates[i][1]))
                
                if(pas_x>pas_x_intermediaire and pas_x_intermediaire>0):
                    pas_x=pas_x_intermediaire
                if(pas_y>pas_y_intermediaire and pas_y_intermediaire>0):
                    pas_y=pas_y_intermediaire
            
            ### détermine le nombre de probes en x et y
            m=int((max_val_x-min_val_x)/pas_x)+1
            n=int((max_val_y-min_val_y)/pas_y)+1
            
            ### créer une liste de matrice avec en chaque valeur la valeur RGB de la case au lieu de sa valeur en polluant
            rgb_matrixes=listIntoRgbMatrix(map_coordinates,map_values,n,m,pas_x,pas_y,min_val_x,min_val_y,color_building)
            
            
            ### si il y a plus d'une seule image créer un répertoire
            if(len(rgb_matrixes)!=1):
                path_directory_for_direction=path_map_out.replace(".png","")
                makeDirectory(path_directory_for_direction)
                for i,matrix in enumerate(rgb_matrixes):
                    #commence à +3 car les trois premières colonnes sont les x,y,z
                    path_map_out_final=os.path.join(path_directory_for_direction,map_raw_lines[0].split(",")[i+3]).replace("\n","")
                    get_concat_v_blank(Image.fromarray(matrix,'RGBA').resize(size_image),image_logo,image_color_bar).save(path_map_out_final+"."+format_image)
                    
                    
            else:
                get_concat_v_blank(Image.fromarray(rgb_matrixes[0],"RGBA").resize(size_image),image_logo,image_color_bar).save(path_map_out+"."+format_image)
            
print("")
print("")
print("Fin du script")































