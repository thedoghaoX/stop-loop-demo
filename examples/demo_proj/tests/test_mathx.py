from mathx import median


def test_single():
    assert median([5]) == 5


def test_odd_unsorted():
    assert median([3, 1, 2]) == 2


def test_even_sorted():
    assert median([1, 2, 3, 4]) == 2.5


def test_even_unsorted():
    assert median([4, 1, 3, 2]) == 2.5
