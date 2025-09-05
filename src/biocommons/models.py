from pydantic import BaseModel
from enum import Enum

"""A file for models used in the converter tool"""
class ObservationTypes(str, Enum):
    STRING = "ST",
    NUMERIC = "NM",
    NUMERICRANGE = "NR",
    CODEABLECONCEPT = "CWE"


class VARConcepts(str, Enum):
    VARCONCEPT503 = "Variant Type",
    VARCONCEPT504 = "Variant Name",
    VARCONCEPT505 = "Discrete Variant",
    VARCONCEPT510 = "Chromosome",
    VARCONCEPT511_1 = "Allele Start",
    VARCONCEPT511_2 = "Allele End",
    VARCONCEPT513 = "Dna Region",
    VARCONCEPT514 = "Gene Studied",
    VARCONCEPT516 = "Transcript Reference Sequence Id",
    VARCONCEPT518 = "Dna Change",
    VARCONCEPT520 = "Amino Acid Change",
    VARCONCEPT521 = "Molecular Consequence",
    VARCONCEPT522 = "Protein Reference Sequence",
    VARCONCEPT524 = "Genomic Reference Sequence Id",
    VARCONCEPT526 = "Reference Allele",
    VARCONCEPT527 = "Observed Allele",
    VARCONCEPT528 = "Genomic Dna Change",
    VARCONCEPT532 = "Cytogenetic Location",
    VARCONCEPT534 = "Penetrance",
    VARCONCEPT535 = "Genetic Variant Source",
    VARCONCEPT545 = "Allele Length",
    VARCONCEPT546_1 = "Structural Inner Start",
    VARCONCEPT546_2 = "Structural Inner End",
    VARCONCEPT547_1 = "Structural Outer Start",
    VARCONCEPT547_2 = "Structural Outer End",
    VARCONCEPT550 = "Copy Number",
    VARCONCEPT552 = "Genetic Variant Assessment",
    VARCONCEPT553 = "Variant Classification",
    VARCONCEPT554 = "Interpretation",
    VARCONCEPT560 = "Mode Of Inheritance",
    VARCONCEPT561 = "Functional Effect",
    VARCONCEPT564 = "Repeat Nucleotides",
    VARCONCEPT565 = "Repeat Number",
    VARCONCEPT572_1 = "Affected Exon Start",
    VARCONCEPT572_2 = "Affected Exon End",
    VARCONCEPT573_1 = "Affected Intron Start",
    VARCONCEPT573_2 = "Affected Intron End",
    VARCONCEPT575 = "Interpretation Note"


class OBXSegmentBase(BaseModel):
    """Common OBX fields (1..5 without the value)."""

    variant_identifier_line: str | None = None           # OBX-5  


class OBXSegmentST(OBXSegmentBase):
    '''A class representing a segment with a string type'''

    observation_type: ObservationTypes = ObservationTypes.STRING

    value: str


class OBXSegmentCWE(OBXSegmentBase):
    '''A class representing a segment with a codeable concept type'''

    observation_type: ObservationTypes = ObservationTypes.CODEABLECONCEPT

    code: str | None = None

    coding_system: str | None = None

    label: str | None = None


class OBXSegmentNM(OBXSegmentBase): 
    '''A class representing a segment with a numeric type'''

    observation_type: ObservationTypes = ObservationTypes.NUMERIC

    value: float


class OBXSegmentNR(OBXSegmentBase): 
    '''A class representing a segment with a numeric range type'''
    
    observation_type: ObservationTypes = ObservationTypes.NUMERICRANGE

    lower_bound: float

    upper_bound: float


class OBXSegmentGroup(BaseModel):
    '''A class representing one or more segments that have the same type and segment identifier (e.g., the Discrete Genetic Variant lines)'''

    segments: list[OBXSegmentBase]

    segment_type:  str = "OBX"                           # OBX-1

    observation_type: ObservationTypes                   # OBX-3

    variant_type: int = 2                                # OBX-5

    variant_identifier: str                              # OBX-5

    segment_identifier: VARConcepts                      # OBX-4.1

    segment_identifier_system: str = "EPICGENOMICS"      # OBX 4.3
