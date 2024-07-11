from dataclasses import dataclass
from typing import List, TypedDict

from BaseClasses import Location, Region
from .Enums import Area, Level, SubLevel, Character, KeyItem, LevelMission, Upgrade, EVERYONE, FLYERS, \
    SubLevelMission, pascal_to_space
from .Names import ItemName
from .Names.ItemName import EVERY_LURE


@dataclass
class LevelLocation:
    area: Area
    character: Character
    level: Level
    levelMission: LevelMission
    extraItems: List[str]

    def get_id(self) -> int:
        return 10000 * self.character.value + 100 * self.level.value + 1 * self.levelMission.value


@dataclass
class SubLevelLocation:
    locationId: int
    area: Area
    characters: List[Character]
    subLevel: SubLevel
    subLevelMission: SubLevelMission


@dataclass
class UpgradeLocation:
    locationId: int
    area: Area
    character: Character
    originalUpgrade: Upgrade
    extraItems: List[str]


@dataclass
class EmblemLocation:
    locationId: int
    area: Area
    characters: List[Character]
    emblemName: str


level_location_table: List[LevelLocation] = [
    # Station Square
    LevelLocation(Area.StationSquareMain, Character.Big, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(Area.StationSquareMain, Character.Big, Level.TwinklePark, LevelMission.B, EVERY_LURE),
    LevelLocation(Area.StationSquareMain, Character.Big, Level.TwinklePark, LevelMission.A, EVERY_LURE),
    LevelLocation(Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, LevelMission.C, []),
    LevelLocation(Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, LevelMission.B, []),
    LevelLocation(Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, LevelMission.A, []),
    LevelLocation(Area.Hotel, Character.Sonic, Level.EmeraldCoast, LevelMission.C, []),
    LevelLocation(Area.Hotel, Character.Sonic, Level.EmeraldCoast, LevelMission.B, []),
    LevelLocation(Area.Hotel, Character.Sonic, Level.EmeraldCoast, LevelMission.A, []),
    LevelLocation(Area.Hotel, Character.Big, Level.EmeraldCoast, LevelMission.C, []),
    LevelLocation(Area.Hotel, Character.Big, Level.EmeraldCoast, LevelMission.B, EVERY_LURE),
    LevelLocation(Area.Hotel, Character.Big, Level.EmeraldCoast, LevelMission.A, EVERY_LURE),
    LevelLocation(Area.Hotel, Character.Gamma, Level.EmeraldCoast, LevelMission.C, []),
    LevelLocation(Area.Hotel, Character.Gamma, Level.EmeraldCoast, LevelMission.B, []),
    LevelLocation(Area.Hotel, Character.Gamma, Level.EmeraldCoast, LevelMission.A, []),
    LevelLocation(Area.Casino, Character.Sonic, Level.Casinopolis, LevelMission.C, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Casino, Character.Sonic, Level.Casinopolis, LevelMission.B, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Casino, Character.Sonic, Level.Casinopolis, LevelMission.A, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.C, []),
    LevelLocation(Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.B, []),
    LevelLocation(Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.A, []),
    LevelLocation(Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.C, []),
    LevelLocation(Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.B, []),
    LevelLocation(Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.A, []),
    LevelLocation(Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.B, []),
    LevelLocation(Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.A, []),
    LevelLocation(Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.B, []),
    LevelLocation(Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.A, []),
    LevelLocation(Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, LevelMission.C, []),
    LevelLocation(Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, LevelMission.B, []),
    LevelLocation(Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, LevelMission.A, []),
    LevelLocation(Area.SpeedHighway, Character.Tails, Level.SpeedHighway, LevelMission.C, []),
    LevelLocation(Area.SpeedHighway, Character.Tails, Level.SpeedHighway, LevelMission.B, []),
    LevelLocation(Area.SpeedHighway, Character.Tails, Level.SpeedHighway, LevelMission.A, []),

    # Mystic Ruins
    LevelLocation(Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.C, []),
    LevelLocation(Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.B, []),
    LevelLocation(Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.A, []),
    LevelLocation(Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.C, []),
    LevelLocation(Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.B, []),
    LevelLocation(Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.A, []),
    LevelLocation(Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.C,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.B,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.A,
                  [ItemName.Gamma.JetBooster]),

    # TODO: Check if is okay to requiere Train or something more complex like "Station Square access"
    LevelLocation(Area.AngelIsland, Character.Sonic, Level.IceCap, LevelMission.C,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Sonic, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Sonic, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Tails, Level.IceCap, LevelMission.C,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Tails, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Tails, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.C,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train]),
    LevelLocation(Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, KeyItem.Train] + EVERY_LURE),
    LevelLocation(Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, KeyItem.Train] + EVERY_LURE),
    LevelLocation(Area.AngelIsland, Character.Sonic, Level.RedMountain, LevelMission.C,
                  [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LevelLocation(Area.AngelIsland, Character.Sonic, Level.RedMountain, LevelMission.B,
                  [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LevelLocation(Area.AngelIsland, Character.Sonic, Level.RedMountain, LevelMission.A,
                  [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LevelLocation(Area.AngelIsland, Character.Knuckles, Level.RedMountain, LevelMission.C,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.AngelIsland, Character.Knuckles, Level.RedMountain, LevelMission.B,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.AngelIsland, Character.Knuckles, Level.RedMountain, LevelMission.A,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.AngelIsland, Character.Gamma, Level.RedMountain, LevelMission.C, []),
    LevelLocation(Area.AngelIsland, Character.Gamma, Level.RedMountain, LevelMission.B, []),
    LevelLocation(Area.AngelIsland, Character.Gamma, Level.RedMountain, LevelMission.A, []),

    LevelLocation(Area.Jungle, Character.Sonic, Level.LostWorld, LevelMission.C, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Jungle, Character.Sonic, Level.LostWorld, LevelMission.B, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Jungle, Character.Sonic, Level.LostWorld, LevelMission.A, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Jungle, Character.Knuckles, Level.LostWorld, LevelMission.C, [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.Jungle, Character.Knuckles, Level.LostWorld, LevelMission.B, [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.Jungle, Character.Knuckles, Level.LostWorld, LevelMission.A, [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.Jungle, Character.Sonic, Level.FinalEgg, LevelMission.C, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Jungle, Character.Sonic, Level.FinalEgg, LevelMission.B, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Jungle, Character.Sonic, Level.FinalEgg, LevelMission.A, [ItemName.Sonic.LightShoes]),
    LevelLocation(Area.Jungle, Character.Amy, Level.FinalEgg, LevelMission.C, []),
    LevelLocation(Area.Jungle, Character.Amy, Level.FinalEgg, LevelMission.B, []),
    LevelLocation(Area.Jungle, Character.Amy, Level.FinalEgg, LevelMission.A, []),
    LevelLocation(Area.Jungle, Character.Gamma, Level.FinalEgg, LevelMission.C, []),
    LevelLocation(Area.Jungle, Character.Gamma, Level.FinalEgg, LevelMission.B, []),
    LevelLocation(Area.Jungle, Character.Gamma, Level.FinalEgg, LevelMission.A, []),
    # Egg Carrier
    LevelLocation(Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.C, []),
    LevelLocation(Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.B, []),
    LevelLocation(Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.A, []),
    LevelLocation(Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.C, []),
    LevelLocation(Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.B, []),
    LevelLocation(Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.A, []),
    LevelLocation(Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, LevelMission.C,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, LevelMission.B,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, LevelMission.A,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(Area.EggCarrierMain, Character.Amy, Level.HotShelter, LevelMission.C, []),
    LevelLocation(Area.EggCarrierMain, Character.Amy, Level.HotShelter, LevelMission.B, []),
    LevelLocation(Area.EggCarrierMain, Character.Amy, Level.HotShelter, LevelMission.A, []),
    LevelLocation(Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.C, []),
    LevelLocation(Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.B,
                  EVERY_LURE + [ItemName.Big.LifeBelt]),
    LevelLocation(Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.A,
                  EVERY_LURE + [ItemName.Big.LifeBelt]),
    LevelLocation(Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.C, []),
    LevelLocation(Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.B, []),
    LevelLocation(Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.A, []),
]

upgrade_location_table: List[UpgradeLocation] = [
    # Station Square
    UpgradeLocation(100, Area.StationSquareMain, Character.Sonic, Upgrade.LightShoes, [ItemName.Sonic.LightShoes]),
    UpgradeLocation(200, Area.StationSquareMain, Character.Tails, Upgrade.JetAnkle, []),
    UpgradeLocation(602, Area.StationSquareMain, Character.Big, Upgrade.Lure1, []),
    UpgradeLocation(101, Area.Hotel, Character.Sonic, Upgrade.CrystalRing, [ItemName.Sonic.LightShoes]),
    # Mystic Ruins
    UpgradeLocation(300, Area.MysticRuinsMain, Character.Knuckles, Upgrade.ShovelClaw, [ItemName.Knuckles.ShovelClaw]),
    UpgradeLocation(604, Area.AngelIsland, Character.Big, Upgrade.Lure3,
                    [KeyItem.IceStone, KeyItem.Train] + EVERY_LURE),
    UpgradeLocation(600, Area.AngelIsland, Character.Big, Upgrade.LifeBelt,
                    [KeyItem.IceStone, KeyItem.Train] + EVERY_LURE),
    UpgradeLocation(102, Area.AngelIsland, Character.Sonic, Upgrade.AncientLight, []),
    UpgradeLocation(301, Area.Jungle, Character.Knuckles, Upgrade.FightingGloves, []),
    UpgradeLocation(603, Area.Jungle, Character.Big, Upgrade.Lure2, []),
    UpgradeLocation(601, Area.Jungle, Character.Big, Upgrade.PowerRod, []),
    # Egg Carrier
    UpgradeLocation(400, Area.EggCarrierMain, Character.Amy, Upgrade.WarriorFeather, []),
    UpgradeLocation(401, Area.EggCarrierMain, Character.Amy, Upgrade.LongHammer, []),
    UpgradeLocation(500, Area.EggCarrierMain, Character.Gamma, Upgrade.JetBooster, []),
    UpgradeLocation(501, Area.EggCarrierMain, Character.Gamma, Upgrade.LaserBlaster, []),
    UpgradeLocation(605, Area.EggCarrierMain, Character.Big, Upgrade.Lure4, []),

]

sub_level_location_table: List[SubLevelLocation] = [
    SubLevelLocation(15, Area.TwinklePark, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.B),
    SubLevelLocation(16, Area.TwinklePark, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.A),
    SubLevelLocation(25, Area.Jungle, [Character.Sonic, Character.Tails], SubLevel.SandHill, SubLevelMission.B),
    SubLevelLocation(27, Area.Jungle, [Character.Sonic, Character.Tails], SubLevel.SandHill, SubLevelMission.A),
]

field_emblem_location_table: List[EmblemLocation] = [
    # Station Square
    EmblemLocation(10, Area.StationSquareMain, EVERYONE, "Station Emblem"),
    EmblemLocation(11, Area.StationSquareMain, EVERYONE, "Burger Shop Emblem"),
    EmblemLocation(12, Area.StationSquareMain, [Character.Knuckles, Character.Tails, Character.Amy],
                   "City Hall Emblem"),
    EmblemLocation(13, Area.Casino, FLYERS, "Casino Emblem"),
    # Mystic Ruins
    EmblemLocation(20, Area.MysticRuinsMain, FLYERS, "Tails' Workshop Emblem"),
    EmblemLocation(21, Area.AngelIsland, FLYERS, "Shrine Emblem"),
    EmblemLocation(22, Area.Jungle, EVERYONE, "Jungle Path Emblem"),
    EmblemLocation(23, Area.Jungle, FLYERS, "Tree Stump Emblem"),
    # Egg Carrier
    EmblemLocation(30, Area.EggCarrierMain, FLYERS, "Pool Emblem"),
    EmblemLocation(31, Area.EggCarrierMain, FLYERS, "Spinning Platform Emblem"),
    EmblemLocation(32, Area.EggCarrierMain, [Character.Sonic, Character.Tails, Character.Knuckles],
                   "Hidden Bed Emblem"),
    EmblemLocation(33, Area.EggCarrierMain, [Character.Sonic, Character.Tails], "Main Platform Emblem"),

]


class LocationInfo(TypedDict):
    id: int
    name: str


def get_location_from_level() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for level in level_location_table:
        level_id: int = level.get_id()
        level_name: str = f"{pascal_to_space(level.level.name)} ({level.character.name} - Mission {level.levelMission.name})"
        locations += [{"id": level_id, "name": level_name}]
    return locations


def get_location_from_upgrade() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for upgrade in upgrade_location_table:
        upgrade_name = f"{pascal_to_space(upgrade.originalUpgrade.name)} Upgrade Point ({upgrade.character.name})"
        locations += [{"id": upgrade.locationId, "name": upgrade_name}]
    return locations


def get_location_from_sub_level() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for sub_level in sub_level_location_table:
        sub_level_name = f"{pascal_to_space(sub_level.subLevel.name)} (Sub-Level) {sub_level.subLevelMission.name}"
        locations += [{"id": sub_level.locationId, "name": sub_level_name}]
    return locations


def get_location_from_emblem() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for emblem in field_emblem_location_table:
        locations += [{"id": emblem.locationId, "name": emblem.emblemName}]
    return locations


all_location_table: List[LocationInfo] = (get_location_from_level() + get_location_from_upgrade()
                                          + get_location_from_sub_level() + get_location_from_emblem()) + [
                                             {"id": 9, "name": "Perfect Chaos Fight"}]


def get_location_by_id(location_id: int) -> LocationInfo:
    for location in all_location_table:
        if location["id"] == location_id:
            return location


def get_location_by_name(location_name: str) -> LocationInfo:
    for location in all_location_table:
        if location["name"] == location_name:
            return location


class SonicAdventureDXLocation(Location):
    game: str = "Sonic Adventure DX"

    def __init__(self, player, location_id: int, parent: Region):
        location = get_location_by_id(location_id)
        super().__init__(player, location["name"], location["id"], parent)
