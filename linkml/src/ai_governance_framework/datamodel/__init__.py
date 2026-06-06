"""Data model package for ai-governance-framework."""

from pathlib import Path
from .ai_governance_framework import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "ai_governance_framework.yaml"
