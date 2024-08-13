from dataclasses import dataclass
from typing import TypedDict, List

from BaseClasses import ItemClassification, Item
from .Enums import Character, SADX_BASE_ID
from .Names import ItemName


@dataclass
class StoryProgressionItem:
    itemId: int
    name: str


@dataclass
class CharacterUnlockItem:
    itemId: int
    character: Character
    name: str


@dataclass
class CharacterUpgradeItem:
    itemId: int
    character: Character
    name: str
    classification: ItemClassification


@dataclass
class KeyItem:
    itemId: int
    name: str


@dataclass
class FillerItem:
    itemId: int
    name: str


@dataclass
class TrapItem:
    itemId: int
    name: str


class ItemInfo(TypedDict):
    id: int
    name: str
    count: int
    classification: ItemClassification


story_progression_item_table: List[StoryProgressionItem] = [
    StoryProgressionItem(90, ItemName.Progression.Emblem),
    StoryProgressionItem(91, ItemName.Progression.ChaosPeace),
    StoryProgressionItem(92, ItemName.Progression.WhiteEmerald),
    StoryProgressionItem(93, ItemName.Progression.RedEmerald),
    StoryProgressionItem(94, ItemName.Progression.CyanEmerald),
    StoryProgressionItem(95, ItemName.Progression.PurpleEmerald),
    StoryProgressionItem(96, ItemName.Progression.GreenEmerald),
    StoryProgressionItem(97, ItemName.Progression.YellowEmerald),
    StoryProgressionItem(98, ItemName.Progression.BlueEmerald),
]

character_unlock_item_table: List[CharacterUnlockItem] = [

    CharacterUnlockItem(1, Character.Sonic, ItemName.Sonic.Playable),
    CharacterUnlockItem(2, Character.Tails, ItemName.Tails.Playable),
    CharacterUnlockItem(3, Character.Knuckles, ItemName.Knuckles.Playable),
    CharacterUnlockItem(4, Character.Amy, ItemName.Amy.Playable),
    CharacterUnlockItem(5, Character.Gamma, ItemName.Gamma.Playable),
    CharacterUnlockItem(6, Character.Big, ItemName.Big.Playable),

]
character_upgrade_item_table: List[CharacterUpgradeItem] = [

    CharacterUpgradeItem(10, Character.Sonic, ItemName.Sonic.LightShoes, ItemClassification.progression),
    CharacterUpgradeItem(11, Character.Sonic, ItemName.Sonic.CrystalRing, ItemClassification.useful),
    CharacterUpgradeItem(12, Character.Sonic, ItemName.Sonic.AncientLight, ItemClassification.progression),

    CharacterUpgradeItem(20, Character.Tails, ItemName.Tails.JetAnklet, ItemClassification.progression),
    CharacterUpgradeItem(21, Character.Tails, ItemName.Tails.RhythmBadge, ItemClassification.useful),

    CharacterUpgradeItem(30, Character.Knuckles, ItemName.Knuckles.ShovelClaw, ItemClassification.progression),
    CharacterUpgradeItem(31, Character.Knuckles, ItemName.Knuckles.FightingGloves, ItemClassification.useful),

    CharacterUpgradeItem(40, Character.Amy, ItemName.Amy.WarriorFeather, ItemClassification.useful),
    CharacterUpgradeItem(41, Character.Amy, ItemName.Amy.LongHammer, ItemClassification.useful),

    CharacterUpgradeItem(50, Character.Gamma, ItemName.Gamma.JetBooster, ItemClassification.progression),
    CharacterUpgradeItem(51, Character.Gamma, ItemName.Gamma.LaserBlaster, ItemClassification.useful),

    CharacterUpgradeItem(60, Character.Big, ItemName.Big.LifeBelt, ItemClassification.progression),
    CharacterUpgradeItem(61, Character.Big, ItemName.Big.PowerRod, ItemClassification.useful),
    CharacterUpgradeItem(62, Character.Big, ItemName.Big.Lure1, ItemClassification.progression),
    CharacterUpgradeItem(63, Character.Big, ItemName.Big.Lure2, ItemClassification.progression),
    CharacterUpgradeItem(64, Character.Big, ItemName.Big.Lure3, ItemClassification.progression),
    CharacterUpgradeItem(65, Character.Big, ItemName.Big.Lure4, ItemClassification.progression),

]

filler_item_table: List[FillerItem] = [
    FillerItem(71, ItemName.Filler.Invincibility),
    FillerItem(72, ItemName.Filler.Rings5),
    FillerItem(73, ItemName.Filler.Rings10),
    FillerItem(74, ItemName.Filler.Shield),
    FillerItem(75, ItemName.Filler.MagneticShield),
    FillerItem(76, ItemName.Filler.ExtraLife),
]

key_item_table: List[KeyItem] = [
    KeyItem(80, ItemName.KeyItem.Train),
    KeyItem(81, ItemName.KeyItem.Boat),
    KeyItem(82, ItemName.KeyItem.Raft),
    KeyItem(83, ItemName.KeyItem.HotelKeys),
    KeyItem(84, ItemName.KeyItem.CasinoKeys),
    KeyItem(85, ItemName.KeyItem.TwinkleParkTicket),
    KeyItem(86, ItemName.KeyItem.EmployeeCard),
    KeyItem(87, ItemName.KeyItem.IceStone),
    KeyItem(88, ItemName.KeyItem.Dynamite),
    KeyItem(89, ItemName.KeyItem.JungleCart),
    KeyItem(120, ItemName.KeyItem.WindStone),
    KeyItem(121, ItemName.KeyItem.StationKeys),

]

trap_item_table: List[TrapItem] = [
    TrapItem(100, ItemName.Traps.IceTrap),
    TrapItem(101, ItemName.Traps.SpringTrap),
    TrapItem(102, ItemName.Traps.PoliceTrap),
    TrapItem(103, ItemName.Traps.BuyonTrap),
]


def get_progression_items() -> List[ItemInfo]:
    items: List[ItemInfo] = []
    for key in story_progression_item_table:
        items += [{"id": key.itemId, "name": key.name, "count": 0, "classification": ItemClassification.progression}]
    return items


def get_items_from_unlock() -> List[ItemInfo]:
    items: List[ItemInfo] = []
    for unlock in character_unlock_item_table:
        items += [{"id": unlock.itemId, "name": unlock.name, "count": 1,
                   "classification": ItemClassification.progression}]
    return items


def get_items_from_upgrades() -> List[ItemInfo]:
    items: List[ItemInfo] = []
    for upgrade in character_upgrade_item_table:
        items += [{"id": upgrade.itemId, "name": upgrade.name, "count": 1, "classification": upgrade.classification}]
    return items


def get_items_from_keys() -> List[ItemInfo]:
    items: List[ItemInfo] = []
    for key in key_item_table:
        items += [{"id": key.itemId, "name": key.name, "count": 1, "classification": ItemClassification.progression}]
    return items


def get_items_from_filler() -> List[ItemInfo]:
    items: List[ItemInfo] = []
    for key in filler_item_table:
        items += [{"id": key.itemId, "name": key.name, "count": 0, "classification": ItemClassification.filler}]
    return items


def get_items_from_traps() -> List[ItemInfo]:
    items: List[ItemInfo] = []
    for key in trap_item_table:
        items += [{"id": key.itemId, "name": key.name, "count": 0, "classification": ItemClassification.trap}]
    return items


class SonicAdventureDXItem(Item):
    game: str = "Sonic Adventure DX"

    def __init__(self, name: str, player, force_non_progression=False):
        item = get_item_by_name(name)
        classification = ItemClassification.filler if force_non_progression else item["classification"]
        super().__init__(item["name"], classification, item["id"] + SADX_BASE_ID, player)


all_item_table: List[ItemInfo] = (get_progression_items() + get_items_from_unlock() + get_items_from_upgrades()
                                  + get_items_from_keys() + get_items_from_filler() + get_items_from_traps())


def get_item_by_name(name: str) -> ItemInfo:
    for item in all_item_table:
        if item['name'] == name:
            return item


def get_item(item_id: int) -> ItemInfo:
    for item in all_item_table:
        if item["id"] == item_id:
            return item
