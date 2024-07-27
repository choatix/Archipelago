import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


def pascal_to_space(s):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s)


class Character(Enum):
    Sonic = 1
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()


EVERYONE: List[Character] = [Character.Sonic, Character.Tails, Character.Knuckles,
                             Character.Amy, Character.Big, Character.Gamma]
FLYERS: List[Character] = [Character.Tails, Character.Knuckles]


class Upgrade(Enum):
    LightShoes = auto()
    CrystalRing = auto()
    AncientLight = auto()
    JetAnkle = auto()
    RhythmBadge = auto()
    ShovelClaw = auto()
    FightingGloves = auto()
    LongHammer = auto()
    WarriorFeather = auto()
    JetBooster = auto()
    LaserBlaster = auto()
    LifeBelt = auto()
    PowerRod = auto()
    Lure1 = auto()
    Lure2 = auto()
    Lure3 = auto()
    Lure4 = auto()


class Level(Enum):
    EmeraldCoast = 0
    WindyValley = auto()
    Casinopolis = auto()
    IceCap = auto()
    TwinklePark = auto()
    SpeedHighway = auto()
    RedMountain = auto()
    SkyDeck = auto()
    LostWorld = auto()
    FinalEgg = auto()
    HotShelter = auto()


class SubLevelMission(Enum):
    B = 0
    A = auto()


class LevelMission(Enum):
    C = 0
    B = auto()
    A = auto()


class SubLevel(Enum):
    SandHill = auto()
    TwinkleCircuit = auto()


class AdventureField(Enum):
    StationSquare = auto()
    MysticRuins = auto()
    EggCarrier = auto()
    Past = auto()


class KeyItem(Enum):
    HotelKeys = auto()
    CasinoDistrictKeys = auto()
    TwinkleParkTicket = auto()
    EmployeeCard = auto()
    Dynamite = auto()
    IceStone = auto()
    JungleKart = auto()
    Train = auto()
    Boat = auto()
    Raft = auto()
    NONE = auto()


class StartingArea(Enum):
    StationSquareMain = 0
    HotelArea = auto()
    CasinoArea = auto()
    MysticRuinsMain = auto()
    Jungle = auto()
    EggCarrier = auto()


@dataclass
class AreaDetails:
    field: AdventureField
    keyItem: KeyItem


class Area(Enum):
    StationSquareMain = (AdventureField.StationSquare, KeyItem.NONE)
    Hotel = (AdventureField.StationSquare, KeyItem.HotelKeys)
    Casino = (AdventureField.StationSquare, KeyItem.CasinoDistrictKeys)
    TwinklePark = (AdventureField.StationSquare, KeyItem.TwinkleParkTicket)
    SpeedHighway = (AdventureField.StationSquare, KeyItem.EmployeeCard)
    MysticRuinsMain = (AdventureField.MysticRuins, KeyItem.NONE)
    AngelIsland = (AdventureField.MysticRuins, KeyItem.Dynamite)
    Jungle = (AdventureField.MysticRuins, KeyItem.JungleKart)
    EggCarrierMain = (AdventureField.EggCarrier, KeyItem.NONE)
