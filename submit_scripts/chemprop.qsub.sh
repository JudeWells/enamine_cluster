#$ -l tmem=8G
#$ -l h_vmem=8G
#chemprop approx 0.25s per ligand 
#$ -l h_rt=00:35:00
#These are optional flags but you probably want them in all jobs

#$ -S /bin/bash
#$ -j y
#$ -N REAL2
#$ -wd /SAN/orengolab/nsp13/enamine_cluster 
#second number should n mols in enamine file / batch size
#$ -t 2-23000
#The code you want to run now goes here.


date

#Python 3.8.3 Source
export PATH=/share/apps/python-3.8.5-shared/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/python-3.8.5-shared/lib:$LD_LIBRARY_PATH
source /share/apps/source_files/python/python-3.8.5.source
python3 --version
bash predict_batch.sh $SGE_TASK_ID > /dev/null
date
