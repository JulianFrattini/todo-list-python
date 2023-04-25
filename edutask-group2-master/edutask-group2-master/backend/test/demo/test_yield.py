import pytest
import json, os

class FileHandler:
    def __init__(self, filename):
        with open(filename, 'r') as readfile:
            self.file = json.load(readfile)

    def getContent(self):
        return self.file

class TestFileHandler:
    """This test demonstrates the use of yield as an alternative to return, which allows to write code *after* the statement
    which will be executed once all tests have run. This can be used for cleanup."""

    @pytest.fixture
    def sut(self):
        fabricatedFileName = 'fabricatedUser.json'
        self.json_string = {'Name': 'John'}
        with open(fabricatedFileName, 'w') as outfile:
            json.dump(self.json_string, outfile)

        # yield instead of return the system under test
        yield FileHandler(filename=fabricatedFileName)

        # clean up the file after all tests have run
        os.remove(fabricatedFileName)

    @pytest.mark.demo
    def test_getContent(self, sut):
        content = sut.getContent()
        assert content['Name'] == self.json_string['Name']

