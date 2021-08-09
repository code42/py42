from py42.util import get_attribute_keys_from_class


class Choices:
    """Helper class to provide the choices() method to a class."""

    @classmethod
    def choices(cls):
        """Returns attribute names for the given class.

        Returns:
            (list): A list containing the attribute names of the given class.
        """
        return get_attribute_keys_from_class(cls)
