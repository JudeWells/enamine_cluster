#$ -l tmem=16G
#$ -l h_vmem=16G
#chemprop approx 0.25s per ligand 
#$ -l h_rt=11:45:00
#These are optional flags but you probably want them in all jobs

#$ -S /bin/bash
#$ -j y
#$ -N c4_classifier
#$ -wd /SAN/orengolab/nsp13/enamine_cluster 
#second number should n mols in enamine file / batch size
#$ -t 1-4023
#$ -o /SAN/orengolab/nsp13/enamine_cluster/logs/
#The code you want to run now goes here.

WORKING_DIR=/SAN/orengolab/nsp13/enamine_cluster
cd $WORKING_DIR
FILE=${WORKING_DIR}/Enamine_REAL_HAC_22_23_402M_CXSMILES.cxsmiles #402282236
MODEL_DIR=${WORKING_DIR}/chemprop_new_classifier_ens_2
THRESHOLD=0.9
EXPERIMENT_NAME=c4_22_23
BATCH_SIZE=100000
echo $EXPERIMENT_NAME

which conda
conda activate cache3
which python
bash predict_batch.sh $SGE_TASK_ID $FILE $MODEL_DIR $THRESHOLD $EXPERIMENT_NAME $BATCH_SIZE
date
