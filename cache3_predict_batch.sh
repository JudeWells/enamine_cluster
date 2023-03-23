BATCHSIZE=20000
INDEX=${1}
START=$(($((INDEX * BATCHSIZE)) + 1))
END=$(($START + BATCHSIZE))
FILE=Enamine_REAL_HAC_22_23_402M_CXSMILES.cxsmiles
sed -n "$START,${END}p;$(($END + 1))q" $FILE > smiles_file.txt
wc -l smiles_file.txt
$head -10 smiles_file.txt
python run_forest.py smiles_file.txt $START $FILE
echo nice_jobdone
rm REAL.o*
