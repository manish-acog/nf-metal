#!/usr/bin/env python3

import yaml
import pandas as pd
from pathlib import Path
import argparse


# io_path = "/data"
# config_file = "gwas_data_fields.yaml"


def qc(df: pd.DataFrame, study: str, config):
    """Removes variants that do not pass the QC conditions"""

    org_len = len(df)

    if config['EFFECT_ALLELE_FREQ'] in df.columns: 
        df = df[df[config['EFFECT_ALLELE_FREQ']] >= 0.01]
    else:
        print(f"{study}: 'effect_allele_frequency' column missing. Skipping frequency filter.")

    if {config['EFFECT_ALLELE'], config['OTHER_ALLELE']}.issubset(df.columns):
        df = df[(df[config['EFFECT_ALLELE']].str.len() == 1) & (df[config['OTHER_ALLELE']].str.len() == 1)]
    else:
        print(f"{study}: Allele columns missing. Skipping multi-allele filter.")

    df = df.drop_duplicates(subset = [config['VARIANT_ID']])

    curr_len = len(df)
    print(f"{study}: No of variants lost during QC: {org_len - curr_len}")

    return df


def main():
    parser = argparse.ArgumentParser(description="Run QC on GWAS data.")
    parser.add_argument("--input_path", required=True, help="Path to input data directory. eg. /data")
    parser.add_argument("--config_file", required=True, help="Path to config file. eg. /data/config.yaml")
    parser.add_argument("--output_path", required=True, help="Path to output directory. eg. /output")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    config_file = Path(args.config_file)

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    for study in config['INPUT_FILES']:
        study_path = input_path / study
        try:
            sep = '\t' if study_path.suffix == '.tsv' else ','
            df = pd.read_csv(study_path, sep=sep)
        except FileNotFoundError:
            print(f"File not found: {study_path}")
            continue
        except pd.errors.ParserError:
            print(f"Error parsing file: {study_path}")
            continue
        
        qc_df = qc(df, study, config)
        output_file = output_path / f"qc_{study}"
        qc_df.to_csv(output_file, index=False, sep='\t')


if __name__ == "__main__":
    main()