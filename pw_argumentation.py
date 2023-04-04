from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value


class ArgumentAgent(CommunicatingAgent):
    def __init__(self, unique_id, model, name, list_items):
        super().__init__(unique_id, model, name)
        self.list_items = list_items
        self.preference = self.generate_preferences()

    def step(self):
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self):
        """
        Takes a dictionnary like {Item: {CriterionName: Value}}
        """
        pref = Preferences()
        for item in self.list_items.keys():
            for criterion in self.list_items[item].keys():
                pref.add_criterion_value(
                    CriterionValue(item, criterion, self.list_items[item][criterion])
                )
        return pref


class ArgumentModel(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
        self.electric_engine = Item("Electric Engine", "A very quiet engine")
        A1_preferences = {
            self.diesel_engine: {
                CriterionName.PRODUCTION_COST: Value.VERY_GOOD,
                CriterionName.CONSUMPTION: Value.GOOD,
                CriterionName.DURABILITY: Value.VERY_GOOD,
                CriterionName.ENVIRONMENT_IMPACT: Value.BAD,
                CriterionName.NOISE: Value.AVERAGE,
            },
            self.electric_engine: {
                CriterionName.PRODUCTION_COST: Value.AVERAGE,
                CriterionName.CONSUMPTION: Value.BAD,
                CriterionName.DURABILITY: Value.GOOD,
                CriterionName.ENVIRONMENT_IMPACT: Value.VERY_GOOD,
                CriterionName.NOISE: Value.VERY_GOOD,
            },
        }

        A2_preferences = {
            self.diesel_engine: {
                CriterionName.PRODUCTION_COST: Value.GOOD,
                CriterionName.CONSUMPTION: Value.AVERAGE,
                CriterionName.DURABILITY: Value.GOOD,
                CriterionName.ENVIRONMENT_IMPACT: Value.BAD,
                CriterionName.NOISE: Value.BAD,
            },
            self.electric_engine: {
                CriterionName.PRODUCTION_COST: Value.GOOD,
                CriterionName.CONSUMPTION: Value.AVERAGE,
                CriterionName.DURABILITY: Value.AVERAGE,
                CriterionName.ENVIRONMENT_IMPACT: Value.VERY_GOOD,
                CriterionName.NOISE: Value.VERY_GOOD,
            },
        }

        self.A1 = ArgumentAgent(
            unique_id=1,
            model=self,
            name="Nicolas",
            list_items=A1_preferences,
        )
        self.A2 = ArgumentAgent(
            unique_id=2,
            model=self,
            name="Thomas",
            list_items=A2_preferences,
        )
        self.schedule.add(self.A1)
        self.schedule.add(self.A2)
        self.running = True

    def step(self):
        message = Message(
            "Nicolas",
            "Thomas",
            message_performative=MessagePerformative.PROPOSE,
            content=self.electric_engine,
        )

        self.A1.send_message(message)

        propositions = self.A2.get_messages_from_performative(
            MessagePerformative.PROPOSE
        )

        for proposition in propositions:
            if self.A2.preference.is_item_among_top_10_percent(
                proposition.get_content(),
                item_list=self.A1.list_items.keys(),
            ):
                message = Message(
                    "Thomas",
                    "Nicolas",
                    message_performative=MessagePerformative.ACCEPT,
                    content="Ouais go",
                )
                self.A2.send_message(message)

                self.A1.send_message(
                    Message(
                        "Thomas",
                        "Nicolas",
                        message_performative=MessagePerformative.COMMIT,
                        content="",
                    )
                )

                self.A2.send_message(
                    Message(
                        "Nicolas",
                        "Thomas",
                        message_performative=MessagePerformative.COMMIT,
                        content="",
                    )
                )
                del self.A1.list_items[proposition.get_content()]
                self.A1.generate_preferences()
                del self.A2.list_items[proposition.get_content()]
                self.A2.generate_preferences()
            else:
                message = Message(
                    "Nicolas",
                    "Thomas",
                    message_performative=MessagePerformative.ARGUE,
                    content="?",
                )

                self.A1.send_message(message)
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()
    argument_model.step()
