import glob

from tqdm import tqdm

from CuePoint import NotACuePointFileException, CuePointNotFoundException
from decode import extract_cue_points
from tinydb import TinyDB
import mutagen

db = TinyDB('tracks.db')
types = ('*.m4a', '*.mp3')

if __name__ == '__main__':
    path = 'C:\\Users\\admin\\Music\\_Serato_\\Imported\\Serato Demo Tracks\\'
    files = []
    for file_type in tqdm(types):
        files.extend(glob.glob(path + file_type))

    for file in tqdm(files):
        track = mutagen.File(file)
        track_length_int = int(track.info.length)
        try:
            track_cue_points = extract_cue_points(file)
        except NotACuePointFileException as e:
            print(file + ' is not a cue point file')
            continue
        except CuePointNotFoundException as e:
            print(file + ' does not contain cue points')
            continue

        db.insert({
            'id': track_cue_points.id,
            'track_filename': file,
            'track_length': track_length_int,
            'cue_points': track_cue_points.cue_points,
        })