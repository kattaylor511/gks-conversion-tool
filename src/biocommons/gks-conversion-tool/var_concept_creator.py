from models import *
from obx_segment_generator import *
from enum import Enum


def createVARSegmentsGroups(variant_information: dict[str, str], variant_identifier: str) -> list[OBXSegmentGroup]:
    segment_groups: list[OBXSegmentGroup] = []
    segment_groups.append(createVAR503VariantType(variant_identifier))
    segment_groups.append(createVAR514VariantGene(variant_identifier, variant_information["GENENAME"], variant_information["GENEID"]))
    segment_groups.append(createVAR552VariantAssesment(variant_identifier))
    segment_groups.append(createVAR553VariantClassification(variant_identifier, variant_information["CLASSIFICATION"]))
    return segment_groups


def createVAR503VariantType(variant_identifier: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label="Simple"
    )
    return OBXSegmentGroup(
        segments=[segment],
        observation_type=ObservationTypes.CODEABLECONCEPT,
        variant_identifier=variant_identifier,
        segment_identifier=VARConcepts.VARCONCEPT503
        )


def createVAR514VariantGene(variant_identifier: str, gene_name: str, gene_id: str, gene_system: str = "HGNC") -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=gene_name,
        code=gene_id,
        coding_system=gene_system
    )
    return OBXSegmentGroup(
        segments=[segment],
        observation_type=ObservationTypes.CODEABLECONCEPT,
        variant_identifier=variant_identifier,
        segment_identifier=VARConcepts.VARCONCEPT514
        )


def createVAR552VariantAssesment(variant_identifier: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label="Detected"
    )
    return OBXSegmentGroup(
        segments=[segment],
        observation_type=ObservationTypes.CODEABLECONCEPT,
        variant_identifier=variant_identifier,
        segment_identifier=VARConcepts.VARCONCEPT552
        )


def createVAR553VariantClassification(variant_identifier: str, classification_value: str) -> OBXSegmentGroup:
    segment = OBXSegmentCWE(
        label=classification_value
    )
    return OBXSegmentGroup(
        segments=[segment],
        observation_type=ObservationTypes.CODEABLECONCEPT,
        variant_identifier=variant_identifier,
        segment_identifier=VARConcepts.VARCONCEPT553
        )

variant_information: dict[str, str] = {}
variant_information["GENENAME"] = "BRAF"
variant_information["GENEID"] = "123"
variant_information["CLASSIFICATION"] = "Likely Pathogenic"

segments = createVARSegmentsGroups(variant_information=variant_information, variant_identifier="a")
print_obx_segments(segments)



