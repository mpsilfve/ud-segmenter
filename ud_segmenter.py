#!/usr/bin/pypy3
import base_sample

def run(train_data, test_data, N=1000):
    """Runs the model on given datasets and outputs the segmented version
    
    Parameters
    ----------
    train_data: str
        A string containing train data in lemma-tags form.
    test_data: str
        Same for test data.
    N: int
        Number of passes.
    """
    train_data = train_data.split('\n')
    test_data = test_data.split('\n')
    return base_sample.segment(train_data, test_data, N=N)

if __name__ == '__main__':
    import argparse
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--train',
        metavar='filename',
        type=str,
        required=True,
        help='Train dataset file in lemma-tags form.',
    )
    arg_parser.add_argument(
        '--test',
        metavar='filename',
        type=str,
        required=True,
        help='Test dataset file in lemma-tags form.',
    )
    arg_parser.add_argument(
        '-o',
        '--output',
        metavar='filename',
        type=str,
        required=True,
        help='Output file for the result of the segmentation.',
    )
    arg_parser.add_argument(
        '-n',
        '--number_of_passes',
        metavar='N',
        type=int,
        required=True,
        default=1000,
        help='Number of passes for the model.',
    )
    args = arg_parser.parse_args()
    
    with open(args.train) as f:
        train_data = f.read()
    with open(args.test) as f:
        test_data = f.read()
    result = run(train_data, test_data, N=args.number_of_passes)
    with open(args.output, 'w') as f:
        f.write(result)
