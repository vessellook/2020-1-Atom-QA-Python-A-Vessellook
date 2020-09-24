"""tests for int type"""
import math
import pytest


def test_zero_divisision():
    with pytest.raises(ZeroDivisionError):
        - 1 / 0


class TestRoot:
    def test_negative_root(self):
        with pytest.raises(ValueError):
            math.sqrt(-16)

    @pytest.mark.parametrize("i", list(range(100)))
    def test_positive_root(self, i):
        assert math.sqrt(i**2) == i


class TestStringConversion:
    """Tests for conversion from other types to string"""
    def test_negative(self):
        with pytest.raises(ValueError):
            int('19.7')

    def test_equal(self):
        assert int('19') == 19
