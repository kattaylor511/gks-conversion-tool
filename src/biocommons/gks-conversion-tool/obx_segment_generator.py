from models import *

pipe_separator: str = "|"

carat_separator: str = "^"

period_separator: str = "."


def print_obx_segments(segment_groups: list[OBXSegmentGroup]):
    '''Function to print all OBX segments'''
    for segment in generate_all_obx_for_variants(segment_groups=segment_groups):
        print(segment)


def generate_all_obx_for_variants(segment_groups: list[OBXSegmentGroup]) -> list[str]:
    '''Generates all the OBX segments for a variant given a list of segment groups'''
    all_segments: list[str] = []

    current_line_number = 1
    for segment_group in segment_groups:
        all_segments += generate_obx_segments(segment_group=segment_group, current_line_number=current_line_number)
        current_line_number += len(segment_group.segments)
    
    return all_segments


def generate_obx_segments(segment_group: OBXSegmentGroup, current_line_number: int) -> list[str]:
    '''Generates an OBX segment for each member of the OBXSegmentGroup'''
    segment_array: list[str] = [""] * 22
    all_final_segments: list[str] = []

    # This should always be OBX
    segment_array[0] = segment_group.segment_type

    # Whether this is a string, codeable concept, etc.
    segment_array[2] = str(segment_group.observation_type.value)

    # Name and code of concept
    segment_array[3] = generate_obx3(segment_group=segment_group)

    for segment_line in segment_group.segments:
        all_final_segments.append(generate_obx_segment(segment_group=segment_group, segment_line=segment_line, segment_array=segment_array, line_number=current_line_number))
        current_line_number += 1

    return all_final_segments


def generate_obx_segment(segment_group: OBXSegmentGroup, segment_line: OBXSegmentBase, segment_array: list[str], line_number: int) -> str:
    '''Generates a single OBX segment for one member of the OBXSegmentGroup'''
    # Line number
    segment_array[1] = str(line_number)

    # Variant identifier
    segment_array[4] = generate_obx4(segment_group=segment_group, segment=segment_line)

    # Result value
    segment_array[5] = generate_obx5(segment=segment_line)

    return pipe_separator.join(segment_array)


def generate_obx3(segment_group: OBXSegmentGroup) -> str:
    '''Generates the OBX-3 value which details the VAR concept and its name'''
    return str(segment_group.segment_identifier.name) + carat_separator + str(segment_group.segment_identifier.value) + carat_separator + segment_group.segment_identifier_system


def generate_obx4(segment_group: OBXSegmentGroup, segment: OBXSegmentBase) -> str:
    '''Generates OBX-4 which is the variant identifier'''
    return str(segment_group.variant_type) + \
        segment_group.variant_identifier + \
        (period_separator + segment.variant_identifier_line if segment.variant_identifier_line is not None else "") 


def generate_obx5(segment: OBXSegmentBase) -> str:
    '''Generates OBX-5 which is the actual value being sent. Each data type will be handled slightly differently'''
    if isinstance(segment, OBXSegmentST):
        return segment.value
    elif isinstance(segment, OBXSegmentNM):
        return str(segment.value)
    elif isinstance(segment, OBXSegmentNR):
        return str(segment.lower_bound) + carat_separator + str(segment.upper_bound)
    elif isinstance(segment, OBXSegmentCWE):
        if all(value is None for value in (segment.code, segment.label, segment.coding_system)):
            raise ValueError("Codeable concepts must have either a code and coding system or a label")
        elif (segment.code is None or segment.coding_system is None) and segment.label is not None:
            return carat_separator + segment.label
        else:
            return segment.code + carat_separator + (segment.label if segment.label is not None else "") + carat_separator + segment.coding_system  
    else:
        raise ValueError("Segment is not an instance of any supported segments")