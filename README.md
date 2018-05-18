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

When in the projects folder run the command `python main.py filename.avi`, this will parse the file and generate:
* **xmls** folder in the project's directory if not already existing;
* a **filename-tree.xml** file in the *xmls* folder;
* (eventually) **logs** folder in the project's directory if not already existing;
* (eventually) a **filename-log.txt** file in the *logs* folder.

Alternatively there is the possibility to specify the path and file name of the outputted XML and log file. For example:

`python main.py filename.avi -o path/to/output/file.xml`

In this case no "*xmls*" folder will be created. Eventually a **logs** folder with a **filename-log.txt** file will be created.

Finally there is also the possibility to specify the path in which to create the log file if needed. For example:


`python main.py filename.avi -o path/to/output/file.xml -l path/to/log/file.txt`


In this case not folder will be created.

The following optional arguments are available:

*  **-h, --help**           show this help message and exit
*  **-v** VERBOSE, **--verbose** VERBOSE     Verbosity flag for warnings (default: True)
*  **-o** OUT, **--out** OUT     path and name of the XML file created (default: ./xmls/[AVI filename]-tree.xml)
*  **-l** LOG, **--log** LOG     path and name of the log file created (default: ./logs/[AVI filename]-log.txt)
*  **-m** MOVI, **--movi** MOVI  flag to show stream chunks in movi list (default: True)

Only known chunks' content will be correctly interpreted.

## Authors
* [Aurel Pjetri](https://github.com/aurelpjetri)
* [Matteo Nesti](https://github.com/emmeenne93)
