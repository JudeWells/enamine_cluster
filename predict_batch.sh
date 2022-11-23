BATCHSIZE=20
INDEX=${1}
START=$(($((INDEX * BATCHSIZE)) + 1))
END=$(($START + BATCHSIZE))
echo $START
echo $END
sed -n "$START,${END}p;$(($END + 1))q" enamine_real_sample.txt > smiles_file.txt
python3 run_chempro.py smiles_file.txt
