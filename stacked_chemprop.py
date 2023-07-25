import sys
import os
import copy
import numpy as np
import chemprop
import pandas as pd
import warnings

"""
Created by Jude Wells 2023-07-23
Purpose of script is to first run the chemprop classification model
Second run the chemprop regression model 
(if it passes the classification model)
Script is called as follows:
python3 run_chemprop.py smiles_file.txt $START $FILE $MODEL_DIR  $THRESHOLD
"""

warnings.simplefilter(action='ignore', category=FutureWarning)

smiles_file = sys.argv[1]
index_start = sys.argv[2]
FILE=sys.argv[3]
class_model_dir=sys.argv[4]
reg_model_dir=sys.argv[5]
experiment_name=sys.argv[6]
outdir=os.path.join(experiment_name, FILE.replace("Enamine_REAL_HAC_","").split(".")[0])
class_threshold=float(sys.argv[7])
reg_threshold=float(sys.argv[8])

def process_enamine_data():
    data = pd.read_csv(smiles_file, delimiter='\t', header=None)
    data.columns = ['smiles', 'idnumber', 'reagent1', 'reagent2', 'reagent3', 'reagent4',
       'reaction', 'MW', 'HAC', 'sLogP', 'HBA', 'HBD', 'RotBonds', 'FSP3',
       'TPSA', 'QED', 'PAINS', 'BRENK', 'NIH', 'ZINC', 'LILLY', 'lead-like',
       '350/3_lead-like', 'fragments', 'strict_fragments', 'PPI_modulators',
       'natural_product-like', 'Type', 'InChiKey']
    if 'smiles' in data.loc[0].values:
        data = data.loc[1:]
        data = data.reset_index(drop=True)
    return data

def run_model(arguments, data):
    args = chemprop.args.PredictArgs().parse_args(arguments)
    model_objects = chemprop.train.load_model(args=args)
    smiles_lines = data.iloc[:,0].values.reshape([len(data), 1])
    preds = chemprop.train.make_predictions(args=args, smiles=smiles_lines, return_uncertainty=False,
                                             model_objects=model_objects)
    return preds

def filter_class_results(data, preds, threshold):
    preds = np.array(preds)
    if 'Invalid SMILES' in preds:
        preds[preds == 'Invalid SMILES'] = 999
        preds = preds.astype(float)
    data['classification_pred'] = preds[:, 0]
    keep = np.where(preds[:,0] < threshold)[0]
    results = []
    for i in keep:
        try:
            one_row = data.loc[i].to_dict()
            if 'PAINS' in one_row and one_row['PAINS']==True:
                continue
            if float(one_row['MW']) < 600 and float(one_row['sLogP']) < 8:
                results.append(one_row)
        except:
            continue
    return pd.DataFrame(results)

def filter_reg_preds(data, preds, threshold):
    preds = np.array(preds)
    if 'Invalid SMILES' in preds:
        preds[preds == 'Invalid SMILES'] = 100000
        preds = preds.astype(float)
    keep = np.where(preds[:,0] < threshold)[0]
    return data.iloc[keep]


def main():
    data = process_enamine_data()
    classifier_arguments = [
        '--test_path', '/dev/null',
        '--preds_path', '/dev/null',
        # '--uncertainty_method', 'ensemble',
        '--num_workers', '1',
        '--batch_size', '100',
        '--checkpoint_dir',
    ]

    regression_arguments = copy.copy(classifier_arguments)
    classifier_arguments.append(class_model_dir)
    regression_arguments.append(reg_model_dir)
    preds = run_model(classifier_arguments, data)
    filtered_data = filter_class_results(data, preds, class_threshold)
    reg_preds = run_model(regression_arguments, filtered_data)
    final_keep = filter_reg_preds(filtered_data, reg_preds, reg_threshold)
    print('preds completed, len keep:', len(final_keep))
    if len(final_keep) > 0:
        os.makedirs(outdir, exist_ok=True)
        savepath = os.path.join(outdir, str(index_start).zfill(8)+'.csv')
        pd.DataFrame(final_keep).to_csv(str(savepath), index=False)




if __name__=="__main__":
    main()
