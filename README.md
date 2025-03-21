# Nextflow pipeline for GWAS meta-analysis using METAL

This nextflow pipeline performs the following steps:
1. Prepares the gwas data files in the input folder for meta-analysis by filtering it using some QC tests
2. Creates a METAL script with the help of a config file
3. Performs the meta-analysis on the QCd GWAS data using METAL
4. Cleans the meta-analysis results which can then be used for further analysis and visualisation. The final and intermediate files can be found in the output folder. 

## Assumptions about the input GWAS data
1. All files will have the same column names
2. Beta and/or odds ratio and std error will be available
3. The GWAS study data is harmonized

## Prerequisites
1. conda
2. docker
3. Harmonized gwas studies in the input folder (.csv or .tsv)
3. Updated gwas_data_fields.yaml file in the input folder

## Running the nextflow pipeline
1. conda env create -f env.yml
2. conda activate nflow
3. nextflow run main.nf

## TODO:
1. Forest plot
2. Handling of multiple ancestries
3. Data harmonization