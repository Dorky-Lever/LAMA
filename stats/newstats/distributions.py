#!/usr/bin/env python3

"""
06/08/18

* Determine a null distributiom in order to set an appropriate p-value threshold
* Try first on organ volume results

Steps
=====

For each mutant line
    get n number of homs
    relabel n wildtypes as mutants
    run organ volume LM   organ_volume ~ genotype + 'crown-rump length'



"""

from os.path import expanduser
from typing import Union, Tuple
import pandas as pd
import random
import numpy as np
from logzero import logger as logging
from pathlib import Path
import sys
sys.path.insert(0, Path(__file__).absolute() / '..')
from linear_model import lm_r



home = expanduser('~')


def null(data: pd.DataFrame,
                       num_perm: int,
                       plot_dir: Union[None, Path] = None,
                       specimen_level: bool = False,
                       boxcox: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate null distributions for line and specimen-level data

    Parameters
    ----------
    data
        columns volume(index), crl, line, organ_volumes(colum per organ)
    num_perm
    plot_dir
    specimen_level
    boxcox

    Returns
    -------

    Notes
    -----
    TODO: Remove crl and using 'staging instead'

    """
    random.seed(999)

    label_names = data.drop(['crl', 'line'], axis='columns').columns

    # Store p-value results. One tuple(len=num labels) per iteration
    line_p = []
    spec_p = []
    # keep a list of sets of synthetic mutants, only run a set once
    synthetics_sets_done = []

    # Create synthetic specimens by iteratively relabelling each basline as synthetic mutant
    baselines = data[data['line'] == 'baseline']

    # Get the line specimen n numbers. Keep the first column
    line_specimen_counts = data[data['line'] != 'baseline'].groupby('line').count()
    line_specimen_counts = list(line_specimen_counts.iloc[:, 0])

    for index, _ in baselines.iterrows():

        baselines['genotype'] = 'wt'
        baselines.ix[[index], 'genotype'] = 'synth_hom'

        p = lm_r(baselines, plot_dir, boxcox)
        spec_p.append(p)

    # Create synthetic lines by iteratively relabelling n baselines as synthetic mutants
    # n is determined by sampling the number of homs in each mutant line
    perms_done = 0
    for _ in range(num_perm):

        for n in line_specimen_counts: # muant lines
            perms_done += 1
            print(f'permutation: {perms_done}')

            # Set all to wt genotype
            baselines['genotype'] = 'wt'

            # label n number of baselines as mutants
            synthetics_mut_indices = random.sample(range(0, len(baselines)), n)

            if synthetics_mut_indices in synthetics_sets_done:
                continue

            synthetics_sets_done.append(synthetics_mut_indices)

            baselines.ix[synthetics_mut_indices, 'genotype'] = 'synth_hom'  # Why does iloc not work here?

            p = lm_r(baselines, plot_dir, boxcox) # returns p_values for all organs, 1 iteration
            line_p.append(p)

    line_df = pd.DataFrame.from_records(line_p, columns=label_names)
    spec_df = pd.DataFrame.from_records(spec_p, columns=label_names)

    # Get rid of the x in the headers
    strip_x(line_df)
    strip_x(spec_df)

    return line_df, spec_df


def strip_x(df):
    df.columns = [x.strip('x') for x in df.columns]


def alternative(data: pd.DataFrame,
                              plot_dir: Union[None, Path] = None,
                              boxcox: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate alterntive (mutnat) distributions for line and pecimen-level data

    Parameters
    ----------
    data
    plot_dir
    boxcox

    Returns
    -------
    alternative distribution dataframes with either line or specimen as index
    """

    # Group by line and sequntaily run
    line_groupby = data.groupby('line')

    label_names = data.drop(['crl', 'line'], axis='columns').columns

    baseline = data[data['line'] == 'baseline']

    # Set the wt dataframes genotypes back to 'wt'
    baseline['genotype'] = 'wt'

    alt_line_pvalues = []
    alt_spec_pvalues = []

    for line_id, line_df in line_groupby:

        if line_id == 'baseline':
            continue

        line_df['genotype'] = 'hom'
        line_df.drop(['line'], axis=1) #?

        df_wt_mut = pd.concat([baseline, line_df])
        p = lm_r(df_wt_mut, plot_dir, boxcox)  # returns p_values for all organs, 1 iteration
        res = [line_id] + list(p)
        alt_line_pvalues.append(res)

    for specimen, row in data[data['line'] != 'baselines'].iterrows():
        df_wt_mut = pd.concat([baseline, row])
        p = lm_r(df_wt_mut, plot_dir, boxcox)  # returns p_values for all organs, 1 iteration
        res = specimen + list(p)
        alt_spec_pvalues.append(res)

    alt_line_df = pd.DataFrame.from_records(alt_line_pvalues, columns=label_names)
    alt_spec_df = pd.DataFrame.from_records(alt_spec_pvalues, columns=label_names)

    return alt_line_df, alt_spec_df


