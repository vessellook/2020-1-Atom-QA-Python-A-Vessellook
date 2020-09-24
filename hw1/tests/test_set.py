"""tests for set type"""
import random
import pytest


class TestEmpty:
    """Tests for empty set"""
    def test_length(self):
        my_set = set()
        assert len(my_set) == 0

    def test_negative(self):
        my_set = set()
        assert 10 not in my_set



class TestFilled:
    """Tests for non-empty set"""
    def test_length(self):
        length = random.randint(100, 1000)
        my_set = {i ** 2 for i in range(length)}
        assert len(my_set) == length

    @pytest.mark.parametrize('values, expected', [
        ([1, 2, 3, 4], {1, 2, 3, 4})
    ])
    def test_convertion(self, values, expected):
        assert {i for i in values} == expected

    def test_clear(self):
        length = random.randint(100, 1000)
        my_set = {range(length)}
        my_set.clear()
        assert not my_set
