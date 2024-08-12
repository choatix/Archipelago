import re
from enum import Enum, auto
from typing import List

SADX_BASE_ID = 543800000


def pascal_to_space(s):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', ' ', s)


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
    SkyChaseAct1 = auto()
    SkyChaseAct2 = auto()


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
    Station = 0
    Hotel = auto()
    Casino = auto()
    MysticRuins = auto()
    Jungle = auto()
    EggCarrier = auto()


class Area(Enum):
    StationSquareMain = 0
    Station = auto()
    Hotel = auto()
    Casino = auto()
    TwinklePark = auto()
    SpeedHighway = auto()
    MysticRuinsMain = auto()
    AngelIsland = auto()
    Jungle = auto()
    EggCarrierMain = auto()
