#!/usr/bin/env python3
"""
DSResSol standardized batch wrapper for benchmarking
- Accepts: --fasta <input.fasta> --out <output.csv>
- Runs the DSResSol predictor and outputs a unified benchmarking CSV
"""
import os
import sys
import argparse
import tempfile
import pandas as pd
from Bio import SeqIO

WRAPPER_PREDICTOR_NAME = "DSResSol"

def parse_fasta(fasta_path):
    """Parse a FASTA file and return sequence records"""
    seqs = []
    for record in SeqIO.parse(fasta_path, "fasta"):
        seqs.append((record.id, str(record.seq)))
    return seqs

def standardize_output(input_csv, output_csv, fasta_seqs):
    """Standardize the DSResSol output to the benchmark format"""
    # Read the DSResSol predictions
    df = pd.read_csv(input_csv)
    
    # Create the standardized output format
    out_rows = []
    
    # Map between seq_id and sequence for proper output
    seq_map = {sid: seq for sid, seq in fasta_seqs}
    
    for _, row in df.iterrows():
        # Extract relevant information from DSResSol output
        acc = row.get('name', 'Unknown')
        seq = seq_map.get(acc, row.get('sequence', ''))
        
        # Convert solubility score to probabilities
        score = row.get('solubility', 0.0)
        
        out_rows.append({
            "Accession": acc,
            "Sequence": seq,
            "Predictor": WRAPPER_PREDICTOR_NAME,
            "SolubilityScore": score,
            "Probability_Soluble": score,
            "Probability_Insoluble": 1.0 - score
        })
    
    # Write the standardized output
    pd.DataFrame(out_rows).to_csv(output_csv, index=False)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DSResSol batch wrapper for benchmarking.")
    parser.add_argument("--fasta", required=True, help="Input FASTA file")
    parser.add_argument("--out", required=True, help="Output CSV file")
    parser.add_argument("--model", default=None, help="Path to model (default: use best model)")
    args = parser.parse_args()

    # Get absolute paths
    fasta_path = os.path.abspath(args.fasta)
    out_csv = os.path.abspath(args.out)
    
    # Get directory of this script for proper path resolution
    wrapper_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use the best model if not specified
    if args.model is None:
        model_path = os.path.join(wrapper_dir, "Most accurate models", "model5_dense_seq6.h5")
    else:
        model_path = os.path.abspath(args.model)
    
    # Parse input FASTA for standardizing output later
    fasta_seqs = parse_fasta(fasta_path)
    
    # Create a temporary file for DSResSol output
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        tmp_output = tmp.name
    
    try:
        # Run the DSResSol predictor
        predict_script = os.path.join(wrapper_dir, "predict.py")
        cmd = [
            "python", predict_script,
            "--model", model_path,
            "--input", fasta_path,
            "--output", tmp_output
        ]
        
        import subprocess
        subprocess.run(cmd, check=True, cwd=wrapper_dir)
        
        # Convert to standard format for benchmarking
        standardize_output(tmp_output, out_csv, fasta_seqs)
        
        print(f"DSResSol predictions completed. Results written to {out_csv}")
        
    finally:
        # Clean up temporary files
        if os.path.exists(tmp_output):
            os.remove(tmp_output)

if __name__ == "__main__":
    main()
