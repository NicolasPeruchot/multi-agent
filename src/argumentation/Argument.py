from mesa import Model
from mesa.time import RandomActivation

from src.agent.ArgumentAgent import ArgumentAgent

from src.communication.MessageService import MessageService
from src.preferences.Preferences import Preferences
from src.communication.Message import Message
from src.communication.MessagePerformative import MessagePerformative

from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue
from src.preferences.Item import Item

from typing import List, Dict


class Argument:
    # Argument class.
    # The class implements an argument used during the interaction.

    def __init__(self, favorable: bool, item: Item, agent: ArgumentAgent):
        self.favorable = favorable
        self.item = item
        self.Agent = agent
        self.preference: Dict[
            CriterionName, CriterionValue
        ] = agent.preference.items_with_infos[self.item]
        self.proposals = []
        self.get_proposal()
        self.best = self.get_best()

    def get_proposal(self):
        if self.favorable == True:
            cond = lambda x: x >= 3
        else:
            cond = lambda x: x < 3
        for criterion in self.preference:
            if cond(self.preference[criterion].value):
                self.proposals.append([criterion, self.preference[criterion]])
        return None

    def display_proposal(self):
        readable_proposals = [
            f"{CriterionName(x[0].value).name}: {CriterionValue(x[1].value).name}"
            for x in self.proposals
        ]
        return readable_proposals

    def get_best(self):
        best_value = -1
        best = []
        for x in self.proposals:
            if x[1].value > best_value:
                best = x[1].value
                best = x
        return best

    def __str__(self) -> str:
        return f"{self.best[0].name} {self.best[1].name}"
