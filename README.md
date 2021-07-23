# serato_to_rb
Serato Cuepoint to Rekordbox Cuepoint

This converter utilize the `rekordbox.xml`  collection mechanism to import embedded serato cuepoint.

## Technical Detail

### System Overview
The Serato embedded cuepoint & beatgrid system took advantage of ID3(or other format equivalent) tagging system. The Cuepoint information is stored in a base64 encoded format.

### Tagging 
Different file format store the tag differently but the concept is the same. Serato will write the tag identify itself with `Serato`. The tag identifier for Apple audio(m4a) format is `com.serato.dj`. Cuepoints are stored in `Marker2` and `markersv2` respectively.

### Encoding Format
A proprietary hex format schema is encoded in base64. After decoding , the cuepoint and be searched using the header `0x43 0x55 0x45`(ASCII: `CUE`).

An example of the Cuepoint "Packet":
```
43 55 45  00  00 00 00 0d  00      00      00 00 14 3b   00   cc 00 00  00  00    
C  U   E  PAD  CUE TEXT    PAD  CUE INDEX   CUE TIME     PAD    COLOR  PAD  Name
```

Cue time is a big-endian unsigned int

## Running

The converter is designed to save a copy of decoded audio file into an internal database(`tracks.db`) then generate a rekordbox collection file.

Tested on MacOS 10.15.7, Python 3.9

### Set up

1. Clone the repo
1. `python3 -m venv venv`
1. `pip install -r requirments.txt` to install dependency

### Import Serato Audio folder

`python3 import_tracks.py [path_to_folder]`

Ex.: `python3 import_tracks.py /User/apple/Music/tunes`

### Export database to rekordbox collection

`python3 to_rekordbox.py`

The `rekordbox.xml` file should appear. 

You might find this helpful: [How to import rekordbox collection file](https://www.choones.app/blog/2019-08-30/importing-and-exporting-rekordbox-xml)