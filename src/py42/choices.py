from py42.util import get_attribute_values_from_class


class Choices:
    """Helper class to provide the choices() method to a class."""

    @classmethod
    def choices(cls):
        """Returns attribute values for the given class.

        Returns:
            (list): A list containing the attribute values of the given class.
        """
        return get_attribute_values_from_class(cls)
