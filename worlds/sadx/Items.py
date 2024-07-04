from BaseClasses import ItemClassification
from typing import TypedDict, Dict, List, Set


class ItemDict(TypedDict):
    id: int
    name: str
    count: int
    classification: ItemClassification


item_table: List[ItemDict] = [
    {"id": 2, "name": "Story unlock (Tails)", "count": 1, "classification": ItemClassification.progression},
    {"id": 3, "name": "Story unlock (Knuckles)", "count": 1, "classification": ItemClassification.progression},
    {"id": 4, "name": "Story unlock (Amy)", "count": 1, "classification": ItemClassification.progression},
    {"id": 5, "name": "Story unlock (Gamma)", "count": 1, "classification": ItemClassification.progression},
    {"id": 6, "name": "Story unlock (Big)", "count": 1, "classification": ItemClassification.progression},

    {"id": 10, "name": "Light shoes (Sonic)", "count": 1, "classification": ItemClassification.progression},
    {"id": 11, "name": "Crystal ring (Sonic)", "count": 1, "classification": ItemClassification.useful},
    {"id": 12, "name": "Ancient light (Sonic)", "count": 1, "classification": ItemClassification.progression},

    {"id": 20, "name": "Jet Ankle (Tails)", "count": 1, "classification": ItemClassification.progression},
    {"id": 21, "name": "Rhythm Badge (Tails)", "count": 1, "classification": ItemClassification.useful},

    {"id": 30, "name": "Shovel claw (Knuckles)", "count": 1, "classification": ItemClassification.progression},
    {"id": 31, "name": "Fighting gloves (Knuckles)", "count": 1, "classification": ItemClassification.useful},

    {"id": 40, "name": "Long Hammer (Amy)", "count": 1, "classification": ItemClassification.useful},
    {"id": 41, "name": "Warrior feather (Amy)", "count": 1, "classification": ItemClassification.useful},

    {"id": 50, "name": "Laser Blaster (Gamma)", "count": 1, "classification": ItemClassification.useful},
    {"id": 51, "name": "Jet booster (Gamma)", "count": 1, "classification": ItemClassification.progression},

    {"id": 60, "name": "Life belt (Big)", "count": 1, "classification": ItemClassification.progression},
    {"id": 61, "name": "Power rod (Big)", "count": 1, "classification": ItemClassification.useful},

]


def get_item_name(item_id: int) -> str:
    item = get_item(item_id)
    return item["name"]


def get_item(item_id: int) -> ItemDict:
    for item in item_table:
        if item["id"] == item_id:
            return item