#!/usr/bin/env python3
"""Wrapper for linkml gen-rust that patches an upstream type-annotation bug.

Bug - RustStructOrSubtypeEnum.type_designators annotated as dict[str, str]
(template.py) but populated as dict[str, list[str]] (rustgen.py) and indexed
as a list by the Jinja template (struct_or_subtype_enum.rs.jinja uses
``tds[0]`` and ``tds[1:]``).

Under Pydantic v2 strict validation this raises::

    ValidationError: type_designators.<Class>
      Input should be a valid string [type=string_type, input_value=[...], ...]

The crash fires whenever the schema contains a class hierarchy that uses
``designates_type: true`` on a slot (e.g. ai-atlas-nexus Taxonomy subclasses
RiskTaxonomy, RiskControlGroupTaxonomy, CapabilityTaxonomy).

Fix: rebuild the Pydantic model with the field annotation corrected to
``dict[str, list[str]]`` (which matches both the producer code and the Jinja
template), then re-invoke the upstream click CLI unchanged.

Bug raised upstream.

See project.justfile gen-rust-artifact for usage.
"""

import sys

from linkml.generators.rustgen import template as _rust_template
from linkml.generators.rustgen.cli import cli as _gen_rust_cli

# ---------------------------------------------------------------------------
# Patch RustStructOrSubtypeEnum.type_designators annotation to dict[str, list[str]]
# ---------------------------------------------------------------------------
_field = _rust_template.RustStructOrSubtypeEnum.model_fields["type_designators"]
_field.annotation = dict[str, list[str]]
_rust_template.RustStructOrSubtypeEnum.model_rebuild(force=True)


if __name__ == "__main__":
    # Delegate to the upstream click CLI (same arguments).
    sys.exit(_gen_rust_cli())
