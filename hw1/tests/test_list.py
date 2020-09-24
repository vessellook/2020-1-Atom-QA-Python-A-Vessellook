"""tests for list type"""
import random
import pytest


class TestEmpty:
    """Tests for empty list"""

    def test_length(self):
        my_list = []
        assert len(my_list) == 0

    def test_negative(self):
        my_list = []
        with pytest.raises(IndexError):
            my_list.pop()


class TestFilled:
    """Tests for non-empty list"""

    def test_length(self):
        length = random.randint(100, 1000)
        my_list = [i / 2 for i in range(length)]
        assert len(my_list) == length

    def test_pop(self):
        length = random.randint(100, 1000)
        my_list = list(range(length))
        for i in range(length):
            my_list.pop()
        assert not my_list

    @pytest.mark.parametrize(
        'values, expected', [
            ([1, 5, 3, 2, 4], [1, 2, 3, 4, 5]),
            (['a', 'c', 'd', 'f'], ['a', 'c', 'd', 'f'])
        ])
    def test_values(self, values, expected):
        values.sort()
        assert values == expected
