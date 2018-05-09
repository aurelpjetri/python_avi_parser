# Python AVI Parser

This program is an AVI parser written in Python. It parses the given AVI file and generates an XML file representing its chunk tree structure.

Written by [Aurel Pjetri](https://github.com/aurelpjetri) and [Matteo Nesti](https://github.com/emmeenne93).

## Requirements

Package | Version
:-------: | :-------:
[Python](https://www.python.org/downloads/) | 3.6.2

It should work also with other versions of Python.

## Used Python Packages

* [chunk](https://docs.python.org/3/library/chunk.html)
* [xml.etree.cElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)

## Running the Project

When in the projects folder run the command `python main.py filename.avi`, this will parse the file and generate an xml file named *filename-tree.xml* and eventually a log file named *filename-log.txt*.

The following optional arguments are available:

*  **-h, --help**           show this help message and exit
*  **-v** VERBOSE, **--verbose** VERBOSE     Verbosity flag for warnings (default: True)
*  **-o** OUT, **--out** OUT     XML filename (default: <AVI filename>-tree.xml)
*  **-l** LOG, **--log** LOG     log filename (default: <AVI filename>-log.txt)
*  **-m** MOVI, **--movi** MOVI  flag to show stream chunks in movi list (default: True)
*  **-xd** XMLDIR, **--xmldir** XMLDIR directory path for the generated xml (default: ./xmls/)
*  **-ld** LOGDIR, **--logdir** LOGDIR directory path for the log eventually generated (default: ./logs/)

Only known chunks' content will be correctly interpreted.

## Authors
* [Aurel Pjetri](https://github.com/aurelpjetri)
* [Matteo Nesti](https://github.com/emmeenne93)
