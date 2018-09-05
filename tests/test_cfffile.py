from cffreader import reader
from pykwalifire.errors import SchemaError, SchemaConflict
from requests import HTTPError
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

        cfffile = reader.CFFfile(text, initialise_empty=True)

        assert cfffile.get_version() == "1.0.3"

    def test_schema(self):
        data = {
            'cff-version': "1.0.3",
            'message': "test data",
            'authors': [{"given-names":"foo",
                         "family-names":"bar"}],
            'date-released': "2001-01-01",
            'title': "test title",
            'version': "1.2.3",
        }

        cfffile = reader.CFFfile(cffdict=data, initialise_empty=True)

        try:
            cfffile.get_schema()
        except HTTPError:
            pytest.fail("Failed to get schema from web")

    def test_required_fields(self):
        data = {"cff-version": "1.0.3"}
        cfffile = reader.CFFfile(cffdict=data, initialise_empty=True)

        expected_fields = ['cff-version', 'message', 'authors',
                           'date-released', 'title', 'version']

        assert cfffile.required_fields() == expected_fields

    def test_validate(self):
        data = {
            'cff-version': "1.0.3",
            'message': "test data",
            'authors': [{"given-names":"foo",
                         "family-names":"bar"}],
            'date-released': "2001-01-01",
            'title': "test title",
            'version': "1.2.3",
        }

        cfffile = reader.CFFfile(cffdict=data, initialise_empty=True)

        try:
            assert cfffile.validate()
        except (SchemaError, SchemaConflict):
            pytest.fail("Failed to validate against schema")



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
