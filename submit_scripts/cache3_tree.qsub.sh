# submit script for forest model cache3
#$ -l tmem=8G
#$ -l h_vmem=8G
# RF model approx 0.02s per ligand 
#$ -l h_rt=00:12:00
#These are optional flags but you probably want them in all jobs

#$ -S /bin/bash
#$ -j y
#$ -N REAL2
#$ -wd /SAN/orengolab/nsp13/enamine_cluster 
#second number should n mols in enamine file / batch size
#$ -t 1-5
#The code you want to run now goes here.


date

cd /SAN/orengolab/nsp13/enamine_cluster
which conda
conda activate cache3
which python
# bash cache3_predict_batch.sh $SGE_TASK_ID > /dev/null
bash cache3_predict_batch.sh $SGE_TASK_ID
date
