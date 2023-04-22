from mesa import Model
from mesa.time import RandomActivation

from src.agent.ArgumentAgent import ArgumentAgent

from src.communication.MessageService import MessageService
from src.preferences.Preferences import Preferences
from src.communication.Message import Message
from src.communication.MessagePerformative import MessagePerformative

from src.argumentation.Argument import Argument

from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue
from src.preferences.Item import Item

from typing import List


class ArgumentModel(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
        self.electric_engine = Item("Electric Engine", "A very quiet engine")
        A1_preferences = {
            self.diesel_engine: {
                CriterionName.PRODUCTION_COST: CriterionValue.VERY_GOOD,
                CriterionName.CONSUMPTION: CriterionValue.GOOD,
                CriterionName.DURABILITY: CriterionValue.VERY_GOOD,
                CriterionName.ENVIRONMENT_IMPACT: CriterionValue.BAD,
                CriterionName.NOISE: CriterionValue.AVERAGE,
            },
            self.electric_engine: {
                CriterionName.PRODUCTION_COST: CriterionValue.AVERAGE,
                CriterionName.CONSUMPTION: CriterionValue.BAD,
                CriterionName.DURABILITY: CriterionValue.GOOD,
                CriterionName.ENVIRONMENT_IMPACT: CriterionValue.VERY_GOOD,
                CriterionName.NOISE: CriterionValue.VERY_GOOD,
            },
        }

        A2_preferences = {
            self.diesel_engine: {
                CriterionName.PRODUCTION_COST: CriterionValue.GOOD,
                CriterionName.CONSUMPTION: CriterionValue.AVERAGE,
                CriterionName.DURABILITY: CriterionValue.GOOD,
                CriterionName.ENVIRONMENT_IMPACT: CriterionValue.BAD,
                CriterionName.NOISE: CriterionValue.BAD,
            },
            self.electric_engine: {
                CriterionName.PRODUCTION_COST: CriterionValue.GOOD,
                CriterionName.CONSUMPTION: CriterionValue.AVERAGE,
                CriterionName.DURABILITY: CriterionValue.AVERAGE,
                CriterionName.ENVIRONMENT_IMPACT: CriterionValue.VERY_GOOD,
                CriterionName.NOISE: CriterionValue.VERY_GOOD,
            },
        }

        self.A1 = ArgumentAgent(
            unique_id=1,
            model=self,
            name="Nicolas",
            items_with_infos=A1_preferences,
        )
        self.A2 = ArgumentAgent(
            unique_id=2,
            model=self,
            name="Thomas",
            items_with_infos=A2_preferences,
        )
        self.schedule.add(self.A1)
        self.schedule.add(self.A2)
        self.running = True

    def step(self):
        message = Message(
            "Nicolas",
            "Thomas",
            message_performative=MessagePerformative.PROPOSE,
            content=self.diesel_engine,
        )

        self.A1.send_message(message)

        propositions: List[Message] = self.A2.get_messages_from_performative(
            MessagePerformative.PROPOSE
        )

        for proposition in propositions:
            item = proposition.get_content()
            if self.A2.preference.is_item_among_top_10_percent(
                item,
                item_list=[self.electric_engine, self.diesel_engine],
            ):
                message = Message(
                    "Thomas",
                    "Nicolas",
                    message_performative=MessagePerformative.ACCEPT,
                    content=item,
                )
                self.A2.send_message(message)

                self.A1.send_message(
                    Message(
                        "Thomas",
                        "Nicolas",
                        message_performative=MessagePerformative.COMMIT,
                        content=item,
                    )
                )

                self.A2.send_message(
                    Message(
                        "Nicolas",
                        "Thomas",
                        message_performative=MessagePerformative.COMMIT,
                        content=item,
                    )
                )
                del self.A1.items_with_infos[proposition.get_content()]
                self.A1.generate_preferences()
                del self.A2.items_with_infos[proposition.get_content()]
                self.A2.generate_preferences()
            else:
                message = Message(
                    "Thomas",
                    "Nicolas",
                    message_performative=MessagePerformative.ASK_WHY,
                    content=item,
                )
                self.A2.send_message(message)

                message = Message(
                    "Nicolas",
                    "Thomas",
                    message_performative=MessagePerformative.ARGUE,
                    content=[
                        item.__str__(),
                        Argument(True, item, self.A1).__str__(),
                    ],
                )
                self.A2.send_message(message)

        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()
    argument_model.step()
