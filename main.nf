#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

log.info """
    META-ANALYSIS   P I P E L I N E
    =======================================
    input_dir   : ${params.input_dir}
    config_file : ${params.config_file}
    output_dir  : ${params.output_dir}
    """

workflow {
    // Step 1: Run data preparation and capture its output
    data_output_ch = DATA_PREP(params.input_dir, params.config_file, params.output_dir)

    // Step 2: Create METAL script, waits for DATA_PREP to complete
    metal_script_ch = CREATE_METAL_SCRIPT(params.config_file, params.output_dir, data_output_ch)

    // Step 3: Run METAL for GWAS meta-analysis
    metal_results_ch = RUN_METAL(metal_script_ch, params.output_dir)

    // Step 4: Clean the METAL results
    // results_cleanup_ch = RESULTS_CLEANUP(metal_results_ch, params.config_file, params.output_dir)
}


process DATA_PREP {
    label "process_other"
    input:
        path input_dir
        path config_file
        path output_dir

    output:
        path "${output_dir}/qc_*.tsv"

    script:
        """
        /workspace/scripts/data_prep.py --input_path $input_dir --config_file $config_file --output_path $output_dir        
        """
}

process CREATE_METAL_SCRIPT {
    label "process_other"
    input:
        path config_file
        path output_dir
        path qc_files

    output:
        path "${output_dir}/metal_script.txt"

    script:
        """
        /workspace/scripts/create_metal_script.py --config_file $config_file --output_path $output_dir --qc_files ${qc_files.collect { it.getName() }.join(' ')}
        """
}

process RUN_METAL {
    container 'manninglab/metal:latest'
    containerOptions "--volume ${params.output_dir as String}:${params.output_dir as String}"

    input:
    path metal_script
    path output_dir

    output:
    path "${output_dir}/*.tbl"

    script:
    """
    echo "Resolved path: ${output_dir}/${metal_script}"
    metal "${output_dir}/${metal_script}"
    """
}

process RESULTS_CLEANUP {
    label "process_other"
    input:
    path metal_file
    path config_file
    path output_dir

    output:
    path "${output_dir}/*.tsv"

    script:
    """
    /workspace/scripts/metal_results_cleanup.py --metal_results $metal_file --config_file $config_file --output_path $output_dir
    """
}
