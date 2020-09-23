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
        with pytest.raises(AssertionError):
            assert 10 in my_set


class TestFilled:
    """Tests for non-empty set"""
    def test_length(self):
        length = random.randint(100, 1000)
        my_set = {i ** 2 for i in range(length)}
        assert len(my_set) == length

    @pytest.mark.parametrize('i', list(range(100)))
    def test_values(self, i):
        length = random.randint(100, 1000)
        my_set = {str(i) for i in range(length)}
        assert str(i) in my_set

    def test_clear(self):
        length = random.randint(100, 1000)
        my_set = {range(length)}
        my_set.clear()
        assert not my_set
