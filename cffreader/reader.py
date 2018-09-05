import re
import requests
import yaml
import sys
import contextlib
import requests


CFF_CORE_SCHEMA_URL = ("https://raw.githubusercontent.com/citation-file-format"
                       "/schema/{0}/CFF-Core/schema.yaml")


@contextlib.contextmanager
def smart_open(filename, mode='Ur'):
    """Open stdin or stdout using a contextmanager
    From: http://stackoverflow.com/a/29824059/2043465
    """
    if filename == '-':
        if mode is None or mode == '' or 'r' in mode:
            fh = sys.stdin
        else:
            fh = sys.stdout
    else:
        fh = open(filename, mode)
    try:
        yield fh
    finally:
        if filename is not '-':
            fh.close()


def reader(from_filename=None, from_file=None,from_url=None):
    ''' Reads a cff file from filename, open file, stdin (specify from_filename='-') or url and returns a dictionary.'''

    #Need to first get the input and turn it into a string.

    if from_filename:
        with smart_open(from_filename, 'r') as f:
            cffstr = f.read()

    elif from_file:
        if isinstance(from_file, str):
            raise ValueError("Please pass a filename using argument from_filename.")

        cffstr = from_file.read()

    elif from_url:
        if from_url.startswith("https://github.com"):
            #We know how to handle github urls so can continue
            #URL could be a link to a repository or the citation file
            baseurl = "https://raw.githubusercontent.com"

            regexp = re.compile("^" +
                                "(?P<baseurl>https://github\.com)/" +
                                "(?P<org>[^/\n]*)/" +
                                "(?P<repo>[^/\n]*)" +
                                "(/tree/(?P<label>[^/\n]*))?", re.IGNORECASE)

            matched = re.match(regexp, from_url)
            if matched is None:
                raise Exception("Error extracting (user|organization) and/or repository " +
                                "information from the provided URL ({0}).".format(from_url))
            else:
                url_parts = matched.groupdict()

            file_url = "/".join([baseurl,
                                url_parts["org"],
                                url_parts["repo"],
                                url_parts["label"] if url_parts["label"] is not None else "master",
                                "CITATION.cff"])

            r = requests.get(file_url)
            if r.ok:
                cffstr = r.text
            else:
                raise Exception("Error requesting file: {0}".format(file_url))

        else:
            raise Exception("Only 'https://github.com' URLs are supported at the moment.")

    else:
        raise ValueError("You should specify the file/filename to read, url to read from or stdin")


    cffdict = yaml.safe_load(cffstr)
    if not isinstance(cffdict, dict):
        raise ValueError("Provided CITATION.cff does not seem valid YAML.")

    return cffdict

class CFFfile:
    def __init__(self, text, initialise_empty=False):
        self.cffstr = text
        # self._parse_yaml()
        if not initialise_empty:
            self._version = self.get_version()
            self._schema = self.get_schema()

    def _parse_yaml(self):
        self.cffyaml = yaml.safe_load(self.cffstr)
        if not isinstance(self.yaml, dict):
            raise ValueError("Provided CITATION.cff does not seem valid YAML.")

    def get_version(self):
        """Get the Citation File Format version number of the file

        """

        if hasattr(self, "_version") and self._version is not None:
            return self._version

        regexp = re.compile("^cff-version: (['|\"])?(?P<semver>[\d\.]*)(['\"])?\s*$")
        semver = None
        for line in self.cffstr.split("\n"):
            matched = re.match(regexp, line)
            if matched is not None:
                semver = matched.groupdict()["semver"]
                break

        if semver is None:
            raise ValueError("Unable to identify the schema version. Does the CFF include the 'cff-version' key?")

        return semver

    def get_schema(self):
        """Get the schema for the version of the file

        """
        if hasattr(self, "_schema") and self._schema is not None:
            return self._schema

        semver = self.get_version()
        r = requests.get(CFF_CORE_SCHEMA_URL.format(semver))
        r.raise_for_status()
        return r.text

    def validate(self):
        pass


if __name__ == "__main__":
    cffdict = reader(from_filename="../CITATION.cff")
    print(cffdict)
