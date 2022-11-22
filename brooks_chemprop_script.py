import numpy as np
import chemprop

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# with open('enamine_hts_test_set.csv') as f:
#     smiles = [[s.strip().split(',')[-1]] for s in f.readlines()[1:]]

with open('enamine_real_sample.txt', 'r') as f:
    smiles = [[s.strip().split('\t')[0]] for s in f.readlines()[1:]]


arguments = [
    '--test_path', '/dev/null',
    '--preds_path', '/dev/null',
    '--checkpoint_dir', 'checkpoints/jude_mmgbsa_nov21',
    '--uncertainty_method', 'ensemble',
    '--num_workers', '8',
    '--batch_size', '180',
]

outfile = "chemprop_hts_preds_nov21.csv"

args = chemprop.args.PredictArgs().parse_args(arguments)
model_objects = chemprop.train.load_model(args=args)

already_processed = set()
try:
    with open(outfile, "r") as f:
        for line in f.readlines()[1:]:
            already_processed.add(line.split(',')[0])
except:
    pass

fresh = len(already_processed) == 0

with open(outfile, "w" if fresh else "a") as f:
    if fresh:
        print("SMILES,prediction,uncertainty", file=f)
    for it, chunk in enumerate(chunker(smiles, 50000)):
        print("completed %d" % (it * 50000))
        complete = already_processed.intersection([c[0] for c in chunk])
        if len(complete) == len(chunk):
            print("-- (skipping previously processed chunk)")
            continue
        for sm in complete:
            chunk.remove([sm])
        preds, unc = chemprop.train.make_predictions(args=args, smiles=chunk, return_uncertainty=True, model_objects=model_objects)
        f.writelines([','.join(np.array(a).squeeze().tolist())+'\n' for a in zip(chunk, preds, unc)])
    already_processed.update(set([sm[0] for sm in chunk]))