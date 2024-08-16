from dataclasses import dataclass
from typing import List, TypedDict, Dict

from BaseClasses import Location, Region
from .Enums import Area, Level, SubLevel, Character, LevelMission, EVERYONE, FLYERS, \
    SubLevelMission, pascal_to_space, SADX_BASE_ID
from .Names import ItemName, LocationName
from .Names.ItemName import EVERY_LURE
from .Names.LocationName import Boss


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
    locationName: str
    area: Area
    character: Character
    extraItems: List[str]


@dataclass
class EmblemLocation:
    locationId: int
    area: Area
    characters: List[Character]
    emblemName: str


@dataclass
class LifeCapsuleLocation:
    locationId: int
    area: Area
    character: Character
    level: Level
    lifeCapsuleNumber: int
    extraItems: List[str]


@dataclass
class BossFightLocation:
    locationId: int
    area: Area
    characters: List[Character]
    boss: Boss
    unified: bool = False


@dataclass
class MissionLocation:
    locationId: int
    cardArea: Area
    objectiveArea: Area
    character: Character
    missionNumber: int
    extraItems: List[str]


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
    LevelLocation(2100, Area.Casino, Character.Tails, Level.Casinopolis, LevelMission.A, [ItemName.Tails.JetAnklet]),
    LevelLocation(3102, Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.C, []),
    LevelLocation(3101, Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.B, []),
    LevelLocation(3100, Area.Casino, Character.Knuckles, Level.Casinopolis, LevelMission.A, []),
    LevelLocation(1402, Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(1401, Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.B, []),
    LevelLocation(1400, Area.TwinklePark, Character.Sonic, Level.TwinklePark, LevelMission.A, []),
    LevelLocation(4002, Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.C, []),
    LevelLocation(4001, Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.B, []),
    LevelLocation(4000, Area.TwinklePark, Character.Amy, Level.TwinklePark, LevelMission.A, []),
    LevelLocation(1502, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, LevelMission.C,
                  [ItemName.KeyItem.EmployeeCard]),
    LevelLocation(1501, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, LevelMission.B,
                  [ItemName.KeyItem.EmployeeCard]),
    LevelLocation(1500, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, LevelMission.A,
                  [ItemName.KeyItem.EmployeeCard]),
    LevelLocation(2402, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, LevelMission.C,
                  [ItemName.KeyItem.EmployeeCard]),
    LevelLocation(2401, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, LevelMission.B,
                  [ItemName.KeyItem.EmployeeCard]),
    LevelLocation(2400, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, LevelMission.A,
                  [ItemName.KeyItem.EmployeeCard, ItemName.Tails.JetAnklet]),

    # Mystic Ruins
    LevelLocation(1102, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.C,
                  [ItemName.KeyItem.WindStone]),
    LevelLocation(1101, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.B,
                  [ItemName.KeyItem.WindStone]),
    LevelLocation(1100, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, LevelMission.A,
                  [ItemName.KeyItem.WindStone]),
    LevelLocation(2002, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.C,
                  [ItemName.KeyItem.WindStone]),
    LevelLocation(2001, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.B,
                  [ItemName.KeyItem.WindStone]),
    LevelLocation(2000, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, LevelMission.A,
                  [ItemName.KeyItem.WindStone, ItemName.Tails.JetAnklet]),
    LevelLocation(5202, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.C,
                  [ItemName.KeyItem.WindStone, ItemName.Gamma.JetBooster]),
    LevelLocation(5201, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.B,
                  [ItemName.KeyItem.WindStone, ItemName.Gamma.JetBooster]),
    LevelLocation(5200, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, LevelMission.A,
                  [ItemName.KeyItem.WindStone, ItemName.Gamma.JetBooster]),
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
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    LevelLocation(6101, Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.B,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train] + EVERY_LURE),
    LevelLocation(6100, Area.AngelIsland, Character.Big, Level.IceCap, LevelMission.A,
                  [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train] + EVERY_LURE),
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
    LevelLocation(1702, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.C, []),
    LevelLocation(1701, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.B, []),
    LevelLocation(1700, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, LevelMission.A, []),
    LevelLocation(2302, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.C, []),
    LevelLocation(2301, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.B, []),
    LevelLocation(2300, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, LevelMission.A,
                  [ItemName.Tails.JetAnklet]),
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
    LevelLocation(6301, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.B, EVERY_LURE),
    LevelLocation(6300, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.A, EVERY_LURE),
    LevelLocation(5402, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.C,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(5401, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.B,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(5400, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.A,
                  [ItemName.Gamma.JetBooster]),
]

upgrade_location_table: List[UpgradeLocation] = [
    # Station Square
    UpgradeLocation(100, LocationName.Sonic.LightShoes, Area.StationSquareMain, Character.Sonic, []),
    UpgradeLocation(200, LocationName.Tails.JetAnklet, Area.StationSquareMain, Character.Tails, []),
    UpgradeLocation(602, LocationName.Big.Lure1, Area.StationSquareMain, Character.Big, []),
    UpgradeLocation(101, LocationName.Sonic.CrystalRing, Area.Hotel, Character.Sonic, [ItemName.Sonic.LightShoes]),
    # Mystic Ruins
    UpgradeLocation(300, LocationName.Knuckles.ShovelClaw, Area.MysticRuinsMain, Character.Knuckles, []),
    UpgradeLocation(604, LocationName.Big.Lure3, Area.AngelIsland, Character.Big,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    UpgradeLocation(600, LocationName.Big.LifeBelt, Area.AngelIsland, Character.Big,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    UpgradeLocation(102, LocationName.Sonic.AncientLight, Area.AngelIsland, Character.Sonic, []),
    UpgradeLocation(301, LocationName.Knuckles.FightingGloves, Area.Jungle, Character.Knuckles, []),
    UpgradeLocation(603, LocationName.Big.Lure2, Area.Jungle, Character.Big, []),
    UpgradeLocation(601, LocationName.Big.PowerRod, Area.Jungle, Character.Big, []),

    # Egg Carrier
    UpgradeLocation(400, LocationName.Amy.WarriorFeather, Area.EggCarrierMain, Character.Amy, []),
    UpgradeLocation(401, LocationName.Amy.LongHammer, Area.EggCarrierMain, Character.Amy, []),
    UpgradeLocation(500, LocationName.Gamma.JetBooster, Area.EggCarrierMain, Character.Gamma, []),
    UpgradeLocation(501, LocationName.Gamma.LaserBlaster, Area.EggCarrierMain, Character.Gamma, []),
    UpgradeLocation(605, LocationName.Big.Lure4, Area.EggCarrierMain, Character.Big, []),

    # Past
    UpgradeLocation(201, LocationName.Tails.RhythmBadge, Area.AngelIsland, Character.Tails, []),
]

sub_level_location_table: List[SubLevelLocation] = [
    SubLevelLocation(15, Area.TwinklePark, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.B),
    SubLevelLocation(16, Area.TwinklePark, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.A),
    SubLevelLocation(25, Area.Jungle, [Character.Sonic, Character.Tails], SubLevel.SandHill, SubLevelMission.B),
    SubLevelLocation(26, Area.Jungle, [Character.Sonic, Character.Tails], SubLevel.SandHill, SubLevelMission.A),
    SubLevelLocation(27, Area.MysticRuinsMain, [Character.Sonic, Character.Tails], SubLevel.SkyChaseAct1,
                     SubLevelMission.B),
    SubLevelLocation(28, Area.MysticRuinsMain, [Character.Sonic, Character.Tails], SubLevel.SkyChaseAct1,
                     SubLevelMission.A),
    SubLevelLocation(35, Area.EggCarrierMain, [Character.Sonic, Character.Tails], SubLevel.SkyChaseAct2,
                     SubLevelMission.B),
    SubLevelLocation(36, Area.EggCarrierMain, [Character.Sonic, Character.Tails], SubLevel.SkyChaseAct2,
                     SubLevelMission.A),
]

field_emblem_location_table: List[EmblemLocation] = [
    # Station Square
    EmblemLocation(10, Area.Station, [Character.Sonic, Character.Knuckles, Character.Tails,
                                      Character.Amy, Character.Big], "Station Emblem"),
    EmblemLocation(11, Area.StationSquareMain, EVERYONE, "Burger Shop Emblem"),
    EmblemLocation(12, Area.StationSquareMain, [Character.Knuckles, Character.Tails],
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
    EmblemLocation(32, Area.EggCarrierMain, [Character.Tails, Character.Sonic], "Hidden Bed Emblem"),
    EmblemLocation(33, Area.EggCarrierMain, [Character.Sonic], "Main Platform Emblem"),

]

life_capsule_location_table: List[LifeCapsuleLocation] = [
    LifeCapsuleLocation(1010, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 1, []),
    LifeCapsuleLocation(1011, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 2, []),
    LifeCapsuleLocation(1012, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 3, []),
    LifeCapsuleLocation(1013, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 4, []),
    LifeCapsuleLocation(1110, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 1,
                        [ItemName.KeyItem.WindStone, ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1111, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 2,
                        [ItemName.KeyItem.WindStone]),
    LifeCapsuleLocation(1112, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 3,
                        [ItemName.KeyItem.WindStone]),
    LifeCapsuleLocation(1113, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 4,
                        [ItemName.KeyItem.WindStone, ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1114, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 5,
                        [ItemName.KeyItem.WindStone]),
    LifeCapsuleLocation(1210, Area.Casino, Character.Sonic, Level.Casinopolis, 1, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1211, Area.Casino, Character.Sonic, Level.Casinopolis, 2, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1212, Area.Casino, Character.Sonic, Level.Casinopolis, 3, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1310, Area.AngelIsland, Character.Sonic, Level.IceCap, 1,
                        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LifeCapsuleLocation(1410, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 1, []),
    LifeCapsuleLocation(1411, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 2, []),
    LifeCapsuleLocation(1412, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 3, []),
    LifeCapsuleLocation(1413, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 4, []),
    LifeCapsuleLocation(1510, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 1,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1511, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 2,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1512, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 3,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1513, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 4,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1514, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 5,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1515, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 6,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1516, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 7,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1517, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 8,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(1518, Area.StationSquareMain, Character.Sonic, Level.SpeedHighway, 9,
                        [ItemName.KeyItem.EmployeeCard]),

    LifeCapsuleLocation(1610, Area.AngelIsland, Character.Sonic, Level.RedMountain, 1,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1611, Area.AngelIsland, Character.Sonic, Level.RedMountain, 2,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1612, Area.AngelIsland, Character.Sonic, Level.RedMountain, 3,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1613, Area.AngelIsland, Character.Sonic, Level.RedMountain, 4,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1614, Area.AngelIsland, Character.Sonic, Level.RedMountain, 5,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1615, Area.AngelIsland, Character.Sonic, Level.RedMountain, 6,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1616, Area.AngelIsland, Character.Sonic, Level.RedMountain, 7,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    LifeCapsuleLocation(1617, Area.AngelIsland, Character.Sonic, Level.RedMountain, 8,
                        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),

    LifeCapsuleLocation(1710, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 1, []),
    LifeCapsuleLocation(1711, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 2, []),
    LifeCapsuleLocation(1712, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 3, []),
    LifeCapsuleLocation(1713, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 4, []),
    LifeCapsuleLocation(1714, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 5, []),
    LifeCapsuleLocation(1715, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 6, []),
    LifeCapsuleLocation(1716, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 7, []),
    LifeCapsuleLocation(1717, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 8, []),
    LifeCapsuleLocation(1718, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 9, []),
    LifeCapsuleLocation(1719, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 10, []),
    LifeCapsuleLocation(1720, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 11, []),
    LifeCapsuleLocation(1721, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 12, []),
    LifeCapsuleLocation(1810, Area.Jungle, Character.Sonic, Level.LostWorld, 1, []),
    LifeCapsuleLocation(1811, Area.Jungle, Character.Sonic, Level.LostWorld, 2, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1910, Area.Jungle, Character.Sonic, Level.FinalEgg, 1, []),
    LifeCapsuleLocation(1911, Area.Jungle, Character.Sonic, Level.FinalEgg, 2, []),
    LifeCapsuleLocation(1912, Area.Jungle, Character.Sonic, Level.FinalEgg, 3, []),
    LifeCapsuleLocation(1913, Area.Jungle, Character.Sonic, Level.FinalEgg, 4, []),
    LifeCapsuleLocation(1914, Area.Jungle, Character.Sonic, Level.FinalEgg, 5, []),
    LifeCapsuleLocation(1915, Area.Jungle, Character.Sonic, Level.FinalEgg, 6, []),
    LifeCapsuleLocation(1916, Area.Jungle, Character.Sonic, Level.FinalEgg, 7, []),
    LifeCapsuleLocation(1917, Area.Jungle, Character.Sonic, Level.FinalEgg, 8, []),
    LifeCapsuleLocation(1918, Area.Jungle, Character.Sonic, Level.FinalEgg, 9, []),
    LifeCapsuleLocation(1919, Area.Jungle, Character.Sonic, Level.FinalEgg, 10, []),
    LifeCapsuleLocation(1920, Area.Jungle, Character.Sonic, Level.FinalEgg, 11, []),
    LifeCapsuleLocation(1921, Area.Jungle, Character.Sonic, Level.FinalEgg, 12, []),
    LifeCapsuleLocation(1922, Area.Jungle, Character.Sonic, Level.FinalEgg, 13, []),
    LifeCapsuleLocation(1923, Area.Jungle, Character.Sonic, Level.FinalEgg, 14, []),
    LifeCapsuleLocation(1924, Area.Jungle, Character.Sonic, Level.FinalEgg, 15, []),
    LifeCapsuleLocation(1925, Area.Jungle, Character.Sonic, Level.FinalEgg, 16, []),

    LifeCapsuleLocation(2010, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, 1,
                        [ItemName.KeyItem.WindStone]),
    LifeCapsuleLocation(2110, Area.Casino, Character.Tails, Level.Casinopolis, 1, []),
    LifeCapsuleLocation(2111, Area.Casino, Character.Tails, Level.Casinopolis, 2, []),
    LifeCapsuleLocation(2310, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 1, []),
    LifeCapsuleLocation(2311, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 2, []),
    LifeCapsuleLocation(2312, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 3, []),
    LifeCapsuleLocation(2313, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 4, []),
    LifeCapsuleLocation(2410, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, 1,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(2411, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, 2,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(2412, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, 3,
                        [ItemName.KeyItem.EmployeeCard]),
    LifeCapsuleLocation(2413, Area.StationSquareMain, Character.Tails, Level.SpeedHighway, 4,
                        [ItemName.KeyItem.EmployeeCard]),

    LifeCapsuleLocation(3010, Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, 1, []),
    LifeCapsuleLocation(3011, Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, 2, []),
    LifeCapsuleLocation(3012, Area.StationSquareMain, Character.Knuckles, Level.SpeedHighway, 3, []),
    LifeCapsuleLocation(3110, Area.Casino, Character.Knuckles, Level.Casinopolis, 1, []),
    LifeCapsuleLocation(3111, Area.Casino, Character.Knuckles, Level.Casinopolis, 2, []),
    LifeCapsuleLocation(3210, Area.AngelIsland, Character.Knuckles, Level.RedMountain, 1,
                        [ItemName.Knuckles.ShovelClaw]),
    LifeCapsuleLocation(3211, Area.AngelIsland, Character.Knuckles, Level.RedMountain, 2,
                        [ItemName.Knuckles.ShovelClaw]),
    LifeCapsuleLocation(3212, Area.AngelIsland, Character.Knuckles, Level.RedMountain, 3,
                        [ItemName.Knuckles.ShovelClaw]),
    LifeCapsuleLocation(3213, Area.AngelIsland, Character.Knuckles, Level.RedMountain, 4,
                        [ItemName.Knuckles.ShovelClaw]),
    LifeCapsuleLocation(3410, Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, 1, []),

    LifeCapsuleLocation(4010, Area.TwinklePark, Character.Amy, Level.TwinklePark, 1, []),
    LifeCapsuleLocation(4110, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 1, []),
    LifeCapsuleLocation(4111, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 2, []),
    LifeCapsuleLocation(4112, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 3, []),
    LifeCapsuleLocation(4113, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 4, []),
    LifeCapsuleLocation(4210, Area.Jungle, Character.Amy, Level.FinalEgg, 1, []),
    LifeCapsuleLocation(4211, Area.Jungle, Character.Amy, Level.FinalEgg, 2, []),

    LifeCapsuleLocation(5110, Area.Hotel, Character.Gamma, Level.EmeraldCoast, 1, []),
    LifeCapsuleLocation(5210, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, 1,
                        [ItemName.KeyItem.WindStone, ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5211, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, 2,
                        [ItemName.KeyItem.WindStone, ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5310, Area.AngelIsland, Character.Gamma, Level.RedMountain, 1, []),
    LifeCapsuleLocation(5410, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 1, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5411, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 2, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5412, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 3, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5413, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 4, [ItemName.Gamma.JetBooster]),

    LifeCapsuleLocation(6110, Area.AngelIsland, Character.Big, Level.IceCap, 1,
                        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    LifeCapsuleLocation(6210, Area.Hotel, Character.Big, Level.EmeraldCoast, 1, []),
    LifeCapsuleLocation(6310, Area.EggCarrierMain, Character.Big, Level.HotShelter, 1, []),
]

boss_location_table: List[BossFightLocation] = [
    # Station Square
    BossFightLocation(700, Area.StationSquareMain, [Character.Sonic], LocationName.Boss.Chaos0),
    BossFightLocation(710, Area.Hotel, [Character.Knuckles], LocationName.Boss.Chaos2),
    BossFightLocation(720, Area.Casino, [Character.Tails], LocationName.Boss.EggWalker),
    # Mystic Ruins
    BossFightLocation(730, Area.MysticRuinsMain, [Character.Sonic], LocationName.Boss.EggHornet),
    BossFightLocation(731, Area.MysticRuinsMain, [Character.Tails], LocationName.Boss.EggHornet),
    BossFightLocation(739, Area.MysticRuinsMain, [Character.Sonic, Character.Tails], LocationName.Boss.EggHornet, True),

    BossFightLocation(740, Area.MysticRuinsMain, [Character.Sonic], LocationName.Boss.Chaos4),
    BossFightLocation(741, Area.MysticRuinsMain, [Character.Tails], LocationName.Boss.Chaos4),
    BossFightLocation(742, Area.MysticRuinsMain, [Character.Knuckles], LocationName.Boss.Chaos4),
    BossFightLocation(749, Area.MysticRuinsMain, [Character.Sonic, Character.Tails, Character.Knuckles],
                      LocationName.Boss.Chaos4, True),

    BossFightLocation(750, Area.Jungle, [Character.Sonic], LocationName.Boss.EggViper),
    BossFightLocation(760, Area.Jungle, [Character.Gamma], LocationName.Boss.E101Beta),

    # Egg Carrier
    BossFightLocation(770, Area.EggCarrierMain, [Character.Sonic], LocationName.Boss.Chaos6),
    BossFightLocation(771, Area.EggCarrierMain, [Character.Knuckles], LocationName.Boss.Chaos6),
    BossFightLocation(772, Area.EggCarrierMain, [Character.Big], LocationName.Boss.Chaos6),
    BossFightLocation(779, Area.EggCarrierMain, [Character.Sonic, Character.Big, Character.Big],
                      LocationName.Boss.Chaos6, True),

    BossFightLocation(780, Area.EggCarrierMain, [Character.Gamma], LocationName.Boss.E101mkII),
    BossFightLocation(790, Area.EggCarrierMain, [Character.Amy], LocationName.Boss.Zero),

]

mission_location_table: List[MissionLocation] = [
    MissionLocation(801, Area.StationSquareMain, Area.StationSquareMain, Character.Sonic, 1, []),
    MissionLocation(802, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Sonic, 2, []),
    MissionLocation(803, Area.Hotel, Area.Hotel, Character.Sonic, 3, [ItemName.Sonic.LightShoes]),
    MissionLocation(804, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 4, []),
    MissionLocation(805, Area.Casino, Area.Casino, Character.Knuckles, 5, []),
    MissionLocation(806, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Amy, 6, []),
    MissionLocation(807, Area.MysticRuinsMain, Area.Jungle, Character.Gamma, 7, []),
    MissionLocation(808, Area.StationSquareMain, Area.StationSquareMain, Character.Big, 8, []),
    MissionLocation(809, Area.StationSquareMain, Area.Hotel, Character.Sonic, 9, []),
    MissionLocation(810, Area.Hotel, Area.Hotel, Character.Tails, 10, []),
    MissionLocation(811, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Sonic, 11, [ItemName.KeyItem.WindStone]),
    MissionLocation(812, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Knuckles, 12,
                    [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(813, Area.Casino, Area.Casino, Character.Sonic, 13, [ItemName.Sonic.LightShoes]),
    MissionLocation(814, Area.StationSquareMain, Area.Hotel, Character.Big, 14, []),
    MissionLocation(815, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Sonic, 15, [ItemName.KeyItem.WindStone]),
    MissionLocation(816, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 16, [ItemName.KeyItem.WindStone]),
    MissionLocation(817, Area.StationSquareMain, Area.Casino, Character.Sonic, 17, [ItemName.Sonic.LightShoes]),
    MissionLocation(818, Area.Station, Area.TwinklePark, Character.Amy, 18, []),
    MissionLocation(819, Area.StationSquareMain, Area.TwinklePark, Character.Amy, 19, []),
    MissionLocation(820, Area.AngelIsland, Area.AngelIsland, Character.Sonic, 20,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    MissionLocation(821, Area.Jungle, Area.Jungle, Character.Gamma, 21, []),
    MissionLocation(822, Area.Hotel, Area.Hotel, Character.Big, 22, [ItemName.Big.LifeBelt]),
    MissionLocation(823, Area.TwinklePark, Area.TwinklePark, Character.Sonic, 23, []),
    MissionLocation(824, Area.Casino, Area.Casino, Character.Tails, 24, []),
    MissionLocation(825, Area.StationSquareMain, Area.Casino, Character.Knuckles, 25, []),
    MissionLocation(826, Area.StationSquareMain, Area.Casino, Character.Knuckles, 26, []),
    MissionLocation(827, Area.StationSquareMain, Area.StationSquareMain, Character.Sonic, 27,
                    [ItemName.KeyItem.EmployeeCard]),
    MissionLocation(828, Area.StationSquareMain, Area.StationSquareMain, Character.Sonic, 28,
                    [ItemName.KeyItem.EmployeeCard]),
    MissionLocation(829, Area.StationSquareMain, Area.StationSquareMain, Character.Big, 29, []),
    MissionLocation(830, Area.Jungle, Area.AngelIsland, Character.Sonic, 30,
                    [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    MissionLocation(831, Area.Station, Area.Casino, Character.Tails, 31, []),
    MissionLocation(832, Area.AngelIsland, Area.AngelIsland, Character.Knuckles, 32, []),
    MissionLocation(833, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 33, []),
    MissionLocation(834, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 34, [ItemName.Sonic.LightShoes]),
    MissionLocation(835, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Big, 35,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    MissionLocation(836, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 36, []),
    MissionLocation(837, Area.Jungle, Area.Jungle, Character.Tails, 37, [ItemName.Tails.JetAnklet]),
    MissionLocation(838, Area.Jungle, Area.Jungle, Character.Knuckles, 38, [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(839, Area.Hotel, Area.Hotel, Character.Gamma, 39, [ItemName.Gamma.JetBooster]),
    MissionLocation(840, Area.MysticRuinsMain, Area.Jungle, Character.Sonic, 40, [ItemName.Sonic.LightShoes]),
    MissionLocation(841, Area.Jungle, Area.MysticRuinsMain, Character.Sonic, 41, [ItemName.Sonic.LightShoes]),
    MissionLocation(842, Area.EggCarrierMain, Area.EggCarrierMain, Character.Gamma, 42, []),
    MissionLocation(843, Area.EggCarrierMain, Area.EggCarrierMain, Character.Amy, 43, []),
    MissionLocation(844, Area.EggCarrierMain, Area.EggCarrierMain, Character.Big, 44, []),
    MissionLocation(845, Area.Jungle, Area.Jungle, Character.Sonic, 45, []),
    MissionLocation(846, Area.Jungle, Area.Jungle, Character.Sonic, 46, []),
    MissionLocation(847, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 47, []),
    MissionLocation(848, Area.StationSquareMain, Area.Casino, Character.Knuckles, 48, []),
    MissionLocation(849, Area.StationSquareMain, Area.TwinklePark, Character.Sonic, 49, []),  # TP Kart
    MissionLocation(850, Area.Jungle, Area.Jungle, Character.Amy, 50, []),
    MissionLocation(851, Area.Jungle, Area.MysticRuinsMain, Character.Gamma, 51,
                    [ItemName.KeyItem.WindStone, ItemName.Gamma.JetBooster]),
    MissionLocation(852, Area.Jungle, Area.Jungle, Character.Big, 52, []),
    MissionLocation(853, Area.AngelIsland, Area.AngelIsland, Character.Sonic, 53,  # Triple snowboard jump
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    MissionLocation(854, Area.AngelIsland, Area.AngelIsland, Character.Tails, 54,  # Snowboard flags
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    MissionLocation(855, Area.TwinklePark, Area.StationSquareMain, Character.Sonic, 55,
                    [ItemName.KeyItem.EmployeeCard]),
    MissionLocation(856, Area.MysticRuinsMain, Area.AngelIsland, Character.Knuckles, 56,
                    [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(857, Area.AngelIsland, Area.MysticRuinsMain, Character.Sonic, 57,
                    [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    MissionLocation(858, Area.Jungle, Area.Jungle, Character.Sonic, 58, []),  # Lost World flags
    MissionLocation(859, Area.EggCarrierMain, Area.EggCarrierMain, Character.Knuckles, 59, []),

    MissionLocation(860, Area.MysticRuinsMain, Area.AngelIsland, Character.Big, 60,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
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
        locations += [{"id": upgrade.locationId, "name": upgrade.locationName}]
    return locations


def get_location_from_sub_level() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for sub_level in sub_level_location_table:
        sub_level_name = f"{pascal_to_space(sub_level.subLevel.name)} (Sub-Level - Mission {sub_level.subLevelMission.name})"
        locations += [{"id": sub_level.locationId, "name": sub_level_name}]
    return locations


def get_location_from_emblem() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for emblem in field_emblem_location_table:
        locations += [{"id": emblem.locationId, "name": emblem.emblemName}]
    return locations


def get_location_from_life_capsule() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for life_capsule in life_capsule_location_table:
        level_name: str = f"{pascal_to_space(life_capsule.level.name)} ({life_capsule.character.name} - Life Capsule {life_capsule.lifeCapsuleNumber})"
        locations += [{"id": life_capsule.locationId, "name": level_name}]
    return locations


def get_location_from_boss() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for boss_fight in boss_location_table:
        if boss_fight.unified:
            location_name: str = f"{boss_fight.boss} Boss Fight"
        else:
            location_name: str = f"{boss_fight.boss} Boss Fight ({boss_fight.characters[0].name})"

        locations += [{"id": boss_fight.locationId, "name": location_name}]
    return locations


def get_location_from_mission() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for mission in mission_location_table:
        mission_name: str = f"Mission {mission.missionNumber} ({mission.character.name})"
        locations += [{"id": mission.locationId, "name": mission_name}]
    return locations


all_location_table: List[LocationInfo] = (
        get_location_from_level() +
        get_location_from_upgrade() +
        get_location_from_sub_level() +
        get_location_from_emblem() +
        get_location_from_life_capsule() +
        get_location_from_boss() +
        get_location_from_mission() +
        [{"id": 9, "name": "Perfect Chaos Fight"}]
)


def get_location_name_by_level(level_name: str) -> List[str]:
    return [location["name"] for location in get_location_from_level() if level_name in location["name"]] + \
        [location["name"] for location in get_location_from_life_capsule() if level_name in location["name"]]


group_location_table: Dict[str, List[str]] = {
    LocationName.Groups.UpgradePoints: [location["name"] for location in get_location_from_upgrade()],
    LocationName.Groups.FieldEmblems: [location["name"] for location in get_location_from_emblem()],
    LocationName.Groups.Levels: [location["name"] for location in get_location_from_level()],
    LocationName.Groups.Sublevels: [location["name"] for location in get_location_from_sub_level()],
    LocationName.Groups.LifeCapsules: [location["name"] for location in get_location_from_life_capsule()],
    LocationName.Groups.Bosses: [location["name"] for location in get_location_from_boss()],
    pascal_to_space(Level.EmeraldCoast.name): get_location_name_by_level(pascal_to_space(Level.EmeraldCoast.name)),
    pascal_to_space(Level.WindyValley.name): get_location_name_by_level(pascal_to_space(Level.WindyValley.name)),
    pascal_to_space(Level.Casinopolis.name): get_location_name_by_level(pascal_to_space(Level.Casinopolis.name)),
    pascal_to_space(Level.IceCap.name): get_location_name_by_level(pascal_to_space(Level.IceCap.name)),
    pascal_to_space(Level.TwinklePark.name): get_location_name_by_level(pascal_to_space(Level.TwinklePark.name)),
    pascal_to_space(Level.SpeedHighway.name): get_location_name_by_level(pascal_to_space(Level.SpeedHighway.name)),
    pascal_to_space(Level.RedMountain.name): get_location_name_by_level(pascal_to_space(Level.RedMountain.name)),
    pascal_to_space(Level.LostWorld.name): get_location_name_by_level(pascal_to_space(Level.LostWorld.name)),
    pascal_to_space(Level.FinalEgg.name): get_location_name_by_level(pascal_to_space(Level.FinalEgg.name)),
    pascal_to_space(Level.HotShelter.name): get_location_name_by_level(pascal_to_space(Level.HotShelter.name)),

}


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
        super().__init__(player, location["name"], location["id"] + SADX_BASE_ID, parent)
