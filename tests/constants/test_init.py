from pycpg.constants import SortDirection


class TestSortDirection:
    def test_choices_are_correct(self):
        actual = SortDirection.choices()
        expected = ["DESC", "ASC"]
        assert set(actual) == set(expected)
