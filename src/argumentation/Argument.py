from src.agent.ArgumentAgent import ArgumentAgent


from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue
from src.preferences.Item import Item

from typing import List, Dict


class Argument:
    # Argument class.
    # The class implements an argument used during the interaction.

    def __init__(
        self,
        favorable: bool,
        item: Item,
        list_items: List[Item],
        agent: ArgumentAgent,
        last_argument=None,
    ):
        self.favorable = favorable
        self.item = item
        self.preference = agent.preference.items_with_infos
        self.proposals = []
        self.last_argument = last_argument
        self.list_items = list_items
        self.get_proposal()

    def get_proposal(self):
        if self.favorable == True:
            cond = lambda x: x >= 3
        else:
            cond = lambda x: x < 3
        for criterion in self.preference[self.item]:
            if cond(self.preference[self.item][criterion].value):
                self.proposals.append(
                    [criterion, self.preference[self.item][criterion]]
                )
        return None

    def get_argument(self):
        if self.last_argument == None:
            return self.get_best()
        else:
            return self.get_other_item_with_better_value_for_same_criterion()

    def get_best(self):
        best_value = -1
        best = []
        for x in self.proposals:
            if x[1].value > best_value:
                best = x[1].value
                best = x
        return [self.item, best[0], best[1]]

    def get_other_item_with_better_value_for_same_criterion(self):
        for item in self.list_items:
            if item != self.item:
                if (
                    self.preference[item][self.last_argument[1]].value
                    > self.last_argument[2].value
                ):
                    return [
                        item,
                        self.last_argument[1],
                        self.preference[item][self.last_argument[1]],
                    ]
        else:
            return None

    def __str__(self) -> str:
        return f"{self.best[0].get_name()} {self.best[1].name} {self.best[2].name}"
