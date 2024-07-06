from typing import TypedDict, List

from BaseClasses import ItemClassification
from .Names import ItemName


class ItemDict(TypedDict):
    id: int
    name: str
    count: int
    classification: ItemClassification


item_table: List[ItemDict] = [
    {"id": 2, "name": ItemName.Tails.StoryUnlock, "count": 1, "classification": ItemClassification.progression},
    {"id": 3, "name": ItemName.Knuckles.StoryUnlock, "count": 1, "classification": ItemClassification.progression},
    {"id": 4, "name": ItemName.Amy.StoryUnlock, "count": 1, "classification": ItemClassification.progression},
    {"id": 5, "name": ItemName.Gamma.StoryUnlock, "count": 1, "classification": ItemClassification.progression},
    {"id": 6, "name": ItemName.Big.StoryUnlock, "count": 1, "classification": ItemClassification.progression},

    {"id": 10, "name": ItemName.Sonic.LightShoes, "count": 1, "classification": ItemClassification.progression},
    {"id": 11, "name": ItemName.Sonic.CrystalRing, "count": 1, "classification": ItemClassification.useful},
    {"id": 12, "name": ItemName.Sonic.AncientLight, "count": 1, "classification": ItemClassification.progression},

    {"id": 20, "name": ItemName.Tails.JetAnkle, "count": 1, "classification": ItemClassification.progression},
    {"id": 21, "name": ItemName.Tails.RhythmBadge, "count": 1, "classification": ItemClassification.useful},

    {"id": 30, "name": ItemName.Knuckles.ShovelClaw, "count": 1, "classification": ItemClassification.progression},
    {"id": 31, "name": ItemName.Knuckles.FightingGloves, "count": 1, "classification": ItemClassification.useful},

    {"id": 40, "name": ItemName.Amy.LongHammer, "count": 1, "classification": ItemClassification.useful},
    {"id": 41, "name": ItemName.Amy.WarriorFeather, "count": 1, "classification": ItemClassification.useful},

    {"id": 50, "name": ItemName.Gamma.LaserBlaster, "count": 1, "classification": ItemClassification.useful},
    {"id": 51, "name": ItemName.Gamma.JetBooster, "count": 1, "classification": ItemClassification.progression},

    {"id": 60, "name": ItemName.Big.LifeBelt, "count": 1, "classification": ItemClassification.progression},
    {"id": 61, "name": ItemName.Big.PowerRod, "count": 1, "classification": ItemClassification.useful},

    {"id": 90, "name": ItemName.Progression.Emblem, "count": 32, "classification": ItemClassification.progression},

    {"id": 91, "name": ItemName.Progression.ChaosPeace, "count": 0, "classification": ItemClassification.progression},

]


def get_item_name(item_id: int) -> str:
    item = get_item(item_id)
    return item["name"]


def get_item(item_id: int) -> ItemDict:
    for item in item_table:
        if item["id"] == item_id:
            return item
