Ce script python permet de créer à partir des stl inletPolx (avec x le numéro de l'inlet), du stl wallBlock et du stl wallGround de créer tous les fichiers nécéssaires pour lancer le calcul sur openFoam pour différentes vitesses.

!!! LES STL DOIVENT ËTRE ORIENTES NORD  (angle 360 ou 0)!!!

Pour l'utiliser il faut: 

Aller dans le fichier preProcessingDict et computationDict, le remplir avec les informations demandées:

	-Le fichier preProcessingDict doit être modifié pour chaque nouvelle étude,
	-Le fichier computationDict permet de changer les raffinements, le solver et le nombre de coeurs pour la création du maillage et le lancement des calculs.  

Lancer le fichier python.

	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	
!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!
!!!! LES STL DE L INLET POLLUANT DOIVENT ETRE EXTRUDE VERS LE BAS PEUT IMPORTE 
!!!! LA LONGUEUR (2 par exemple) ET VERS LE HAUT DE 0.002 (DEPENDANT DE LA DEFLECTION CHOISI
!!!! A L EXPORT DES STL.
!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!
	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	!!!!	
