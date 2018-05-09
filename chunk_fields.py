'''
Avi Chunk Fields Dictionary
---------------------------

acfd() is a function that returns the dictionary.

In the dictionary every known chunk's name is key to an other dictionary with its fields.
    Moreover in this inner dictionary every field is key to the number of bits occupied by it.

So we have:

    'chunk id': {'field name': bits, 'field name': bits ...}

Theree special cases:

    1) STRUCT FIELDS.
        Some fields can be structs, in this case its value is an annidated dictionary with the same sintax.
        For example:
                {..., "rcFrame":{"left":2, "top":2, "right":2, "bottom":2}, ...}.

        1.2) ARRAY WITH UNDEFINED NUMBER OF ELEMENTS.
            There may be arrays whose entries are structs. Moreover the number of array members is not explicitly declared.
            In this cas we we use two annidated dictionaries :
                the outer dictionary has only one key that is the identifier of the struct entry and the inner specifies the struct's structure.
                {..., {"array": {"strucht entry": {"key":value, ...} } }, ... }

    2) FCC FIELDS.
        There are some fields whose value is a FourCC, therefore a 4 byte text.
        In these cases we replace the bits value with the 'fcc' keyword.
        This way the parser will read 4 bytes and decode them with the UTF-8 codec.

    3) UKNOWKN FIELDS.
        There can be some fields whose content and size is unkown. In this case we use the keyword 'unknown' and the value '-1'.
        This case may occur only in the final part of the chunk therefore with the -1 value the parser will read all the remaining bytes and insert them in the 'unkown' field.

'''

def acfd():
    _acfd = {
    'avih':{
        'dwMicroSecPerFrame': 4,
        'dwMaxBytesPerSec': 4,
        'dwPaddingGranularity': 4,
        'dwFlags': 4,
        'dwTotalFrames': 4,
        'dwInitialFrames': 4,
        'dwStreams': 4,
        'dwSuggestedBufferSizeWidth': 4,
        'dwWidth': 4,
        'dwHeight': 4,
        'dwReserved':{ 'dwReserved_1':4, 'dwReserved_2':4, 'dwReserved_3':4, 'dwReserved_4':4}},

    'strh':{
        'fccType': 'fcc',
        'fccHandler': 'fcc',
        'dwFlags': 4,
        'wPriority': 2,
        'wLanguage': 2,
        'dwInitialFrames': 4,
        'dwScale': 4,
        'dwRate': 4,
        'dwStart': 4,
        'dwLength': 4,
        'dwSuggestedBufferSize': 4,
        'dwQuality': 4,
        'dwSampleSize': 4,
        'rcFrame':{'left':2, 'top':2, 'right':2, 'bottom':2}},

    'strfvids':{
        'biSize': 4,
        'biWidth': 4,
        'biHeight': 4,
        'biPlanes': 2,
        'biBitCount': 2,
        'biCompression': 'fcc',
        'biSizeImage': 4,
        'biXPelsPerMeter': 4,
        'biYPelsPerMeter': 4,
        'biClrUsed': 4,
        'biClrImportant': 4,
        'bmiColors': {'rgbBlue': 4, 'rgbGreen': 4, 'rgbRed': 4, 'rgbReserved': 4},
        'unknown': -1},

    'strfdvsd': {
        'biSize': 4,
        'biWidth': 4,
        'biHeight': 4,
        'biPlanes': 2,
        'biBitCount': 2,
        'biCompression': 'fcc',
        'biSizeImage': 4,
        'biXPelsPerMeter': 4,
        'biYPelsPerMeter': 4,
        'biClrUsed': 4,
        'biClrImportant': 4,
        'dwDVAAuxSrc': 4,
        'dwDVAAuxCtl': 4,
        'dwDVAAuxSrc1': 4,
        'dwDVAAuxCtl1': 4,
        'dwDVVAuxSrc': 4,
        'dwDVVAuxCtl': 4,
        'dwDVReserved': {'Res1': 4, 'Res2': 4}},

    #struttura audio base
    'strfauds':{
        'wFormatTag': 2,
        'nChannels': 2,
        'nSamplesPerSec': 4,
        'nAvgBytesPerSec': 4,
        'nBlockAlign': 2,
        'wBitsPerSample': 2,
        'cbSize': 2,
        'unknown': -1},
    # struttura audio per wFormatTag = 85 (corrispondente a MPEGLAYER3WAVEFORMAT)
    'strfau85': {
        'wFormatTag': 2,
        'nChannels': 2,
        'nSamplesPerSec': 4,
        'nAvgBytesPerSec': 4,
        'nBlockAlign': 2,
        'wBitsPerSample': 2,
        'cbSize': 2,
        'wID': 2,
        'fdwFlags': 4,
        'nBlockSize': 2,
        'nFramesPerBlock': 2,
        'nCodecDelay': 2},

    #struttura audio per wFormatTag = 80 (corrispondente a MPEG1WAVEFORMAT)
    'strfau80': {
        'wFormatTag': 2,
        'nChannels': 2,
        'nSamplesPerSec': 4,
        'nAvgBytesPerSec': 4,
        'nBlockAlign': 2,
        'wBitsPerSample': 2,
        'cbSize': 2,
        'fwHeadLayer': 2,
        'dwHeadBitrate': 4,
        'fwHeadMode': 2,
        'fwHeadModeExt': 2,
        'wHeadEmphasis': 2,
        'fwHeadFlags': 2,
        'dwPTSLow': 4,
        'dwPTSHigh': 4
        },

    # struttura audio per wFormatTag = 65534 (corrispondente a WAVEFORMATEXTENSIBLE)
    'strfau65534': {
        'wFormatTag': 2,
        'nChannels': 2,
        'nSamplesPerSec': 4,
        'nAvgBytesPerSec': 4,
        'nBlockAlign': 2,
        'wBitsPerSample': 2,
        'cbSize': 2,
        'Samples': {'wValidBitsPerSample': 2,
                    'wSamplesPerBlock': 2,
                    'wReserved': 2},
        'dwChannelMask': 4,
        'SubFormat': -1
    },

    # struttura per file con DV Data
    'strfiavs':{
        'dwDVAAuxSrc': 4,
        'dwDVAAuxCtl': 4,
        'dwDVAAuxSrc1': 4,
        'dwDVAAuxCtl1': 4,
        'dwDVVAuxSrc': 4,
        'dwDVVAuxCtl': 4,
        'dwDVReserved': {'Res1': 4, 'Res2': 4}},

    'dmlh':{
        'dwTotalFrames':4,
        'unknown':-1},

    'vprp':{
        'VideoFormatToken': 4,
        'VideoStandard': 4,
        'dwVerticalRefreshRate': 4,
        'dwHTotalInT': 4,
        'dwVTotalInLines': 4,
        'dwFrameAspectRatio': 4,
        'dwFrameWidthInPixels': 4,
        'dwFrameHeightInPixels': 4,
        'nbFieldPerFrame': 4,
        'FieldInfo': {
            'nbFieldPerFrame': {
                'CompressedBMHeight': 4,
                'CompressedBMWidth': 4,
                'ValidBMHeight': 4,
                'ValidBMWidth': 4,
                'ValidBMXOffset': 4,
                'ValidBMYOffset': 4,
                'VideoXOffsetInT': 4,
                'VideoYValidStartLine': 4
                }
            }
        },

    'ISFT':{
        'Software':-1
        },

    'idx1':{
        'aIndex': {
            '_avioldindex_entry':{'dwChunkId': 'fcc', 'dwFlags': 4, 'dwOffset': 4, 'dwSize': 4}}},

    'indx':{
        'wLongsPerEntry':2,
        'bIndexSubType':1,
        'bIndexType':1,
        'nEntriesInUse':4,
        'dwChunkId':'fcc',
        'dwReserved':{ 'dwReserved_1':4, 'dwReserved_2':4, 'dwReserved_3':4},
        'aIndex':{
            '_avisuperindex_entry': {'qwOffset':8, 'dwSize':4, 'dwDuration':4}}},

    'ix':{
        'wLongsPerEntry':2,
        'bIndexSubType':1,
        'bIndexType':1,
        'nEntriesInUse':4,
        'dwChunkId':'fcc',
        'qwBaseOffset':8,
        'dwReserved':{'dwReserved_1':4, 'dwReserved_2':4, 'dwReserved_3':4},
        'aIndex':{
            '_avistdindex_entry':{'qwOffset':4, 'dwSize':4}}},

    'mx':{
        'wLongsPerEntry':2,
        'bIndexSubType':1,
        'bIndexType':1,
        'nEntriesInUse':4,
        'dwChunkId':'fcc',
        'qwBaseOffset':8,
        'dwReserved':{'dwReserved_1':4, 'dwReserved_2':4, 'dwReserved_3':4},
        'aIndex':-1}
    }
    return _acfd
