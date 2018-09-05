import re
import yaml


class Reader:
    def __init__(self, url=None, filename=None):
        # Either get the file from url
        # Or open and read filename

        # Create and return CFFfile
        pass


class CFFfile:
    def __init__(self, text):
        self.cffstr = text
        # self._parse_yaml()
        self.version = None
        self.version = self.get_version()

    def _parse_yaml(self):
        self.cffyaml = yaml.safe_load(self.cffstr)
        if not isinstance(self.yaml, dict):
            raise ValueError("Provided CITATION.cff does not seem valid YAML.")

    def get_version(self):
        if self.version is not None:
            return self.version

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
