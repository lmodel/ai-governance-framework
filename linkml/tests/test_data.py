"""Data test."""

import os
import glob
import pytest
from pathlib import Path

import ai_governance_framework.datamodel.ai_governance_framework
from linkml_runtime.loaders import yaml_loader

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"
DATA_DIR_FINOS = Path(__file__).parent / "data" / "finos"

VALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_VALID, "*.yaml"))
INVALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_INVALID, "*.yaml"))
FINOS_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_FINOS, "*.yaml"))


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath):
    """Test loading of all valid data files."""
    target_class_name = Path(filepath).stem.split("-")[0]
    tgt_class = getattr(
        ai_governance_framework.datamodel.ai_governance_framework,
        target_class_name,
    )
    obj = yaml_loader.load(filepath, target_class=tgt_class)
    assert obj


@pytest.mark.parametrize("filepath", FINOS_EXAMPLE_FILES)
def test_finos_data_files(filepath):
    """Test loading of all standalone FINOS Container dumps."""
    tgt_class = ai_governance_framework.datamodel.ai_governance_framework.Container
    obj = yaml_loader.load(filepath, target_class=tgt_class)
    assert obj
