import glob
import argparse
import mutagen
import os
from tqdm import tqdm
from CuePoint import NotACuePointFileException, CuePointNotFoundException
from decode import extract_cue_points
from tinydb import TinyDB

db = TinyDB('tracks.db')
types = ('*.m4a', '*.mp3')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import Serato Markers')
    parser.add_argument('path', help='Directory Path')
    args = parser.parse_args()

    path = os.path.abspath(args.path) + '/'
    print('Searching for ' + path)
    files = []
    for file_type in tqdm(types):
        files.extend(glob.glob(path + file_type))

    cuepoint_failread_count = 0

    for file in tqdm(files):
        track = mutagen.File(file)
        track_length_int = int(track.info.length)
        try:
            track_cue_points = extract_cue_points(file)
        except NotACuePointFileException as e:
            cuepoint_failread_count = cuepoint_failread_count + 1
            print(file + ' is not a cue point file')
            continue
        except CuePointNotFoundException as e:
            cuepoint_failread_count = cuepoint_failread_count + 1
            print(file + ' does not contain cue points')
            continue

        db.insert({
            'id': track_cue_points.id,
            'track_filename': file,
            'track_length': track_length_int,
            'cue_points': track_cue_points.cue_points,
        })

    print('Imported ' + str(len(files) - cuepoint_failread_count) +
        ' tracks, failed : ' + str(cuepoint_failread_count))