from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], root_folder: typing.Optional[str], database: LatchFile, add_decoys: typing.Optional[bool], openms_peakpicking: typing.Optional[bool], peakpicking_inmemory: typing.Optional[bool], peakpicking_ms_levels: typing.Optional[str], convert_dotd: typing.Optional[bool], min_pr_mz: typing.Optional[float], max_pr_mz: typing.Optional[float], min_fr_mz: typing.Optional[float], max_fr_mz: typing.Optional[float], enable_mod_localization: typing.Optional[bool], description_correct_features: typing.Optional[int], consensusid_considered_top_hits: typing.Optional[int], min_consensus_support: typing.Optional[float], select_activation: typing.Optional[str], labelling_type: typing.Optional[str], best_charge_and_fraction: typing.Optional[bool], mass_recalibration: typing.Optional[bool], diann_speclib: typing.Optional[str], skip_post_msstats: typing.Optional[bool], ref_condition: typing.Optional[str], contrasts: typing.Optional[str], enable_pmultiqc: typing.Optional[bool], pmultiqc_idxml_skip: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], local_input_type: typing.Optional[str], acquisition_method: typing.Optional[str], decoy_string: typing.Optional[str], decoy_string_position: typing.Optional[str], decoy_method: typing.Optional[str], shuffle_max_attempts: typing.Optional[int], shuffle_sequence_identity_threshold: typing.Optional[float], reindex_mzml: typing.Optional[bool], search_engines: typing.Optional[str], sage_processes: typing.Optional[int], enzyme: typing.Optional[str], num_enzyme_termini: typing.Optional[str], allowed_missed_cleavages: typing.Optional[int], precursor_mass_tolerance: typing.Optional[int], precursor_mass_tolerance_unit: typing.Optional[str], fragment_mass_tolerance: typing.Optional[float], fragment_mass_tolerance_unit: typing.Optional[str], fixed_mods: typing.Optional[str], variable_mods: typing.Optional[str], isotope_error_range: typing.Optional[str], instrument: typing.Optional[str], protocol: typing.Optional[str], min_precursor_charge: typing.Optional[int], max_precursor_charge: typing.Optional[int], min_peptide_length: typing.Optional[int], max_peptide_length: typing.Optional[int], num_hits: typing.Optional[int], max_mods: typing.Optional[int], mod_localization: typing.Optional[str], unmatched_action: typing.Optional[str], IL_equivalent: typing.Optional[bool], posterior_probabilities: typing.Optional[str], run_fdr_cutoff: typing.Optional[float], FDR_level: typing.Optional[str], train_FDR: typing.Optional[float], test_FDR: typing.Optional[float], subset_max_train: typing.Optional[int], outlier_handling: typing.Optional[str], consensusid_algorithm: typing.Optional[str], reporter_mass_shift: typing.Optional[float], min_precursor_intensity: typing.Optional[float], min_precursor_purity: typing.Optional[float], min_reporter_intensity: typing.Optional[float], precursor_isotope_deviation: typing.Optional[float], isotope_correction: typing.Optional[bool], iso_normalization: typing.Optional[bool], reference_channel: typing.Optional[int], protein_inference_method: typing.Optional[str], protein_score: typing.Optional[str], use_shared_peptides: typing.Optional[bool], min_peptides_per_protein: typing.Optional[int], top_PSMs: typing.Optional[int], protein_level_fdr_cutoff: typing.Optional[float], picked_fdr: typing.Optional[bool], psm_level_fdr_cutoff: typing.Optional[float], top: typing.Optional[int], average: typing.Optional[str], ratios: typing.Optional[bool], normalize: typing.Optional[bool], fix_peptides: typing.Optional[bool], include_all: typing.Optional[bool], protein_quant: typing.Optional[str], export_mztab: typing.Optional[bool], quantification_method: typing.Optional[str], targeted_only: typing.Optional[bool], feature_with_id_min_score: typing.Optional[float], feature_without_id_min_score: typing.Optional[float], lfq_intensity_threshold: typing.Optional[float], alignment_order: typing.Optional[str], quantify_decoys: typing.Optional[bool], mass_acc_automatic: typing.Optional[bool], scan_window_automatic: typing.Optional[bool], scan_window: typing.Optional[int], min_corr: typing.Optional[float], corr_diff: typing.Optional[float], time_corr_only: typing.Optional[bool], pg_level: typing.Optional[float], species_genes: typing.Optional[bool], diann_normalize: typing.Optional[bool], msstats_threshold: typing.Optional[float], add_triqler_output: typing.Optional[bool], msstatslfq_feature_subset_protein: typing.Optional[str], msstatslfq_quant_summary_method: typing.Optional[str], msstats_remove_one_feat_prot: typing.Optional[bool], msstatslfq_removeFewMeasurements: typing.Optional[bool], msstatsiso_useunique_peptide: typing.Optional[bool], msstatsiso_rmpsm_withfewmea_withinrun: typing.Optional[bool], msstatsiso_summaryformultiple_psm: typing.Optional[str], msstatsiso_summarization_method: typing.Optional[str], msstatsiso_global_norm: typing.Optional[bool], msstatsiso_remove_norm_channel: typing.Optional[bool], msstatsiso_reference_normalization: typing.Optional[bool], msstats_plot_profile_qc: typing.Optional[bool], skip_table_plots: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('root_folder', root_folder),
                *get_flag('local_input_type', local_input_type),
                *get_flag('acquisition_method', acquisition_method),
                *get_flag('database', database),
                *get_flag('add_decoys', add_decoys),
                *get_flag('decoy_string', decoy_string),
                *get_flag('decoy_string_position', decoy_string_position),
                *get_flag('decoy_method', decoy_method),
                *get_flag('shuffle_max_attempts', shuffle_max_attempts),
                *get_flag('shuffle_sequence_identity_threshold', shuffle_sequence_identity_threshold),
                *get_flag('openms_peakpicking', openms_peakpicking),
                *get_flag('peakpicking_inmemory', peakpicking_inmemory),
                *get_flag('peakpicking_ms_levels', peakpicking_ms_levels),
                *get_flag('convert_dotd', convert_dotd),
                *get_flag('reindex_mzml', reindex_mzml),
                *get_flag('search_engines', search_engines),
                *get_flag('sage_processes', sage_processes),
                *get_flag('enzyme', enzyme),
                *get_flag('num_enzyme_termini', num_enzyme_termini),
                *get_flag('allowed_missed_cleavages', allowed_missed_cleavages),
                *get_flag('precursor_mass_tolerance', precursor_mass_tolerance),
                *get_flag('precursor_mass_tolerance_unit', precursor_mass_tolerance_unit),
                *get_flag('fragment_mass_tolerance', fragment_mass_tolerance),
                *get_flag('fragment_mass_tolerance_unit', fragment_mass_tolerance_unit),
                *get_flag('fixed_mods', fixed_mods),
                *get_flag('variable_mods', variable_mods),
                *get_flag('isotope_error_range', isotope_error_range),
                *get_flag('instrument', instrument),
                *get_flag('protocol', protocol),
                *get_flag('min_precursor_charge', min_precursor_charge),
                *get_flag('max_precursor_charge', max_precursor_charge),
                *get_flag('min_peptide_length', min_peptide_length),
                *get_flag('max_peptide_length', max_peptide_length),
                *get_flag('num_hits', num_hits),
                *get_flag('max_mods', max_mods),
                *get_flag('min_pr_mz', min_pr_mz),
                *get_flag('max_pr_mz', max_pr_mz),
                *get_flag('min_fr_mz', min_fr_mz),
                *get_flag('max_fr_mz', max_fr_mz),
                *get_flag('enable_mod_localization', enable_mod_localization),
                *get_flag('mod_localization', mod_localization),
                *get_flag('unmatched_action', unmatched_action),
                *get_flag('IL_equivalent', IL_equivalent),
                *get_flag('posterior_probabilities', posterior_probabilities),
                *get_flag('run_fdr_cutoff', run_fdr_cutoff),
                *get_flag('FDR_level', FDR_level),
                *get_flag('train_FDR', train_FDR),
                *get_flag('test_FDR', test_FDR),
                *get_flag('subset_max_train', subset_max_train),
                *get_flag('description_correct_features', description_correct_features),
                *get_flag('outlier_handling', outlier_handling),
                *get_flag('consensusid_algorithm', consensusid_algorithm),
                *get_flag('consensusid_considered_top_hits', consensusid_considered_top_hits),
                *get_flag('min_consensus_support', min_consensus_support),
                *get_flag('select_activation', select_activation),
                *get_flag('reporter_mass_shift', reporter_mass_shift),
                *get_flag('min_precursor_intensity', min_precursor_intensity),
                *get_flag('min_precursor_purity', min_precursor_purity),
                *get_flag('min_reporter_intensity', min_reporter_intensity),
                *get_flag('precursor_isotope_deviation', precursor_isotope_deviation),
                *get_flag('isotope_correction', isotope_correction),
                *get_flag('iso_normalization', iso_normalization),
                *get_flag('reference_channel', reference_channel),
                *get_flag('protein_inference_method', protein_inference_method),
                *get_flag('protein_score', protein_score),
                *get_flag('use_shared_peptides', use_shared_peptides),
                *get_flag('min_peptides_per_protein', min_peptides_per_protein),
                *get_flag('top_PSMs', top_PSMs),
                *get_flag('protein_level_fdr_cutoff', protein_level_fdr_cutoff),
                *get_flag('picked_fdr', picked_fdr),
                *get_flag('psm_level_fdr_cutoff', psm_level_fdr_cutoff),
                *get_flag('labelling_type', labelling_type),
                *get_flag('top', top),
                *get_flag('average', average),
                *get_flag('best_charge_and_fraction', best_charge_and_fraction),
                *get_flag('ratios', ratios),
                *get_flag('normalize', normalize),
                *get_flag('fix_peptides', fix_peptides),
                *get_flag('include_all', include_all),
                *get_flag('protein_quant', protein_quant),
                *get_flag('export_mztab', export_mztab),
                *get_flag('quantification_method', quantification_method),
                *get_flag('mass_recalibration', mass_recalibration),
                *get_flag('targeted_only', targeted_only),
                *get_flag('feature_with_id_min_score', feature_with_id_min_score),
                *get_flag('feature_without_id_min_score', feature_without_id_min_score),
                *get_flag('lfq_intensity_threshold', lfq_intensity_threshold),
                *get_flag('alignment_order', alignment_order),
                *get_flag('quantify_decoys', quantify_decoys),
                *get_flag('mass_acc_automatic', mass_acc_automatic),
                *get_flag('scan_window_automatic', scan_window_automatic),
                *get_flag('scan_window', scan_window),
                *get_flag('min_corr', min_corr),
                *get_flag('corr_diff', corr_diff),
                *get_flag('time_corr_only', time_corr_only),
                *get_flag('pg_level', pg_level),
                *get_flag('species_genes', species_genes),
                *get_flag('diann_speclib', diann_speclib),
                *get_flag('diann_normalize', diann_normalize),
                *get_flag('skip_post_msstats', skip_post_msstats),
                *get_flag('ref_condition', ref_condition),
                *get_flag('contrasts', contrasts),
                *get_flag('msstats_threshold', msstats_threshold),
                *get_flag('add_triqler_output', add_triqler_output),
                *get_flag('msstatslfq_feature_subset_protein', msstatslfq_feature_subset_protein),
                *get_flag('msstatslfq_quant_summary_method', msstatslfq_quant_summary_method),
                *get_flag('msstats_remove_one_feat_prot', msstats_remove_one_feat_prot),
                *get_flag('msstatslfq_removeFewMeasurements', msstatslfq_removeFewMeasurements),
                *get_flag('msstatsiso_useunique_peptide', msstatsiso_useunique_peptide),
                *get_flag('msstatsiso_rmpsm_withfewmea_withinrun', msstatsiso_rmpsm_withfewmea_withinrun),
                *get_flag('msstatsiso_summaryformultiple_psm', msstatsiso_summaryformultiple_psm),
                *get_flag('msstatsiso_summarization_method', msstatsiso_summarization_method),
                *get_flag('msstatsiso_global_norm', msstatsiso_global_norm),
                *get_flag('msstatsiso_remove_norm_channel', msstatsiso_remove_norm_channel),
                *get_flag('msstatsiso_reference_normalization', msstatsiso_reference_normalization),
                *get_flag('msstats_plot_profile_qc', msstats_plot_profile_qc),
                *get_flag('enable_pmultiqc', enable_pmultiqc),
                *get_flag('pmultiqc_idxml_skip', pmultiqc_idxml_skip),
                *get_flag('skip_table_plots', skip_table_plots),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_quantms", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_quantms(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], root_folder: typing.Optional[str], database: LatchFile, add_decoys: typing.Optional[bool], openms_peakpicking: typing.Optional[bool], peakpicking_inmemory: typing.Optional[bool], peakpicking_ms_levels: typing.Optional[str], convert_dotd: typing.Optional[bool], min_pr_mz: typing.Optional[float], max_pr_mz: typing.Optional[float], min_fr_mz: typing.Optional[float], max_fr_mz: typing.Optional[float], enable_mod_localization: typing.Optional[bool], description_correct_features: typing.Optional[int], consensusid_considered_top_hits: typing.Optional[int], min_consensus_support: typing.Optional[float], select_activation: typing.Optional[str], labelling_type: typing.Optional[str], best_charge_and_fraction: typing.Optional[bool], mass_recalibration: typing.Optional[bool], diann_speclib: typing.Optional[str], skip_post_msstats: typing.Optional[bool], ref_condition: typing.Optional[str], contrasts: typing.Optional[str], enable_pmultiqc: typing.Optional[bool], pmultiqc_idxml_skip: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], local_input_type: typing.Optional[str] = 'mzML', acquisition_method: typing.Optional[str] = 'dda', decoy_string: typing.Optional[str] = 'DECOY_', decoy_string_position: typing.Optional[str] = 'prefix', decoy_method: typing.Optional[str] = 'reverse', shuffle_max_attempts: typing.Optional[int] = 30, shuffle_sequence_identity_threshold: typing.Optional[float] = 0.5, reindex_mzml: typing.Optional[bool] = True, search_engines: typing.Optional[str] = 'comet', sage_processes: typing.Optional[int] = 1, enzyme: typing.Optional[str] = 'Trypsin', num_enzyme_termini: typing.Optional[str] = 'fully', allowed_missed_cleavages: typing.Optional[int] = 2, precursor_mass_tolerance: typing.Optional[int] = 5, precursor_mass_tolerance_unit: typing.Optional[str] = 'ppm', fragment_mass_tolerance: typing.Optional[float] = 0.03, fragment_mass_tolerance_unit: typing.Optional[str] = 'Da', fixed_mods: typing.Optional[str] = 'Carbamidomethyl (C)', variable_mods: typing.Optional[str] = 'Oxidation (M)', isotope_error_range: typing.Optional[str] = '0,1', instrument: typing.Optional[str] = 'high_res', protocol: typing.Optional[str] = 'automatic', min_precursor_charge: typing.Optional[int] = 2, max_precursor_charge: typing.Optional[int] = 4, min_peptide_length: typing.Optional[int] = 6, max_peptide_length: typing.Optional[int] = 40, num_hits: typing.Optional[int] = 1, max_mods: typing.Optional[int] = 3, mod_localization: typing.Optional[str] = 'Phospho (S),Phospho (T),Phospho (Y)', unmatched_action: typing.Optional[str] = 'warn', IL_equivalent: typing.Optional[bool] = True, posterior_probabilities: typing.Optional[str] = 'percolator', run_fdr_cutoff: typing.Optional[float] = 0.01, FDR_level: typing.Optional[str] = 'peptide-level-fdrs', train_FDR: typing.Optional[float] = 0.05, test_FDR: typing.Optional[float] = 0.05, subset_max_train: typing.Optional[int] = 300000, outlier_handling: typing.Optional[str] = 'none', consensusid_algorithm: typing.Optional[str] = 'best', reporter_mass_shift: typing.Optional[float] = 0.002, min_precursor_intensity: typing.Optional[float] = 1.0, min_precursor_purity: typing.Optional[float] = 0.0, min_reporter_intensity: typing.Optional[float] = 0.0, precursor_isotope_deviation: typing.Optional[float] = 10.0, isotope_correction: typing.Optional[bool] = True, iso_normalization: typing.Optional[bool] = False, reference_channel: typing.Optional[int] = 126, protein_inference_method: typing.Optional[str] = 'aggregation', protein_score: typing.Optional[str] = 'best', use_shared_peptides: typing.Optional[bool] = True, min_peptides_per_protein: typing.Optional[int] = 1, top_PSMs: typing.Optional[int] = 1, protein_level_fdr_cutoff: typing.Optional[float] = 0.01, picked_fdr: typing.Optional[bool] = True, psm_level_fdr_cutoff: typing.Optional[float] = 0.01, top: typing.Optional[int] = 3, average: typing.Optional[str] = 'median', ratios: typing.Optional[bool] = 'false', normalize: typing.Optional[bool] = 'false', fix_peptides: typing.Optional[bool] = 'false', include_all: typing.Optional[bool] = True, protein_quant: typing.Optional[str] = 'unique_peptides', export_mztab: typing.Optional[bool] = True, quantification_method: typing.Optional[str] = 'feature_intensity', targeted_only: typing.Optional[bool] = True, feature_with_id_min_score: typing.Optional[float] = 0.0, feature_without_id_min_score: typing.Optional[float] = 0.0, lfq_intensity_threshold: typing.Optional[float] = 10000, alignment_order: typing.Optional[str] = 'star', quantify_decoys: typing.Optional[bool] = False, mass_acc_automatic: typing.Optional[bool] = True, scan_window_automatic: typing.Optional[bool] = True, scan_window: typing.Optional[int] = 7, min_corr: typing.Optional[float] = 2.0, corr_diff: typing.Optional[float] = 1.0, time_corr_only: typing.Optional[bool] = True, pg_level: typing.Optional[float] = 2, species_genes: typing.Optional[bool] = False, diann_normalize: typing.Optional[bool] = True, msstats_threshold: typing.Optional[float] = 0.05, add_triqler_output: typing.Optional[bool] = False, msstatslfq_feature_subset_protein: typing.Optional[str] = 'top3', msstatslfq_quant_summary_method: typing.Optional[str] = 'TMP', msstats_remove_one_feat_prot: typing.Optional[bool] = True, msstatslfq_removeFewMeasurements: typing.Optional[bool] = True, msstatsiso_useunique_peptide: typing.Optional[bool] = True, msstatsiso_rmpsm_withfewmea_withinrun: typing.Optional[bool] = True, msstatsiso_summaryformultiple_psm: typing.Optional[str] = 'sum', msstatsiso_summarization_method: typing.Optional[str] = 'msstats', msstatsiso_global_norm: typing.Optional[bool] = True, msstatsiso_remove_norm_channel: typing.Optional[bool] = True, msstatsiso_reference_normalization: typing.Optional[bool] = True, msstats_plot_profile_qc: typing.Optional[bool] = False, skip_table_plots: typing.Optional[bool] = False) -> None:
    """
    nf-core/quantms

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, root_folder=root_folder, local_input_type=local_input_type, acquisition_method=acquisition_method, database=database, add_decoys=add_decoys, decoy_string=decoy_string, decoy_string_position=decoy_string_position, decoy_method=decoy_method, shuffle_max_attempts=shuffle_max_attempts, shuffle_sequence_identity_threshold=shuffle_sequence_identity_threshold, openms_peakpicking=openms_peakpicking, peakpicking_inmemory=peakpicking_inmemory, peakpicking_ms_levels=peakpicking_ms_levels, convert_dotd=convert_dotd, reindex_mzml=reindex_mzml, search_engines=search_engines, sage_processes=sage_processes, enzyme=enzyme, num_enzyme_termini=num_enzyme_termini, allowed_missed_cleavages=allowed_missed_cleavages, precursor_mass_tolerance=precursor_mass_tolerance, precursor_mass_tolerance_unit=precursor_mass_tolerance_unit, fragment_mass_tolerance=fragment_mass_tolerance, fragment_mass_tolerance_unit=fragment_mass_tolerance_unit, fixed_mods=fixed_mods, variable_mods=variable_mods, isotope_error_range=isotope_error_range, instrument=instrument, protocol=protocol, min_precursor_charge=min_precursor_charge, max_precursor_charge=max_precursor_charge, min_peptide_length=min_peptide_length, max_peptide_length=max_peptide_length, num_hits=num_hits, max_mods=max_mods, min_pr_mz=min_pr_mz, max_pr_mz=max_pr_mz, min_fr_mz=min_fr_mz, max_fr_mz=max_fr_mz, enable_mod_localization=enable_mod_localization, mod_localization=mod_localization, unmatched_action=unmatched_action, IL_equivalent=IL_equivalent, posterior_probabilities=posterior_probabilities, run_fdr_cutoff=run_fdr_cutoff, FDR_level=FDR_level, train_FDR=train_FDR, test_FDR=test_FDR, subset_max_train=subset_max_train, description_correct_features=description_correct_features, outlier_handling=outlier_handling, consensusid_algorithm=consensusid_algorithm, consensusid_considered_top_hits=consensusid_considered_top_hits, min_consensus_support=min_consensus_support, select_activation=select_activation, reporter_mass_shift=reporter_mass_shift, min_precursor_intensity=min_precursor_intensity, min_precursor_purity=min_precursor_purity, min_reporter_intensity=min_reporter_intensity, precursor_isotope_deviation=precursor_isotope_deviation, isotope_correction=isotope_correction, iso_normalization=iso_normalization, reference_channel=reference_channel, protein_inference_method=protein_inference_method, protein_score=protein_score, use_shared_peptides=use_shared_peptides, min_peptides_per_protein=min_peptides_per_protein, top_PSMs=top_PSMs, protein_level_fdr_cutoff=protein_level_fdr_cutoff, picked_fdr=picked_fdr, psm_level_fdr_cutoff=psm_level_fdr_cutoff, labelling_type=labelling_type, top=top, average=average, best_charge_and_fraction=best_charge_and_fraction, ratios=ratios, normalize=normalize, fix_peptides=fix_peptides, include_all=include_all, protein_quant=protein_quant, export_mztab=export_mztab, quantification_method=quantification_method, mass_recalibration=mass_recalibration, targeted_only=targeted_only, feature_with_id_min_score=feature_with_id_min_score, feature_without_id_min_score=feature_without_id_min_score, lfq_intensity_threshold=lfq_intensity_threshold, alignment_order=alignment_order, quantify_decoys=quantify_decoys, mass_acc_automatic=mass_acc_automatic, scan_window_automatic=scan_window_automatic, scan_window=scan_window, min_corr=min_corr, corr_diff=corr_diff, time_corr_only=time_corr_only, pg_level=pg_level, species_genes=species_genes, diann_speclib=diann_speclib, diann_normalize=diann_normalize, skip_post_msstats=skip_post_msstats, ref_condition=ref_condition, contrasts=contrasts, msstats_threshold=msstats_threshold, add_triqler_output=add_triqler_output, msstatslfq_feature_subset_protein=msstatslfq_feature_subset_protein, msstatslfq_quant_summary_method=msstatslfq_quant_summary_method, msstats_remove_one_feat_prot=msstats_remove_one_feat_prot, msstatslfq_removeFewMeasurements=msstatslfq_removeFewMeasurements, msstatsiso_useunique_peptide=msstatsiso_useunique_peptide, msstatsiso_rmpsm_withfewmea_withinrun=msstatsiso_rmpsm_withfewmea_withinrun, msstatsiso_summaryformultiple_psm=msstatsiso_summaryformultiple_psm, msstatsiso_summarization_method=msstatsiso_summarization_method, msstatsiso_global_norm=msstatsiso_global_norm, msstatsiso_remove_norm_channel=msstatsiso_remove_norm_channel, msstatsiso_reference_normalization=msstatsiso_reference_normalization, msstats_plot_profile_qc=msstats_plot_profile_qc, enable_pmultiqc=enable_pmultiqc, pmultiqc_idxml_skip=pmultiqc_idxml_skip, skip_table_plots=skip_table_plots, multiqc_methods_description=multiqc_methods_description)

