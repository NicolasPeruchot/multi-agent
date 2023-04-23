from src.agent.ArgumentAgent import ArgumentAgent
from src.argumentation.Argument import Argument
from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue
from src.preferences.Item import Item

diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
electric_engine = Item("Electric Engine", "A very quiet engine")
A1_preferences = {
    diesel_engine: {
        CriterionName.PRODUCTION_COST: CriterionValue.VERY_GOOD,
        CriterionName.CONSUMPTION: CriterionValue.GOOD,
        CriterionName.DURABILITY: CriterionValue.VERY_GOOD,
        CriterionName.ENVIRONMENT_IMPACT: CriterionValue.BAD,
        CriterionName.NOISE: CriterionValue.AVERAGE,
    },
    electric_engine: {
        CriterionName.PRODUCTION_COST: CriterionValue.AVERAGE,
        CriterionName.CONSUMPTION: CriterionValue.VERY_GOOD,
        CriterionName.DURABILITY: CriterionValue.GOOD,
        CriterionName.ENVIRONMENT_IMPACT: CriterionValue.VERY_GOOD,
        CriterionName.NOISE: CriterionValue.VERY_GOOD,
    },
}
A1 = ArgumentAgent(
    unique_id=1,
    name="Nicolas",
    items_with_infos=A1_preferences,
)


def test_supporting():
    supporting = Argument(True, diesel_engine, [diesel_engine, electric_engine], A1)
    assert supporting.__str__() == "Diesel Engine DURABILITY VERY_GOOD"


def test_attacking():
    non_supporting = Argument(
        False, diesel_engine, [diesel_engine, electric_engine], A1
    )
    assert non_supporting.__str__() == "Diesel Engine NOISE AVERAGE"


def test_counter():
    counter = Argument(
        True,
        diesel_engine,
        [diesel_engine, electric_engine],
        A1,
        last_argument=[electric_engine, CriterionName.DURABILITY, CriterionValue.GOOD],
    )
    assert counter.__str__() == "Diesel Engine DURABILITY VERY_GOOD"


def test_better_item():
    non_supporting = Argument(
        False,
        diesel_engine,
        [electric_engine, diesel_engine],
        A1,
        last_argument=[diesel_engine, CriterionName.CONSUMPTION, CriterionValue.GOOD],
    )

    assert non_supporting.__str__() == "Electric Engine CONSUMPTION VERY_GOOD"
