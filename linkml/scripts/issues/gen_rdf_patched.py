#!/usr/bin/env python3
"""Wrapper for linkml gen-rdf that strips unresolvable JSON-LD @context refs.

CDM's schema is split across ~35 modules.  gen-jsonld embeds a relative context
file reference per module (./cdm_base.context.jsonld, etc.) in the generated
JSON-LD @context array.  When gen-rdf feeds that JSON-LD to rdflib for
conversion to Turtle, rdflib resolves those relative refs against the schema's
@base URI (https://w3id.org/lmodel/common_domain_model/), which returns HTTP
404 because the files are not published at that URL.

The merged @context already contains all prefix bindings from every module, so
the relative module refs are redundant and can be safely dropped.

The same strip is applied to the remote https://w3id.org/linkml/types.context.jsonld
entry to remove an unnecessary network dependency (the meta.context.jsonld
vendored locally already covers the linkml type definitions).

See ISSUE.md § Bug 8 for full analysis and minimal reproducer.
See project.justfile gen-rdf-artifact for usage.
"""

import json
import sys
import urllib.parse as urlparse
from copy import deepcopy
from dataclasses import dataclass

import click
from linkml._version import __version__
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model import SchemaDefinition
from rdflib import Graph

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE


def _strip_unresolvable_context_refs(jsonld_str: str) -> str:
    """Remove relative and remote-only context refs from the @context array.

    Keeps:
    - inline dicts (prefix/vocab maps, @base)
    - absolute file:// or other non-http refs
    Removes:
    - ./relative.context.jsonld  (module context files not published on web)
    - https://w3id.org/linkml/types.context.jsonld  (covered by vendored meta)
    """
    d = json.loads(jsonld_str)
    ctx = d.get("@context")
    if not isinstance(ctx, list):
        return jsonld_str

    def _keep(item: object) -> bool:
        if not isinstance(item, str):
            return True  # keep inline dicts
        if item.startswith("./"):
            return False  # relative module context ref - not on web
        if "w3id.org/linkml/types" in item:
            return False  # covered by vendored meta.context.jsonld
        return True

    d["@context"] = [item for item in ctx if _keep(item)]
    return json.dumps(d)


@dataclass
class PatchedRDFGenerator(RDFGenerator):
    """RDFGenerator subclass that patches the JSON-LD before rdflib parsing."""

    def end_schema(
        self, output: str | None = None, context: str | None = None, **_
    ) -> str:
        """Emit the schema as RDF after patching the intermediate JSON-LD."""
        gen = JSONLDGenerator(
            self.original_schema,
            format=JSONLDGenerator.valid_formats[0],
            metadata=self.emit_metadata,
            importmap=self.importmap,
            metamodel_context=LOCAL_METAMODEL_LDCONTEXT_FILE,
        )
        for e in gen.schema.enums.values():
            for pv in e.permissible_values.values():
                pv.text = urlparse.quote(pv.text)

        jsonld_str = gen.serialize(context=context)
        jsonld_str = _strip_unresolvable_context_refs(jsonld_str)

        graph = Graph()
        graph.parse(
            data=jsonld_str,
            format="json-ld",
            base=str(self.namespaces._base),
            prefix=True,
        )
        if output:
            fmt = "turtle" if self.format == "ttl" else self.format
            try:
                out = graph.serialize(format=fmt)
            except UnicodeDecodeError:
                graph.serialize(destination=output, format=fmt)
                return ""
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(out)
            return out
        return self._data(graph)


@shared_arguments(PatchedRDFGenerator)
@click.command(name="rdf")
@click.option("-o", "--output", help="Output file name")
@click.option(
    "--context",
    default=[LOCAL_METAMODEL_LDCONTEXT_FILE],
    show_default=True,
    multiple=True,
    help="JSONLD context file (default: vendored meta.context.jsonld)",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """gen-rdf wrapper: strips unresolvable relative JSON-LD context refs before rdflib parsing.

    See scripts/gen_rdf_patched.py for full explanation.
    """
    result = PatchedRDFGenerator(yamlfile, **kwargs).serialize(**kwargs)
    if not kwargs.get("output"):
        print(result)


if __name__ == "__main__":
    cli()
