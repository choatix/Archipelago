import copy
import logging
import math
from typing import List

from . import Utils as ShadowUtils

from dataclasses import dataclass

from Options import OptionError
from . import Levels, Options, Locations


@dataclass
class PathInfo:
    start_stage_id: int
    alignment_id: int
    end_stage_id: int
    cutscenes: []
    boss = None

    def __init__(self, o_id, alignment, n_id, cutscenes):
        self.start_stage_id = o_id
        self.alignment_id = alignment
        self.end_stage_id = n_id
        self.cutscenes = cutscenes
        self.boss = None

    def via_boss(self, boss):
        self.boss = boss
        return self

    def __str__(self):
        start = "START" if self.start_stage_id is None else Levels.LEVEL_ID_TO_LEVEL[self.start_stage_id]
        end = "END" if self.end_stage_id is None else Levels.LEVEL_ID_TO_LEVEL[self.end_stage_id]
        alignment = Levels.ALIGNMENT_TO_STRING[self.alignment_id] if self.alignment_id is not None else ""
        boss = "" if self.boss is None else " via " + Levels.LEVEL_ID_TO_LEVEL[self.boss]

        return f"{start} {alignment}{boss}>{end}\n"


@dataclass
class LibraryInfo:
    index: int
    library_name: str
    required_levels: List[int]



DefaultStoryMode = \
[
    PathInfo(None, None, Levels.STAGE_WESTOPOLIS, []),

    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_DIGITAL_CIRCUIT, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_GLYPHIC_CANYON, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LETHAL_HIGHWAY, [])
    ,
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_PRISON_ISLAND, []),

    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_PRISON_ISLAND, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, []),

    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_PRISON_ISLAND, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),
    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),

    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CENTRAL_CITY, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_THE_DOOM, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SKY_TROOPS, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),

    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_DOOM, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_MAD_MATRIX, []),

    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_MAD_MATRIX, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_DEATH_RUINS, []),

    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, []),
    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_AIR_FLEET, []),

    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_AIR_FLEET, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),

    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_AIR_FLEET, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_IRON_JUNGLE, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SPACE_GADGET, []),

    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),

    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),
    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),

    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),
    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),

    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LAVA_SHELTER, []),

    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_LAVA_SHELTER, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_COSMIC_FALL, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),

    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_LAVA_SHELTER, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_GF),
    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_GF),

    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_BC),
    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_BC),

    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),
    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),

    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_CF),
    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_CF),

    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_FH),
    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_FH),

]

def GetBossAssociatedWithStage(stage_id, alignment):
    stages = [(b.boss, b.alignment_id) for b in DefaultStoryMode if b.start_stage_id == stage_id]

    if alignment is None:
        return stages[0][0]
    else:
        found = [ s[0] for s in stages if s[1] == alignment]
        if len(found) > 0:
            return found[0]

        return None



def AddMissingLevels(levels, end_alignment):
    new_levels = []
    for l in levels:
        if l in Levels.FINAL_STAGES:
            boss = GetBossAssociatedWithStage(l, end_alignment)
            new_levels.append((l, end_alignment))
            new_levels.append(boss)
        else:
            next_level = levels[levels.index(l) + 1]
            stage = [ s for s in DefaultStoryMode if s.start_stage_id == l and s.end_stage_id == next_level ]
            if len(stage) > 0:
                stage = stage[0]
                new_levels.append((l, stage.alignment_id))
            else:
                print("Error with library stage lookup")

            boss = GetBossAssociatedWithStage(l, None)
            if boss is not None:
                new_levels.append(boss)

    return new_levels

def GetLibraries():

    libraries = []
    libraries.append(LibraryInfo(1, "Punishment, Thy Name is Ruin", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(2, "Prologue to World Conquest", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(3, "The March to a Darker World", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(4, "The Ultimate Ego", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(5, "Purification via Ruination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(6, "Apogee of Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(7, "True Soldier of Destruction", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(8, "Believe in Yourself", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(9, "An Android's Determination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(10, "For Machine, By Machine...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(11, "Revenge at Last", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(12, "Ego's Awakening", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(13, "Destruction and Scorn", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(14, "The Last Remaining Purpose", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(15, "The Nightmare's Insulation", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(16, "The Nightmare's Sublimation", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(17, "The Loner's Choice", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(18, "Subjugation in Black", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(19, "Replica's Depression", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(20, "Machine, Machine", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(21, "Disciple from the Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(22, "Beloved Clone", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(23, "Revenge Upon the Doctor", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(24, "The Ultimate Replica", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(25, "Sanction's Demise", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(26, "Along With My Home", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(27, "The Cleansing of Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(28, "Birth of a God", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(29, "The Last Soldier's Grim Fate", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(30, "Isolation and Solitude", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(31, "Archimedes and the Tortoise", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(32, "Where Is My Happiness?", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(33, "Seduced By Taste of Blood", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(34, "A Machine Made for War", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(35, "Original Definition", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(36, "Machine Paradise", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(37, "Last Will and Testament", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(38, "Enveloped in Solitude", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(39, "Parricidal Savior", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(40, "Copy of a Savior", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(41, "Excess of Intellect", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(42, "Crystallization of Intellect", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(43, "The Ultimate Confrontation", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(44, "Miracle of Love", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(45, "The World's Demise", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(46, "The Ultimate Power", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(47, "Dyed in Lovely Darkness...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(48, "Vainglory or Abandonment?", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(49, "Messenger of Ruination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(50, "Standing at the Summit", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(51, "Controller from the Capsule", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(52, "Beyond One’s Own Power...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(53, "A Clone's Determination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(54, "Machine Utopia", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(55, "A Toast to the Ruler", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(56, "Answer from the Black Comet", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(57, "Transcendentalism", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(58, "Imperialism", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(59, "The Weight of One's Crimes", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(60, "Imprisoned by the Past...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(61, "The Ultimate World Conquest", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(62, "Black Angel", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(63, "Under Darkness’ Control", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(64, "To Love Oneself", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(65, "Revenge and Determination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(66, "Birth of the Robot Emperor", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(67, "Shadow, the Black Android", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(68, "A Solitary Android", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(69, "Over the Original", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(70, "Machine Sunshine", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(71, "Life is Guilty", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(72, "Fallen Angel of Despair", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(73, "An Eternal Rival...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(74, "This is Just the Beginning", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(75, "Crystal of Tragic Knowledge", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(76, "Shadow's Second Death...?", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(77, "The Legend of Shadow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(78, "Power of Love", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(79, "Deep Black", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(80, "Walk My Way", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(81, "This is Shadow's Way of Life", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(82, "A Monarch's Style", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(83, "In the Gap of Sadness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(84, "To Be Ignorant of the Past", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(85, "At Vengeance's End", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(86, "Machine Boys", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(87, "Reborn Along with Sorrow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(88, "With a Fate of Self-Denial", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(89, "I Am Shadow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(90, "Shining Within Memory...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(91, "The Rise and Fall of the ARK", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(92, "Requiem for a Fallen Angel", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(93, "Ultimate Shadow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(94, "For Love's Sake", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(95, "A Heart Awoken from Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(96, "Destruction From Perfection", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(97, "Darkness’ Strongest Soldier", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(98, "Severed Chains", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(99, "Retribution Against Humanity", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(100, "To Be Known as ‘Ultimate’", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(101, "Dark Warrior’s Advent", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(102, "Arriving at the Ego", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(103, "Determination of a Fake", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(104, "Path to the Machine Empire", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CENTRAL_CITY,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(105, "Demise Wrought by Tragedy", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(106, "Turning Sorrow Into Strength", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(107, "The Liberated Soldier", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(108, "Stupefaction’s End", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(109, "Humanity’s Folly", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(110, "Surpassing All Else", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(111, "Soldier of Grief", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(112, "Reclaimed Heart", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(113, "Fighting Spirit of Steel", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(114, "Machine Soldier Uprising", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(115, "The Devil Born From Betrayal", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(116, "Beyond the Truth of Impact", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(117, "The Immortal Android", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(118, "The New, Coldhearted Empire", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(119, "A Singular Atonement", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(120, "Spawn of the Devil", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(121, "Black Doom's Scheme", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(122, "Subjugating Heaven and Earth", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(123, "Road of the Dark Soldier", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(124, "Dark Finale", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(125, "Realization While On Board", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(126, "Birth of a Champion", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(127, "With the Black Arms", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(128, "The Road to Self-Assurance", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(129, "The Pursuit of Dr. Eggman", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(130, "Surpassing His Creator", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(131, "ARK, Colony of Pathos", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(132, "Perfection Lost to Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(133, "A New Challenge", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(134, "The Machines' Coup d'Etat", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(135, "A Vow for the Victims", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(136, "The Truth of Sadness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(137, "The Destined Sonic Showdown", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(138, "The Black Hero’s Rebirth", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(139, "Truth, Thy Name is Vengeance", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(140, "Searching for 'Ultimate'", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(141, "Reborn Hatred for Humanity", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(142, "A Future Taken from the Past", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(143, "The Devils’ Victory Song", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(144, "One to Succeed a God", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(145, "Disappointed in Humanity", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(146, "Faith Taken from Solitude", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(147, "Planted Memories", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(148, "To Unite Humanity", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(149, "Isolated Soldier Shadow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(150, "Answer Derived from Truth", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(151, "A Fake’s Disposition", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(152, "A New World Without Betrayal", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(153, "Together With Maria...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(154, "The Tragedy’s Conclusion", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(155, "The Day That Hope Died", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(156, "Dark Destroyer", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(157, "Diabolical Power", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(158, "For Freedom", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(159, "At Least, Be Like Shadow...", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(160, "Seeking a Silent Paradise", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(161, "The Lion’s Awakening", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(162, "Identity", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(163, "An Android's Rebellion", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(164, "A New Empire's Beginning", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(165, "Bullets from Tears", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(166, "Journey to Nihility", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(167, "Shadow Surpassing Shadow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(168, "Dr. Eggman’s Miscalculation", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(169, "Along with the ARK", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(170, "Requiem for the Heavens", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(171, "Sonic Dethroned!", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(172, "Justice Reborn in Space", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(173, "Steel Ruler", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(174, "For the Sake of the Self", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(175, "Farewell to the Past", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(176, "Steel Paradise", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(177, "The Guardian With No Past", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(178, "The Ultimate Atonement", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(179, "A Fake's Aspiration", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(180, "Machine World", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(181, "Twilight Ark", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(182, "Compensation for a Miracle", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(183, "The Strongest Hedgehog", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(184, "The Ultimate Punisher", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(185, "Voyage of Reminiscence", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(186, "Wandering's End", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(187, "The Ultimate Proof", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(188, "Punisher of Love", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(189, "Messenger from the Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(190, "The New Ruler", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(191, "Dark Soldier", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(192, "The Road of Light", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(193, "The Machine-Laden Kingdom", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(194, "New Determination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(195, "Birth of the Dark Soldier", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(196, "A New Journey", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(197, "The Android’s Opposition", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(198, "Founding of the Robot Nation", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(199, "The Eternal Protector", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(200, "The Sinner’s Repose", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(201, "A Hero’s Resolution", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(202, "The Weapons’ Empire", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(203, "Perpetual Voyage", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(204, "A Hero’s Atonement", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(205, "Dark Hegemony", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(206, "And the Dream Continues", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(207, "Fighter for Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(208, "The Path I Believed In", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(209, "Determination’s Daybreak", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(210, "Machine Kingdom at Dawn", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(211, "Sinful Protector", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(212, "At the End of the Journey", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(213, "Surmounting the Nightmare", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(214, "Dawn of the Machines", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(215, "Wandering for Eternity", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(216, "At Vagrancy’s End", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(217, "The Summit of Power", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(218, "Under the Name of Love", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(219, "Eternally Drifting", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(220, "The Importance of Truth", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(221, "The Beginning of Judgment", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(222, "This World’s Guardian", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(223, "Light Born from Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(224, "The Order of Steel", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(225, "Solitary Journey", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(226, "The Fall Home", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(227, "Sovereign of All Creation", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(228, "I Shall Be the One to Judge", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(229, "Gone With the Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(230, "The Ultimate Choice", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(231, "I Am the Strongest!", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(232, "Justice’s Awakening", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(233, "Prelude to Ruination", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(234, "A World United by Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(235, "The Pulse of Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(236, "To Just Be Myself", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_THE_ARK, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(237, "Punishment in Jet Black", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(238, "The Ruler’s First Cry", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(239, "Darkness’ Conspiracy", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(240, "The Faint Light of Tomorrow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(241, "Time of Departure", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(242, "Rise of the Machine Kingdom", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(243, "Despair’s Quickening", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(244, "The Beginning", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(245, "Setting Out in the Morning", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(246, "The Weapons’ Dawn", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(247, "Pure Ark", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(248, "Making Up For It in the End", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_THE_DOOM,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(249, "The Coming of the Dark Time", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(250, "The Throne of God", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(251, "God of War", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(252, "Howl of Solitude", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(253, "Proof of Existence", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(254, "Ardent Vow", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(255, "A Deal With the Devil", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(256, "A Reason to Live", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(257, "Induplicable Thoughts", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(258, "Steel Struck With Flame", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(259, "A Heart Bound to the ARK", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(260, "Tears Shed by the Stars", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(261, "Imitation Complex", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(262, "Steel Combat Boots", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(263, "Protector of the Ashen Moon", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(264, "A Demon Drifting", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(265, "The Ultimate Pride", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(266, "I Know the Will of Heaven", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(267, "Ego Dyed in Black", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(268, "Isolation By Choice", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(269, "Faith Without Falsehood", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(270, "Machine Empire", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(271, "The Eternally-Closed Door", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(272, "The Sealed-Away Ark of Sin", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(273, "Silver Emergence", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(274, "Pulsating Supercurrent", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(275, "The Reason I Was Born", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(276, "The Dark Part of the Galaxy", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(277, "The View From Atop the World", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(278, "Maria’s Testament", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(279, "A Genius Scientist’s Lineage", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(280, "Distorted Truth", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(281, "A Counterfeit Existence", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(282, "Beloved Memories", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(283, "Birth of a Devil", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(284, "A Dark Myth’s Beginnings", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_GUN_FORTRESS], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(285, "Black Thunder", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(286, "The Torn-Away Necklace", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(287, "A Soul Sheltered by Iron", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(288, "Steel Nation’s Decree", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_AIR_FLEET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(289, "Coronation of Darkness", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(290, "Opened Eyes", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(291, "The Doctor’s Lie", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(292, "The Uninvited Successor", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(293, "The Closed Pandora’s Box", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(294, "A Heart Bound by Sin", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(295, "Courage from Turning Gears", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(296, "Fullmetal Prince", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(297, "Time’s Watchman", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(298, "Galaxy’s Requiem", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(299, "Charm of the Chaos Emeralds", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(300, "Promise of a Far-Off Day", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(301, "The Grim Reaper’s Horn", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(302, "A Flame Extinguished by Fate", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_BLACK_COMET], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(303, "Shouting at the Morning Sun", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(304, "Iron Ambition", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(305, "Sleeping on Hallowed Ground", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(306, "Explanation of the Truth", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_IRON_JUNGLE, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(307, "An Android’s Dream", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(308, "Metallic Quickening", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(309, "Funeral Procession in Space", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(310, "Lost to the Universe’s Abyss", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(311, "Destiny for Two", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(312, "The Spun Threads of Fate", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(313, "Ark of the Heavens", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(314, "Ghost of the ARK", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(315, "A Pair of Shooting Stars", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(316, "The One Who Maria Entrusted", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_MAD_MATRIX,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(317, "A.I.’s Enlightenment", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(318, "A Dying Empire’s Cry", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_LAVA_SHELTER], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(319, "Moon of Atonement", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(320, "Tear-Soaked Hometown", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(321, "Sparks on the Horizon", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(322, "A Use for a Saved Life", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_SPACE_GADGET, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(323, "Coffin of Memories", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(324, "The Self-Imposed Seal", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_COSMIC_FALL], Levels.MISSION_ALIGNMENT_HERO)))
    libraries.append(LibraryInfo(325, "Pretense in the Mirror", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_DARK)))
    libraries.append(LibraryInfo(326, "A Missive from 50 Years Ago", AddMissingLevels(
        [Levels.STAGE_WESTOPOLIS, Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_DEATH_RUINS,
         Levels.STAGE_LOST_IMPACT, Levels.STAGE_FINAL_HAUNT], Levels.MISSION_ALIGNMENT_HERO)))
    return libraries

Libraries = GetLibraries()

def GetVanillaBossStage(boss):
    stages = [ b.start_stage_id for b in DefaultStoryMode if b.boss == boss]
    if len(stages) > 0:
        return stages[0]

    return None



def SortByAvailableLength(item):
    return len(item[1])

def ChoosePathOption(world, story_options):

    # Increase likelihood of taking hero/dark path depending on goal conditions

    balancing_value = world.options.story_progression_balancing
    hero_ratio_base = world.options.goal_hero_missions + 1
    dark_ratio_base = world.options.goal_dark_missions + 1

    sorted_options = sorted(story_options, key=SortByAvailableLength)

    balance_index = (len(sorted_options) - 1) / 100 * balancing_value
    chosen_index = round(balance_index)

    weights = []
    for i in range(0, len(story_options)):
        story_option_path = story_options[i][0]
        weight_value = 1000 / pow((abs(chosen_index-i) + 1), 2)

        if story_option_path.alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            weight_value *= (dark_ratio_base/hero_ratio_base)

        if story_option_path.alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            weight_value *= (hero_ratio_base/dark_ratio_base)

        weights.append(weight_value)


    randomised_item = world.random.choices(story_options, k=1, weights=weights)[0]

    #print("SOI", story_options.index(randomised_item), weights, chosen_index)

    # If 100: always the last item in the list
    # If 1, always the first item in the list

    return randomised_item

def PrintStoryMode(world, spoiler_handle):
    if spoiler_handle is not None:
        spoiler_handle.write(f"{world.multiworld.get_player_name(world.player)}'s Shuffled Story Path\n")
    for stage in world.shuffled_story_mode:
        text = str(stage)
        if spoiler_handle is not None:
            spoiler_handle.writelines(text)
        else:
            print("SS", text)
    if spoiler_handle is not None:
        spoiler_handle.write("\n")

def TraversePath(story, available_stages, available_missions):
    clear_locations = Locations.MissionClearLocations

    unhandled_progression = [[s for s in story if s.start_stage_id == c.stageId and s.alignment_id == c.alignmentId][0].end_stage_id
                             for c in clear_locations if c in available_missions and
                             [s for s in story if s.start_stage_id == c.stageId and s.alignment_id == c.alignmentId][
                                 0].end_stage_id not in available_stages
                             ]

    unhandled_progression = [ u for u in unhandled_progression if u is not None]

    available_stages.extend(unhandled_progression)

    first = True
    new_available_without_objectivesanity = []
    while first or len(new_available_without_objectivesanity) != 0:
        first = False

        available_without_objectivesanity = [c for c in clear_locations if c.stageId in available_stages
                                             and c.requirement_count is None]

        new_available_without_objectivesanity = [a for a in available_without_objectivesanity if
                                                 a not in available_missions]


        for mission_clear in new_available_without_objectivesanity:
            story_element = [c for c in story if c.start_stage_id == mission_clear.stageId
                             and c.alignment_id == mission_clear.alignmentId][0]

            if story_element.end_stage_id is not None and story_element.end_stage_id not in available_stages:
                available_stages.append(story_element.end_stage_id)

            available_missions.append(mission_clear)

class StoryAssignmentObject:
    start_stage_id: int
    alignmentId: int
    end_start_id: int
    mission_id: int


def DecideStoryPath(world, story):
    clear_locations = Locations.MissionClearLocations
    starting_stage = [ s for s in story if s.start_stage_id is None]

    stage = starting_stage[0]

    stages = [ x for x in Levels.ALL_STAGES if x not in Levels.BOSS_STAGES and
                        x in world.available_story_levels]

    stage_count = len(stages)

    available_stages = [stage.end_stage_id]
    available_missions = []
    TraversePath(story, available_stages, available_missions)

    # Add sphere 0
    sphere_results = [(None, available_stages, available_missions)]

    while len(available_stages) < stage_count:
        objectivesanity_missions = [ s for s in clear_locations if s.stageId in available_stages and s not in available_missions ]

        options = []
        for option in objectivesanity_missions:
            option_available_stages = available_stages.copy()
            option_available_missions = available_missions.copy()
            option_available_missions.append(option)

            TraversePath(story, option_available_stages, option_available_missions)
            #if len(option_available_stages) > len(available_stages):
            options.append((option, option_available_stages, option_available_missions))

        non_empty_routes = [ e for e in options if len(e[1]) > len(available_stages)]
        if len(non_empty_routes) > 0:
            options = non_empty_routes

        choice = ChoosePathOption(world, options)
        chosen_option = choice[0]
        available_stages = choice[1]
        available_missions = choice[2]

        sphere_results.append(choice)

    return sphere_results


def AlterOverridesForStoryPath(spheres, options):
    current_overrides =  options.percent_overrides.value
    first_sphere_size = len(spheres[0][1])
    new_sphere_size = first_sphere_size

    # TODO: These percentages should work based on any already set value / default for each key
    # Calculate percentages based on story accessibility and total available stages as % not available (100 - a)
    # Alter when using select progression (up or down?)
    # e.g. 1 region out of 23 => a = 4, change value to 4

    new_overrides = {}
    new_available_overrides = {}

    for sphere in spheres:
        if sphere == spheres[0]:
            continue

        sphere_mission = sphere[0]

        objective_info_completion = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                                   sphere_mission.mission_object_name, options,
                                                                   sphere_mission.stageId, sphere_mission.alignmentId,
                                                                              options.percent_overrides)

        objective_info_available = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                                              sphere_mission.mission_object_name,
                                                                              options,
                                                                              sphere_mission.stageId,
                                                                              sphere_mission.alignmentId,
                                                                             options.percent_overrides)

        max_required_base_complete = ShadowUtils.getMaxRequired(
            objective_info_completion,
            sphere_mission.requirement_count, sphere_mission.stageId, sphere_mission.alignmentId,
            options.percent_overrides)

        max_required_base_available = ShadowUtils.getMaxRequired(
            objective_info_available,
            sphere_mission.requirement_count, sphere_mission.stageId, sphere_mission.alignmentId,
            options.percent_overrides)


        completion_key_base = ShadowUtils.GetOverrideKey(objective_info_completion[0],
                                                    sphere_mission.alignmentId)

        available_key_base = ShadowUtils.GetOverrideKey(objective_info_available[0],
                                                    sphere_mission.alignmentId)

        sphere_key = completion_key_base + "."+ Levels.LEVEL_ID_TO_LEVEL[sphere_mission.stageId]
        sphere_key_a = available_key_base + "." + Levels.LEVEL_ID_TO_LEVEL[sphere_mission.stageId]

        # This should look actual value for this stage in time
        current_override_value = (objective_info_completion[1] / 100)

        total_stages = 23
        base_percent_value = new_sphere_size / total_stages

        #available_factor = objective_info_available[1]

        use_percent_value = math.floor(base_percent_value * current_override_value * 100)

        if use_percent_value > max_required_base_complete:
            #print("Alter-", use_percent_value, max_required_base_complete)
            use_percent_value = max_required_base_complete

        if use_percent_value == 0:
            use_percent_value = 1

        new_sphere_size = len(sphere[1])

        # Need a check in here to either
        # Prevent higher values than total
        # Also increase pool amount

        new_overrides[sphere_key] = use_percent_value

        # What should this number even be?
        # Want to calculate the value to be equivalent to new

        copied = current_overrides.copy()
        copied[sphere_key] = use_percent_value

        objective_info_available_pass = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                                             sphere_mission.mission_object_name,
                                                                             options,
                                                                             sphere_mission.stageId,
                                                                             sphere_mission.alignmentId,
                                                                             copied)

        new_max_required = ShadowUtils.getMaxRequired(
            objective_info_available_pass,
            sphere_mission.requirement_count, sphere_mission.stageId, sphere_mission.alignmentId,
            copied)

        if new_max_required < 1:
            new_max_required = 1

        rate = (max_required_base_available / max_required_base_complete)  * 100

        potential_override_available = ((max_required_base_complete / new_max_required) * rate) - 100
        #* available_factor) - 100
        if potential_override_available > 0:
            #pass
            new_available_overrides[sphere_key_a] = potential_override_available

    return new_overrides, new_available_overrides



def StoryToOrder(StoryMode):

    ordered_data = []
    set_data = set()

    starting_stages = [ s.end_stage_id for s in StoryMode if s.start_stage_id is None ]
    set_data = set_data.union(set(starting_stages))
    ordered_data.extend(list(set_data))

    while True:
        story_nodes = [ s for s in StoryMode if s.start_stage_id in set_data]
        if len(story_nodes) == 0:
            break
        b_len = len(set_data)
        set_data = set_data.union(set([s.end_stage_id for s in story_nodes if s.end_stage_id is not None and s.end_stage_id not in set_data]))
        set_data = set_data.union(set([s.boss for s in story_nodes if s.boss not in set_data and s.boss is not None and s.boss not in set_data]))
        if b_len == len(set_data):
            break
        else:
            missing = [ x for x in set_data if x not in ordered_data]
            ordered_data.extend(missing)

    return ordered_data


def ChaosShuffle(world):

    ModifiedStoryMode = copy.deepcopy(DefaultStoryMode)

    include_last_way = world.options.include_last_way_shuffle

    stages_to_assign = [ l for l in Levels.ALL_STAGES if Levels.LEVEL_ID_TO_LEVEL[l] not in world.options.excluded_stages and l
                         not in Levels.BOSS_STAGES and l not in Levels.LAST_STORY_STAGES ]
                         #and l != Levels.STAGE_WESTOPOLIS]

    possible_stages = stages_to_assign.copy()

    final_bosses_full = [boss.boss for boss in ModifiedStoryMode if boss.end_stage_id is None and
                         Levels.LEVEL_ID_TO_LEVEL[boss.boss] not in world.options.excluded_stages]
    final_bosses = final_bosses_full.copy()

    #boss_groups = Levels.BOSS_GROUPING
    #if world.options.single_egg_dealer:
    #    options = [ b for b in final_bosses if b in boss_groups["Egg Dealer"]]
    #    if len(options) > 0:
    #        for o in options:
    #            final_bosses.remove(o)
    #        chosen = world.random.choice(options)
    #        final_bosses.append(chosen)

    #if world.options.single_black_doom:
    #    options = [b for b in final_bosses if b in boss_groups["Black Doom"]]
    #    if len(options) > 0:
    #        for o in options:
    #            final_bosses.remove(o)

#            chosen = world.random.choice(options)
 #           final_bosses.append(chosen)

  #  if world.options.single_diablon:
   #     options = [b for b in final_bosses if b in boss_groups["Diablon"]]
    #    if len(options) > 0:
     #       for o in options:
      #          final_bosses.remove(o)
#
  #          chosen = world.random.choice(options)
 #           final_bosses.append(chosen)


    # Removes the duplicate Lava Shelter Egg Dealer
    final_bosses = list(set(final_bosses))

    world.random.shuffle(final_bosses)

    story_boss_stages = [ l for l in Levels.BOSS_STAGES if Levels.LEVEL_ID_TO_LEVEL[l] not in world.options.excluded_stages
                          and l not in Levels.LAST_STORY_STAGES
                          and l not in final_bosses_full ]

    last_way_active = Levels.LEVEL_ID_TO_LEVEL[Levels.STAGE_THE_LAST_WAY] not in world.options.excluded_stages

    if len(stages_to_assign) == 0:
        raise OptionError("No stages to assign!")

    if include_last_way:
        if last_way_active:
            stages_to_assign.append(Levels.STAGE_THE_LAST_WAY)

        final_bosses.append(Levels.BOSS_DEVIL_DOOM)

    world.random.shuffle(stages_to_assign)

    bosses_to_assign = []
    boss_set = story_boss_stages
    for i in range(0, world.options.story_boss_count):
        bosses_to_assign.extend(boss_set)

    world.random.shuffle(bosses_to_assign)

    # Potentially duplicate some bosses for more clarity

    #steps_to_randomise = [ s for s in ModifiedStoryMode if s.start_stage_id is not None ]
    steps_to_randomise = [s for s in ModifiedStoryMode if s.start_stage_id is not None
                          and Levels.LEVEL_ID_TO_LEVEL[s.start_stage_id] not in world.options.excluded_stages]


    plando_steps = []
    #GetLevelCompletionNames(s.start_stage_id, s.alignment_id)[1] not in world.options.exclude_locations

    for s in steps_to_randomise:
        level_location_name = Levels.GetLevelCompletionNames(s.start_stage_id, s.alignment_id)[1]
        if level_location_name in world.options.exclude_locations:
            plando_steps.append((s, PathInfo(s.start_stage_id, s.alignment_id,
                                             s.start_stage_id, [])))

    for s in plando_steps:
        steps_to_randomise.remove(s[0])

    if include_last_way and last_way_active:
        steps_to_randomise.append(PathInfo(Levels.STAGE_THE_LAST_WAY, Levels.MISSION_ALIGNMENT_NEUTRAL, None, []))

    new_story = []
    bosses_by_alignment = {}

    world.random.shuffle(steps_to_randomise)

    steps_to_randomise.insert(0, PathInfo(None, None, None, []))

    SafeStartingStages = Locations.GetStagesWithNoRequirements(world)
    LegalFirstStages = list(set([ s.start_stage_id for s in steps_to_randomise if s.start_stage_id is not None and
                                  s.start_stage_id not in Levels.LAST_STORY_STAGES]))

    new_steps = []
    stage_nodes = []
    first_stage = None

    force_path = None #[0, Levels.MISSION_ALIGNMENT_HERO, Levels.BOSS_DEVIL_DOOM]

    selected = []

    while len(steps_to_randomise) > 0:
        step = None
        boss_possible = False
        first_step = [ step for step in steps_to_randomise if step.start_stage_id is None ]
        if len(first_step) == 1:
            step = first_step[0]
        else:
            valid_steps = [ s for s in steps_to_randomise if s.start_stage_id in stage_nodes ]
            if len(valid_steps) == len(steps_to_randomise):
                boss_possible = True
            if len(valid_steps) > 0:
                step = world.random.choice(valid_steps)

            #step = steps_to_randomise[0]

        if step is None:
            raise Exception("Unable to work out next step to take!")

        if force_path is not None and step.start_stage_id == force_path[0] and \
            step.alignment_id == force_path[1]:
            if force_path[2] in Levels.BOSS_STAGES and not boss_possible:
                continue
            else:
                if force_path[2] in Levels.BOSS_STAGES and (
                        force_path[2] in final_bosses_full or force_path[2] == Levels.BOSS_DEVIL_DOOM):
                    step.end_stage_id = None
                    step.boss = force_path[2]
                    pass

        elif boss_possible and len(final_bosses) > 0 and step.start_stage_id is not None:
            step.end_stage_id = None
            step.boss = final_bosses.pop()
            selected.append(step.boss)
        else:
            boss_assigned = False
            if boss_possible and len(bosses_to_assign) > 0 and step.start_stage_id is not None:
                possible_boss = world.random.choice(bosses_to_assign)

                if possible_boss not in bosses_by_alignment:
                    bosses_by_alignment[possible_boss] = []

                if step.alignment_id not in bosses_by_alignment[possible_boss]:
                    step.boss = possible_boss
                    bosses_by_alignment[possible_boss].append(step.alignment_id)
                    bosses_to_assign.remove(step.boss)
                    boss_assigned = True

            if not boss_assigned:
                step.boss = None

            if step.start_stage_id is None:

                plando_start_stages = [ x for x in world.options.plando_starting_stages.value
                                        if x not in world.options.excluded_stages ]

                if len(plando_start_stages) > 0:
                    rev_level_map = {v: k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
                    first_stage_name = world.random.choice(plando_start_stages)
                    first_stage = rev_level_map[first_stage_name]
                    step.end_stage_id = first_stage
                    stages_to_assign.remove(step.end_stage_id)
                    if force_path is not None and force_path[0] == 0:
                        force_path[0] = first_stage

                elif (len(SafeStartingStages) > 0 and
                      world.options.starting_level_method == Options.StartingLevelMethod.option_clear_stage):
                    step.end_stage_id = world.random.choice(SafeStartingStages)
                    stages_to_assign.remove(step.end_stage_id)
                    first_stage = step.end_stage_id
                    if force_path is not None and force_path[0] == 0:
                        force_path[0] = first_stage

                else:
                    first_stage = world.random.choice(LegalFirstStages)
                    stages_to_assign.remove(first_stage)
                    step.end_stage_id = first_stage
                    if force_path is not None and force_path[0] == 0:
                        force_path[0] = first_stage

            elif len(stages_to_assign) > 0:
                step.end_stage_id = stages_to_assign.pop()
                selected.append(step.end_stage_id)
                if step.end_stage_id == step.start_stage_id and len(stages_to_assign) != 0:
                    stages_to_assign.append(step.end_stage_id)
            else:
                step.end_stage_id = world.random.choice(possible_stages)

        steps_to_randomise.remove(step)
        new_steps.append(step)
        if step.end_stage_id not in stage_nodes:
            stage_nodes.append(step.end_stage_id)

    new_story.extend(new_steps)
    new_story.extend([p[1] for p in plando_steps])

    bosses_to_assign = set(bosses_to_assign).union(set(final_bosses))
    leftover_bosses = [ l for l in bosses_to_assign if l not in [ x.boss for x in new_story if x is not None ]]

    logging.debug("Shadow Story is: %s", new_story)
    return new_story, leftover_bosses




def ShuffleStoryMode(world):
    ModifiedStoryMode = copy.deepcopy(DefaultStoryMode)
    story_stages = []
    for step in ModifiedStoryMode:
        if step.end_stage_id is not None and step.end_stage_id not in story_stages and \
                Levels.LEVEL_ID_TO_LEVEL[step.end_stage_id] not in world.options.excluded_stages:
            if step.end_stage_id == Levels.STAGE_WESTOPOLIS:
                continue
            story_stages.append(step.end_stage_id)

    story_base = story_stages.copy()
    world.random.shuffle(story_stages)

    for step in ModifiedStoryMode:
        if step.end_stage_id in story_base:
            index = story_base.index(step.end_stage_id)
            new_stage = story_stages[index]
            step.end_stage_id = new_stage

    return ModifiedStoryMode



def GenerateStoryMode(world):
    ModifiedStoryMode = copy.deepcopy(DefaultStoryMode)
    ModifiedStoryMode[0].end_stage_id = world.random.choice(
        [s for s in Levels.ALL_STAGES if s not in Levels.BOSS_STAGES and s not in Levels.LAST_STORY_STAGES
         and s not in Levels.FINAL_STAGES and Levels.LEVEL_ID_TO_LEVEL[s] not in world.options.excluded_stages])
    return ModifiedStoryMode

def GetStoryMode(world):
    #if world.options.story_shuffle == Options.StoryShuffle.option_basic:
    #    return GenerateStoryMode(world)
    #elif world.options.story_shuffle == Options.StoryShuffle.option_shuffle:
    #    return ShuffleStoryMode(world)
    if world.options.story_shuffle == Options.StoryShuffle.option_chaos:
        return ChaosShuffle(world)
    else:
        return DefaultStoryMode, None


def StoryToString(Story):
    string = ""
    for item in Story:
        start_id = item.start_stage_id
        end_id = item.end_stage_id
        alignment = item.alignment_id
        boss = item.boss
        cutscenes = item.cutscenes
        cutscene_count = len(cutscenes)

        if start_id is None:
            start_id = -1

        if end_id is None:
            end_id = -1

        if boss is None:
            boss = -1

        if alignment is None:
            alignment = -1

        cutscene_string = "" if cutscene_count == 0 else "&".join([str(c) for c in cutscenes])

        string += f"{start_id}&{end_id}&{alignment}&{boss}&{cutscene_count}{cutscene_string}/"

    return string

def StringToStory(string):
    story = []
    items = string.split("/")
    for item in items:
        if len(item) == 0:
            continue
        split = item.split("&")
        start_id = int(split[0])
        end_id = int(split[1])
        alignment = int(split[2])
        boss = int(split[3])
        cutscene_count = int(split[4])

        if start_id == -1:
            start_id = None

        if end_id == -1:
            end_id = None

        if alignment == -1:
            alignment = None

        if boss == -1:
            boss = None

        step = PathInfo(start_id, alignment, end_id, [])

        if cutscene_count > 0:
            cutscenes = [ int(x) for x in split[5].split(",")]
            step.cutscenes = cutscenes

        if boss is not None:
            step.boss = boss

        story.append(step)

    return story

def ChooseGoalLibraryPaths(world, count):
    # TODO Add handling here for select bosses being disabled on select only

    valid_libraries = [ l for l in Libraries if
                        len([ ll for ll in l.required_levels if ((type(ll) is int and ll in world.available_levels)
                              or (type(ll) is tuple and ll[0] in world.available_levels))])
                        == len(l.required_levels)]

    if len(valid_libraries) < count:
        return []

    return [p.index for p in world.random.sample(valid_libraries, k=count.value)]

def GetCombinedLevelsForGoal(paths):
    paths = [l for l in Libraries if l.index in paths]
    combined_data = []
    for p in paths:
        combined_data.extend(p.required_levels)

    return combined_data

def IsStageRequiredForChosenPaths(paths, stageId, alignment_id):
    combined_data = GetCombinedLevelsForGoal(paths)
    if stageId in Levels.BOSS_STAGES:
        return stageId in combined_data
    else:
        return (stageId, alignment_id) in combined_data

    return False
