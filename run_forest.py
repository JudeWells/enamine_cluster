import sys
import os
import numpy as np
import pandas as pd
import dill
from rdkit import Chem
from rdkit.Chem import AllChem
from imblearn.ensemble import BalancedRandomForestClassifier
from nonconformist.cp import IcpClassifier
from nonconformist.acp import AggregatedCp
from nonconformist.nc import NcFactory,AbsErrorErrFunc
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.neighbors import KNeighborsRegressor
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

smiles_file = sys.argv[1]
index_start = sys.argv[2]
FILE=sys.argv[3]
outdir=FILE.replace("Enamine_REAL_HAC_","").split(".")[0]


def load_agg_forest(model_path='models/saved_model.dill'):
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    return model

def contains_carboxylic_acid_or_carboxylate(mol):
    carboxylate_pattern = Chem.MolFromSmarts('[CX3](=O)[OX1H0-,OX2H1]')
    return mol.HasSubstructMatch(carboxylate_pattern)

def featurize_from_smiles(smiles_array):
    RADIUS = 3
    NBITS = 2048
    DEFAULT_VALUE = np.zeros(NBITS)
    mols = [Chem.MolFromSmiles(smi[0]) for smi in smiles_array]
    print(f"len mols: {len(mols)}", f"not None: {len([mol for mol in mols if mol is not None])}")
    X = [np.array(AllChem.GetMorganFingerprintAsBitVect(mol, RADIUS, nBits=NBITS)) if mol is not None else DEFAULT_VALUE for mol in mols]
    return np.array(X), mols


if __name__=="__main__":
    data = pd.read_csv(smiles_file, delimiter='\t', header=None, error_bad_lines=False)
    print(f'data shape: {data.shape}')    
# data = pd.read_csv('01000.csv', delimiter='\t', header=None)
    data.columns = ['smiles', 'idnumber', 'reagent1', 'reagent2', 'reagent3', 'reagent4',
       'reaction', 'MW', 'HAC', 'sLogP', 'HBA', 'HBD', 'RotBonds', 'FSP3',
       'TPSA', 'QED', 'PAINS', 'BRENK', 'NIH', 'ZINC', 'LILLY', 'lead-like',
       '350/3_lead-like', 'fragments', 'strict_fragments', 'PPI_modulators',
       'natural_product-like', 'Type', 'InChiKey']

    if 'smiles' in data.loc[0].values:
        data = data.loc[1:]
        data = data.reset_index(drop=True)

    smiles_lines = data.iloc[:, 0].values.reshape([len(data), 1])
    X, mols = featurize_from_smiles(smiles_lines)
    model = load_agg_forest()
    preds = model.predict(X)
    lower = 0.15
    upper = 0.4
    keep = np.where(np.logical_and(preds[:, 0]< lower, preds[:, 1]>upper))[0]
    results = []
    for i in keep:
        try:
            one_row = data.loc[i].to_dict()
            if one_row['PAINS']==True:
                continue
            if float(one_row['MW']) < 500 and float(one_row['sLogP']) < 4.5:
                if not contains_carboxylic_acid_or_carboxylate(mols[i]):
                    one_row['pred'] = preds[i, 1]
                    # one_row['unc'] = unc[i,0]
                    results.append(one_row)
        except:
            pass
    print('preds completed, len keep:', len(results))
    if len(results):
        os.makedirs(outdir, exist_ok=True)
        savepath = os.path.join(outdir, str(index_start).zfill(5)+'.csv')
        pd.DataFrame(results).to_csv(str(savepath), index=False)
