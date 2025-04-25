
LOCATION_ID_PLUS_O = 110068

from .ObjectTypes import SETObject

STAGE_WESTOPOLIS = 100
STAGE_DIGITAL_CIRCUIT = 200
STAGE_GLYPHIC_CANYON = 201
STAGE_LETHAL_HIGHWAY = 202
STAGE_CRYPTIC_CASTLE = 300
STAGE_PRISON_ISLAND = 301
STAGE_CIRCUS_PARK = 302
STAGE_CENTRAL_CITY = 400
STAGE_THE_DOOM = 401
STAGE_SKY_TROOPS = 402
STAGE_MAD_MATRIX = 403
STAGE_DEATH_RUINS = 404
STAGE_THE_ARK = 500
STAGE_AIR_FLEET = 501
STAGE_IRON_JUNGLE = 502
STAGE_SPACE_GADGET = 503
STAGE_LOST_IMPACT = 504
STAGE_GUN_FORTRESS = 600
STAGE_BLACK_COMET = 601
STAGE_LAVA_SHELTER = 602
STAGE_COSMIC_FALL = 603
STAGE_FINAL_HAUNT = 604

BOSS_BLACK_BULL_LH = 210
BOSS_EGG_BREAKER_CC = 310
BOSS_HEAVY_DOG = 410
BOSS_EGG_BREAKER_MM = 411
BOSS_BLACK_BULL_DR = 412
BOSS_BLUE_FALCON = 510
BOSS_EGG_BREAKER_IJ = 511
BOSS_BLACK_DOOM_GF = 610
BOSS_DIABLON_GF = 611
BOSS_EGG_DEALER_BC = 612
BOSS_DIABLON_BC = 613
BOSS_EGG_DEALER_LS = 614
BOSS_EGG_DEALER_CF = 615
BOSS_BLACK_DOOM_CF = 616
BOSS_BLACK_DOOM_FH = 617
BOSS_DIABLON_FH = 618

STAGE_THE_LAST_WAY = 700
BOSS_DEVIL_DOOM = 710

LEVEL_ID_TO_LEVEL = {
    STAGE_WESTOPOLIS: "Westopolis",
    STAGE_DIGITAL_CIRCUIT: "Digital Circuit",
    STAGE_GLYPHIC_CANYON: "Glyphic Canyon",
    STAGE_LETHAL_HIGHWAY : "Lethal Highway",
    STAGE_CRYPTIC_CASTLE : "Cryptic Castle",
    STAGE_PRISON_ISLAND : "Prison Island",
    STAGE_CIRCUS_PARK : "Circus Park",
    STAGE_CENTRAL_CITY : "Central City",
    STAGE_THE_DOOM : "The Doom",
    STAGE_SKY_TROOPS : "Sky Troops",
    STAGE_MAD_MATRIX : "Mad Matrix",
    STAGE_DEATH_RUINS : "Death Ruins",
    STAGE_THE_ARK : "The Ark",
    STAGE_AIR_FLEET : "Air Fleet",
    STAGE_IRON_JUNGLE : "Iron Jungle",
    STAGE_SPACE_GADGET : "Space Gadget",
    STAGE_LOST_IMPACT : "Lost Impact",
    STAGE_GUN_FORTRESS : "Gun Fortress",
    STAGE_BLACK_COMET : "Black Comet",
    STAGE_LAVA_SHELTER : "Lava Shelter",
    STAGE_COSMIC_FALL : "Cosmic Fall",
    STAGE_FINAL_HAUNT : "Final Haunt",

    STAGE_THE_LAST_WAY : "The Last Way",

    BOSS_BLACK_BULL_LH: "Black Bull Lethal Highway",
    BOSS_EGG_BREAKER_CC: "Egg Breaker Cryptic Castle",
    BOSS_HEAVY_DOG: "Heavy Dog",
    BOSS_EGG_BREAKER_MM: "Egg Breaker Mad Matrix",
    BOSS_BLACK_BULL_DR: "Black Bull Death Ruins",
    BOSS_BLUE_FALCON: "Blue Falcon",
    BOSS_EGG_BREAKER_IJ:"Egg Breaker Iron Jungle",
    BOSS_BLACK_DOOM_GF: "Black Doom Gun Fortress",
    BOSS_DIABLON_GF: "Diablon Gun Fortress",
    BOSS_EGG_DEALER_BC: "Egg Dealer Black Comet",
    BOSS_DIABLON_BC: "Diablon Black Comet",
    BOSS_EGG_DEALER_LS : "Egg Dealer Lava Shelter",
    BOSS_EGG_DEALER_CF: "Egg Dealer Cosmic Fall",
    BOSS_BLACK_DOOM_CF: "Black Doom Cosmic Fall",
    BOSS_BLACK_DOOM_FH : "Black Doom Final Haunt",
    BOSS_DIABLON_FH: "Diablon Final Haunt",

    BOSS_DEVIL_DOOM: "Devil Doom"
}

override_strings = \
[
    "EA", "EG", "EE",
    "OD", "OH",
    "CD", "CH",
    "AD", "AH",
    "OED", "OEH",
    "OECD", "OECH",
    "OFD", "OFH",
    "OEFD", "OEFH",
    "EFE", "EFG", "EFH"

]


def getLevelNames():
    return [ v for v in LEVEL_ID_TO_LEVEL.values() if v != "Devil Doom" ]

def getValidPercentOverrides():
    options = []
    for s in override_strings:
        for l in getLevelNames():
            options.append(s+"."+l)

    return options


class REGION_INDICIES:
    WESTOPOLIS_PULLEY = 1
    WESTOPOLIS_KEY_DOOR = 2
    WESTOPOLIS_GOLD_BEETLE = 3

    DIGITAL_CIRCUIT_KEY_DOOR = 1
    DIGITAL_CIRCUIT_GOLD_BEETLE = 2
    DIGITAL_CIRCUIT_KEY_WARP_HOLE = 3
    DIGITAL_CIRCUIT_DARK_WARP_HOLE = 4

    GLYPHIC_CANYON_PULLEY = 1
    GLYPHIC_CANYON_KEY_DOOR = 2
    GLYPHIC_CANYON_BLACK_VOLT = 3

    LETHAL_HIGHWAY_KEY_DOOR = 1
    LETHAL_HIGHWAY_ROCKET = 2
    LETHAL_HIGHWAY_PULLEY = 3

    CRYPTIC_CASTLE_BALLOON = 1
    CRYPTIC_CASTLE_TORCH = 2
    CRYPTIC_CASTLE_BOMB_EASY_1 = 3
    CRYPTIC_CASTLE_HAWK = 4
    CRYPTIC_CASTLE_KEY_DOOR = 5
    CRYPTIC_CASTLE_BOMB_EASY_2 = 6

    PRISON_ISLAND_AIR_SAUCER = 1
    PRISON_ISLAND_KEY_DOOR = 2
    PRISON_ISLAND_PULLEY_EASY = 3
    PRISON_ISLAND_GOLD_BEETLE = 4

    CIRCUS_PARK_ZIP_WIRE = 1
    CIRCUS_PARK_ROCKET_EASY = 2
    CIRCUS_PARK_GUN_TURRET = 3
    CIRCUS_PARK_KEY_DOOR = 4
    CIRCUS_PARK_ROCKET = 5
    CIRCUS_PARK_PULLEY = 6

    CENTRAL_CITY_ROCKET_1 = 1
    CENTRAL_CITY_TRAVERSE_HARD = 2
    CENTRAL_CITY_ROCKET_1_OR_TRAVERSE_HARD = 3
    CENTRAL_CITY_BOMB_OR_BAZOOKA = 4
    CENTRAL_CITY_TRAVERSE_EASY = 5
    CENTRAL_CITY_KEY_DOOR = 6
    CENTRAL_CITY_BOMB_OR_BAZOOKA_2 = 7
    CENTRAL_CITY_GUN_TURRET = 8
    CENTRAL_CITY_ROCKET_2 = 9
    CENTRAL_CITY_BOMB_OR_BAZOOKA_3 = 10

    THE_DOOM_PULLEY = 1
    THE_DOOM_KEY_DOOR = 2
    THE_DOOM_BOMBS = 3
    THE_DOOM_PULLEY_2 = 4

    SKY_TROOPS_PULLEY = 1
    SKY_TROOPS_LIGHT_DASH = 2
    SKY_TROOPS_GUN_JUMPER_EASY = 3
    SKY_TROOPS_ROCKET_NORMAL = 4
    SKY_TROOPS_ROCKET = 5
    SKY_TROOPS_KEY_DOOR = 6
    SKY_TROOPS_BLACK_VOLT = 7
    SKY_TROOPS_BLACK_HAWK = 8
    SKY_TROOPS_HAWK_OR_VOLT = 9

    MAD_MATRIX_GUN = 1
    MAD_MATRIX_YELLOW_ENTRY = 2
    MAD_MATRIX_GREEN_ENTRY = 3
    MAD_MATRIX_GREEN_PROGRESSION = 4
    MAD_MATRIX_RED_ENTRY = 5
    MAD_MATRIX_KEY_DOOR = 6

    DEATH_RUINS_PULLEY = 1
    DEATH_RUINS_GOLD_BEETLE = 2
    DEATH_RUINS_KEY_DOOR = 3
    DEATH_RUINS_KEY_WARP = 4
    DEATH_RUINS_WALLS = 5

    THE_ARK_BLACK_VOLT = 1
    THE_ARK_KEY_DOOR = 2

    AIR_FLEET_PULLEY = 1
    AIR_FLEET_KEY_DOOR = 2
    AIR_FLEET_AIR_SAUCER = 3
    AIR_FLEET_RAIL_HARD = 4
    AIR_FLEET_RAILS = 5
    AIR_FLEET_GOLD_BEETLE = 6

    IRON_JUNGLE_KEY_DOOR = 1
    IRON_JUNGLE_PULLEY_NORMAL = 2
    IRON_JUNGLE_ROCKET = 3
    IRON_JUNGLE_GUN_JUMPER = 4
    IRON_JUNGLE_LIGHT_DASH = 5
    IRON_JUNGLE_GUN_TURRET = 6

    SPACE_GADGET_ZIPWIRE = 1
    SPACE_GADGET_AIR_SAUCER = 2
    SPACE_GADGET_KEY_DOOR = 3
    SPACE_GADGET_WARP_HOLE = 4
    SPACE_GADGET_WARP_HOLE_DARK = 5

    LOST_IMPACT_GUN_LIFT = 1
    LOST_IMPACT_PULLEY = 2
    LOST_IMPACT_KEY_DOOR = 3
    LOST_IMPACT_ROCKET = 4
    LOST_IMPACT_BOMB_WALL = 5

    # At start, no pulley required, but found required for tunnels
    GUN_FORTRESS_GUN_TURRET = 1
    GUN_FORTRESS_TURRET_OR_FIRE = 2
    GUN_FORTRESS_ZIPWIRE_NORMAL = 3
    GUN_FORTRESS_PULLEY = 4
    GUN_FORTRESS_ZIPWIRE = 5
    GUN_FORTRESS_ROCKET_NORMAL = 6
    GUN_FORTRESS_KEY_DOOR = 7
    GUN_FORTRESS_ZIPLINE_HARD = 8
    GUN_FORTRESS_KEY_OR_ZIPLINE = 9

    BLACK_COMET_AIR_SAUCER = 1
    BLACK_COMET_FLOATERS = 2
    BLACK_COMET_WARP_HOLE = 3
    BLACK_COMET_FLOATERS_2 = 4
    BLACK_COMET_FLOATING_ENEMY_WALL = 5
    BLACK_COMET_KEY_DOOR = 6

    LAVA_SHELTER_KEY_DOOR = 1
    LAVA_SHELTER_AIR_SAUCER = 2
    LAVA_SHELTER_PULLEY = 3
    LAVA_SHELTER_PULLEY_OR_LAVA = 4
    LAVA_SHELTER_LIGHT_DASH_DARK = 5
    LAVA_SHELTER_PULLEY_DARK = 6

    COSMIC_FALL_ZIPWIRE = 1
    COSMIC_FALL_PULLEY_NORMAL = 2
    COSMIC_FALL_PULLEY_CORE = 3
    COSMIC_FALL_KEY_DOOR = 4
    COSMIC_FALL_LIGHT_DASH = 5
    COSMIC_FALL_GUN_JUMPER = 6
    COSMIC_FALL_LD_OR_JUMPER = 7
    COSMIC_FALL_ROCKET = 8

    FINAL_HAUNT_VACUUM = 1
    FINAL_HAUNT_VACUUM_HARD = 2
    FINAL_HAUNT_BLACK_VOLT = 3
    FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT = 4
    FINAL_HAUNT_SHIELD_COUNT_2 = 5
    FINAL_HAUNT_ROCKET_NORMAL = 6
    FINAL_HAUNT_BLACK_VOLT_2 = 7
    FINAL_HAUNT_KEY_DOOR = 8
    FINAL_HAUNT_LIGHT_DASH = 9
    #FINAL_HAUNT_SHIELD_3_BASE_ACCESS = 10
    FINAL_HAUNT_SHIELD_COUNT_3 = 10
    FINAL_HAUNT_KEY_DOOR_2 = 11
    FINAL_HAUNT_SHIELD_4 = 12

    THE_LAST_WAY_BLACK_VOLT = 1
    THE_LAST_WAY_KEY_DOOR = 2
    THE_LAST_WAY_WARP_HOLE = 3
    THE_LAST_WAY_VOLT_OR_WARP = 4
    THE_LAST_WAY_LIGHT_DASH_EASY = 5


LEVEL_ID_TO_LEVEL = {
    STAGE_WESTOPOLIS: "Westopolis",
    STAGE_DIGITAL_CIRCUIT: "Digital Circuit",
    STAGE_GLYPHIC_CANYON: "Glyphic Canyon",
    STAGE_LETHAL_HIGHWAY : "Lethal Highway",
    STAGE_CRYPTIC_CASTLE : "Cryptic Castle",
    STAGE_PRISON_ISLAND : "Prison Island",
    STAGE_CIRCUS_PARK : "Circus Park",
    STAGE_CENTRAL_CITY : "Central City",
    STAGE_THE_DOOM : "The Doom",
    STAGE_SKY_TROOPS : "Sky Troops",
    STAGE_MAD_MATRIX : "Mad Matrix",
    STAGE_DEATH_RUINS : "Death Ruins",
    STAGE_THE_ARK : "The Ark",
    STAGE_AIR_FLEET : "Air Fleet",
    STAGE_IRON_JUNGLE : "Iron Jungle",
    STAGE_SPACE_GADGET : "Space Gadget",
    STAGE_LOST_IMPACT : "Lost Impact",
    STAGE_GUN_FORTRESS : "Gun Fortress",
    STAGE_BLACK_COMET : "Black Comet",
    STAGE_LAVA_SHELTER : "Lava Shelter",
    STAGE_COSMIC_FALL : "Cosmic Fall",
    STAGE_FINAL_HAUNT : "Final Haunt",

    STAGE_THE_LAST_WAY : "The Last Way",

    BOSS_BLACK_BULL_LH: "Black Bull Lethal Highway",
    BOSS_EGG_BREAKER_CC: "Egg Breaker Cryptic Castle",
    BOSS_HEAVY_DOG: "Heavy Dog",
    BOSS_EGG_BREAKER_MM: "Egg Breaker Mad Matrix",
    BOSS_BLACK_BULL_DR: "Black Bull Death Ruins",
    BOSS_BLUE_FALCON: "Blue Falcon",
    BOSS_EGG_BREAKER_IJ:"Egg Breaker Iron Jungle",
    BOSS_BLACK_DOOM_GF: "Black Doom Gun Fortress",
    BOSS_DIABLON_GF: "Diablon Gun Fortress",
    BOSS_EGG_DEALER_BC: "Egg Dealer Black Comet",
    BOSS_DIABLON_BC: "Diablon Black Comet",
    BOSS_EGG_DEALER_LS : "Egg Dealer Lava Shelter",
    BOSS_EGG_DEALER_CF: "Egg Dealer Cosmic Fall",
    BOSS_BLACK_DOOM_CF: "Black Doom Cosmic Fall",
    BOSS_BLACK_DOOM_FH : "Black Doom Final Haunt",
    BOSS_DIABLON_FH: "Diablon Final Haunt",


    BOSS_DEVIL_DOOM: "Devil Doom"
}

ALIGNMENT_TO_STRING = \
{
    0: "Dark",
    1: "Neutral",
    2: "Hero"
}

def GetMissionClearEventName(stageId, alignmentId):
    view_name = f"Story_{LEVEL_ID_TO_LEVEL[stageId]}_{ALIGNMENT_TO_STRING[alignmentId]}".replace(" ", "_").upper()
    return view_name

def GetDistributionRegionEventName(stageId, index):
    stage_name = LEVEL_ID_TO_LEVEL[stageId]
    region_name = "DISTRIBUTION_" + stage_name.upper().replace(" ", "_")+"_ENTRANCE"
    if index == 0:
        return region_name

    for name,lookup_index in REGION_INDICIES.__dict__.items():
        if name.startswith(stage_name.upper().replace(" ","_")) and \
            index == lookup_index :
            region_name = "DISTRIBUTION_" + name

    return region_name

def GetBossClearEventName(stageId, from_id, alignment_id):
    view_name = ("Story_" + LEVEL_ID_TO_LEVEL[stageId] +
                 f"_{from_id}_{alignment_id}")\
    .replace(" ", "_").upper()
    return view_name

def GetObjectLocationName(object: SETObject):
    id_name = int(str(LOCATION_ID_PLUS_O) + str(2) + str(object.stage) + "0" + str(object.index))
    view_name = LEVEL_ID_TO_LEVEL[object.stage] + "-" + object.name

    return id_name, view_name

def GetNameForVehicle(baseName):
    return f"Vehicle:{baseName}"

class REGION_RESTRICTION_TYPES:
    KeyDoor = 1
    BlackHawk = 2
    BlackVolt = 3
    Torch = 4
    AirSaucer = 5
    Car = 6
    GunJumper = 7
    LongRangeGun = 8
    GunLift = 9
    NoRestriction = 10
    Vacuum = 11
    Gun = 12
    Heal = 13,
    BlackArmsTurret = 14
    GunTurret = 15
    ShootOrTurret = 16
    AnyStageWeapon = 17
    ShadowRifle = 18

    HealCannonOrLongRangeGun = 19
    Pulley = 20
    WarpHole = 21
    Rocket = 22
    Zipwire = 23
    Explosion = 24 # Access to Bazooka, or Bombs
    LightDash = 25
    HardLogicOnly = 26
    GoldBeetle = 27