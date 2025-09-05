"""Converter for GKS <-> HL7 v2"""

import logging
from typing import Any

from ga4gh.va_spec.base.core import Statement
from ga4gh.vrs.models import Allele, Expression, SequenceLocation

_logger = logging.getLogger(__name__)

# TODO: make this a pydantic class to enforce required vs optional fields and types for the values
HL7V2 = {
    "VARIANT_NAME": "504",
    "DISCRETE_VARIANT": "505",
    "CHROMOSOME": "510",
    "ALLELE_START": "511.1",
    "ALLELE_END": "511.2",
    "DNA_REGION": "513",
    "GENE_STUDIED": "514",
    "TRANSCRIPT_REFERENCE_SEQUENCE_ID": "516",
    "DNA_CHANGE": "518",
    "AMINO_ACID_CHANGE": "520",
    "MOLECULAR_CONSEQUENCE": "521",
    "PROTEIN_REFERENCE_SEQUENCE": "522",
    "GENOMIC_REFERENCE_SEQUENCE_ID": "524",
    # "AMPLIFICATION": "525", TODO: I don't think we can go from GKS to this yet / no guarantee this is in extensions
    "REFERENCE_ALLELE": "526",
    "OBSERVED_ALLELE": "527",
    "GENOMIC_DNA_CHANGE": "528",
    "CYTOGENETIC_LOCATION": "532",
    "PENETRANCE": "534",
    "GENETIC_VARIANT_SOURCE": "535",
    "ALLELE_LENGTH": "545",
    "STRUCTURAL_INNER_START": "546.1",
    "STRUCTURAL_INNER_END": "546.2",
    "STRUCTURAL_OUTER_START": "547.1",
    "STRUCTURAL_OUTER_END": "547.2",
    "COPY_NUMBER": "550",
    # "FUSED_GENES": "551", Not supported until Cat-VRS 2.0
    "VARIANT_CLASSIFICATION": "553",
    "INTERPRETATION": "554",
    "MODE_OF_INHERITANCE": "560",
    # This one has a dashed arrow but I can't remember why :(
    "FUNCTIONAL_EFFECT": "561",
    "REPEAT_NUCLEOTIDES": "564",
    "REPEAT_NUMBER": "565",
    "AFFECTED_EXON_START": "572.1",
    "AFFECTED_EXON_END": "572.2",
    "AFFECTED_INTRON_START": "573.1",
    "AFFECTED_INTRON_END": "573.2",
    "INTERPRETATION_NOTE": "575",
}


def convert_gks_to_hl7_v2(statement: Statement) -> dict[str, Any]:
    """
    Convert a VA-Spec Statement to an HL7 v2-compatible dictionary of fields.

    Returns a dict keyed by HL7 field identifiers (see HL7V2 constants).
    Raises ValueError if required data are missing.
    """
    proposition = statement.proposition
    subject_variant = proposition.subjectVariant

    # 504 - Variant Name
    variant_name = subject_variant.name
    if not variant_name:
        _logger.warning("subjectVariant.name is missing or empty")
        # TODO: error here because I'm pretty sure this is required?
        variant_name = None

    # 505 - Discrete Genetic Variant (placeholder until models solidify)
    # TODO: need to wait for models for this or find out what expected format is

    members = subject_variant.members or []
    genomic_allele, genomic_location = _find_genomic_allele_and_location(members)

    # Get hgvs.g expression from the allele (e.g., 'NC_000007.13:g.140453136A>T')
    expression = _find_expression(genomic_allele, syntax="hgvs.g")
    hgvs_g = expression.value if expression else None
    chromosome, g_dot = _parse_hgvs_g(hgvs_g)

    # 511 - Allele start/end
    allele_start, allele_end = _get_location_interval(genomic_location)

    # 513 - DNA Region

    # 514 - Gene Studied

    # 516 - Transcript Reference Sequence ID

    # 518 - DNA Change

    # 520 - Amino Acid Change

    # 521 - Molecular Consequence

    # 522 - Protein Reference Sequence

    # 524 - Genomic Reference Sequence ID

    # 526 - Reference Allele

    # 527 - Observed Allele

    # 528 - Genomic DNA Change

    # 532 - Cytogenetic Location

    # 534 - Penetrance

    # 535 - Genetic Variant Source

    # 545 - Allele Length

    # 546 - Structural Inner Start/End

    # 547 - Structural Outer Start/End

    # 550 - Copy Number

    # 553 - Variant Classification

    # 554 - Interpretation

    # 560 - Mode of Inheritance

    # 561 - Functional Effect

    # 564 - Repeat Nucleotides

    # 565 - Repeat Number

    # 572 - Affected Exon Start/End

    # 573 - Affected Intron Start/End

    # 575 - Interpretation Note

    result: dict[str, Any] = {}
    result[HL7V2["VARIANT_NAME"]] = variant_name
    result[HL7V2["CHROMOSOME"]] = chromosome
    result[HL7V2["ALLELE_START"]] = allele_start
    result[HL7V2["ALLELE_END"]] = allele_end

    return result


# --- Helpers: extract from VA objects -------------------------------------


def _find_genomic_allele_and_location(
    members: list[Allele],
) -> tuple[Allele, SequenceLocation] | None:
    """
    From a list of members, return the first (allele, location)
    whose location.sequenceReference.moleculeType == 'genomic'.
    # TODO: not sure if this is a reliable field to check for getting the genomic alleles -
    # consider checking expressions instead or as a backup.
    """
    for allele in members:
        location = allele.location
        if location is None:
            continue
        seq_ref = location.sequenceReference
        molecule_type = seq_ref.moleculeType if seq_ref else None
        # TODO: it would be nice to make this helper take this as a parameter for more potential usability later
        if molecule_type == "genomic":
            return allele, location
    return None


def _find_expression(allele: Allele, syntax: str) -> Expression | None:
    """
    Find an expression with a given syntax (e.g., 'hgvs.g') from allele.expressions.
    Returns the first matching expression found.
    """
    expressions = allele.expressions or []

    for expr in expressions:
        s = expr.get("syntax")
        if s == syntax:
            return expr
    # TODO: raise error?
    return None


def _get_location_interval(location: SequenceLocation) -> tuple[int, int]:
    """
    Extract (start, end) from a SequenceLocation.
    """
    start = location.start
    end = location.end
    return start, end


# --- Helpers: transformation / parsing ---------------------------------------


def _parse_hgvs_g(hgvs_g_value: str) -> tuple[str, str]:
    """
    Parse an hgvs.g expression.

    Expected styles:
      - 'NC_000007.13:g.140453136A>T'
    # TODO: should we also accept 'chr7:g....' or '7:g....'?

    Returns:
      (chromosome, g_dot) where chromosome is the left of ':', and g_dot includes 'g.' onwards.
    """
    chromosome, g_dot = hgvs_g_value.split(":", 1)

    return chromosome, g_dot
