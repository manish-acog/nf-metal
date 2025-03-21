#!/usr/bin/env python3

import yaml
from pathlib import Path
import argparse


# output_path = "/data"
# config_file = "/data/gwas_data_fields.yaml"


def generate_metal_script(qc_files, config, output_path):
    """Creates the METAL script"""
    metal_script = f"""
    GENOMICCONTROL ON
    SCHEME STDERR

    MARKER {config.get('VARIANT_ID')}
    ALLELE {config.get('OTHER_ALLELE')} {config.get('EFFECT_ALLELE')}
    EFFECT {config.get('BETA')}
    PVALUE {config.get('PVALUE')}
    STDERR {config.get('STDERR')}
    SEPARATOR TAB
    """

    for qc_file in qc_files:
        metal_script += f"PROCESS {output_path}/{qc_file}\n"

    # QCd TTAM studies if any to be added to the scripts

    metal_script += f"""
    OUTFILE {output_path}/METAANALYSIS_results_ .tbl

    ANALYZE HETEROGENEITY

    QUIT
    """
    return metal_script


def main():
    parser = argparse.ArgumentParser(description="Create METAL script.")
    parser.add_argument("--config_file", required=True, help="Path to config file. eg. /data/config.yaml")
    parser.add_argument("--output_path", required=True, help="Path to output directory. eg. /output")
    parser.add_argument('--qc_files', nargs='+', required=True, help='List of QC files')
    args = parser.parse_args()

    qc_files = [Path(file) for file in args.qc_files]
    output_path = Path(args.output_path)
    config_file = Path(args.config_file)

    # Load configuration
    with open(config_file, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # Generate METAL script
    metal_script = generate_metal_script(qc_files, config, output_path)

    # Write the METAL script to a file
    metal_file = 'metal_script.txt'
    with open(output_path / metal_file, 'w') as script_file:
        script_file.write(metal_script)

    print("METAL script has been generated successfully!")


if __name__ == "__main__":
    main()