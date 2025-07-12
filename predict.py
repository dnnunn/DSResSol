#!/usr/bin/env python3
"""
predict.py - Batch solubility prediction for DSResSol from the command line

Usage:
  python predict.py --model path/to/model.h5 --input sequences.fasta --output predictions.csv
  python predict.py --model path/to/model.h5 --input peptides.csv --output predictions.csv

- Input: CSV (with header 'Seq') or FASTA file of protein/peptide sequences
- Output: CSV with columns: Seq, PredictedSolubility
"""
import argparse
import os
import sys
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from lib.Util import Util

def read_fasta(fasta_path):
    seqs = []
    with open(fasta_path, 'r') as f:
        seq = ''
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if seq:
                    seqs.append(seq)
                    seq = ''
            else:
                seq += line
        if seq:
            seqs.append(seq)
    return pd.DataFrame({'Seq': seqs})

def main():
    parser = argparse.ArgumentParser(description='Batch solubility prediction for DSResSol')
    parser.add_argument('--model', required=True, help='Path to trained DSResSol .h5 model (e.g., Most accurate models/model5_dense_seq6.h5)')
    parser.add_argument('--input', required=True, help='Input CSV (header: Seq) or FASTA file')
    parser.add_argument('--output', required=False, help='Output CSV for predictions (default: stdout)')
    args = parser.parse_args()

    # Load sequences
    if args.input.lower().endswith('.csv'):
        df = pd.read_csv(args.input)
        if 'Seq' not in df.columns:
            print('Error: Input CSV must have a header column named "Seq".', file=sys.stderr)
            sys.exit(1)
    elif args.input.lower().endswith(('.fa', '.fasta')):
        df = read_fasta(args.input)
    else:
        print('Error: Input file must be .csv or .fasta/.fa', file=sys.stderr)
        sys.exit(1)
    if len(df) == 0:
        print('Error: No sequences found in input.', file=sys.stderr)
        sys.exit(1)

    # Prepare encoding and padding
    util = Util()
    encoded = util.integer_encoding(df)
    pad_len = util.config['model_config']['max_pad_length'].get(int)
    X = pad_sequences(encoded, maxlen=pad_len, padding='post', truncating='post')

    # Load model
    model = load_model(args.model)
    y_pred = model.predict(X)
    print("Raw model output:", y_pred)

    # Prepare PeptideFrontEnd-compatible output
    if len(y_pred.shape) == 2 and y_pred.shape[1] == 2:
        # Assume column 0 = soluble probability
        solubility = y_pred[:, 0]
        prediction = np.where(solubility >= 0.5, 'soluble', 'insoluble')
    else:
        solubility = y_pred.flatten() if len(y_pred.shape) == 2 and y_pred.shape[1] == 1 else y_pred
        prediction = np.where(solubility >= 0.5, 'soluble', 'insoluble')

    # Assign names: if FASTA, use header, else use index or 'Unknown'
    if 'Name' in df.columns:
        names = df['Name']
    elif 'name' in df.columns:
        names = df['name']
    elif 'Seq' in df.columns:
        # Try to parse FASTA header from Seq if possible
        names = ['Unknown'] * len(df)
    else:
        names = ['Unknown'] * len(df)

    # Sequence column
    if 'Seq' in df.columns:
        sequences = df['Seq']
    elif 'sequence' in df.columns:
        sequences = df['sequence']
    else:
        sequences = [''] * len(df)

    output_df = pd.DataFrame({
        'name': names,
        'sequence': sequences,
        'solubility': solubility,
        'prediction': prediction
    })

    if args.output:
        output_df.to_csv(args.output, index=False)
        print(f'Predictions written to {args.output}')
    else:
        print(output_df.to_csv(index=False))

if __name__ == '__main__':
    main()
