#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:15:50 2018

@author: jurado
"""

import os, errno
import numpy as np
import math
### GETTING PATH OF THE SCRIPT DIRECTORY ###

path_script_absolute = os.path.abspath(os.path.dirname(__file__))
#print(path_script_absolute)


###############################################
### Reading the config files and closing it ###
###############################################

def second_largest(numbers):
    first, second = None, None
    for n in numbers:
        if n > first:
            first, second = n, first
        elif first > n > second:
            second = n
    return second

# function to get unique values 
def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    
    return unique_list

def getGroundBoundaries(dirEtude):

    """
    
    Récupère les dimensions extrème d'un carré suivant l'axe x,y dans salomé
    
    """
    wallGround_file=open(dirEtude+"/wallGround.stl","r")
    wallGround_lines=wallGround_file.readlines()
    wallGround_file.close()
    
    
    x_ground_list=list()
    y_ground_list=list()
    
    
    for i in range(0,3):
        
        wallGround_split=wallGround_lines[i+3].split()
        x_ground_list.append(wallGround_split[1])
        y_ground_list.append(wallGround_split[2])
    
    xmin=float(min(x_ground_list))
    xmax=float(max(x_ground_list))
    ymin=float(min(y_ground_list))
    ymax=float(max(y_ground_list))
    
    transX=transX=(xmax-xmin)/2+xmin
    transY=transY=(ymax-ymin)/2+ymin
    
    return(xmin,xmax,ymin,ymax,transX,transY)


def getHeightBuildingZmax(dirEtude,zmin,wallground_list,meshingMaxSize,nblayer,refinementGround,heightFactor=5):
    
    hauteurAvantMailleMax=float(refinementGround[-1].split(";")[0].replace("(",""))
    wallBlock_file=open(dirEtude+"/wallBlock.stl","r")
    wallBlock_lines=wallBlock_file.readlines()
    wallBlock_file.close()
    
    
    
    z_ground_list=list()
    z_block_list=list()
    
    for wallground in wallground_list:
    
        wallGround_file=open(dirEtude+"/"+wallground,"r")
        wallGround_lines=wallGround_file.readlines()
        wallGround_file.close()
        
        if("stl" in wallground):
            i=3
            k=0
            #Permet d'extraire la 3ème coordonnée correspondant au z des stl, les stl ont une entête de 3 lignes (pour cela if pour k=3) puis les informations sur les vertex de ses lignes qui 
            #sont de la forme vertex x y z, le z correspond donc au 4ème élément de la liste (l'indexation commencant à 0, le 3)
            while( i<len(wallGround_lines)-3):
                z_ground_list.append(float(wallGround_lines[i].split()[3]))
                k=k+1
                i=i+1
                if(k==3):
                    k=0
                    i=i+4
        elif("obj" in wallground):
            for elem in wallGround_lines:
                if(elem[:2]=="v "):
                    z_ground_list.append(float(elem.split()[-1]))
                
                
    i=3
    k=0
    while( i<len(wallBlock_lines)-3):
        z_block_list.append(float(wallBlock_lines[i].split()[3]))
        k=k+1
        i=i+1
        if(k==3):
            k=0
            i=i+4
            

    hmin=min(z_ground_list)
    hmax=max(z_block_list)-zmin
    zmax=int(float(heightFactor)*float(hmax))+(meshingMaxSize-int(float(heightFactor)*float(hmax)-hauteurAvantMailleMax)%meshingMaxSize)+hmin

    if(zmax-hmin<90):
        #probablement overkill de faire comme ca
        a=(90-hauteurAvantMailleMax)/meshingMaxSize
        print(a)
        if(a%meshingMaxSize==0):
            zmax=hauteurAvantMailleMax+a*meshingMaxSize
            print(zmax)
        else:
            zmax=hauteurAvantMailleMax+int(a+1)*meshingMaxSize
            print(zmax)
    return zmax,hmax,hmin
    

def getHeightBuildingAndZmaxAndZmin(dirEtude,wallground_files_list,meshingMaxSize,nblayer,refinementGround,heightFactor=5):
    
    """
    
    Récupère les hauteurs max et min des batiments. 
    A partir de la hauteur max des batiments ils calculent la hauteur du toit par rapport au height factor , le zmax est au moins >90m
    zmin = hauteur min
    
    """

        
    hauteurAvantMailleMax=float(refinementGround[-1].split(";")[0].replace("(",""))
    wallBlock_file=open(dirEtude+"/wallBlock.stl","r")
    wallBlock_lines=wallBlock_file.readlines()
    wallBlock_file.close()
    

    
    z_ground_list=list()
    z_block_list=list()
    
    
    i=3
    k=0
    
    
    for wallground in wallground_files_list:
        
        wallGround_file=open(dirEtude+"/"+wallground,"r")
        wallGround_lines=wallGround_file.readlines()
        wallGround_file.close()    
        #Permet d'extraire la 3ème coordonnée correspondant au z des stl, les stl ont une entête de 3 lignes (pour cela if pour k=3) puis les informations sur les vertex de ses lignes qui 
        #sont de la forme vertex x y z, le z correspond donc au 4ème élément de la liste (l'indexation commencant à 0, le 3)
        while( i<len(wallGround_lines)-3):
            z_ground_list.append(float(wallGround_lines[i].split()[3]))
            k=k+1
            i=i+1
            if(k==3):
                k=0
                i=i+4
            
    i=3
    k=0
    while( i<len(wallBlock_lines)-3):
        z_block_list.append(float(wallBlock_lines[i].split()[3]))
        k=k+1
        i=i+1
        if(k==3):
            k=0
            i=i+4
    #le minimum correspond au point bas du sol
    hmin=min(z_ground_list)
    hmax=max(z_block_list)-hmin
    #print(int(float(heightFactor)*float(hmax)))
    #print(int(float(heightFactor)*float(hmax))%4)

    zmax=int(float(heightFactor)*float(hmax))+(meshingMaxSize-int(float(heightFactor)*float(hmax)-hauteurAvantMailleMax)%meshingMaxSize)+hmin

    if(zmax-hmin<90):
        #probablement overkill de faire comme ca
        a=(90-hauteurAvantMailleMax)/meshingMaxSize
        print(a)
        if(a%meshingMaxSize==0):
            zmax=hauteurAvantMailleMax+a*meshingMaxSize
            print(zmax)
        else:
            zmax=hauteurAvantMailleMax+int(a+1)*meshingMaxSize
            print(zmax)
    return hmin,zmax,hmax


def getGroundBoundariesSteadyDirection(dirEtude,angle):
    
    wallGround_file=open(dirEtude+"/wallGround.stl","r")
    wallGround_lines=wallGround_file.readlines()
    wallGround_file.close()
    
    angle=float(angle)
    x_ground_list=list()
    y_ground_list=list()

    for i in range(0,3):
         
        wallGround_split=wallGround_lines[i+3].split()
        x_ground_list.append(float(wallGround_split[1]))
        y_ground_list.append(float(wallGround_split[2]))
    
    for i in range(0,3):
        
        wallGround_split=wallGround_lines[i+10].split()
        x_ground_list.append(float (wallGround_split[1]))
        y_ground_list.append(float(wallGround_split[2]))
    
    x_ground_list=unique(x_ground_list)
    y_ground_list=unique(y_ground_list)
    
    transX=(max(x_ground_list)+min(x_ground_list))/2
    transY=(max(y_ground_list)+min(y_ground_list))/2
    
    x_ground_list=[x-transX for x in x_ground_list]
    y_ground_list=[y-transY for y in y_ground_list]
    
    xMax=max(x_ground_list)
    yMax=max(y_ground_list)
    xMin=min(x_ground_list)
    yMin=min(y_ground_list)
    
    x_index_list=np.argsort(x_ground_list)
    y_index_list=np.argsort(y_ground_list) 

    if(angle > 0 and angle < 90):
        """
        x0=x_ground_list[y_index_list[-1]]
        y0=y_ground_list[y_index_list[-1]] #
        x1=x_ground_list[x_index_list[-1]] #
        y1=y_ground_list[x_index_list[-1]]
        x2=x_ground_list[y_index_list[0]] 
        y2=y_ground_list[y_index_list[0]]  #
        x3=x_ground_list[x_index_list[0]]  #
        y3=y_ground_list[x_index_list[0]]

        x0=x3
        y0=y3
        x1=x2
        y1=y2
        x2=x1
        y2=y1
        x3=x0
        y3=y0
        """
        x0=x_ground_list[x_index_list[0]]  #
        y0=y_ground_list[x_index_list[0]]
        x1=x_ground_list[y_index_list[0]] 
        y1=y_ground_list[y_index_list[0]]  #
        x2=x_ground_list[x_index_list[-1]] #
        y2=y_ground_list[x_index_list[-1]]
        x3=x_ground_list[y_index_list[-1]]
        y3=y_ground_list[y_index_list[-1]] #     
        
        
    elif(angle > 90 and angle < 180):
        """
        x0=x_ground_list[x_index_list[-1]] #
        y0=y_ground_list[x_index_list[-1]] 
        x1=x_ground_list[y_index_list[0]] 
        y1=y_ground_list[y_index_list[0]] #
        x2=x_ground_list[x_index_list[0]] #
        y2=y_ground_list[x_index_list[0]] 
        x3=x_ground_list[y_index_list[-1]]
        y3=y_ground_list[y_index_list[-1]] # 
        """
        x0=x_ground_list[y_index_list[-1]]
        y0=y_ground_list[y_index_list[-1]] #
        x1=x_ground_list[x_index_list[0]] #
        y1=y_ground_list[x_index_list[0]] 
        x2=x_ground_list[y_index_list[0]] 
        y2=y_ground_list[y_index_list[0]] #
        x3=x_ground_list[x_index_list[-1]] #
        y3=y_ground_list[x_index_list[-1]] 
        
        
 
    elif(angle > 180 and angle < 270):
        """
        x0=x_ground_list[y_index_list[0]]
        y0=y_ground_list[y_index_list[0]] #
        x1=x_ground_list[x_index_list[0]] #
        y1=y_ground_list[x_index_list[0]]
        x2=x_ground_list[y_index_list[-1]] 
        y2=y_ground_list[y_index_list[-1]]  #
        x3=x_ground_list[x_index_list[-1]]  #
        y3=y_ground_list[x_index_list[-1]]        
        """
        x0=x_ground_list[x_index_list[-1]]  #
        y0=y_ground_list[x_index_list[-1]] 
        x1=x_ground_list[y_index_list[-1]] 
        y1=y_ground_list[y_index_list[-1]]  #
        x2=x_ground_list[x_index_list[0]] #
        y2=y_ground_list[x_index_list[0]]
        x3=x_ground_list[y_index_list[0]]
        y3=y_ground_list[y_index_list[0]] #
        
    elif(angle > 270 and angle < 360):
        """
        x0=x_ground_list[x_index_list[0]] #
        y0=y_ground_list[x_index_list[0]] 
        x1=x_ground_list[y_index_list[-1]] 
        y1=y_ground_list[y_index_list[-1]] #
        x2=x_ground_list[x_index_list[-1]] #
        y2=y_ground_list[x_index_list[-1]] 
        x3=x_ground_list[y_index_list[0]]
        y3=y_ground_list[y_index_list[0]] # 
        """
        x0=x_ground_list[y_index_list[0]]
        y0=y_ground_list[y_index_list[0]] # 
        x1=x_ground_list[x_index_list[-1]] #
        y1=y_ground_list[x_index_list[-1]] 
        x2=x_ground_list[y_index_list[-1]] 
        y2=y_ground_list[y_index_list[-1]] #
        x3=x_ground_list[x_index_list[0]] #
        y3=y_ground_list[x_index_list[0]] 
    
    elif(angle==90):

        x0=xMin
        y0=yMax
        x1=xMin
        y1=yMin
        x2=xMax
        y2=yMin
        x3=xMax
        y3=yMax
        
    elif(angle==180):
       
        x0=xMax
        y0=yMax
        x1=xMin
        y1=yMax
        x2=xMin
        y2=yMin
        x3=xMax
        y3=yMin
        
    elif(angle==270):

        x0=xMax
        y0=yMin
        x1=xMax
        y1=yMax
        x2=xMin
        y2=yMax
        x3=xMin
        y3=yMin
     
    elif(angle==360 or angle==0):
        
        x0=xMin
        y0=yMin
        x1=xMax
        y1=yMin
        x2=xMax
        y2=yMax
        x3=xMin
        y3=yMax 
        
        
    x0=x0+transX
    y0=y0+transY
    x1=x1+transX
    y1=y1+transY
    x2=x2+transX
    y2=y2+transY
    x3=x3+transX
    y3=y3+transY

    return x0,y0,x1,y1,x2,y2,x3,y3


def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  
 
def probes_rotation_translation(xminProbes,xmaxProbes,yminProbes,ymaxProbes,zlistProbes,transXcenter,transYcenter,pasXProbes,pasYProbes,angleProbes):
    
    int(xminProbes)
    int(xmaxProbes)
    int(yminProbes)
    int(ymaxProbes)
    zlistProbes=sorted([float(x) for x in zlistProbes])
    float(transXcenter)
    float(transYcenter)
    int(pasXProbes)
    int(pasYProbes)
    float(angleProbes)
    
    angleProbesRadian=0.01745329251*float(angleProbes)
    
    lines_probesOutput=list()
    for z in zlistProbes:
        for y in range(yminProbes,ymaxProbes+1,pasYProbes):
            
            for x in range(xminProbes,xmaxProbes+1,pasXProbes):
                
                if(angleProbes==0 or angleProbes==360):
                    xnew=x+transXcenter
                    ynew=y+transYcenter
                    
                else:
                    #rotation de l'angle
                    xnew=x*math.cos(angleProbesRadian)-y*math.sin(angleProbesRadian)
                    ynew=-x*math.sin(angleProbesRadian)-y*math.cos(angleProbesRadian)
                    #translation en xCentreProbes,yCentreProbes
                    xnew=xnew+transXcenter
                    ynew=-ynew+transYcenter
                
                line="        ( "+str(xnew)+" "+str(ynew)+" "+str(z)+" )\n" 
                lines_probesOutput.append(line)
    
    return lines_probesOutput

#print(getHeightBuildingAndZmaxAndZmin("/home/jurado/OpenFOAM/jurado-5.0/run/Etude_Air&D/2019_02_Istra/D_220/constant/triSurface",4,3,4,heightFactor=5))
