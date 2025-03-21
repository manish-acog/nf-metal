#!/usr/bin/env python3

import pandas as pd
import yaml
from pathlib import Path
import argparse

# config_path = "gwas_data_fields.yaml"
# meta_file_path = Path("/data")

def process_meta_file(meta_file: Path, output_path: Path, num_files: int, p_value_threshold: float = 0.05):
    """
    Processes the meta-analysis file:
    1. Filters rows based on P-value significance.
    2. Retains variants present in at least 2 studies.
    3. Saves the results to the output path.
    """
    # Load the data
    meta_df = pd.read_csv(meta_file, sep='\t')

    # Filter rows with significant P-values
    filtered_df = meta_df[meta_df['P-value'] <= p_value_threshold].sort_values('P-value')

    # Retain variants present in at least 2 studies
    filtered_df = filtered_df[filtered_df['Direction'].str.count('\?') <= num_files - 2]

    # Save the processed DataFrame
    filtered_df.to_csv(output_path, index=False, sep='\t')


def main():
    parser = argparse.ArgumentParser(description="Clean METAL results.")
    parser.add_argument("--metal_results", required=True, help="Path to METAL results file. eg. /output/METAANALYSIS_1.tbl")
    parser.add_argument("--config_file", required=True, help="Path to config file. eg. /data/config.yaml")
    parser.add_argument("--output_path", required=True, help="Path to output directory. eg. /output")
    args = parser.parse_args()

    metal_results = Path(args.metal_results)
    config_file = Path(args.config_file)
    output_path = Path(args.output_path)

    # Load configuration
    with open(config_file, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
        
    output_file = config.get('META_OUTPUT_FILE')
    print(output_file)
    num_files = len(config.get('INPUT_FILES', []))

    # Process the file
    file_path = output_path / output_file
    process_meta_file(metal_results, file_path, num_files)

    print(f"Processed meta-analysis file saved to: {file_path}")


if __name__ == "__main__":
    main()