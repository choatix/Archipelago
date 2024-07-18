from typing import List


class Progression:
    Emblem = "Emblem"
    ChaosPeace = "Chaos' Peace"


class KeyItem:
    Train = "Train"
    Boat = "Boat"
    Raft = "Raft"
    HotelKeys = "Hotel Keys"
    CasinoKeys = "Casino District Keys"
    TwinkleParkTicket = "Twinkle Park Ticket"
    EmployeeCard = "Employee Card"
    IceStone = "Ice Stone"
    Dynamite = "Dynamite"
    JungleKart = "Jungle Kart"


class Sonic:
    Playable = "Playable Sonic"
    LightShoes = "Light shoes (Sonic)"
    CrystalRing = "Crystal ring (Sonic)"
    AncientLight = "Ancient light (Sonic)"


class Tails:
    Playable = "Playable Tails"
    JetAnklet = "Jet Anklet (Tails)"
    RhythmBadge = "Rhythm Badge (Tails)"


class Knuckles:
    Playable = "Playable Knuckles"
    ShovelClaw = "Shovel claw (Knuckles)"
    FightingGloves = "Fighting gloves (Knuckles)"


class Amy:
    Playable = "Playable Amy"
    LongHammer = "Long Hammer (Amy)"
    WarriorFeather = "Warrior feather (Amy)"


class Gamma:
    Playable = "Playable Gamma"
    LaserBlaster = "Laser Blaster (Gamma)"
    JetBooster = "Jet booster (Gamma)"


class Big:
    Playable = "Playable Big"
    LifeBelt = "Life belt (Big)"
    PowerRod = "Power rod (Big)"
    Lure1 = "Lure 1 (Big)"
    Lure2 = "Lure 2 (Big)"
    Lure3 = "Lure 3 (Big)"
    Lure4 = "Lure 4 (Big)"


# TODO: Add lures
EVERY_LURE: List[str] = []
# EVERY_LURE: List[str] = [Big.Lure1, Big.Lure2, Big.Lure3, Big.Lure4]
