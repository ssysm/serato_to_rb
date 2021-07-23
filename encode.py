# deprecated
import base64
import json
import struct
import mutagen
from mutagen.mp4 import MP4FreeForm
from CuePoint import CuePoint, CuePointCollection
from kMarkerTags import marker_tags


def recover_cue_points(json_obj) -> CuePointCollection:
    track_filename = json_obj['track_filename']
    cue_points_collection = CuePointCollection(track_filename)
    for cue_point in json_obj['cue_points']:
        cue_points_collection.add_new_cue_point(CuePoint(cue_point['cue_type'],
                                                         cue_point['cue_index'],
                                                         cue_point['cue_position'],
                                                         cue_point['cue_color']))
    return cue_points_collection


if __name__ == '__main__':
    filename = 'sample/01 You & Me.m4a'
    cut_point_file = 'sample/01 You & Me.json'
    track = mutagen.File(filename)
    cp_str = open(cut_point_file).read()
    cue_points = recover_cue_points(json_obj=json.loads(cp_str))

    marker_header = b'\x01\x01\x43\x4f\x4c\x4f\x52\x00\x00\x00\x00\x04\x00\xff\xff\xff'
    marker_footer = b'\x42\x50\x4d\x4c\x4f\x43\x4b\x00\x00\x00\x00\x01\x00\x00'

    cue_point_header = b'\x43\x55\x45\x00\x00\x00\x00\x0d'
    cue_point_footer = b'\x00\x00\x00'

    tag_header = b'\x61\x70\x70\x6c\x69\x63\x61\x74\x69\x6f\x6e\x2f\x6f\x63\x74\x65\x74\x2d\x73\x74\x72\x65\x61\x6d' \
                 b'\x00\x00\x53\x65\x72\x61\x74\x6f\x20\x4d\x61\x72\x6b\x65\x72\x73\x32\x00\x01\x01'

    marker_bytes = bytes()
    marker_bytes += marker_header
    for cue_point_obj in cue_points.cue_points:
        marker_bytes += cue_point_header
        marker_bytes += struct.pack('>h', cue_point_obj.cue_index)
        marker_bytes += struct.pack('>I', cue_point_obj.cue_position)
        marker_bytes += b'\x00'  # pad
        marker_bytes += bytearray.fromhex(cue_point_obj.cue_color)
        marker_bytes += cue_point_footer
    marker_bytes += marker_footer

    packed_marker_base64 = base64.b64encode(marker_bytes)

    tag_bytes = bytes()
    tag_bytes += tag_header
    tag_bytes += packed_marker_base64
    tag_bytes += b'\x00\x00\x00\x00\x00\x00'
    packed_tag_base64 = base64.b64encode(tag_bytes)
    print(packed_tag_base64)
    track.tags[marker_tags['m4a']] = MP4FreeForm(data=packed_tag_base64)
    track.save()