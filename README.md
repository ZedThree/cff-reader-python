# cff-reader-python
A python reader for the Citation File Format (cff). It can load cff
files locally or from github repositories, and provides a class for
citations.

Heavily based on https://github.com/citation-file-format/cff-converter-python

## Getting started

Download the code and install using 

    pip install --user .
    
in the download folder. 

Use the code by importing into your own python file:
```python
import cffreader
```

## Usage examples
Read from a local CITATION.cff file:
```python
citation = cffreader.reader(from_filename="CITATION.cff")
```

Read from a github repository (eg this one!):
```python
citation = cffreader.reader(from_url="https://github.com/ZedThree/cff-reader-python")
```

## Running the tests
Tests are written using pytest. Run pytest in the toplevel. 

## Acknowledgments
Some code from the cff-convertor-python project at https://github.com/citation-file-format/cff-converter-python/

Initial code developed at the cff-file-format hackday
