#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 13:48:15 2018

@author: jurado
"""
from math import *

def turbulenceComputationRichards(z0,zRef,zMax,uRef,K=0.41,Cmu=0.09):

    """
    Fonction qui calcule les paramètre de turbulence k et epsilon moyen
    Cette fonction se base sur l'article de Richards&Haxley 1993 ou Richards 2011
    Il faut spécifier z0 la hauteur de rugosité qui vaut entre 0.5 et 1 en ville ( des tables existent comme EuropeanAtlasWind)
    zRef correspond à l'altitude de référence utilisé pour calculer uRef, zRef > zMax sinon openFoam met une constante à partir de zRef
    zMax correspond à la hauteur maximal du domaine
    uRef correspond à la vitesse à zRef lorsque le profil de vitesse suit la loi logarithmique u*/K*ln((z+z0)/z0)
    K et Cmu sont des constantes 
    """

    uStar=K*uRef/log((zRef+z0)/z0)
    k=pow(uStar,2)/pow(Cmu,0.5)
    epsilon=pow(uStar,3)/(K*pow(zMax,0.5))
    return(k,epsilon)

def turbulenceComputationPipe(D,l,U,altitudeU=10,visco=0.0000156,Hmax=1000,Cmu=0.09,alpha=0.3):

    """
    Fonction qui calcule les paramètre de turbulence k et epsilon pour les écoulements interne 
    L'utilisateur doit entrer la longueur caractéristique D (prise comme la hauteur total du domaine)
    L'utilisateur doit entrer la longueur de l'échelle de turbulence l (prise comme la hauteur total du domaine)
    La vitesse à une certaine altitude (par défaut à 10m)
    l'altitude par défaut de la vitesse entré par l'utilisateur est prise à 10mm
    la viscocité de l'air est prise pour 300K,
    la couche limite est prise égale à 1000m 
    Cmu est pris égale à 0.09
    la puissance de la loi de vent est prise par défaut à 0.3
    """
    #if(U<2.5):
    #    U=3
    #Paramètre de vitesse
    Umax=U*pow(Hmax/altitudeU,alpha)
    B=Umax/pow(Hmax,alpha)
    zUmoyen=D/pow(2,1/(1+alpha))
    Umoyen=B*pow(zUmoyen,alpha)

    #Paramètre de turbulence
    Re=Umoyen*D/visco
    I=0.16*pow(Re,-1/8)
    k=3.0/2.0*pow(Umoyen*I,2)
    epsilon=pow(Cmu,0.75)*pow(k,1.5)/l
    return(k,epsilon)


def turbulenceComputationKato(z,U,altitudeU=10,Hmax=1000,VonKarman=0.41,Cmu=0.09,alpha=0.3):
    
    """
    Fonction qui calcule les paramètre de turbulence k et epsilon en utilisant l'article de Kato 1992 pour définir l'intensité turbulente
    cette formulation est adapté en ville
    z correspond à la hauteur max du domaine
    U correspond à la vitesse à l'altitude de 10m
    K, Cmu et alpha sont des constantes
    """    
    #Paramètre de vitesse
    Umax=U*pow(Hmax/altitudeU,alpha)
    B=Umax/pow(Hmax,alpha)
    zUmoyen=z/pow(2,1/(1+alpha))
    Umoyen=B*pow(zUmoyen,alpha)
    
    if(z <= 30):
        I=0.287
    else:
        a=40*pow(10,alpha)
        zPrime = z-30
        zImoySup30 = pow(1/2*(pow(z,1-alpha)+pow(30,1-alpha)),(1/(1-alpha)))
        IMoySup30 = a*pow(zImoySup30,-alpha)/100
        I=30/z*0.287+zPrime/z*IMoySup30
    k=1/2*pow(I,2)*pow(Umoyen,2)
    epsilon=pow(Cmu,0.75)*pow(k,1.5)/(VonKarman*pow(z,0.5))
    
    return(k,epsilon)

z0=0.7
zRef=10
zMax=200
uRef=20

from math import *

#uStar=0.41*float(20)/log((10+0.7)/0.7)
#uRef=round(uStar/0.41*log((200+0.7)/0.7),5)
