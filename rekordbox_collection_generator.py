from lxml import etree
import CuePoint


def generate(tracks: [CuePoint.CuePointCollection]):
    entry_length = len(tracks)

    dj_playlist = etree.Element('DJ_PLAYLISTS')
    dj_playlist.set('Version', '1.0.0')
    product_elm = etree.Element('PRODUCT')
    product_elm.set('Name', 'rekordbox')
    product_elm.set('Version', '6.5.1')
    product_elm.set('Company', 'AlphaTheta')
    collection_elm = etree.Element('COLLECTION')
    collection_elm.set('Entries', str(entry_length))

    for track in tracks:
        track_elm = etree.Element('TRACK')
        track_elm.set('TrackID', str(track.id))
        track_elm.set('TotalTime', str(track.length))
        track_elm.set('Location', 'file://localhost/' + track.track_filename)
        for cue_point in track.cue_points:
            cue_element = etree.Element('POSITION_MARK')
            cue_element.set('Name', cue_point.cue_text.rstrip('\x00'))
            cue_element.set('Num', str(cue_point.cue_index))
            cue_element.set('Start', str(cue_point.cue_position/1000))
            cue_element.set('Red', '40')
            cue_element.set('Green', '226')
            cue_element.set('Blue', '20')
            cue_element.set('Type', '0')
            track_elm.append(cue_element)
        collection_elm.append(track_elm)

    dj_playlist.append(product_elm)
    dj_playlist.append(collection_elm)

    s = etree.tostring(dj_playlist, pretty_print=True)
    return s
