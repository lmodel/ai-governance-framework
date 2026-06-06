#!/usr/bin/env python3
"""Wrapper for linkml gen-sparql that patches one upstream bug.

Bug 13 - SparqlGenerator template iterates schema.classes (root-only) instead
of all_classes() (with imports):

  SparqlGenerator uses uses_schemaloader=False and its Jinja2 template renders
  with schema=self.schema, iterating schema.classes.items() which contains only
  classes defined directly in the root YAML file.

  For a split/multi-module schema like CDM whose root file contains only imports
  and zero direct class definitions, schema.classes is empty, so the template
  produces no # @CHECK markers and split_sparql() returns an empty dict -> no
  .rq files are written.

  Passing --mergeimports on the CLI has no effect because SparqlGenerator sets
  uses_schemaloader=False; the mergeimports flag only applies to the SchemaLoader
  path.

  The cause is subtle: SparqlGenerator.__post_init__ creates a SchemaView and
  calls materialize_schema(), then calls super().__post_init__() which is
  Generator.__post_init__().  For uses_schemaloader=False generators, that
  method unconditionally creates a NEW SchemaView and reassigns both
  self.schemaview and self.schema - discarding the materialized view.  The
  Jinja2 template is then rendered against this fresh, unmerged schema with
  empty schema.classes.

  Fix: after normal construction, call schemaview.merge_imports() to populate
  schema.classes (which is the same object as self.schema.classes), then
  re-run generate_sparql() to re-render the template against the full class set.

See project.justfile gen-sparql-artifact for usage.
"""

import click
from linkml._version import __version__
from linkml.generators.sparqlgen import SparqlGenerator
from linkml.utils.generator import shared_arguments


@shared_arguments(SparqlGenerator)
@click.command(name="sparql")
@click.option("--dir", "-d", help="Directory in which queries will be deposited")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, dir, **kwargs):
    """Generate SPARQL queries for validation (patched: merges imports before rendering)."""
    gen = SparqlGenerator(yamlfile, **kwargs)
    # Bug 13 fix: after Generator.__post_init__ creates a fresh SchemaView,
    # schema.classes is empty for split schemas.  Merge imports to populate it,
    # then re-run generate_sparql() to re-render the Jinja2 template against
    # the complete set of classes.
    gen.schemaview.merge_imports()
    gen.queries = gen.generate_sparql(named_graphs=gen.named_graphs, limit=gen.limit)
    gen.serialize(directory=dir)


if __name__ == "__main__":
    cli()
