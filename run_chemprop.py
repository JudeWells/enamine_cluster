import chemprop

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
    
