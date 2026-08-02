from dataclasses import dataclass

from . import Options, Names, Backtracking
from .LevelRegions.LevelRegion import LevelRegion
from .LevelRegions import Regions_Westopolis, Regions_DigitalCircuit, Regions_GlyphicCanyon, Regions_Bosses, \
    Regions_LethalHighway, Regions_CrypticCastle, Regions_PrisonIsland, Regions_CentralCity, Regions_TheDoom, \
    Regions_SkyTroops, Regions_MadMatrix, Regions_DeathRuins, Regions_CircusPark, Regions_TheArk, Regions_AirFleet, \
    Regions_IronJungle, Regions_SpaceGadget, Regions_LostImpact, Regions_BlackComet, Regions_LavaShelter, \
    Regions_CosmicFall, Regions_FinalHaunt, Regions_TheLastWay, Regions_GunFortress

from .Names import *

MISSION_ALIGNMENT_DARK = 0
MISSION_ALIGNMENT_NEUTRAL = 1
MISSION_ALIGNMENT_HERO = 2

LOCATION_ID_PLUS = 100066
LOCATION_ID_SHADOW_RIFLE_COMPLETE = 100067


STAGE_TO_STORY_BLOCK = \
{
    Names.STAGE_WESTOPOLIS: 5,
    Names.STAGE_DIGITAL_CIRCUIT: 6,
    Names.STAGE_GLYPHIC_CANYON: 7,
    Names.STAGE_LETHAL_HIGHWAY: 8,
    Names.STAGE_CRYPTIC_CASTLE: 9,
    Names.STAGE_PRISON_ISLAND: 10,
    Names.STAGE_CIRCUS_PARK: 11,
    Names.STAGE_CENTRAL_CITY: 12,
    Names.STAGE_THE_DOOM: 13,
    Names.STAGE_SKY_TROOPS: 14,
    Names.STAGE_MAD_MATRIX: 15,
    Names.STAGE_DEATH_RUINS: 16,
    Names.STAGE_THE_ARK: 17,
    Names.STAGE_AIR_FLEET: 18,
    Names.STAGE_IRON_JUNGLE: 19,
    Names.STAGE_SPACE_GADGET: 20,
    Names.STAGE_LOST_IMPACT: 21,
    Names.STAGE_GUN_FORTRESS: 22,
    Names.STAGE_BLACK_COMET: 23,
    Names.STAGE_LAVA_SHELTER: 24,
    Names.STAGE_COSMIC_FALL: 25,
    Names.STAGE_FINAL_HAUNT: 26,

    Names.STAGE_THE_LAST_WAY: 27,

    Names.BOSS_BLACK_BULL_LH: 28,
    Names.BOSS_EGG_BREAKER_CC: 29,
    Names.BOSS_HEAVY_DOG: 30,
    Names.BOSS_EGG_BREAKER_MM: 31,
    Names.BOSS_BLACK_BULL_DR: 32,
    Names.BOSS_BLUE_FALCON: 33,
    Names.BOSS_EGG_BREAKER_IJ: 34,
    Names.BOSS_BLACK_DOOM_GF:  35,
    Names.BOSS_DIABLON_GF: 36,
    Names.BOSS_EGG_DEALER_BC: 37,
    Names.BOSS_DIABLON_BC: 38,
    Names.BOSS_EGG_DEALER_LS: 39,
    Names.BOSS_EGG_DEALER_CF: 40,
    Names.BOSS_BLACK_DOOM_CF: 41,
    Names.BOSS_BLACK_DOOM_FH: 42,
    Names.BOSS_DIABLON_FH: 43,
    Names.BOSS_DEVIL_DOOM: 44

}

BOSS_GROUPING = {
    "Black Doom": [Names.BOSS_BLACK_DOOM_GF, Names.BOSS_BLACK_DOOM_CF, Names.BOSS_BLACK_DOOM_FH],
    "Egg Dealer": [Names.BOSS_EGG_DEALER_BC, Names.BOSS_EGG_DEALER_LS, Names.BOSS_EGG_DEALER_CF],
    "Diablon": [Names.BOSS_DIABLON_GF, Names.BOSS_DIABLON_BC, Names.BOSS_DIABLON_FH],
    "Egg Breaker": [Names.BOSS_EGG_BREAKER_CC, Names.BOSS_EGG_BREAKER_MM, Names.BOSS_EGG_BREAKER_IJ],
    "Black Bull": [Names.BOSS_BLACK_BULL_LH, Names.BOSS_BLACK_BULL_DR]

}


def IsObjectRestriction(restriction_types):

    objects_to_restrictions = Names.GetAssociatedRestrictionForObjects()
    for r in restriction_types:
        if r == Names.REGION_RESTRICTION_TYPES.NoRestriction:
            continue
        for o in objects_to_restrictions.values():
            if r == o:
                return True

    return False


class REGION_RESTRICTION_REFERENCE_TYPES:
    BaseLogic = 1
    BossLogic = 2

def IsWeaponsanityRestriction(restriction_types):
    weapons = [Names.REGION_RESTRICTION_TYPES.Torch, Names.REGION_RESTRICTION_TYPES.LongRangeGun,
               Names.REGION_RESTRICTION_TYPES.Vacuum, Names.REGION_RESTRICTION_TYPES.Gun,
               Names.REGION_RESTRICTION_TYPES.Heal, Names.REGION_RESTRICTION_TYPES.AnyStageWeapon,
               Names.REGION_RESTRICTION_TYPES.VacuumOrShot, Names.REGION_RESTRICTION_TYPES.VacuumWall,
               Names.REGION_RESTRICTION_TYPES.BombSuck,
               Names.REGION_RESTRICTION_TYPES.SatelliteGun]

    for w in weapons:
        if w in restriction_types:
            return True

    return False

def IsVeichleSanityRestriction(restriction_types):
    vehicles = [Names.REGION_RESTRICTION_TYPES.BlackHawk, Names.REGION_RESTRICTION_TYPES.BlackVolt,
                Names.REGION_RESTRICTION_TYPES.AirSaucer, Names.REGION_RESTRICTION_TYPES.Car,
                Names.REGION_RESTRICTION_TYPES.GunJumper, Names.REGION_RESTRICTION_TYPES.GunLift,
                Names.REGION_RESTRICTION_TYPES.BlackArmsTurret, Names.REGION_RESTRICTION_TYPES.GunTurret]

    for v in vehicles:
        if v in restriction_types:
            return True

    return False


@dataclass
class EscapePath:
    stageId: int
    escapeFrom: int
    escapeVia: []

    def __init__(self, stageId, escapeFrom, escapeVia):
        self.stageId = stageId
        self.escapeFrom = escapeFrom
        self.escapeVia = escapeVia


def IsRegionRestrictionApplication(region_restriction, options, starting_items):
    if region_restriction == Names.REGION_RESTRICTION_TYPES.ShootOrTurret and \
            not (options.weapon_sanity_unlock and options.vehicle_logic):
        return False

    if region_restriction == Names.REGION_RESTRICTION_TYPES.ShootOrTurret and "Vehicle:Gun Turret" in starting_items:
        return False

    if region_restriction == Names.REGION_RESTRICTION_TYPES.Explosion and not \
            (options.weapon_sanity_unlock or "Bombs" in options.object_unlocks):
        return False

    if region_restriction == Names.REGION_RESTRICTION_TYPES.Explosion and "Bombs" in starting_items:
        return False

    if IsWeaponsanityRestriction([region_restriction]) and not options.weapon_sanity_unlock:
        return False

    if IsVeichleSanityRestriction([region_restriction]) and not options.vehicle_logic:
        return False

    if IsObjectRestriction([region_restriction]):
        if not options.object_unlocks:
            return False

        objects_to_restrictions = Names.GetAssociatedRestrictionForObjects()
        associated_skill = [ x for x in objects_to_restrictions.items() if x[1] == region_restriction][0][0]

        associated_skill_name = associated_skill.name.replace('_',' ')
        if associated_skill_name not in options.object_unlocks or associated_skill_name in starting_items:
            return False

        # if (region_restriction == Names.REGION_RESTRICTION_TYPES.Zipwire and
        #         (not options.object_ziplines or "Zipwire" in starting_items)):
        #     return False
        # if (region_restriction == Names.REGION_RESTRICTION_TYPES.LightDash and
        #         (not options.object_light_dashes or "Air Shoes" in starting_items)):
        #     return False
        # if (region_restriction == Names.REGION_RESTRICTION_TYPES.WarpHole and
        #         (not options.object_warp_holes or "Warp Hole" in starting_items)):
        #     return False
        # if (region_restriction == Names.REGION_RESTRICTION_TYPES.Rocket and
        #         (not options.object_rockets or "Rocket" in starting_items)):
        #     return False
        # if (region_restriction == Names.REGION_RESTRICTION_TYPES.Pulley and
        #         (not options.object_pulleys or "Pulley" in starting_items)):
        #     return False

    return True

def IsLogicLevelApplicable(region, options, path_type, starting_items):

    logic_level = options.logic_level

    if path_type == REGION_RESTRICTION_REFERENCE_TYPES.BossLogic:

        if options.boss_logic_level == Options.BossLogicLevel.option_hard:
            if region.logicType == Options.LogicLevel.option_easy:
                return False

        logic_level = options.boss_logic_level

    region_restrictions = region.restrictionTypes

    if region.hardLogicOnly:
        if logic_level != Options.LogicLevel.option_hard:
            return False

    if region.logicType == Options.LogicLevel.option_easy and \
            logic_level != Options.LogicLevel.option_easy:
        return False

    if region.logicType == Options.LogicLevel.option_hard and \
            logic_level  == Options.LogicLevel.option_hard:
        return False

    if len(region_restrictions) == 1 and Names.REGION_RESTRICTION_TYPES.NoRestriction in region_restrictions and \
        len(region.fromRegions) == 1:
        return False

    if region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_easy and \
            options.chaos_control_logic_level != Options.ChaosControlLogicLevel.option_off:
        return False

    if region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_intermediate and \
            options.chaos_control_logic_level not in \
        [Options.ChaosControlLogicLevel.option_off, Options.ChaosControlLogicLevel.option_easy]:

        #if region.chaosControlLogicRequiresHeal:
        #    return True

        return False

    if region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_hard and \
            options.chaos_control_logic_level == Options.ChaosControlLogicLevel.option_hard:

        #if region.chaosControlLogicRequiresHeal:
        #    return True

        return False

    required = False
    for region_restriction in region_restrictions:
        r = IsRegionRestrictionApplication(region_restriction, options, starting_items)
        required = required or r

    return required

def GetBaseAccessibleRegions(stages, options, starting_items):
    accessible = {}
    for level in stages:
        accessible[level] = [0]
    for i in INDIVIDUAL_LEVEL_REGIONS:
        if i.stageId not in accessible:
            continue
        if not IsLogicLevelApplicable(i, options, None, starting_items):
            for f in i.fromRegions:
                if f in accessible[i.stageId]:
                    accessible[i.stageId].append(i.regionIndex)
                    break

    result = []
    for stage,regions in accessible.items():
        for r in regions:
            result.append((stage, r))

    return result


INDIVIDUAL_LEVEL_REGIONS = []

INDIVIDUAL_LEVEL_REGIONS.extend(Regions_Westopolis.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_DigitalCircuit.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_GlyphicCanyon.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_LethalHighway.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_CrypticCastle.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_PrisonIsland.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_CircusPark.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_CentralCity.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_TheDoom.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_SkyTroops.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_MadMatrix.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_DeathRuins.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_TheArk.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_AirFleet.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_IronJungle.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_SpaceGadget.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_LostImpact.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_GunFortress.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_BlackComet.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_LavaShelter.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_CosmicFall.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_FinalHaunt.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_TheLastWay.LEVEL_REGIONS)
INDIVIDUAL_LEVEL_REGIONS.extend(Regions_Bosses.LEVEL_REGIONS)

FINAL_STAGES = [STAGE_GUN_FORTRESS, STAGE_BLACK_COMET, STAGE_LAVA_SHELTER, STAGE_COSMIC_FALL, STAGE_FINAL_HAUNT]

# The order here matters, since this order is used to determine the flags to unlock these bosses in Select Mode
FINAL_BOSSES = [
    BOSS_BLACK_DOOM_GF,
    BOSS_DIABLON_GF ,
    BOSS_EGG_DEALER_BC,
    BOSS_DIABLON_BC,
    BOSS_EGG_DEALER_LS,
    BOSS_EGG_DEALER_CF,
    BOSS_BLACK_DOOM_CF,
    BOSS_BLACK_DOOM_FH,
    BOSS_DIABLON_FH
]



ALL_STAGES = list(LEVEL_ID_TO_LEVEL.keys())


DevilDoom_Name = "Devil Doom"
Anytime_Clear = "Anytime Clear"


# Starting at Westopolis Clear
# Levels store all ranks of missions even though they don't exist
# We can abuse this :)

ITEM_TOKEN_TYPE_STANDARD = 0
ITEM_TOKEN_TYPE_ALIGNMENT = 1
ITEM_TOKEN_TYPE_FINAL = 2
ITEM_TOKEN_TYPE_OBJECTIVE = 3
ITEM_TOKEN_TYPE_BOSS = 4
ITEM_TOKEN_TYPE_FINAL_BOSS = 5
ITEM_TOKEN_TYPE_PATH = 6
ITEM_TOKEN_TYPE_LAST_WAY = 7
ITEM_TOKEN_TYPE_CHARACTER = 8

TOKEN_TYPE_TO_STRING = \
{
    ITEM_TOKEN_TYPE_STANDARD: "Base",
    ITEM_TOKEN_TYPE_ALIGNMENT: "Alignment",
    ITEM_TOKEN_TYPE_FINAL: "Final",
    ITEM_TOKEN_TYPE_OBJECTIVE: "Objective",
    ITEM_TOKEN_TYPE_BOSS: "Boss",
    ITEM_TOKEN_TYPE_FINAL_BOSS: "Final Boss",
    ITEM_TOKEN_TYPE_PATH: "Path",
    ITEM_TOKEN_TYPE_LAST_WAY: "Last Way",
    ITEM_TOKEN_TYPE_CHARACTER: "Character"
}


def GetLevelTokenNames(stageId, alignmentId, type):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(type) + str(alignmentId) + "0")
    view_name = (LEVEL_ID_TO_LEVEL[stageId] + " Mission Token " + ALIGNMENT_TO_STRING[alignmentId] +
                 (" " + TOKEN_TYPE_TO_STRING[type] if type != ITEM_TOKEN_TYPE_STANDARD else "") )

    return id_name, view_name

def GetCharacterTokenNames(characterName, characterId, stageId, type):
    if stageId is None:
        stageId = 0


    id_name = int(str(LOCATION_ID_PLUS) + str(characterId) + str(stageId) + str(type) + "0")
    view_name = ("Character Token: " + characterName +
                 (" " + TOKEN_TYPE_TO_STRING[type] if type != ITEM_TOKEN_TYPE_STANDARD else "") )

    return id_name, view_name

def GetBossTokenNames(stageId, type):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(type) + "0")
    token_name_part = "Final Boss Token" if type == ITEM_TOKEN_TYPE_FINAL_BOSS else "Boss Token"
    view_name = f"{LEVEL_ID_TO_LEVEL[stageId]} {token_name_part}"

    return id_name, view_name

def GetLevelCompletionNames(stageId, alignmentId):

    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(alignmentId) + "1")
    view_name = LEVEL_ID_TO_LEVEL[stageId] + " Mission Clear " + ALIGNMENT_TO_STRING[alignmentId]

    return id_name, view_name


def GetLevelWarpName(stageId):
    id_name = int(str(LOCATION_ID_PLUS) + str(2) + str(stageId) + "11")
    view_name = LEVEL_ID_TO_LEVEL[stageId] + " Level Warp"

    return id_name, view_name

def GetLevelObjectNames(stageId, alignmentId, objectName, i):
    id_name =  int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(alignmentId) + str(i) + "0")
    objective_location_name = (LEVEL_ID_TO_LEVEL[stageId] + "-" +
                               objectName + " Count " + str(i))

    return id_name, objective_location_name

# Minimum requirements for minimal traversal (so add 1)
MINIMUM_STAGE_REQUIREMENTS = \
[
    (STAGE_WESTOPOLIS, MISSION_ALIGNMENT_HERO, 2),
    (STAGE_WESTOPOLIS, MISSION_ALIGNMENT_DARK, 6),

    (STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_HERO, 1),

    (STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_DARK, 2),
    # Circus Park Dark, probably not?

    (STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_DARK, 1),
    (STAGE_MAD_MATRIX, MISSION_ALIGNMENT_HERO, 1),
    (STAGE_DEATH_RUINS, MISSION_ALIGNMENT_HERO, 5),

    (STAGE_AIR_FLEET, MISSION_ALIGNMENT_HERO, 9),
    (STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_DARK, 2),
    # Iron Jungle Dark, probably not?
    (STAGE_SPACE_GADGET, MISSION_ALIGNMENT_DARK, 1),
    (STAGE_BLACK_COMET, MISSION_ALIGNMENT_DARK, 1),
    (STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_DARK, 2),
    (STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_DARK, 1)


]

NON_OBJECTIVESANITY_REGIONS = \
[
    (STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_KEY_DOOR),
    (STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_BLACK_VOLT)
]




UseCheckpointZeroCache = {}
HasCheckpointZeroCache = {}
HasGoalRingCheckpointCache = {}

def HasGoalRingCheckpoint(stage):
    key = stage

    if key in HasGoalRingCheckpointCache:
        return HasGoalRingCheckpointCache[key]

    return False

def UseCheckpointZero(stage,logic_level):
    key =  (stage, logic_level)

    if key in UseCheckpointZeroCache:
        return UseCheckpointZeroCache[key]

    has_zero = HasCheckpointZero(stage)
    if not has_zero:
        UseCheckpointZeroCache[key] = False
        return False

    # This needs to factor in accessibility from a checkpoint, just not from anywhere!

    stage_name = LEVEL_ID_TO_LEVEL[stage].upper().replace(" ","_")

    checkpoint_keys = list([k[1] for k in REGION_INDICES.__dict__.items() if
                            k[0].startswith(stage_name.upper()) and "CHECKPOINT_" in k[0]
                            and "ZERO" not in k[0]])

    b_regions = [ b for b in Backtracking.BACKTRACKING_REGIONS if b.stageId == stage and b.backtrackToRegion == 0 ]
    found = False
    for b_region in b_regions:
        safe_progression = False


        if b_region.hardLogicOnly:
            if logic_level == Options.LogicLevel.option_hard:
                safe_progression = True
        elif b_region.logicType == Options.LogicLevel.option_easy and logic_level != Options.LogicLevel.option_easy:
            safe_progression = True
        elif b_region.logicType == Options.LogicLevel.option_normal and logic_level != Options.LogicLevel.option_easy:
            safe_progression = True

        if safe_progression:

            if b_region.backtrackFromRegion in checkpoint_keys:
                found = True
                break
            else:
                new_b_regions = [b for b in Backtracking.BACKTRACKING_REGIONS if b.stageId == stage and b.backtrackToRegion == b_region.backtrackFromRegion and
                                 b not in b_regions]
                if len(new_b_regions) > 0:
                    b_regions.extend(new_b_regions)

    UseCheckpointZeroCache[key] = not found
    return not found


def HasCheckpointZero(stage):

    if stage in HasCheckpointZeroCache:
        return HasCheckpointZeroCache[stage]

    stage_name = LEVEL_ID_TO_LEVEL[stage].replace(" ", "_")
    checkpoint_keys = list([k for k in REGION_INDICES.__dict__.items() if
                            k[0].startswith(stage_name.upper()) and "CHECKPOINT_" in k[0] and
                            "CHECKPOINT_ZERO" in k[0]])

    hasCheckpointZero = len(checkpoint_keys) > 0
    HasCheckpointZeroCache[stage] = hasCheckpointZero
    return hasCheckpointZero

def stage_id_to_region(level_id: int, region_id) -> str:
    if level_id in BOSS_STAGES:
        raise Exception("Wrong function called" + str(level_id))
    region_name_base = Names.GetRegionName(level_id, region_id)
    region_name = "REGION_" + region_name_base
    return region_name

def boss_stage_id_to_region(level_id: int, region_id=0) -> str:
    if level_id not in BOSS_STAGES:
        raise Exception("Wrong function called" + str(level_id))
    level_name = LEVEL_ID_TO_LEVEL[level_id]
    region_name = "BOSS_REGION_" + level_name + "_" + str(region_id)
    return region_name



def BasePath(graph, start, goals, path=None):
    if path is None:
        path = []
    path = path + [start]  # create new list including this node

    if start in goals:
        return [path]  # one complete path found

    if start not in graph:
        return []  # dead end

    paths = []
    for neighbor in graph[start]:
        if neighbor not in path:  # avoid cycles / revisits
            new_paths = BasePath(graph, neighbor, goals, path)
            for p in new_paths:
                paths.append(p)
    return paths

def CheckpointEscapePathing(stage):
    graph = {}

    LH_regions = [i for i in INDIVIDUAL_LEVEL_REGIONS if i.stageId == stage]
    for region in LH_regions:
        fromRegions = region.fromRegions
        for i in fromRegions:
            if i not in graph:
                graph[i] = []

            graph[i].append(region.regionIndex)

        if region.isDiversion:
            for from_region in fromRegions:
                if region.regionIndex not in graph:
                    graph[region.regionIndex] = []

                toResult = str(from_region) + "d"
                graph[region.regionIndex].append(toResult)

                if toResult not in graph:
                    graph[toResult] = []

                graph[toResult].append(from_region)

    LH_bt_regions = [b for b in Backtracking.BACKTRACKING_REGIONS if b.stageId == stage]
    for b_region in LH_bt_regions:
        if b_region.backtrackFromRegion not in graph:
            graph[b_region.backtrackFromRegion] = []

        backtrackTo = str(b_region.backtrackToRegion) + "/" + str(b_region.backtrackFromRegion) + "b"
        graph[b_region.backtrackFromRegion].append(backtrackTo)

        if backtrackTo not in graph:
            graph[backtrackTo] = []

        graph[backtrackTo].append(b_region.backtrackToRegion)


    all_region_names = REGION_INDICES.__dict__.items()
    stage_name = LEVEL_ID_TO_LEVEL[stage].replace(" ", "_")
    stage_keys = [c for c in all_region_names if c[0].startswith(stage_name.upper())]
    checkpoint_keys = list([k for k in all_region_names if
                            k[0].startswith(stage_name.upper()) and
                            "CHECKPOINT_" in k[0] and "CHECKPOINT_ZERO" not in k[0]
                            ])

    checkpoint_indexes = [c[1] for c in checkpoint_keys]

    results = {}
    available_paths = BasePath(graph, 0, checkpoint_indexes, None)
    results[0] = available_paths
    for region in stage_keys:
        if region[1] == 0:
            continue

        available_paths = BasePath(graph, region[1], checkpoint_indexes, None)
        results[region[1]] = available_paths

    return results

def GenerateCheckpointPaths():
    checkpoint_paths = {}
    for stage in ALL_STAGES:
        results = CheckpointEscapePathing(stage)
        checkpoint_paths[stage] = results

    return checkpoint_paths


RegionEscapes = GenerateCheckpointPaths()
