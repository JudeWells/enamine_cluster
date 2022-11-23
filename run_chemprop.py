import sys
import chemprop

smiles_file = sys.argv[0]
index_start = sys.argv[1]
index_end = sys.argv[2]

arguments = [
    '--test_path', '/dev/null',
    '--preds_path', '/dev/null',
    '--checkpoint_dir', 'jude_mmgbsa_nov21',
    '--uncertainty_method', 'ensemble',
    '--num_workers', '8',
    '--batch_size', '180',
]


if __name__=="__main__":
    args = chemprop.args.PredictArgs().parse_args(arguments)
    model_objects = chemprop.train.load_model(args=args)

