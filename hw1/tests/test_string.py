"""tests for string type"""
from string import ascii_lowercase, ascii_uppercase
import pytest


class TestEmpty:
    """Tests for empty string"""
    def test_length(self):
        string = ""
        assert len(string) == 0

    def test_index(self):
        string = ""
        with pytest.raises(IndexError):
            string[10]


class TestTypeConversion:
    def test_from_int(self):
        assert str(19) == '19'

    def test_from_float(self):
        assert str(19.5) == '19.5'


@pytest.mark.parametrize("i", list(range(26)))
def test_uppercase(i):
    assert ascii_uppercase[i] == ascii_lowercase.upper()[i]
