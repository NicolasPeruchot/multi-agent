from src.agent.CommunicatingAgent import CommunicatingAgent
from src.preferences.Item import Item
from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue
from src.preferences.Preferences import Preferences

from typing import Dict


class ArgumentAgent(CommunicatingAgent):
    def __init__(
        self,
        unique_id,
        name,
        items_with_infos: Dict[Item, Dict[CriterionName, CriterionValue]],
        model=None,
    ):
        super().__init__(unique_id, model, name)
        self.items_with_infos = items_with_infos
        self.preference = self.generate_preferences()

    def step(self):
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self):
        return Preferences(self.items_with_infos)
