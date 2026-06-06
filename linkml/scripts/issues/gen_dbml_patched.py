#!/usr/bin/env python3
"""Wrapper for linkml gen-dbml that patches two upstream bugs.

Bug A - FileNotFoundError on schema imports (schemaloader.py + dbmlgen.py):
  DBMLGenerator.__post_init__ creates a fresh SchemaView(self.schema) after
  Generator.__post_init__ has already loaded the schema via SchemaLoader.
  SchemaLoader.resolve() deliberately strips source_file to its basename
  (schemaloader.py line ~705: source_file = os.path.basename(source_file)).
  When the new SchemaView later calls load_import(), os.path.dirname(basename)
  returns "" so hbopen() resolves import filenames relative to cwd rather than
  the schema directory, raising FileNotFoundError for split/multi-module schemas.
  Fix: restore source_file from schema_location (which SchemaLoader saved before
  stripping) so SchemaView can resolve imports relative to the schema directory.

Bug B - ValueError for classes without an identifier slot (dbmlgen.py):
  DBMLGenerator._generate_relationships() raises ValueError when a slot's range
  class carries no identifier slot.  Most LinkML schemas (including CDM) use
  object-identity rather than explicit @id fields, so this raises for essentially
  every cross-class reference and makes the generator unusable.
  Fix: skip (continue) instead of raising; emit only the relationships that can
  be expressed.

  Bugs raised upstream.

See project.justfile gen-dbml-artifact for usage.
"""

import logging
import os
from dataclasses import dataclass

import click
from linkml.generators.dbmlgen import DBMLGenerator
from linkml.utils.generator import Generator
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView


@dataclass
class PatchedDBMLGenerator(DBMLGenerator):
    """DBMLGenerator subclass that patches import resolution and relationship generation."""

    def __post_init__(self) -> None:
        """Run base init then restore source_file / SchemaView so relative imports resolve."""
        # Run Generator (grandparent) __post_init__ via SchemaLoader: loads the
        # schema, resolves imports, and sets self.base_dir / self.schema_location.
        # NOTE: this also strips self.schema.source_file to its basename.
        Generator.__post_init__(self)
        self.logger = logging.getLogger(__name__)

        # Bug A fix: restore source_file from schema_location so that the new
        # SchemaView can resolve relative imports against the schema directory.
        if self.schema_location and not os.path.dirname(self.schema.source_file):
            self.schema.source_file = self.schema_location

        self.schemaview = SchemaView(self.schema)

    def _generate_relationships(self) -> str:
        """Like DBMLGenerator._generate_relationships but skips classes with no identifier slot.

        Bug B fix: upstream raises ValueError when a referenced class has no
        identifier slot.  We skip those references instead so the rest of the
        schema is still serialised.
        """
        relationships = []
        for class_name, _class_def in self.schemaview.all_classes().items():
            for slot_name in self.schemaview.class_induced_slots(class_name):
                slot = self.schemaview.get_slot(slot_name.name)
                if slot.range not in self.schemaview.all_classes():
                    continue
                identifier_slot_name = next(
                    (
                        sn.name
                        for sn in self.schemaview.class_induced_slots(slot.range)
                        if self.schemaview.get_slot(sn.name).identifier
                    ),
                    None,
                )
                if identifier_slot_name is None:
                    continue  # Bug B fix: skip instead of raise
                relationships.append(
                    f"Ref: {camelcase(class_name)}.{underscore(slot.name)} > "
                    f"{camelcase(slot.range)}.{underscore(identifier_slot_name)}"
                )
        return "\n".join(relationships)


@click.command()
@click.option(
    "--schema",
    "-s",
    required=True,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="Path to the LinkML schema YAML file",
)
@click.option(
    "--output",
    "-o",
    required=False,
    type=click.Path(dir_okay=False, writable=True),
    help="Output file (default: stdout)",
)
def cli(schema: str, output: str | None) -> None:
    """Patched gen-dbml CLI: fixes import resolution and relationship generation."""
    generator = PatchedDBMLGenerator(schema)
    dbml_output = generator.serialize()
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(dbml_output)
    else:
        print(dbml_output)


if __name__ == "__main__":
    cli()
