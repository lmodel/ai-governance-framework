#!/usr/bin/env python3
"""Wrapper for linkml gen-pandera that patches two upstream bugs.

Bug A - No --mergeimports support (panderagen.py):
  gen-pandera does not expose --mergeimports; its DataframeGenerator base class
  (OOCodeGenerator) calls SchemaView without merging imports, so the generated
  code only reflects the root schema's classes and misses all classes defined in
  imported modules.  There is no CLI flag to work around this.
  Fix: programmatically call schemaview.merge_imports() on the generator's
  SchemaView after construction so that all classes from imported modules are
  visible during code generation.

Bug B - ValueError on cyclic class dependencies (dependency_sorter.py):
  DependencySorter._visit raises ValueError when a cycle is detected in the
  class dependency graph:
      raise ValueError(f"Cyclic dependency detected: {cycle_path}")
  CDM has legitimate circular references between classes (e.g.
  BusinessCenters -> BusinessDayAdjustments -> AdjustableDate -> BusinessCenters).
  A topological sort of a cyclic graph is impossible; the generator should break
  the cycle gracefully and continue rather than failing entirely.
  Fix: return instead of raising when a cycle node is encountered, allowing the
  dependency sort to produce a valid (if imperfect) ordering for all classes.

Bugs raised upstream.

See project.justfile gen-pandera-artifact for usage.
"""

import sys

import click
from linkml.generators.panderagen.dependency_sorter import DependencySorter
from linkml.generators.panderagen.pandera.pandera_dataframe_generator import (
    PanderaDataframeGenerator,
)
from linkml.generators.panderagen.panderagen import DataframeGeneratorCli

# ---------------------------------------------------------------------------
# Bug B fix: patch DependencySorter._visit to skip cycles instead of raising
# ---------------------------------------------------------------------------
_orig_visit = DependencySorter._visit


def _patched_visit(self, node, visited, in_progress, result):
    if node in in_progress:
        return  # cycle edge - skip rather than raise ValueError
    return _orig_visit(self, node, visited, in_progress, result)


DependencySorter._visit = _patched_visit


@click.command()
@click.argument("yamlfile", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    required=False,
    type=click.Path(dir_okay=False, writable=True),
    help="Output file (default: stdout)",
)
def cli(yamlfile: str, output: str | None) -> None:
    """Patched gen-pandera CLI: merges imports and handles cyclic dependencies."""
    # Bug A fix: create the generator and then merge imports into its SchemaView
    gen = PanderaDataframeGenerator(yamlfile)
    gen.schemaview.merge_imports()

    cli_wrapper = DataframeGeneratorCli(generator=gen)
    code = cli_wrapper.serialize()

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(code)
    else:
        print(code)


if __name__ == "__main__":
    cli()
