from dataclasses import dataclass
from typing import List, TypedDict

from BaseClasses import Location, Region
from .Enums import Area, Level, SubLevel, Character, LevelMission, Upgrade, EVERYONE, FLYERS, \
    SubLevelMission, pascal_to_space
from .Names import ItemName
from .Names.ItemName import EVERY_LURE


@dataclass
class LevelLocation:
    locationId: int
    area: Area
    character: Character
    level: Level
    levelMission: LevelMission
    extraItems: List[str]


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
    LevelLocation(6002, Area.StationSquareMain, Character.Big, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(6001, Area.StationSquareMain, Character.Big, Level.TwinklePark, LevelMission.B, EVERY_LURE),
    LevelLocation(6000, Area.StationSquareMain, Character.Big, Level.TwinklePark, LevelMission.A, EVERY_LURE),
    LevelLocation(3002, Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, LevelMission.C, []),
    LevelLocation(3001, Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, LevelMission.B, []),
    LevelLocation(3000, Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, LevelMission.A, []),
    LevelLocation(1002, Area.Hotel, Character.Sonic, Level.EmeraldCoast, LevelMission.C, []),
    LevelLocation(1001, Area.Hotel, Character.Sonic, Level.EmeraldCoast, LevelMission.B, []),
    LevelLocation(1000, Area.Hotel, Character.Sonic, Level.EmeraldCoast, LevelMission.A, []),
    LevelLocation(6202, Area.Hotel, Character.Big, Level.EmeraldCoast, LevelMission.C, []),
    LevelLocation(6201, Area.Hotel, Character.Big, Level.EmeraldCoast, LevelMission.B, EVERY_LURE),
    LevelLocation(6200, Area.Hotel, Character.Big, Level.EmeraldCoast, LevelMission.A, EVERY_LURE),
    LevelLocation(5102, Area.Hotel, Character.Gamma, Level.EmeraldCoast, LevelMission.C, []),
    LevelLocation(5101, Area.Hotel, Character.Gamma, Level.EmeraldCoast, LevelMission.B, []),
    LevelLocation(5100, Area.Hotel, Character.Gamma, Level.EmeraldCoast, LevelMission.A, []),
    LevelLocation(1202, Area.Casino, Character.Sonic, Level.Casinopolis, LevelMission.C, [ItemName.Sonic.LightShoes]),
    LevelLocation(1201, Area.Casino, Character.Sonic, Level.Casinopolis, LevelMission.B, [ItemName.Sonic.LightShoes]),
    LevelLocation(1200, Area.Casino, Character.Sonic, Level.Casinopolis, LevelMission.A, [ItemName.Sonic.LightShoes]),
    LevelLocation(2102, Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.C, []),
    LevelLocation(2101, Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.B, []),
    LevelLocation(2100, Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.A, []),
    LevelLocation(3102, Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.C, []),
    LevelLocation(3101, Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.B, []),
    LevelLocation(3100, Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.A, []),
    LevelLocation(1402, Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(1401, Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.B, []),
    LevelLocation(1400, Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.A, []),
    LevelLocation(4002, Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(4001, Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.B, []),
    LevelLocation(4000, Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.A, []),
    LevelLocation(1502, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, LevelMission.C, []),
    LevelLocation(1501, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, LevelMission.B, []),
    LevelLocation(1500, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, LevelMission.A, []),
    LevelLocation(2402, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, LevelMission.C, []),
    LevelLocation(2401, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, LevelMission.B, []),
    LevelLocation(2400, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, LevelMission.A, []),

    # Mystic Ruins
    LevelLocation(1102, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.C, []),
    LevelLocation(1101, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.B, []),
    LevelLocation(1100, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.A, []),
    LevelLocation(2002, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.C, []),
    LevelLocation(2001, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.B, []),
    LevelLocation(2000, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.A, []),
    LevelLocation(5202, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.C,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(5201, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.B,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(5200, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.A,
                  [ItemName.Gamma.JetBooster]),

    # TODO: Check if is okay to requiere Train or something more complex like "Station Square access"
    LevelLocation(1302, Area.AngelIsland, Character.Sonic, Level.IceCap, LevelMission.C,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(1301, Area.AngelIsland, Character.Sonic, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(1300, Area.AngelIsland, Character.Sonic, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(2202, Area.AngelIsland, Character.Tails, Level.IceCap, LevelMission.C,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(2201, Area.AngelIsland, Character.Tails, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(2200, Area.AngelIsland, Character.Tails, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LevelLocation(6102, Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.C,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train]),
    LevelLocation(6101, Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train] + EVERY_LURE),
    LevelLocation(6100, Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train] + EVERY_LURE),
    LevelLocation(1602, Area.AngelIsland, Character.Sonic, Level.RedMountain, LevelMission.C,
                  [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LevelLocation(1601, Area.AngelIsland, Character.Sonic, Level.RedMountain, LevelMission.B,
                  [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LevelLocation(1600, Area.AngelIsland, Character.Sonic, Level.RedMountain, LevelMission.A,
                  [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LevelLocation(3202, Area.AngelIsland, Character.Knuckles, Level.RedMountain, LevelMission.C,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(3201, Area.AngelIsland, Character.Knuckles, Level.RedMountain, LevelMission.B,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(3200, Area.AngelIsland, Character.Knuckles, Level.RedMountain, LevelMission.A,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(5302, Area.AngelIsland, Character.Gamma, Level.RedMountain, LevelMission.C, []),
    LevelLocation(5301, Area.AngelIsland, Character.Gamma, Level.RedMountain, LevelMission.B, []),
    LevelLocation(5300, Area.AngelIsland, Character.Gamma, Level.RedMountain, LevelMission.A, []),

    LevelLocation(1802, Area.Jungle, Character.Sonic, Level.LostWorld, LevelMission.C, [ItemName.Sonic.LightShoes]),
    LevelLocation(1801, Area.Jungle, Character.Sonic, Level.LostWorld, LevelMission.B, [ItemName.Sonic.LightShoes]),
    LevelLocation(1800, Area.Jungle, Character.Sonic, Level.LostWorld, LevelMission.A, [ItemName.Sonic.LightShoes]),
    LevelLocation(3302, Area.Jungle, Character.Knuckles, Level.LostWorld, LevelMission.C,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(3301, Area.Jungle, Character.Knuckles, Level.LostWorld, LevelMission.B,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(3300, Area.Jungle, Character.Knuckles, Level.LostWorld, LevelMission.A,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(1902, Area.Jungle, Character.Sonic, Level.FinalEgg, LevelMission.C, [ItemName.Sonic.LightShoes]),
    LevelLocation(1901, Area.Jungle, Character.Sonic, Level.FinalEgg, LevelMission.B, [ItemName.Sonic.LightShoes]),
    LevelLocation(1900, Area.Jungle, Character.Sonic, Level.FinalEgg, LevelMission.A, [ItemName.Sonic.LightShoes]),
    LevelLocation(4202, Area.Jungle, Character.Amy, Level.FinalEgg, LevelMission.C, []),
    LevelLocation(4201, Area.Jungle, Character.Amy, Level.FinalEgg, LevelMission.B, []),
    LevelLocation(4200, Area.Jungle, Character.Amy, Level.FinalEgg, LevelMission.A, []),
    LevelLocation(5002, Area.Jungle, Character.Gamma, Level.FinalEgg, LevelMission.C, []),
    LevelLocation(5001, Area.Jungle, Character.Gamma, Level.FinalEgg, LevelMission.B, []),
    LevelLocation(5000, Area.Jungle, Character.Gamma, Level.FinalEgg, LevelMission.A, []),
    # Egg Carrier
    LevelLocation(1702, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.C,
                  [ItemName.Sonic.LightShoes]),
    LevelLocation(1701, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.B,
                  [ItemName.Sonic.LightShoes]),
    LevelLocation(1700, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.A,
                  [ItemName.Sonic.LightShoes]),
    LevelLocation(2302, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.C, []),
    LevelLocation(2301, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.B, []),
    LevelLocation(2300, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.A, []),
    LevelLocation(3402, Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, LevelMission.C,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(3401, Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, LevelMission.B,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(3400, Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, LevelMission.A,
                  [ItemName.Knuckles.ShovelClaw]),
    LevelLocation(4102, Area.EggCarrierMain, Character.Amy, Level.HotShelter, LevelMission.C, []),
    LevelLocation(4101, Area.EggCarrierMain, Character.Amy, Level.HotShelter, LevelMission.B, []),
    LevelLocation(4100, Area.EggCarrierMain, Character.Amy, Level.HotShelter, LevelMission.A, []),
    LevelLocation(6302, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.C, []),
    LevelLocation(6301, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.B,
                  EVERY_LURE + [ItemName.Big.LifeBelt]),
    LevelLocation(6300, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.A,
                  EVERY_LURE + [ItemName.Big.LifeBelt]),
    LevelLocation(5402, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.C, []),
    LevelLocation(5401, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.B, []),
    LevelLocation(5400, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.A, []),
]

upgrade_location_table: List[UpgradeLocation] = [
    # Station Square
    UpgradeLocation(100, Area.StationSquareMain, Character.Sonic, Upgrade.LightShoes, []),
    UpgradeLocation(200, Area.StationSquareMain, Character.Tails, Upgrade.JetAnkle, []),
    # UpgradeLocation(602, Area.StationSquareMain, Character.Big, Upgrade.Lure1, []),
    UpgradeLocation(101, Area.Hotel, Character.Sonic, Upgrade.CrystalRing, [ItemName.Sonic.LightShoes]),
    # Mystic Ruins
    UpgradeLocation(300, Area.MysticRuinsMain, Character.Knuckles, Upgrade.ShovelClaw, [ItemName.Knuckles.ShovelClaw]),
    # UpgradeLocation(604, Area.AngelIsland, Character.Big, Upgrade.Lure3, [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train]),
    UpgradeLocation(600, Area.AngelIsland, Character.Big, Upgrade.LifeBelt,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train]),
    UpgradeLocation(102, Area.AngelIsland, Character.Sonic, Upgrade.AncientLight, []),
    UpgradeLocation(301, Area.Jungle, Character.Knuckles, Upgrade.FightingGloves, []),
    # UpgradeLocation(603, Area.Jungle, Character.Big, Upgrade.Lure2, []),
    UpgradeLocation(601, Area.Jungle, Character.Big, Upgrade.PowerRod, []),
    # Egg Carrier
    UpgradeLocation(400, Area.EggCarrierMain, Character.Amy, Upgrade.WarriorFeather, []),
    UpgradeLocation(401, Area.EggCarrierMain, Character.Amy, Upgrade.LongHammer, []),
    UpgradeLocation(500, Area.EggCarrierMain, Character.Gamma, Upgrade.JetBooster, []),
    UpgradeLocation(501, Area.EggCarrierMain, Character.Gamma, Upgrade.LaserBlaster, []),
    # UpgradeLocation(605, Area.EggCarrierMain, Character.Big, Upgrade.Lure4, []),

]

sub_level_location_table: List[SubLevelLocation] = [
    SubLevelLocation(15, Area.TwinklePark, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.B),
    SubLevelLocation(16, Area.TwinklePark, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.A),
    SubLevelLocation(25, Area.Jungle, [Character.Sonic, Character.Tails], SubLevel.SandHill, SubLevelMission.B),
    SubLevelLocation(26, Area.Jungle, [Character.Sonic, Character.Tails], SubLevel.SandHill, SubLevelMission.A),
]

field_emblem_location_table: List[EmblemLocation] = [
    # Station Square
    EmblemLocation(10, Area.StationSquareMain, EVERYONE, "Station Emblem"),
    EmblemLocation(11, Area.StationSquareMain, EVERYONE, "Burger Shop Emblem"),
    EmblemLocation(12, Area.StationSquareMain, [Character.Knuckles, Character.Tails, Character.Amy],
                   "City Hall Emblem"),
    EmblemLocation(13, Area.Casino, [Character.Tails], "Casino Emblem"),
    # Mystic Ruins
    EmblemLocation(20, Area.MysticRuinsMain, FLYERS, "Tails' Workshop Emblem"),
    EmblemLocation(21, Area.AngelIsland, [Character.Knuckles], "Shrine Emblem"),
    EmblemLocation(22, Area.Jungle, EVERYONE, "Jungle Path Emblem"),
    EmblemLocation(23, Area.Jungle, FLYERS, "Tree Stump Emblem"),
    # Egg Carrier
    EmblemLocation(30, Area.EggCarrierMain, FLYERS, "Pool Emblem"),
    EmblemLocation(31, Area.EggCarrierMain, [Character.Tails], "Spinning Platform Emblem"),
    EmblemLocation(32, Area.EggCarrierMain, [Character.Tails], "Hidden Bed Emblem"),
    EmblemLocation(33, Area.EggCarrierMain, [Character.Sonic], "Main Platform Emblem"),

]


class LocationInfo(TypedDict):
    id: int
    name: str


def get_location_from_level() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for level in level_location_table:
        level_name: str = f"{pascal_to_space(level.level.name)} ({level.character.name} - Mission {level.levelMission.name})"
        locations += [{"id": level.locationId, "name": level_name}]
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

    def __init__(self, player, location_id: int, base_id: int, parent: Region):
        location = get_location_by_id(location_id)
        super().__init__(player, location["name"], location["id"] + base_id, parent)
