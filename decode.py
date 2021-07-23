import base64
import struct
import mutagen
import logging
from CuePoint import CuePoint, CuePointCollection, CuePointNotFoundException, NotACuePointFileException
from kMarkerTags import marker_tags


def extract_m4a_tags(tag_data):
    m4a_base64_str = tag_data.decode('utf-8')
    m4a_base64 = m4a_base64_str.replace('\n', '')
    if len(m4a_base64) % 4:
        # not a multiple of 4, add padding:
        m4a_base64 += '=' * (4 - len(m4a_base64) % 4)
    m4a_base64_decoded = base64.b64decode(m4a_base64)
    return m4a_base64_decoded


def extract_tag_base64(tag_bytes):
    base64_extracted = tag_bytes[2: len(tag_bytes) - 1]
    base64_str = base64_extracted.decode('utf-8')
    base64_str = base64_str.replace('\n', '')
    return base64_str


def extract_cue_points(filename: str) -> CuePointCollection:
    track = mutagen.File(filename)
    file_ext = filename.split('.')[1]

    try:
        if file_ext == 'm4a':
            markers_tag_data = track.tags[marker_tags['m4a']][0]
            print(markers_tag_data)
            markers_tag_data = extract_m4a_tags(markers_tag_data)
        else:
            markers_tag_data = track.tags[marker_tags['mp3']].data
    except KeyError:
        raise NotACuePointFileException('Not a valid Serato cued file.')

    base64_str = extract_tag_base64(markers_tag_data)
    base64_decoded = base64.b64decode(base64_str)
    hex_array = bytearray(base64_decoded)
    cue_points = CuePointCollection(filename)
    last_cue_position = hex_array.find(b'CUE')
    if last_cue_position < 0:
        print('Can not find cue point')
        raise CuePointNotFoundException('Can not find cue points')

    while True:
        cue_length = hex_array[last_cue_position + 7]
        if cue_length != 13: # named cue
            logging.debug('got an named cue')
        cue_index = int(hex_array[last_cue_position + 9])
        cue_position = int(struct.unpack('>I', hex_array[last_cue_position + 10:last_cue_position + 14])[0])
        cue_color = hex_array[last_cue_position + 16:last_cue_position + 19]
        next_cue_position = hex_array.find(b'CUE', last_cue_position + 1)  # find the next cue
        if next_cue_position < 0 and cue_length != 13:
            bpm_lock_pos = hex_array.find(b'\x42\x50\x4d\x4c\x4f\x43\x4b', last_cue_position)
            cue_text = hex_array[last_cue_position + 20:bpm_lock_pos]
        elif cue_length != 13:
            cue_text = hex_array[last_cue_position + 20: next_cue_position - 1]
        else:
            cue_text = b'\x00'
        cue_point = CuePoint(cue_length, cue_index, cue_position, cue_color.hex(), cue_text.decode('utf-8'))
        cue_points.add_new_cue_point(cue_point)
        last_cue_position = next_cue_position
        if last_cue_position < 0:  # no more cue
            break

    return cue_points
