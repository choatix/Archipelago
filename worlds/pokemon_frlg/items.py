from typing import Dict, FrozenSet, Optional
from BaseClasses import Item, ItemClassification
from .data import data, BASE_OFFSET


class PokemonFRLGItem(Item):
    game: str = "Pokemon FireRed and LeafGreen",
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: int) -> int:
    return item_value + BASE_OFFSET


def reverse_offset_item_value(item_id: int) -> int:
    return item_id - BASE_OFFSET


def create_item_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from item names to their AP item ID (code)
    """
    name_to_id_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        name_to_id_map[attributes.name] = offset_item_value(item_value)

    return name_to_id_map


def get_item_classification(item_id: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[reverse_offset_item_value(item_id)].classification
