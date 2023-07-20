BATCHSIZE=20000
INDEX=${1}
FILE=${2}
MODEL_DIR=${3}
THRESHOLD=${4}
START=$(($((INDEX * BATCHSIZE)) + 1))
END=$(($START + BATCHSIZE))
sed -n "$START,${END}p;$(($END + 1))q" $FILE > smiles_file.txt
python3 run_chemprop.py smiles_file.txt $START $FILE $MODEL_DIR $THRESHOLD
echo nice_jobdone
rm REAL.o*
