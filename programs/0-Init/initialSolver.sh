#! /bin/bash

function traitement()
{
	cd $1
	wmake
	wclean
}

N=10
abs_dir="/home/jurado/OpenFOAM/jurado-5.0/application/solver"
listdir=$(ls "$abs_dir")

echo "$listdir"
echo "$abs_dir"

(
for dir in $listdir; do
	#echo "$dir"
	((i=i%N)); ((i++==0)) && wait
	traitement "$abs_dir/$dir" &
done
)
