import chunk
from avi_chunk import ListChunk, LeafChunk
import xml.etree.cElementTree as ET
import codecs
# per filtrare i campi da caratteri di controllo
from unicodedata import category
import string

import utils

import argparse

import os

# gets the file and the bytes it has to explore within the file, returns the list of chunks dicovered
def search_list(file, limit):
    chunks = list()
    bytes_explored = 0

    while (bytes_explored<limit):
        explored_chunk = None
        try:
            current_chunk = chunk.Chunk(file, bigendian=False)
            current_chunk_name = current_chunk.getname()
            current_chunk_size = current_chunk.getsize()
            # if it's a LIST chunk call recurivelly this function
            if current_chunk_name == b'LIST':
                current_chunk_type = current_chunk.read(4)
                explored_chunk = ListChunk(current_chunk_name, current_chunk_size, current_chunk_type)
                subchunks = search_list(file, current_chunk_size - 4)
                explored_chunk.add_subchunks(subchunks)

            # if it's a basic chunk call the utils function to collect its fields ('parse_chunk_data')
            elif bytes_explored + current_chunk_size + 8 <= limit:
                explored_chunk = LeafChunk(current_chunk_name, current_chunk_size)

                utils.parse_chunk_data(file, current_chunk_name.decode('utf-8'), current_chunk, explored_chunk, current_chunk_size)

            # to avoid the chunk to be inserted in the wrong LIST chunk
            else:
                file.seek(-8,1)

        except EOFError:
            print('eof')
            break#return

        if explored_chunk is not None:
            bytes_explored = bytes_explored + explored_chunk.get_size() + 8
            chunks.append(explored_chunk)
        else:
            break
    return chunks

def alert_control_chars(s):
    warning = False
    for ch in s:
        if category(ch)[0] == "C":
            warning = True
    return warning

def populate_xml(parent, et_parent, show_data_chunks, verbose):
    log_strings = list()
    child = 1
    for c in parent.subchunks:
        # if the chunk is a LIST call this function recurivelly
        if type(c) is ListChunk:
            node = ET.SubElement(et_parent, 'LIST' + '-' + str(child))
            node.set("size-1", str(c.get_size()))
            node.set("type-0", c.get_type().decode('utf-8'))
            # recursive call
            ls = populate_xml(c, node, show_data_chunks, verbose)
            log_strings += ls
        else:
            # for LIST movi subchunks check for the "show_data_chunks" flag
            # this specifies if stream data chunks can be shown in the xml.
            # Moreover a special case for the subindex chunks is managed.
            if parent.get_type() == b'movi':
                name=c.get_name().decode('utf-8')

                nameChars = name[2:]

                # subindex special case: some files can have indexes
                # identified for example as 'ix01' instead of '01ix'
                if name[0] and name[1] in string.ascii_letters:

                    if verbose:
                        log_s = "Managed chunk #{} : that is {} instead of standard style: ##CC ".format(str(child), name)
                        print(log_s)
                        log_strings.append(log_s)
                    nameChars = name[:2]
                if show_data_chunks or ( (not show_data_chunks) and (nameChars == 'ix') ):
                    node = ET.SubElement(et_parent, 'stream' + '-' + str(child))

                    frame_type = nameChars
                    if frame_type == 'db':
                        frame_type = 'Uncompressed video'
                    if frame_type == 'dc':
                        frame_type = 'Compressed video'
                    if frame_type == 'pc':
                        frame_type = 'Palette change'
                    if frame_type == 'wb':
                        frame_type = 'Audio data'
                    if frame_type == 'ix':
                        frame_type = 'Subindex'

                    node.set("type", frame_type)
                    node.set("origin", name)
            else:
                # other basic chunks
                node = ET.SubElement(et_parent, c.get_name().decode('utf-8') + '-' +str(child))
                node.set("size-0", str(c.get_size()))

                c_dict = c.get_data()
                c_dict_keys = list(c_dict.keys())

                if len(c_dict) != 0:
                    for i in range(len(c_dict)):
                        key = c_dict_keys[i]

                        # special case in which the decoded field contains control characters which are not decoded
                        w = alert_control_chars(str(c_dict[key]))
                        if w:

                            if verbose:
                                log_s = "Control characters are present in chunk '{}' (#{}): field '{}' (#{}) is {}".format(
                                    c.get_name().decode('utf-8'), str(child), key, str(i), str(c_dict[key]).encode('utf-8'))
                                print('WARNING: \n' + log_s)
                                log_strings.append(log_s)

                            node.set(key + '-' + str(i + 1), str(c_dict[key].encode("utf-8")))
                        else:
                            node.set(key + '-' + str(i + 1), str(c_dict[key]))

                else:
                    node.set("rawData-1", str(c.get_rawdata()))
        child += 1
    return log_strings

def get_file_size(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    fileobject.seek(0,0)
    return size

def main(filename, verbose, output_path, log_path, show_data_chunks):
    file = open(filename, 'rb')
    file_size = get_file_size(file)

    log_strings = list()

    # xml root tag
    root = ET.Element("root")
    title = filename.split('/')[-1]
    root.set('filename', title)
    root.set('size', str(file_size))

    bytes_explored = 0
    while(bytes_explored<file_size):
        riff = chunk.Chunk(file, bigendian=False)

        # get the RIFF  'AVI ' chunk of the file
        riff_name = riff.getname()
        riff_size = riff.getsize()

        if riff_name == b'RIFF':
            riff_type = riff.read(4)
            riffchunk = ListChunk(riff_name, riff_size, riff_type)
            # parse the chunk. This is a recurrent function over the list chunks in the file
            avi_chunks = search_list(file, riff_size-4)

            # add the collected chunks
            riffchunk.add_subchunks(avi_chunks)

            # xml tag for the RIFF chunk
            rifftree = ET.SubElement(root,"RIFF")
            rifftree.set('type', riff_type.decode('utf-8'))
            rifftree.set('size', str(riff_size))

            # recursive function to create xml tags and set the reltive attributes
            log_strings = populate_xml(riffchunk, rifftree, show_data_chunks, verbose)

        else:
            print(riff_name)
            raw = file.read(riff_size)
            unknown = LeafChunk("unknown", len(raw))
            unknown.add_rawdata(raw)

            node = ET.SubElement(root, "unknown")
            node.set('rawData', str(unknown.get_rawdata()))

        bytes_explored += riff_size + 8

    # write the xml file

    if not os.path.exists('./xmls') and output_path is None:
        os.makedirs('./xmls')

    output_name = ('./xmls/'+title.split('.')[0] + "-tree.xml") if output_path is None else output_path
    xmlfile = open(output_name, 'w')
    data = ET.tostring(root, encoding="unicode")
    data = '<?xml version="1.0" encoding="UTF-8"?>'+ data
    xmlfile.write(data)
    xmlfile.close()

    file.close()

    # if log string where collected write a log file
    if len(log_strings)>0:
        # create the log file

        if not (os.path.exists('./logs')) and log_path is None:
            os.makedirs('./logs')

        output_log = ('./logs/'+title.split('.')[0] + "-log.txt") if log_path is None else log_path
        log_file = open(output_log, 'w')
        for ls in log_strings:
            log_file.write(ls+'\n')
        log_file.close()

    return None

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='path to the AVI file')
parser.add_argument('-v', '--verbose', type=str, default="True", help='Verbosity flag for warnings (default: False)')
parser.add_argument('-o', '--out', type=str, default=None, help='path and name of the XML file created (default: ./xmls/<AVI filename>-tree.xml)')
parser.add_argument('-l', '--log', type=str, default=None, help='path and name of the log file created (default: ./logs/<AVI filename>-log.txt)')
parser.add_argument('-m', '--movi', type=str, default="True", help='flag to show stream chunks in movi list (default: True)')

args = parser.parse_args()

if args.movi == 'False' or args.movi == 'false' or args.movi == 'FALSE':
    args.movi = False
elif args.movi == 'True' or args.movi == 'true' or args.movi == 'TRUE':
    args.movi = True
else:
    raise ValueError("ERROR: the movi argument is not valid")


if args.verbose == 'False' or args.verbose == 'false' or args.verbose == 'FALSE':
    args.verbose = False
elif args.verbose == 'True' or args.verbose == 'true' or args.verbose == 'TRUE':
    args.verbose = True
else:
    raise ValueError("ERROR: the verbose argument is not valid")

main(args.path, verbose=args.verbose, output_path=args.out, log_path=args.log, show_data_chunks=args.movi)

#main('avi_samples/sample.AVI', verbose=True, output_path=None, log_path=None, show_data_chunks=True)
