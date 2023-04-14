# !/usr/bin/env python 3

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from preferences.Value import Value
from preferences.Preferences import Preferences
from agent.CommunicatingAgent import Agent



class Argument:
    # Argument class.
    # The class implements an argument used during the interaction.

    # attr:
    #     decision:
    #     item:
    #     comparison_list:
    #     couple_value_list:

    def __init__(self, boolean_decision, item, Agent):
        self.decision = boolean_decision
        self.item = item
        self.Agent = Agent
        self.preference = Agent.get_preference()
        self.comparison_list = []
        self.couple_values_list = []


    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        # Adds a premiss comparison in the comparison list.
        if self.preference.is_preferred_criterion(criterion_name_1,criterion_name_2):
            comparaison = Comparison(criterion_name_1, criterion_name_2)
            self.comparison_list.append(comparaison)

        else : 
            comparaison = Comparison(criterion_name_2, criterion_name_1)
            self.comparison_list.append(comparaison)

    def add_premiss_couple_values(self, criterion_name, value):
        # Add a premiss couple values in the couple values list.
        couplevalue = CoupleValue(criterion_name, value)
        self.couple_values_list.append(couplevalue)

    def List_supporting_proposal(self, item, preferences):
        pos_reason = []
        for criteria in self.preference.get_criterion_name_list():
            if (preferences.get_value(item, criteria) == Value.GOOD) or (preferences.get_value(item, criteria) == Value.VERY_GOOD):
                pos_reason.append(criteria)
        return pos_reason

    def List_attacking_proposal(self, item, preferences):
        neg_reason = []
        for criteria in self.preference.get_criterion_name_list():
            if (preferences.get_value(item, criteria) == Value.BAD) or (preferences.get_value(item, criteria) == Value.VERY_BAD):
                neg_reason.append(criteria)
        return neg_reason

