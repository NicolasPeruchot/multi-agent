#!/usr/bin/env python3


class Item:
    """Item class.
    This class implements the objects about which the argument will be conducted.

    attr:
        name: the name of the item
        description: the description of the item
    """

    def __init__(self, name, description):
        """Creates a new Item."""
        self.__name = name
        self.__description = description

    def __str__(self):
        """Returns Item as a String."""
        return self.__name + " (" + self.__description + ")"

    def get_name(self):
        """Returns the name of the item."""
        return self.__name

    def get_description(self):
        """Returns the description of the item."""
        return self.__description
