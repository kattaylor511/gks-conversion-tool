"""Converter for GKS <-> HL7 v2"""

import logging
from ga4gh.va_spec.base.core import (
    Statement,
)

_logger = logging.getLogger(__name__)


def convert_gks_to_hl7_v2(statement: Statement) -> dict:
    """convert GKS to HL7 v2"""
    
    proposition = statement.proposition
    subject_variant = proposition.subjectVariant

    # 504 - Variant Name
    variant_name = subject_variant.name

    # 505 - Discrete Genetic Variant
    # wait for types and models for this

    # 510 - Chromosome
    members = subject_variant.members
    genomic_allele = None
    genomic_location = None
    for allele in members:
        # get member where the allele's location's sequence reference's moleculeType is genomic
        genomic_location = allele.location
        sequence_reference = genomic_location.sequenceReference
        if sequence_reference.moleculeType == "genomic":
            genomic_allele = allele
            break
    # get chromosome from allele
    expressions = genomic_allele.expressions
    expression = None
    for expr in expressions:
        if expr.get("syntax") == "hgvs.g":
            expression = expr
            break
    g_dot_hgvs = expression.get("value")
    g_dot_split = g_dot_hgvs.split(":", 2)
    chromosome = g_dot_split[0]
    g_dot = g_dot_split[1]

    # 511 - Allele start/end
    allele_start = genomic_location.start
    allele_end = genomic_location.end

    # TODO: finish tomorrow? :-)


    return {}
