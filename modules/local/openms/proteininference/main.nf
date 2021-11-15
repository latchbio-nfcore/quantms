// Import generic module functions
include { initOptions; saveFiles; getSoftwareName } from './functions'

params.options = [:]
options        = initOptions(params.options)

process PROTEININFERENCE {
    label 'process_medium'
    publishDir "${params.outdir}",
        mode: params.publish_dir_mode,
        saveAs: { filename -> saveFiles(filename:filename, options:params.options, publish_dir:getSoftwareName(task.process), meta:[:], publish_by_meta:[]) }

    conda (params.enable_conda ? "openms::openms=2.7.0pre" : null)
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container "https://depot.galaxyproject.org/singularity/openms:2.6.0--h4afb90d_0"
    } else {
        container "quay.io/biocontainers/openms:2.6.0--h4afb90d_0"
    }

    input:
    tuple val(meta), path(consus_file)

    output:
    tuple val(meta), path("${consus_file.baseName}_epi.consensusXML"), emit: protein_inference
    path "*.version.txt", emit: version
    path "*.log", emit: log

    script:
    def software = getSoftwareName(task.process)


    // -picked_fdr $params.picked_fdr
    // -picked_decoy_string $params.decoy_string
    // -protein_fdr true \\
    // -Algorithm:score_aggregation_method $params.protein_score \\
    // TODO update to 2.7.0 !!!! consensusXML is not supported

    """
    ProteinInference \\
        -in ${consus_file} \\
        -threads $task.cpus \\
        -debug 100 \\
        -Algorithm:min_peptides_per_protein $params.min_peptides_per_protein \\
        -out ${consus_file.baseName}_epi.consensusXML \\
        > ${consus_file.baseName}_inference.log

    echo \$(ProteinInference 2>&1) > ${software}.version.txt
    """
}