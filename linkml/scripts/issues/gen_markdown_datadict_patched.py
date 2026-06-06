#!/usr/bin/env python3
"""Wrapper for linkml gen-markdown-datadict that patches one upstream performance bug.

Bug  - ERDiagramGenerator re-instantiated for every class (markdowndatadictgen.py):
  MarkdownDataDictGen._generate_class_diagram() creates a new ERDiagramGenerator
  (and therefore a new SchemaView) for every class in the schema:

      erd_gen = ERDiagramGenerator(self.schema_location, ...)
      diagram = erd_gen.serialize_classes(erd_classes, ...)

  With CDM's 2500+ classes and 37 imported modules, this causes the full CDM YAML
  to be re-parsed from disk once per class - O(n) schema loads - making the
  generator hang indefinitely.

  ERDiagramGenerator.serialize_classes() is stateless across calls (it uses only
  local variables and read-only queries on self.schemaview), so caching one
  instance per MarkdownDataDictGen run is safe.

  Fix: override _generate_class_diagram to lazily create a single
  ERDiagramGenerator instance stored in self._erd_gen and reuse it for all
  subsequent per-class diagram calls.
"""

import sys

from linkml.generators.erdiagramgen import ERDiagramGenerator
from linkml.generators.markdowndatadictgen import MarkdownDataDictGen
from linkml_runtime.linkml_model import ClassDefinition


class PatchedMarkdownDataDictGen(MarkdownDataDictGen):
    """MarkdownDataDictGen with ERDiagramGenerator caching to avoid O(n) schema loads."""

    def _generate_class_diagram(
        self, cls: ClassDefinition, relationships: dict
    ) -> list:
        """Generate per-class ERD, reusing a single cached ERDiagramGenerator."""
        items = []
        erd_classes = relationships["erd_classes"]
        children = relationships["children"]

        if erd_classes:
            # Cache: only create ERDiagramGenerator once; each serialize_classes
            # call uses only local variables, so reuse is safe.
            if not hasattr(self, "_erd_gen"):
                self._erd_gen = ERDiagramGenerator(
                    self.schema_location, exclude_attributes=True, structural=False
                )
            erd_classes.append(cls.name)
            diagram = self._erd_gen.serialize_classes(
                erd_classes, follow_references=False, max_hops=0
            )
            diagram_name = f"class_{cls.name.lower()}_erd"
            items.append(
                self._diagram_renderer.render(diagram, diagram_name=diagram_name)
            )
        elif children or cls.is_a:
            items.append(self.header(4, "Local class diagram"))
            diagram_name = f"class_{cls.name.lower()}_local"
            items.append(
                self._diagram_renderer.render(
                    str(self.local_class_diagram(cls)), diagram_name=diagram_name
                )
            )

        return items


if __name__ == "__main__":
    # Replace MarkdownDataDictGen in the module globals so that the upstream cli()
    # function (which does `gen = MarkdownDataDictGen(yamlfile, **kwargs)`) uses
    # our patched subclass.  The @shared_arguments decorator on cli() was already
    # evaluated against the original class, but PatchedMarkdownDataDictGen inherits
    # all the same dataclass fields so the options remain compatible.
    import linkml.generators.markdowndatadictgen as _mddict_module

    _mddict_module.MarkdownDataDictGen = PatchedMarkdownDataDictGen
    from linkml.generators.markdowndatadictgen import cli

    cli()
