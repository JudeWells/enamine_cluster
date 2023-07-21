BATCHSIZE=40000
INDEX=${1}
FILE=${2}
MODEL_DIR=${3}
THRESHOLD=${4}
EXPERIMENT_NAME=${5}
START=$(($((INDEX * BATCHSIZE)) + 1))
END=$(($START + BATCHSIZE))
sed -n "$START,${END}p;$(($END + 1))q" $FILE > smiles_file.txt
python run_chemprop.py smiles_file.txt $START $FILE $MODEL_DIR $THRESHOLD $EXPERIMENT_NAME
echo nice_jobdone
rm REAL.o*
