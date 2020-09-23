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
            assert my_list.pop()


class TestFilled:
    """Tests for non-empty list"""
    def test_length(self):
        length = random.randint(100, 1000)
        my_list = [i / 2 for i in range(length)]
        assert len(my_list) == length

    @pytest.mark.parametrize('i', list(range(100)))
    def test_values(self, i):
        length = random.randint(100, 1000)
        my_list = list(range(length))
        assert my_list[i] == i

    def test_pop(self):
        length = random.randint(100, 1000)
        my_list = list(range(length))
        for i in range(length):
            my_list.pop()
        assert not my_list
