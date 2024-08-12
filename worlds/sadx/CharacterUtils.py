from typing import List

from Options import Toggle
from worlds.sadx.Enums import Character, LevelMission
from worlds.sadx.Locations import LevelLocation
from worlds.sadx.Options import SonicAdventureDXOptions, BaseMissionChoice


def get_playable_character_item(character: Character) -> str:
    from worlds.sadx.Names import ItemName
    match character:
        case Character.Sonic:
            return ItemName.Sonic.Playable
        case Character.Tails:
            return ItemName.Tails.Playable
        case Character.Knuckles:
            return ItemName.Knuckles.Playable
        case Character.Amy:
            return ItemName.Amy.Playable
        case Character.Big:
            return ItemName.Big.Playable
        case Character.Gamma:
            return ItemName.Gamma.Playable


def character_has_life_sanity(character: Character, options: SonicAdventureDXOptions) -> Toggle:
    character_life_sanity = {
        Character.Sonic: options.sonic_life_sanity,
        Character.Tails: options.tails_life_sanity,
        Character.Knuckles: options.knuckles_life_sanity,
        Character.Amy: options.amy_life_sanity,
        Character.Big: options.big_life_sanity,
        Character.Gamma: options.gamma_life_sanity
    }
    return character_life_sanity.get(character)


def are_character_upgrades_randomized(character: Character, options: SonicAdventureDXOptions) -> Toggle:
    character_randomized_upgrades = {
        Character.Sonic: options.randomized_sonic_upgrades,
        Character.Tails: options.randomized_tails_upgrades,
        Character.Knuckles: options.randomized_knuckles_upgrades,
        Character.Amy: options.randomized_amy_upgrades,
        Character.Big: options.randomized_big_upgrades,
        Character.Gamma: options.randomized_gamma_upgrades
    }
    return character_randomized_upgrades.get(character)


def get_character_missions(character: Character, options: SonicAdventureDXOptions) -> BaseMissionChoice:
    character_missions = {
        Character.Sonic: options.sonic_missions,
        Character.Tails: options.tails_missions,
        Character.Knuckles: options.knuckles_missions,
        Character.Amy: options.amy_missions,
        Character.Big: options.big_missions,
        Character.Gamma: options.gamma_missions
    }
    return character_missions.get(character)


def get_playable_characters(options: SonicAdventureDXOptions) -> List[Character]:
    character_list: List[Character] = []
    if options.sonic_missions > 0:
        character_list.append(Character.Sonic)
    if options.tails_missions > 0:
        character_list.append(Character.Tails)
    if options.knuckles_missions > 0:
        character_list.append(Character.Knuckles)
    if options.amy_missions > 0:
        character_list.append(Character.Amy)
    if options.big_missions > 0:
        character_list.append(Character.Big)
    if options.gamma_missions > 0:
        character_list.append(Character.Gamma)

    return character_list


def is_level_playable(level: LevelLocation, options: SonicAdventureDXOptions) -> bool:
    character_missions = get_character_missions(level.character, options)
    if character_missions == 3:
        return level.levelMission in {LevelMission.C, LevelMission.B, LevelMission.A}
    if character_missions == 2:
        return level.levelMission in {LevelMission.C, LevelMission.B}
    if character_missions == 1:
        return level.levelMission == LevelMission.C
    return False
