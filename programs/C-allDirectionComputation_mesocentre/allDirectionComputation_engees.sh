#! /bin/bash
#SBATCH -p engees2013 
#SBATCH -A qosengees2013 
#SBATCH -n 48
#SBATCH -t 1000:00:00

#Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# Get application directory
application=`getApplication`

#Get openFoam version
source /usr/local/openfoam/OpenFOAM-5.0/etc/bashrc

### DEBUT PARTIE DU CODE A MODIFIER ########################################################

while getopts p:n:s:e: option
do
	case "${option}"
		in
		p) adresseEtude=${OPTARG};;
		e) etudeNom=${OPTARG};;
		n) nbProc=${OPTARG};;
		s) versionSolver=${OPTARG};;
	esac
done

### FIN PARTIE A MODIFIER POUR UTILISATION CLASSIQUE #######################################
echo "nombre de processeur: $nbProc"
echo "version: $versionSolver"
#*							*#
#*							*#
#*							*#
#*							*#


### getting number of inlet###	
nbInletPol=0

cd $adresseEtude
echo "étude en cours de calcul: $adresseEtude"
echo " "

### Permet de déterminer le nombre de source maximale dans l'étude ###

for Dir in D_*/; do
	#pushd ${Dir}
	cd $Dir
		for Speed in V_*/; do
			#pushd ${Speed}
			cd $Speed
				trisurface_files=$(ls constant/triSurface)
		
				stl_list=()

				
				for file in $trisurface_files
				do
					if [[ $file == "inletPol"* && $file == *"stl" ]]
					then
						stl_list+=($file)
					fi
				done 				
				
				if [[ nbInletPol -lt ${#stl_list[@]} ]]
				then
					nbInletPol=${#stl_list[@]}
				fi
			#popd
			cd ..		
		done
	#popd
	cd ..
done

versionSolverNbSources=$versionSolver"-"$nbInletPol"s"

echo "nombre de source de polluant maximal: $nbInletPol"

### CREER LES CHEMINS POUR L ETUDE, LE LOG ET LES PROBES ###
dirLog="$adresseEtude/log"
dirProbes="$adresseEtude/probes"

### CREER LES REPERTOIRES LOG ET PROBES S ILS N EXISTENT PAS ###
if [ ! -e "$dirLog" ]
then
	mkdir "$dirLog"
fi

if [ ! -e "$dirProbes" ]
then
	mkdir "$dirProbes"
	for i in $(seq 1 $nbInletPol)
	do
		mkdir "$dirProbes/s$i"
	done
	mkdir "$dirProbes/U"
	touch  $fileLog
fi

### INITIALISE ET CREER LE FICHIER LOG
logError="$dirLog/error-Etude.log"
date '+%Y-%m-%d:%H:%M:%S'  > $logError
echo '' >> $logError
echo "Fichier de log pour l'etude $nomEtude situé dans: $racine " >> $logError

### INITIALISATION VARIABLE NECESSAIRE POUR LA BOUCLE ###
previousError=0
oldDir=""

for newDir in D_*/; do # Fait une boucle sur tout les dossiers (d'ou la présence du / à coté de l'étoile) présents dans le répertoire de l'étude

    echo "Référence de l'étude: $etudeNom"
    echo "Calcul pour la direction: $newDir"
    echo " "
    pushd ${newDir}
    oldSpeed=""

    for newSpeed in V_*/; do

	newSpeed=${newSpeed::-1} #Sert à supprimer le dernier character de la variable, ici le "/"
	

	### mapFields management ###
	cd $newSpeed
	echo "		la vitesse en cours de calcul: $newSpeed"
	echo "		adresse du répertoire: $adresseEtude/$newDir$newSpeed"
	>&2 echo "$newDir/$newSpeed ## $iter ## $actualDir ##"

	if [ "x${oldDir}" != "x" ]; then
            ## from second direction on
            if [ "x${oldSpeed}" != "x" ]; then
                # from second speed on
                if [ "$previousError" -eq 0 ]; then #Vérifie que le calcul précédent c'est bien passé sinon fait le mapField par rapport à la vitesse équivalente de la direction précédente
                    echo "          mapFields sur $newSpeed par rapport à la vitesse précédente: $newDir$oldSpeed"
                    adresseField="$adresseEtude/$newDir$oldSpeed"
                    mapFields "$adresseField" -consistent >> log.mapFields
                else #prend en compte le cas ou le calcul précédent n'a pas marché et prend donc celui de la direction précédente
                    echo "          La vitesse précédente n'a pas convergé, mapFields sur $newSpeed par rapport à la direction précédente: $oldDir$newSpeed"
                    adresseField="$adresseEtude/$oldDir$newSpeed"
                    mapFields "$adresseField" >> log.mapFields
                fi
            else
                # first speed of the new direction
                echo "          mapFields sur $newSpeed par rapport à la direction précédente: $oldDir$newSpeed"
                adresseField="$adresseEtude/$oldDir$newSpeed"
                mapFields "$adresseField" >> log.mapFields
            fi
        else
            ## first direction
            if [ "x${oldSpeed}" != "x" ]; then 
                # from second speed on
                if [ "$previousError" -eq 0 ]; then   #Vérifie que le calcul précédent c'est bien passé sinon fait le mapField par rapport à la vitesse équivalente de la direction précédente
                    echo "          mapFields sur $newSpeed par rapport à la vitesse précédente: $newDir$oldSpeed"
                    adresseField="$adresseEtude/$newDir$oldSpeed"
                    mapFields "$adresseField" -consistent >> log.mapFields
                else
                    ## nothing to do, we cannot get this mapping from anywhere else
                    echo "          nothing to do for this case"
                fi
            else
                # first speed of the new direction
		## nothing to do here, move along...
                echo "          nothing to do for this case"
            fi
        fi

	sed -i '28s#.*#deltaT          0.00001;#' system/controlDict   # Change la ligne par le string souhaité
	sed -i "18s#.*#numberOfSubdomains $nbProc;#" system/decomposeParDict   # Change la ligne par le string souhaité

	### Allrun launching ###
	echo "		Allrun:"
	echo "			decomposePar"
	decomposePar >> log.DecomposeParRun
	echo "			Lancement du calcul sur $nbProc processeurs"
	mpirun -np $nbProc 3DAIR-USFD-$versionSolverNbSources -parallel >> log.Run
	previousError=$?

	if [ $previousError -ne 0 ];then
		echo "			Seconde tentative pour le calcul qui n'a pas convergé la première fois, lancé sur $nbProc proc"
		sed -i '49s#.*#maxCo           0.5;#' system/controlDict
		sed -i '50s#.*#maxAlphaCo      0.5;#' system/controlDict
		mpirun -np $nbProc 3DAIR-USFD-$versionSolverNbSources -parallel >> log.SecondRun
		previousError=$?
	fi

	echo "			reconstructPar"
	reconstructPar -latestTime >> log.ReconstructPar
	mv system/controlDict system/controlDict.Done
	mv system/controlDict.probes system/controlDict
	echo "			Lancement du calcul avec les probes sur $nbProc processeurs"
	mpirun -np $nbProc 3DAIR-USFD-$versionSolverNbSources -parallel >> log.RunProbes
	echo "			reconstructPar"
	reconstructPar -latestTime >> log.ReconstructPar
	previousError=$?
	rm -r processor*
	
	

	### Error Management ###
	if [ "$previousError" -eq 0 ]
	then
		newDir2="${newDir::-1}_" #Sert à supprimer le "/" dans D_XXX/ pour que le nom du fichier probes soit bien dans le bon format
		echo "  		Pour le vent : $newDir$newSpeed le calcul s'est bien déroulé jusqu'au temps voulu"
		echo "  Pour le vent : $newDir$newSpeed le calcul s'est bien déroulé jusqu'au temps voulu" >> $logError
		echo "		Transfert des résultats probes dans le fichier probes"

		cd postProcessing
			for i in $(seq 1 $nbInletPol)
			do
				sProbeLocation=`find -iname "s$i" | rev | cut -d '/' -f2 | rev | sort -t '\0' -n | tail -1` #Le find trouve la liste qui ont un s, le sed élimine tous ce qui n'est pas des nombres, le sort trie par ordre alphabétique, le tail chope le dernier élément du find, donc la probes le plus récent
				cp -f "$adresseEtude/$newDir$newSpeed/postProcessing/probes/$sProbeLocation/s$i" "$dirProbes/s$i/s$i""_""$newDir2$newSpeed"

			done
			uProbeLocation=`find -iname "U" | rev | cut -d '/' -f2 | rev | sort -t '\0' -n | tail -1`
			cp -f "$adresseEtude/$newDir$newSpeed/postProcessing/probes/$uProbeLocation/U" "$dirProbes/U/U_$newDir2$newSpeed"
		cd ..
	else
		echo "  		Pour le vent : $newDir$newSpeed le calcul a divergé"
		echo "  Pour le vent : $newDir$newSpeed le calcul a divergé" >> $logError
	fi

	echo " "

	### Actualisation next step ###
	oldSpeed=$newSpeed
   	cd ..
    done

    oldDir=$newDir
    echo " "
    popd
done
