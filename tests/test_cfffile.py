from cffreader import reader
import pytest


@pytest.fixture
def valid_cff_filename():
    '''We can use our own CFF file as a test; if it isn't valid we have problems!'''
    return "CITATION.cff"

    
    
class TestCFFfile:
    def test_version(self, valid_cff_filename):
        datafile = valid_cff_filename
        with open(datafile, 'r') as f:
            text = f.read()

        cfffile = reader.CFFfile(text)

        assert cfffile.get_version() == "1.0.3"



def test_reader_from_filename(valid_cff_filename):
    assert isinstance(reader.reader(from_filename=valid_cff_filename),dict)
    
def test_reader_from_file(valid_cff_filename):
    with open(valid_cff_filename, 'r') as f:
        assert isinstance(reader.reader(from_file=f),dict)
        
def test_reader_from_url():
    testurl = "https://github.com/ZedThree/cff-reader-python/"
    assert isinstance(reader.reader(from_url=testurl),dict)
    
def test_reader_exception_notgithuburl():
    with pytest.raises(Exception):
        reader.reader("Imnaeaurl")

def test_reader_exception_typourl():
    with pytest.raises(Exception):
        reader.reader("https://github.com/ZedThree/cff-reader-python-imatypo/")
        
def test_reader_value_error_noinput():
    with pytest.raises(ValueError):
        reader.reader()
        
def test_reader_value_error_invalid():
    with pytest.raises(ValueError):
        reader.reader(from_filename="tests/invalid_yaml.cff")
        
def test_reader_value_error_filename_insteadoffile(valid_cff_filename):
    with pytest.raises(ValueError):
        reader.reader(from_file=valid_cff_filename)
