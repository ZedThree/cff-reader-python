from cffreader import reader

class TestCFFfile:
    def test_version(self):
        datafile = "/home/peter/Codes/citation-file-format/cff-reader-python/CITATION.cff"
        with open(datafile, 'r') as f:
            text = f.read()

        cfffile = reader.CFFfile(text)

        assert cfffile.get_version() == "1.0.3"
