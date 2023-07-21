#$ -l tmem=8G
#$ -l h_vmem=8G
#chemprop approx 0.25s per ligand 
#$ -l h_rt=01:45:00
#These are optional flags but you probably want them in all jobs

#$ -S /bin/bash
#$ -j y
#$ -N mini_real
#$ -wd /SAN/orengolab/nsp13/enamine_cluster 
#second number should n mols in enamine file / batch size
#$ -t 1-2 #10050
#The code you want to run now goes here.
WORKING_DIR=/SAN/orengolab/nsp13/enamine_cluster
cd $WORKING_DIR
FILE=${WORKING_DIR}/Enamine_REAL_HAC_22_23_402M_CXSMILES.cxsmiles
MODEL_DIR=${WORKING_DIR}/checkpoints/cache4_log_ic50
THRESHOLD=1.0
EXPERIMENT_NAME=cache4_log_ic50



date

which conda
conda activate cache3
which python
bash predict_batch.sh $SGE_TASK_ID $FILE $MODEL_DIR $THRESHOLD $EXPERIMENT_NAME
date
