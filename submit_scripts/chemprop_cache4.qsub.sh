#$ -l tmem=8G
#$ -l h_vmem=8G
#chemprop approx 0.25s per ligand 
#$ -l h_rt=00:45:00
#These are optional flags but you probably want them in all jobs

#$ -S /bin/bash
#$ -j y
#$ -N REAL2
#$ -wd /SAN/orengolab/nsp13/enamine_cluster 
#second number should n mols in enamine file / batch size
#$ -t 5001-20100
#The code you want to run now goes here.
WORKING_DIR=/SAN/orengolab/nsp13/enamine_cluster
cd $WORKING_DIR
FILE=${WORKING_DIR}/Enamine_REAL_HAC_22_23_402M_CXSMILES.cxsmiles
MODEL_DIR=${WORKING_DIR}/checkpoints/cache4_log_ic50
THRESHOLD=1.0
EXPERIMENT_NAME=cache4_log_ic50



date

#Python 3.8.3 Source
export PATH=/share/apps/python-3.8.5-shared/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/python-3.8.5-shared/lib:$LD_LIBRARY_PATH
source /share/apps/source_files/python/python-3.8.5.source
python3 --version
bash predict_batch.sh $SGE_TASK_ID $FILE $MODEL_DIR $THRESHOLD $EXPERIMENT_NAME > /dev/null
date
