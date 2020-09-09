from py42.constants import SortDirection


class TestSortDirection(object):
    def test_choices_are_correct(self):
        actual = SortDirection.choices()
        expected = ["DESC", "ASC"]
        assert set(actual) == set(expected)
