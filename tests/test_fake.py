def test_divide_by_zero():
    try:
        1/0
    except ZeroDivisionError:
        assert 1 == 1
