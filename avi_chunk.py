class AviChunk(object):
    def __init__(self, name):
        self.name = name

    def get_size(self):
        raise NotADirectoryError('this is a generic chunk, you have to use one of the subclasses')

    def to_string(self, verbose=False):
        return None

class ListChunk(AviChunk):
    def __init__(self, name, size, chunktype, sub_chunks=None):
        self.name = name
        self.size = size
        self.chunktype = chunktype
        if sub_chunks is None:
            self.subchunks = list()
        else:
            self.subchunks = sub_chunks

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def get_type(self):
        return self.chunktype

    def get_subchunks(self):
        return self.subchunks

    def add_subchunk(self, chunk):
        self.subchunks.append(chunk)

    def add_subchunks(self, chunks):
        self.subchunks = self.subchunks + chunks

    def to_string(self, verbose=False):
        _str = "{} {}\n  ".format(str(self.get_name()),str(self.get_type()))
        for c in self.subchunks:
            _str += "{}\n".format(c.to_string(verbose=verbose))
        return _str

class LeafChunk(AviChunk):
    def __init__(self, name, size, data=None):
            self.name = name
            self.size = size
            # self.dict_data = dict()
            self.has_rawdata = False
            self.raw_data = data
            self.data_dict = dict()

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def add_data(self, field, value):
        # pos in an int specifying the position of the field within the chunk
        self.data_dict[field]=value

    def get_data(self):
        return self.data_dict

    def get_rawdata(self):
        self.has_rawdata = True
        return self.raw_data

    def add_rawdata(self, data):
        self.raw_data = data

    def to_string(self, verbose=False):
        if verbose:
            _str = "{}\n  {}\n".format(str(self.get_name()), str(self.get_rawdata()))
        else:
            _str = "{}\n  [...]\n".format(str(self.get_name()))
        return _str
