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


@dataclass
class LifeCapsuleLocation:
    locationId: int
    area: Area
    character: Character
    level: Level
    lifeCapsuleNumber: int
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
    LevelLocation(6302, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.C, [ItemName.Big.LifeBelt]),
    LevelLocation(6301, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.B,
                  EVERY_LURE + [ItemName.Big.LifeBelt]),
    LevelLocation(6300, Area.EggCarrierMain, Character.Big, Level.HotShelter, LevelMission.A,
                  EVERY_LURE + [ItemName.Big.LifeBelt]),
    LevelLocation(5402, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.C,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(5401, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.B,
                  [ItemName.Gamma.JetBooster]),
    LevelLocation(5400, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, LevelMission.A,
                  [ItemName.Gamma.JetBooster]),
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
    EmblemLocation(10, Area.StationSquareMain, [Character.Sonic, Character.Knuckles, Character.Tails,
                                                Character.Amy, Character.Big], "Station Emblem"),
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

life_capsule_location_table: List[LifeCapsuleLocation] = [
    LifeCapsuleLocation(1010, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 1, []),
    LifeCapsuleLocation(1011, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 2, []),
    LifeCapsuleLocation(1012, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 3, []),
    LifeCapsuleLocation(1013, Area.Hotel, Character.Sonic, Level.EmeraldCoast, 4, []),
    LifeCapsuleLocation(1110, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 1, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1111, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 2, []),
    LifeCapsuleLocation(1112, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 3, []),
    LifeCapsuleLocation(1113, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 4, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1114, Area.MysticRuinsMain, Character.Sonic, Level.WindyValley, 5, []),
    LifeCapsuleLocation(1210, Area.Casino, Character.Sonic, Level.Casinopolis, 1, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1211, Area.Casino, Character.Sonic, Level.Casinopolis, 2, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1212, Area.Casino, Character.Sonic, Level.Casinopolis, 3, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1213, Area.Casino, Character.Sonic, Level.Casinopolis, 4, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1310, Area.AngelIsland, Character.Sonic, Level.IceCap, 1,
                        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    LifeCapsuleLocation(1410, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 1, []),
    LifeCapsuleLocation(1411, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 2, []),
    LifeCapsuleLocation(1412, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 3, []),
    LifeCapsuleLocation(1413, Area.TwinklePark, Character.Sonic, Level.TwinklePark, 4, []),
    LifeCapsuleLocation(1510, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 1, []),
    LifeCapsuleLocation(1511, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 2, []),
    LifeCapsuleLocation(1512, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 3, []),
    LifeCapsuleLocation(1513, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 4, []),
    LifeCapsuleLocation(1514, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 5, []),
    LifeCapsuleLocation(1515, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 6, []),
    LifeCapsuleLocation(1516, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 7, []),
    LifeCapsuleLocation(1517, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 8, []),
    LifeCapsuleLocation(1518, Area.SpeedHighway, Character.Sonic, Level.SpeedHighway, 9, []),

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

    LifeCapsuleLocation(1710, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 1, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1711, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 2, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1712, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 3, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1713, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 4, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1714, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 5, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1715, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 6, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1716, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 7, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1717, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 8, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1718, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 9, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1719, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 10, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1720, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 11, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1721, Area.EggCarrierMain, Character.Sonic, Level.SkyDeck, 12, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1810, Area.Jungle, Character.Sonic, Level.LostWorld, 1, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1811, Area.Jungle, Character.Sonic, Level.LostWorld, 2, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1910, Area.Jungle, Character.Sonic, Level.FinalEgg, 1, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1911, Area.Jungle, Character.Sonic, Level.FinalEgg, 2, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1912, Area.Jungle, Character.Sonic, Level.FinalEgg, 3, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1913, Area.Jungle, Character.Sonic, Level.FinalEgg, 4, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1914, Area.Jungle, Character.Sonic, Level.FinalEgg, 5, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1915, Area.Jungle, Character.Sonic, Level.FinalEgg, 6, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1916, Area.Jungle, Character.Sonic, Level.FinalEgg, 7, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1917, Area.Jungle, Character.Sonic, Level.FinalEgg, 8, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1918, Area.Jungle, Character.Sonic, Level.FinalEgg, 9, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1919, Area.Jungle, Character.Sonic, Level.FinalEgg, 10, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1920, Area.Jungle, Character.Sonic, Level.FinalEgg, 11, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1921, Area.Jungle, Character.Sonic, Level.FinalEgg, 12, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1922, Area.Jungle, Character.Sonic, Level.FinalEgg, 13, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1923, Area.Jungle, Character.Sonic, Level.FinalEgg, 14, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1924, Area.Jungle, Character.Sonic, Level.FinalEgg, 15, [ItemName.Sonic.LightShoes]),
    LifeCapsuleLocation(1925, Area.Jungle, Character.Sonic, Level.FinalEgg, 16, [ItemName.Sonic.LightShoes]),

    LifeCapsuleLocation(2010, Area.MysticRuinsMain, Character.Tails, Level.WindyValley, 1, []),
    LifeCapsuleLocation(2110, Area.Casino, Character.Tails, Level.Casinopolis, 1, []),
    LifeCapsuleLocation(2111, Area.Casino, Character.Tails, Level.Casinopolis, 2, []),
    LifeCapsuleLocation(2310, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 1, []),
    LifeCapsuleLocation(2311, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 2, []),
    LifeCapsuleLocation(2312, Area.EggCarrierMain, Character.Tails, Level.SkyDeck, 3, []),
    LifeCapsuleLocation(2410, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, 1, []),
    LifeCapsuleLocation(2411, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, 2, []),
    LifeCapsuleLocation(2412, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, 3, []),
    LifeCapsuleLocation(2413, Area.SpeedHighway, Character.Tails, Level.SpeedHighway, 4, []),

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
    LifeCapsuleLocation(3410, Area.EggCarrierMain, Character.Knuckles, Level.SkyDeck, 1,
                        [ItemName.Knuckles.ShovelClaw]),

    LifeCapsuleLocation(4010, Area.TwinklePark, Character.Amy, Level.TwinklePark, 1, []),
    LifeCapsuleLocation(4110, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 1, []),
    LifeCapsuleLocation(4111, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 2, []),
    LifeCapsuleLocation(4112, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 3, []),
    LifeCapsuleLocation(4113, Area.EggCarrierMain, Character.Amy, Level.HotShelter, 4, []),
    LifeCapsuleLocation(4210, Area.Jungle, Character.Amy, Level.FinalEgg, 1, []),
    LifeCapsuleLocation(4211, Area.Jungle, Character.Amy, Level.FinalEgg, 2, []),

    LifeCapsuleLocation(5110, Area.Hotel, Character.Gamma, Level.EmeraldCoast, 1, []),
    LifeCapsuleLocation(5210, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, 1, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5211, Area.MysticRuinsMain, Character.Gamma, Level.WindyValley, 2, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5310, Area.AngelIsland, Character.Gamma, Level.RedMountain, 1, []),
    LifeCapsuleLocation(5410, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 1, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5411, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 2, [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5412, Area.EggCarrierMain, Character.Gamma, Level.HotShelter, 3, [ItemName.Gamma.JetBooster]),

    LifeCapsuleLocation(6110, Area.AngelIsland, Character.Big, Level.IceCap, 1,
                        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Train, ItemName.Big.LifeBelt]),
    LifeCapsuleLocation(6302, Area.EggCarrierMain, Character.Big, Level.HotShelter, 1, [ItemName.Big.LifeBelt]),
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


def get_location_from_life_capsule() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for life_capsule in life_capsule_location_table:
        level_name: str = f"{pascal_to_space(life_capsule.level.name)} ({life_capsule.character.name} - Life Capsule {life_capsule.lifeCapsuleNumber})"
        locations += [{"id": life_capsule.locationId, "name": level_name}]
    return locations


all_location_table: List[LocationInfo] = ((get_location_from_level() + get_location_from_upgrade()
                                           + get_location_from_sub_level() + get_location_from_emblem()
                                           + get_location_from_life_capsule()) +
                                          [{"id": 9, "name": "Perfect Chaos Fight"}])


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
