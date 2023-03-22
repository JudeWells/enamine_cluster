BATCHSIZE=40000
INDEX=${1}
START=$(($((INDEX * BATCHSIZE)) + 1))
END=$(($START + BATCHSIZE))
FILE=Enamine_REAL_HAC_25_460M_CXSMILES.cxsmiles
sed -n "$START,${END}p;$(($END + 1))q" $FILE > smiles_file.txt
python3 run_chemprop.py smiles_file.txt $START $FILE
rm REAL.o*
