from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences

from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value


class ArgumentAgent(CommunicatingAgent):
    def __init__(self, unique_id, model, name, List_items):
        super().__init__(unique_id, model, name)
        self.preference = self.generate_preferences(List_items)

    def step(self):
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, List_items):
        """
        Takes a dictionnary like {Item: {CriterionName: Value}}
        """
        pref = Preferences()
        for item in List_items.keys():
            pref.add_criterion_value(
                CriterionValue(item, List_items[item][0], List_items[item][1])
            )
        return pref


class ArgumentModel(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        # To be completed
        #
        # a = ArgumentAgent ( id , " agent_name ")
        # a . generate_preferences ( preferences )
        # self . schedule . add ( a )
        # ...
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == " __main__ ":
    argument_model = ArgumentModel()

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    electric_engine = Item("Electric Engine", "A very quiet engine")

    A1_preferences = {
        diesel_engine: {
            CriterionName.PRODUCTION_COST: Value.VERY_GOOD,
            CriterionName.CONSUMPTION: Value.GOOD,
            CriterionName.DURABILITY: Value.VERY_GOOD,
            CriterionName.ENVIRONMENT_IMPACT: Value.BAD,
            CriterionName.NOISE: Value.AVERAGE,
        },
        electric_engine: {
            CriterionName.PRODUCTION_COST: Value.AVERAGE,
            CriterionName.CONSUMPTION: Value.BAD,
            CriterionName.DURABILITY: Value.GOOD,
            CriterionName.ENVIRONMENT_IMPACT: Value.VERY_GOOD,
            CriterionName.NOISE: Value.VERY_GOOD,
        },
    }

    A2_preferences = {
        diesel_engine: {
            CriterionName.PRODUCTION_COST: Value.GOOD,
            CriterionName.CONSUMPTION: Value.AVERAGE,
            CriterionName.DURABILITY: Value.GOOD,
            CriterionName.ENVIRONMENT_IMPACT: Value.BAD,
            CriterionName.NOISE: Value.BAD,
        },
        electric_engine: {
            CriterionName.PRODUCTION_COST: Value.GOOD,
            CriterionName.CONSUMPTION: Value.AVERAGE,
            CriterionName.DURABILITY: Value.AVERAGE,
            CriterionName.ENVIRONMENT_IMPACT: Value.VERY_GOOD,
            CriterionName.NOISE: Value.VERY_GOOD,
        },
    }

    A1 = ArgumentAgent(
        unique_id=1, model=argument_model, name="Nicolas", preferences=A1_preferences
    )
    A2 = ArgumentAgent(
        unique_id=2, model=argument_model, name="Thomas", preferences=A2_preferences
    )
