from models import *
from obx_segment_generator import *
from enum import Enum

# This is testing code and can be removed later
variant_information: dict[str, str] = {}
variant_information["DNA_CHANGE"] = "c.37556K>T"
variant_information["TRANSCRIPT_REFERENCE_SEQUENCE"] = "NM_37556.1"
variant_information["GENE_STUDIED"] = "BRAF"
variant_information["GENE_ID"] = "123"
variant_information["GENOMIC_REFERENCE_SEQUENCE_ID"] = "NC_000003.7"
variant_information["AMINO_ACID_CHANGE"] = "p.Asp123Arg"
variant_information["PROTEIN_REFERENCE_SEQUENCE"] = "NP_37556.3"
variant_information["GENOMIC_DNA_CHANGE"] = "g.3755637556K>T"
variant_information["VARIANT_CLASSIFICATION"] = "Likely Pathogenic"


def createVARSegmentsGroups(variant_information: dict[str, str], variant_identifier: str) -> list[OBXSegmentGroup]:
    segment_groups: list[OBXSegmentGroup] = []
    segment_groups.append(createVAR503VariantType(variant_identifier))
    segment_groups.append(createVAR514VariantGene(variant_identifier, variant_information["GENE_STUDIED"], variant_information["GENE_ID"]))
    segment_groups.append(createVAR516TranscriptReferenceSequence(variant_identifier, variant_information["TRANSCRIPT_REFERENCE_SEQUENCE"]))
    segment_groups.append(createVAR518DNAChange(variant_identifier,  variant_information["DNA_CHANGE"]))
    segment_groups.append(createVAR520AminoAcidChange(variant_identifier,  variant_information["AMINO_ACID_CHANGE"]))
    segment_groups.append(createVAR522ProteinReferenceSequence(variant_identifier,  variant_information["PROTEIN_REFERENCE_SEQUENCE"]))
    segment_groups.append(createVAR524GenomicReferenceSequence(variant_identifier,  variant_information["GENOMIC_REFERENCE_SEQUENCE_ID"]))
    segment_groups.append(createVAR528GenomicDNAChange(variant_identifier,  variant_information["GENOMIC_DNA_CHANGE"]))
    segment_groups.append(createVAR552VariantAssesment(variant_identifier))
    segment_groups.append(createVAR553VariantClassification(variant_identifier, variant_information["VARIANT_CLASSIFICATION"]))
    return segment_groups


def createCWEOBXSegmentGroup(segment: OBXSegmentCWE, variant_identifier: str, var_concept: VARConcepts) -> OBXSegmentGroup:
    return OBXSegmentGroup(
        segments=[segment],
        observation_type=ObservationTypes.CODEABLECONCEPT,
        variant_identifier=variant_identifier,
        segment_identifier=var_concept
        )


def createSTOBXSegmentGroup(segment: OBXSegmentST, variant_identifier: str, var_concept: VARConcepts) -> OBXSegmentGroup:
    return OBXSegmentGroup(
        segments=[segment],
        observation_type=ObservationTypes.STRING,
        variant_identifier=variant_identifier,
        segment_identifier=var_concept
        )


def createVAR503VariantType(variant_identifier: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label="Simple"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT503)


def createVAR514VariantGene(variant_identifier: str, gene_name: str, gene_id: str, gene_system: str = "HGNC") -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=gene_name,
        code=gene_id,
        coding_system=gene_system
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT514)


def createVAR516TranscriptReferenceSequence(variant_identifier: str, transcript_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=transcript_value,
        code=transcript_value,
        coding_system="RefSeq-T"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT516)


def createVAR518DNAChange(variant_identifier: str, dna_change_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=dna_change_value,
        code=dna_change_value,
        coding_system="HGVS.c"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT518)


def createVAR520AminoAcidChange(variant_identifier: str, protein_change_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=protein_change_value,
        code=protein_change_value,
        coding_system="HGVS.p"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT520)


def createVAR521MolecularConsequence(variant_identifier: str, molecular_consequence: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=molecular_consequence
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT521)


def createVAR522ProteinReferenceSequence(variant_identifier: str, protein_transcript_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentST(
        value=protein_transcript_value
    )
    return createSTOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT522)


def createVAR524GenomicReferenceSequence(variant_identifier: str, genomic_reference_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=genomic_reference_value,
        code=genomic_reference_value,
        coding_system="RefSeq-G"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT524)


def createVAR528GenomicDNAChange(variant_identifier: str, genomic_dna_change: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=genomic_dna_change,
        code=genomic_dna_change,
        coding_system="HGVS.g"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT528)


def createVAR552VariantAssesment(variant_identifier: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label="Detected"
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT552)


def createVAR553VariantClassification(variant_identifier: str, classification_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=classification_value
    )
    return createCWEOBXSegmentGroup(segment, variant_identifier, VARConcepts.VARCONCEPT553)


segments = createVARSegmentsGroups(variant_information=variant_information, variant_identifier="a")
print_obx_segments(segments)



