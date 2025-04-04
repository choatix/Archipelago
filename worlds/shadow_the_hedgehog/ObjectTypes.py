
class ObjectType:
    SHADOW_BOX = 1

    VEHICLE = 2

    class ObjectTypeVehicle:
        STANDARD_CAR = 1
        CONVERTIBLE = 2
        ARMORED_CAR = 3
        GUN_MOTORCYCLE = 4
        GUN_JUMPER = 5
        GUN_CANNON = 6
        AIR_SAUCER = 7
        BLACK_HAWK = 8
        BLACK_VOLT = 9
        GUN_TURRET = 10
        BLACK_TURRET = 11
        GUN_LIFT = 12

    ENERGY_CORE = 4

    LIGHT_DASH_TRAIL = 5
    STANDARD_PULLEY = 6
    SPACE_ZIPWIRE = 7
    GUN_ZIPWIRE = 8
    CIRCUS_ZIPWIRE = 9

    BOMB = 10
    BOMB_SERVER= 11
    HEAL_UNIT = 12
    HEAL_SERVER = 13

    WARP_HOLE = 14
    ROCKET = 15

    KEY_DOOR = 16
    BALLOON_ZIPWIRE = 17

    SMALL_BOMB = 20
    SMALL_BOMB_AUTO_DETONATE = 21

    GUN_SOLIDER = 30
    GUN_BEETLE = 31
    GOLD_BEETLE = 32
    BIG_FOOT = 33
    GUN_ROBOT = 34

    EGG_CLOWN = 35
    EGG_PAWN = 36
    SHADOW_ANDROID = 37

    BLACK_ASSASSIN = 40
    BLACK_VOLT = 41
    BLACK_HAWK = 42
    BLACK_WARRIOR = 43
    BLACK_OAK = 44
    BLACK_WING = 45
    BLACK_WORM = 46
    BLACK_LARVAE = 47

    ARTIFICIAL_CHAOS = 48


class SETObject:
    object_type: int
    stage: int
    index: int
    name: str
    vehicle: int

    def __init__(self, object_type, stage, index, name,
                 vehicle=None, region=None, count=1):
        self.object_type = object_type
        self.stage = stage
        self.index = index
        self.name = name
        self.vehicle = vehicle
        self.region = region
        self.count = count
