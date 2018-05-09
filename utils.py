from chunk_fields import acfd

def collect_fields(file, read, limit, current_chunk, subdict):
    return_dict = dict()
    if read<limit:
        for k, b in subdict.items():
            if type(b) is not dict:
                # standard case, values are the number of bytes to beread
                v = None
                # if the field is a FourCC
                if (b == 'fcc'):
                    v = current_chunk.read(4)
                    # if the field is empty, you must not decode it
                    if v != b'\x00\x00\x00\x00':
                        v = v.decode('utf-8')
                    else:
                        v = ""
                    read += 4
                # if the field is unkown
                elif b < 0:
                    v = current_chunk.read(limit-read)
                    read += (limit-read)
                # the field is int
                else:
                    v = int.from_bytes(current_chunk.read(b), byteorder='little')
                    read += b
                return_dict[k] = v
            elif type(b) is dict and len(b.items())>1:
                # simple structure
                v, r = collect_fields(file, read, limit, current_chunk, b)
                read = r
                return_dict[k] = v
            else:
                # array with an unkown number of entries
                entry_dict = list(b.values())[0]
                # bytes occupied by one entry
                acc = 0
                for val in entry_dict.values():
                    acc += (val if type(val) is int else 4)

                # number of entries in the array
                arr_len = int((limit-read)/acc )

                # iterate to collect all the entries
                array_dict = dict()
                for i in range(arr_len):
                    v, r = collect_fields(file, 0, acc, current_chunk, entry_dict)
                    read += acc
                    array_dict[list(b.keys())[0]+'-'+str(i)] = v
                return_dict[k] = array_dict
    return return_dict, read

def parse_index(file, chunk_name, current_chunk, lc, limit, field_dict):

    chunk_dict = None

    if chunk_name == 'idx1':
        chunk_dict = field_dict[chunk_name]
    elif chunk_name[-1] == 'x' or chunk_name[:2]=='ix':
        file.seek(3, 1)
        index_type = int.from_bytes(file.read(1), byteorder='little')
        file.seek(-4, 1)
        if index_type == 1:
            file.seek(2, 1)
            subindex_type = int.from_bytes(file.read(1), byteorder='little')
            file.seek(-3, 1)
            if subindex_type == 0:
                chunk_dict = field_dict['ix']
            elif subindex_type == 1:
                chunk_dict = field_dict['mx']
        elif index_type == 0:
            chunk_dict = field_dict['indx']
    if chunk_dict is None:
        lc.add_rawdata(current_chunk.read(limit))
    else:
        collected_fields, r = collect_fields(file,0, limit, current_chunk, chunk_dict)
        assert limit==r, "read bytes ({}) are not equal to total ({})".format(r, limit)
        for k in list(collected_fields.keys()):
            lc.add_data(k, collected_fields[k])
    return

def parse_strf(file, _acfd, current_chunk, lc, limit):
    file.seek(-64, 1)
    ty = file.read(4)
    handler = file.read(4)
    file.seek(56, 1)
    if ty.decode("utf-8") == 'vids':
        if handler.decode("utf-8") == 'dvsd':
            subdict = _acfd['strfdvsd']
        else:
            subdict = _acfd['strfvids']
    if ty.decode("utf-8") == 'auds':
        wFormatTag = int.from_bytes(file.read(2), byteorder='little')
        file.seek(-2, 1)
        if wFormatTag == 85:
            subdict = _acfd['strfau85']
        elif wFormatTag == 65534:
            subdict = _acfd['strfau65534']
        elif wFormatTag == 80:
            subdict = _acfd['strfau80']
        else:
            subdict = _acfd['strfauds']
    if ty.decode("utf-8") == 'iavs':
        subdict = _acfd['strfivas']

    collected_fields, r = collect_fields(file,0, limit, current_chunk, subdict)
    #assert limit==r, "read bytes ({}) are not equal to total ({}) in {}".format(r, limit, subdict)
    for k in list(collected_fields.keys()):
        lc.add_data(k, collected_fields[k])
    return

# gets, in order, the file object, chunk's name (string), chunk object used for parsing the file, LeafChunk object and bytes to be explored
# the LeafChunk object is populated with the parsed fields
def parse_chunk_data(file, chunk_name, current_chunk, lc, limit):
    _acfd = acfd()

    # index chunks
    if chunk_name == 'idx1' or chunk_name == 'indx' or chunk_name[:2] == 'ix' or chunk_name[-2:] == 'ix':
        parse_index(file, chunk_name, current_chunk, lc, limit, _acfd)

    # stream format chunks
    elif chunk_name == 'strf':
        parse_strf(file, _acfd, current_chunk, lc, limit)

    # unknown chunk
    elif chunk_name not in [k[:4] for k in list(_acfd.keys())]:
        raw_data = current_chunk.read(limit)
        lc.add_rawdata(raw_data)

    # other known chunks
    else:
        collected_fields, r = collect_fields(file,0, limit, current_chunk, _acfd[chunk_name])
        # check if bytes read are equal to the passed limit value
        assert limit==r, "read bytes ({}) are not equal to total ({})".format(r, limit)
        for k in list(collected_fields.keys()):
            lc.add_data(k, collected_fields[k])
    return
