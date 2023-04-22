from src.preferences.Item import Item
from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue

from typing import Dict


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.
    """

    def __init__(
        self,
        items_with_infos: Dict[Item, Dict[CriterionName, CriterionValue]],
    ):
        """Creates a new Preferences object."""
        self.items_with_infos = items_with_infos
        self.items = list(items_with_infos.keys())
        self.__criterion_name_list = [c for c in CriterionName]
        self.__criterion_value_list = [c for c in CriterionValue]

    def get_criterion_name_list(self):
        """Returns the list of criterion name."""
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value."""
        return self.__criterion_value_list

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name."""
        return self.items_with_infos[item][criterion_name]

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2."""
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def get_item_score(self, item):
        """Returns the score of the Item"""
        criterion_weight = 100
        sum_result = 0
        for criterion_name in self.get_criterion_name_list():
            sum_result += criterion_weight * self.get_value(item, criterion_name).value
            criterion_weight = criterion_weight / 2
        return sum_result

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2."""
        return self.get_item_score(item_1) > self.get_item_score(item_2)

    def most_preferred(self, item_list):
        """Returns the most preferred item from a list."""
        max = 0
        preferred = None
        for item in item_list:
            score = self.get_item_score(self, item)
            if score > max:
                max = score
                preferred = item
        return preferred

    def is_item_among_top_10_percent(self, item, item_list):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        scores = [self.get_item_score(x) for x in item_list]
        scores.sort()
        ten_percent = scores[::-1][int(len(scores) * 0.1)]
        return self.get_item_score(item) >= ten_percent
