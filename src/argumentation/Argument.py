from typing import Dict, List

from src.agent.ArgumentAgent import ArgumentAgent
from src.preferences.Item import Item


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
        all_arguments=[],
    ):
        self.favorable = favorable
        self.item = item
        self.preference = agent.preference.items_with_infos
        self.agent = agent
        self.proposals = []
        self.counter_proposals = []
        self.last_argument = last_argument
        self.all_arguments = all_arguments
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
        elif self.favorable:
            return self.get_best_counter()
        else:
            return self.get_other_item_with_better_value_for_same_criterion()

    def get_best(self):
        best_value = -1
        best = None
        for x in self.proposals:
            if (
                x[1].value > best_value
                and [self.item, x[0], x[1]] not in self.all_arguments
            ):
                best = x
        if best == None:
            return None
        return [self.item, best[0], best[1]]

    def get_best_counter(self):
        self.get_counter_proposal()
        best_value = -1
        best = None
        for x in self.counter_proposals:
            if (
                x[1].value > best_value
                and [self.item, x[0], x[1]] not in self.all_arguments
            ):
                best = x
        if best == None:
            return None
        return [self.item, best[0], best[1]]

    def get_counter_proposal(self):
        if self.favorable == True:
            cond = lambda x: x >= 3
        else:
            cond = lambda x: x < 3
        for criterion in self.preference[self.item]:
            if self.agent.preference.is_preferred_criterion(
                criterion, self.last_argument[1]
            ):
                if cond(self.preference[self.item][criterion].value):
                    self.counter_proposals.append(
                        [criterion, self.preference[self.item][criterion]]
                    )
        return None

    def get_other_item_with_better_value_for_same_criterion(self):
        for item in self.list_items:
            if item != self.item:
                if (
                    self.preference[item][self.last_argument[1]].value
                    > self.last_argument[2].value
                ):
                    if [
                        item,
                        self.last_argument[1],
                        self.preference[item][self.last_argument[1]],
                    ] not in self.all_arguments:
                        return [
                            item,
                            self.last_argument[1],
                            self.preference[item][self.last_argument[1]],
                        ]
                    else:
                        pass
        else:
            return None

    def __str__(self) -> str:
        return f"{self.get_argument()[0].get_name()} {self.get_argument()[1].name} {self.get_argument()[2].name}"
