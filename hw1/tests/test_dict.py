"""tests for dict type"""
import random
import pytest


class TestEmpty:
    """Tests for empty dict"""
    def test_length(self):
        my_dict = {}
        assert len(my_dict) == 0

    def test_negative(self):
        my_dict = {}
        with pytest.raises(KeyError):
            my_dict.pop(10)


class TestFilled:
    """Tests for non-empty dict"""
    def test_length(self):
        length = random.randint(100, 1000)
        my_dict = {}
        for i in range(length):
            my_dict[i] = (i - 7) * 2 + 1
        assert len(my_dict) == length

    @pytest.mark.parametrize(
        'key, value, expected', [
            (1, '1', {1: '1'}),
            (2, '2', {2: '2'})
        ])
    def test_equal(self, key, value, expected):
        my_dict = {key: value}
        assert my_dict == expected

    def test_pop(self):
        length = random.randint(100, 1000)
        my_dict = {}
        for i in range(length):
            my_dict[i] = str(i)
        for i in range(length):
            my_dict.pop(i)
        assert not my_dict
