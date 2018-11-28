from os.path import join, dirname
import sys
sys.path.insert(0, join(dirname(__file__), '../..', 'stats'))
sys.path.insert(0, join(dirname(__file__), '../..', 'stats', 'newstats'))
from logzero import logger as logging
import os
import numpy as np
from pathlib import Path
from nose.tools import assert_raises, nottest

from . import CONFIG_DIR

# # Matplot lib gves a bunch of unwated message during testing
# this does not work!
# import logging
# mpl_logger = logging.getLogger('matplotlib')
# mpl_logger.disabled =True


import pandas as pd

"""
Run all the config files in the test config directory 
Currently just running and making sure there's no uncaught exceptions.
TODO: check that the correct output is generated too

To run these tests, the test data needs to be fechted from bit/dev/lama_stats_test_data
In future we should put this in a web-accessible place
"""
@nottest
def test_organ_vols():
    config = join(CONFIG_DIR, 'organ_vols.yaml')
    run_lama_stats.run(config)

@nottest
def test_all():
    config = join(CONFIG_DIR, 'all_specimens.yaml')
    run_lama_stats.run(config)


@nottest
def test_glcm():
    config = join(CONFIG_DIR, 'test_glcm.yaml')
    run_lama_stats.run(config)

@nottest
def test_from_arbitrary_directory():
    config = join(CONFIG_DIR, 'all_specimens.yaml')
    os.chdir(os.path.expanduser('~'))
    run_lama_stats.run(config)

@nottest
def test_missing_config():
    config = join(CONFIG_DIR, 'all_specimens.flaml')
    assert_raises(Exception, run_lama_stats.run, config)

@nottest
def test_misc():
    config = join(CONFIG_DIR, 'misc_test.yaml')
    run_lama_stats.run(config)


@nottest
def test_incorrect_staging_file():
    pass