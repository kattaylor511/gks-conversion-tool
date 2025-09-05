from pydantic import BaseModel

"""A file for models used in the converter tool"""

class OBXSegmentBase(BaseModel):
    """Common OBX fields (1..5 without the value)."""
      
    line_number: int                                     # OBX-2

    variant_identifier_line: str                         # OBX-5  


class OBXSegmentST(OBXSegmentBase):
    '''A class representing a segment with a string type'''

    observation_type: str = "ST"

    value: str


class OBXSegmentCWE(OBXSegmentBase):
    '''A class representing a segment with a codeable concept type'''

    observation_type: str = "CWE"

    code: str 

    coding_system: str

    label: str


class OBXSegmentNM(OBXSegmentBase): 
    '''A class representing a segment with a numeric type'''

    observation_type: str = "NM"

    value: float


class OBXSegmentNR(OBXSegmentBase): 
    '''A class representing a segment with a numeric range type'''
    
    observation_type: str = "NR"

    lower_bound: float

    upper_bound: float


class OBXSegmentGroup(BaseModel):
    '''A class representing one or more segments that have the same type and segment identifier (e.g., the Discrete Genetic Variant lines)'''

    segments: list[OBXSegmentBase]

    segment_type:  str = "OBX"                           # OBX-1

    observation_type: str                                # OBX-3

    variant_type: int = 2                                # OBX-5

    variant_identifier: str                              # OBX-5

    segment_identifier: str                              # OBX-3.1

    segment_name: str                                    # OBX 3.2

    segment_identifier_system: str                       # OBX 3.3
