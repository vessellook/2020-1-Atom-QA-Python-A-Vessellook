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
            assert my_dict.pop(10)


class TestFilled:
    """Tests for non-empty dict"""
    def test_length(self):
        length = random.randint(100, 1000)
        my_dict = {}
        for i in range(length):
            my_dict[i] = (i - 7) * 2 + 1
        assert len(my_dict) == length

    @pytest.mark.parametrize('k', list(range(100)))
    def test_values(self, k):
        length = random.randint(100, 1000)
        my_dict = {}
        for i in range(length):
            my_dict[i] = str(i)
        assert my_dict[k] == str(k)

    def test_pop(self):
        length = random.randint(100, 1000)
        my_dict = {}
        for i in range(length):
            my_dict[i] = str(i)
        for i in range(length):
            my_dict.pop(i)
        assert not my_dict
