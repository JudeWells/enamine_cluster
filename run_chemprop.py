import sys
import os
import numpy as np
import chemprop
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

smiles_file = sys.argv[1]
index_start = sys.argv[2]
FILE=sys.argv[3]
outdir=FILE.replace("Enamine_REAL_HAC_","").split(".")[0]

arguments = [
    '--test_path', '/dev/null',
    '--preds_path', '/dev/null',
    '--checkpoint_dir', 'checkpoints/jude_mmgbsa_nov21',
    # '--uncertainty_method', 'ensemble',
    '--num_workers', '1',
    '--batch_size', '100',
]


if __name__=="__main__":
    data = pd.read_csv(smiles_file, delimiter='\t', header=None)
    data.columns = ['smiles', 'idnumber', 'reagent1', 'reagent2', 'reagent3', 'reagent4',
       'reaction', 'MW', 'HAC', 'sLogP', 'HBA', 'HBD', 'RotBonds', 'FSP3',
       'TPSA', 'QED', 'PAINS', 'BRENK', 'NIH', 'ZINC', 'LILLY', 'lead-like',
       '350/3_lead-like', 'fragments', 'strict_fragments', 'PPI_modulators',
       'natural_product-like', 'Type', 'InChiKey']
    if 'smiles' in data.loc[0].values:
        data = data.loc[1:]
        data = data.reset_index(drop=True)
    args = chemprop.args.PredictArgs().parse_args(arguments)
    model_objects = chemprop.train.load_model(args=args)
    smiles_lines = data.iloc[:,0].values.reshape([len(data), 1])
    preds = chemprop.train.make_predictions(args=args, smiles=smiles_lines, return_uncertainty=False,
                                             model_objects=model_objects)
    preds = np.array(preds)
    if 'Invalid SMILES' in preds:
        preds[preds == 'Invalid SMILES'] = 100
        preds = preds.astype(float)
    keep = np.where(preds[:,0] < -50)[0]
    results = []
    for i in keep:
        try:
            one_row = data.loc[i].to_dict()
            if one_row['PAINS']==True:
                continue
            if float(one_row['MW']) < 500 and float(one_row['sLogP']) < 4.5:
                one_row['pred'] = preds[i, 0]
                # one_row['unc'] = unc[i,0]
                results.append(one_row)
        except:
            pass
    if len(results):
        os.makedirs(outdir, exist_ok=True)
        savepath = os.path.join(outdir, str(index_start).zfill(5)+'.csv')
        pd.DataFrame(results).to_csv(str(savepath), index=False)
