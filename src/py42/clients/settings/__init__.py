def set_val(d, keys, value):
    """Helper for setting nested values from a dict based on a list of keys."""
    d = get_val(d, keys[:-1])
    d[keys[-1]] = value


def get_val(d, keys):
    """Helper for getting nested values from a dict based on a list of keys."""
    for key in keys:
        d = d[key]
    return d


def show_change(val1, val2):
    if isinstance(val1, str):
        val1 = f'"{val1}"'
    if isinstance(val2, str):
        val2 = f'"{val2}"'
    return f"{val1} -> {val2}"


class BaseSettingProperty:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.init_val = None

    def _register_change(self, instance, orig_val, new_val):
        name = self.name.lstrip("_")
        if self.init_val is None:
            self.init_val = orig_val
        if self.init_val == new_val:
            if name in instance.changes:
                instance.changes.pop(name)
        else:
            instance.changes[name] = show_change(self.init_val, new_val)


class SettingProperty(BaseSettingProperty):
    """Descriptor class to help manage changes to nested dict values. Assumes attributes
    being managed are on a UserDict/UserList subclass.

    Args:
        name (str): name of attribute this class manages (changes will be registered with this name).
        location (list): list of keys defining the location of the value being managed in the managed class.
        get_converter (func, optional): function to convert retrieved values to preferred format. Defaults to no conversion.
        set_converter (func, optional): function to convert values being set to preferred format. Defaults to no conversion.
    """

    def __init__(
        self,
        name,
        location,
        get_converter=None,
        set_converter=None,
        inheritance_attr=None,
    ):
        super().__init__(name, location)
        self.get_converter = get_converter
        self.set_converter = set_converter
        self.inheritance_attr = inheritance_attr

    def __get__(self, instance, owner):
        val = get_val(instance.data, self.location)
        if isinstance(val, dict) and "#text" in val.keys():
            val = val["#text"]
        return self.get_converter(val) if self.get_converter is not None else val

    def __set__(self, instance, new_val):
        converted_new_val = (
            self.set_converter(new_val) if self.set_converter is not None else new_val
        )
        orig_val = get_val(instance.data, self.location)

        # if locked, value is a dict with '#text' as the _real_ value key. Some properties will have dicts with @nil: true, these should stay dicts, as the whole dict is the property value.
        if isinstance(orig_val, dict) and "#text" in orig_val.keys():
            location = self.location + ["#text"]
            orig_val = orig_val["#text"]
        else:
            location = self.location

        self._register_change(instance, orig_val, converted_new_val)
        if self.inheritance_attr is not None and getattr(
            instance, self.inheritance_attr
        ):
            setattr(instance, self.inheritance_attr, False)
        set_val(instance.data, location, converted_new_val)


class TSettingProperty:
    """Descriptor class to help manage transforming t_setting packet values. Assumes t_setting
    dict is stored in `._t_settings` attribute on managed instances.

    Args:
        name (str): name of attribute this class manages (changes will be registered with this name).
        key (str): name of t_setting packet this class is managing.
    """

    def __init__(self, name, key, get_converter=None, set_converter=None):
        self.name = name
        self.key = key
        self.get_converter = get_converter
        self.set_converter = set_converter
        self.init_val = None

    def __get__(self, instance, owner):
        if self.key in instance._packets:
            packet = instance._packets[self.key]
        else:
            packet = instance._t_settings.get(self.key)
        if packet is None:
            return None
        return (
            self.get_converter(packet["value"])
            if self.get_converter is not None
            else packet["value"]
        )

    def __set__(self, instance, val):
        val = self.set_converter(val) if self.set_converter is not None else val
        packet = {"key": self.key, "value": val, "locked": False}
        instance._packets[self.key] = packet
        self._register_change(instance, val)

    def _register_change(self, instance, val):
        if self.init_val is None:
            packet = instance._t_settings.get(self.key)
            if packet is None:
                self.init_val = None
            else:
                self.init_val = packet["value"]
        if self.init_val == val:
            if self.name in instance.changes:
                instance.changes.pop(self.name)
        else:
            instance.changes[self.name] = show_change(self.init_val, val)


def check_lock(locked_attr):
    """Decorator for instance methods that enforces a property to be read-only if the
    `.locked` attribute of the provided `locked_attr` on the instance returns True.
    """

    def f(method):
        def func(_self, *args):
            if getattr(_self, locked_attr).locked:
                raise AttributeError("Unable to modify locked backup set.")
            else:
                return method(_self, *args)

        return func

    return f
