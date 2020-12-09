#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:37:47 2020

@author: jurado
"""

import os,re,errno
import shutil

def sort_nicely( l ):
    """ Sort the given list in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


path="/mnt/hardDiskDrive_4T/Etude_IA"
path_script_absolute = os.path.abspath(os.path.dirname(__file__))

wanted_neighbor=[25,38]
neighbors=[x for x in os.listdir(path) if ("quartier" in x)]
neighbors=[x for x in neighbors if(float(x.split("_")[1].split("-")[0])>=wanted_neighbor[0] and float(x.split("_")[1].split("-")[0])<=wanted_neighbor[1])]
sort_nicely(neighbors)

for neighbor in neighbors: 
    print(neighbor)
    path_neighbor=os.path.join(path,neighbor)
    directions=[x for x in os.listdir(path_neighbor) if("D_" in x)]
    sort_nicely(directions)
    
    for direction in directions:
        
        path_direction=os.path.join(path_neighbor,direction)
#        if(os.path.isfile(os.path.join(path_direction,"log.9_TopoSet"))==False):
#            print(path_direction)
        
        try:
            shutil.rmtree(os.path.join(path_direction,"constant"))
            shutil.rmtree(os.path.join(path_direction,"0"))
            shutil.rmtree(os.path.join(path_direction,"system"))
        except FileNotFoundError:
            print("file already removed")
        speeds=[x for x in os.listdir(path_direction) if("V_" in x)]        
        sort_nicely(speeds)
        for speed in speeds:
            
            copy(os.path.join(path_script_absolute,"system","controlDict.final"),os.path.join(path_direction,speed,"system","controlDict"))




