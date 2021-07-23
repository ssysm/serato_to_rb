from tinydb import TinyDB
import CuePoint
import rekordbox_collection_generator

db = TinyDB('tracks.db')


def recover_cue_points_collection(track_dict) -> CuePoint.CuePointCollection:
    collection = CuePoint.CuePointCollection(track_filename=track_dict['track_filename'],
                                             length=track_dict['track_length'], id=track_dict['id'])
    for cue in track_dict['cue_points']:
        cue_point = CuePoint.CuePoint(
            cue_index=cue['cue_index'],
            cue_position=cue['cue_position'],
            cue_text=cue['cue_text']
        )
        collection.add_new_cue_point(cue_point)
    return collection


if __name__ == '__main__':
    tracks = db.all()

    tracks_collection: [CuePoint.CuePointCollection] = []

    for track in tracks:
        tracks_collection.append(recover_cue_points_collection(track))

    rdb_xml = rekordbox_collection_generator.generate(tracks_collection)

    with open('rekordbox.xml', 'w', encoding='utf-8') as fd:
        fd.write('<!-- How to import rekordbox.xml: https://www.choones.app/blog/2019-08-30/importing-and-exporting-rekordbox-xml -->')
        fd.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fd.write(rdb_xml.decode('utf-8'))
        fd.close()
    print(str(len(tracks)) + ' tracks done')
