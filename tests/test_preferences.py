from src.preferences.Preferences import Preferences
from src.preferences.Item import Item
from src.preferences.CriterionName import CriterionName
from src.preferences.CriterionValue import CriterionValue


def test_one():
    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    electric_engine = Item("Electric Engine", "A very quiet engine")

    pref = {
        diesel_engine: {
            CriterionName.PRODUCTION_COST: CriterionValue.GOOD,
            CriterionName.CONSUMPTION: CriterionValue.AVERAGE,
            CriterionName.DURABILITY: CriterionValue.GOOD,
            CriterionName.ENVIRONMENT_IMPACT: CriterionValue.BAD,
            CriterionName.NOISE: CriterionValue.BAD,
        },
        electric_engine: {
            CriterionName.PRODUCTION_COST: CriterionValue.GOOD,
            CriterionName.CONSUMPTION: CriterionValue.AVERAGE,
            CriterionName.DURABILITY: CriterionValue.AVERAGE,
            CriterionName.ENVIRONMENT_IMPACT: CriterionValue.VERY_GOOD,
            CriterionName.NOISE: CriterionValue.VERY_GOOD,
        },
    }

    preference = Preferences(items_with_infos=pref)
    assert (
        preference.get_value(diesel_engine, CriterionName.CONSUMPTION)
        == CriterionValue.AVERAGE
    )
    assert preference.get_item_score(diesel_engine) == 493.75
    assert preference.is_preferred_item(electric_engine, diesel_engine) == True
    assert (
        preference.is_item_among_top_10_percent(
            electric_engine, [diesel_engine, diesel_engine, diesel_engine]
        )
        == True
    )
