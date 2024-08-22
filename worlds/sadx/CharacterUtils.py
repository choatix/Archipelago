from typing import List

from Options import Toggle
from worlds.sadx.Enums import Character, LevelMission
from worlds.sadx.Locations import LevelLocation
from worlds.sadx.Options import SonicAdventureDXOptions, BaseActionStageMissionChoice


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


def are_character_upgrades_randomized(character: Character, options: SonicAdventureDXOptions) -> bool:
    character_randomized_upgrades = {
        Character.Sonic: options.randomized_sonic_upgrades,
        Character.Tails: options.randomized_tails_upgrades,
        Character.Knuckles: options.randomized_knuckles_upgrades,
        Character.Amy: options.randomized_amy_upgrades,
        Character.Big: options.randomized_big_upgrades,
        Character.Gamma: options.randomized_gamma_upgrades
    }
    return bool(character_randomized_upgrades.get(character).value)


def get_character_playable_option(character: Character, options: SonicAdventureDXOptions) -> Toggle:
    playable_characters = {
        Character.Sonic: options.playable_sonic,
        Character.Tails: options.playable_tails,
        Character.Knuckles: options.playable_knuckles,
        Character.Amy: options.playable_amy,
        Character.Big: options.playable_big,
        Character.Gamma: options.playable_gamma
    }
    return playable_characters.get(character)


def is_character_playable(character: Character, options: SonicAdventureDXOptions) -> bool:
    return get_character_playable_option(character, options).value > 0


def is_any_character_playable(characters: List[Character], options: SonicAdventureDXOptions) -> bool:
    return any(is_character_playable(character, options) for character in characters)


def get_playable_characters(options: SonicAdventureDXOptions) -> List[Character]:
    character_list: List[Character] = []
    if options.playable_sonic.value > 0:
        character_list.append(Character.Sonic)
    if options.playable_tails.value > 0:
        character_list.append(Character.Tails)
    if options.playable_knuckles.value > 0:
        character_list.append(Character.Knuckles)
    if options.playable_amy.value > 0:
        character_list.append(Character.Amy)
    if options.playable_big.value > 0:
        character_list.append(Character.Big)
    if options.playable_gamma.value > 0:
        character_list.append(Character.Gamma)

    return character_list


def get_character_action_stage_missions(character: Character,
                                        options: SonicAdventureDXOptions) -> BaseActionStageMissionChoice:
    character_action_stage_missions = {
        Character.Sonic: options.sonic_action_stage_missions,
        Character.Tails: options.tails_action_stage_missions,
        Character.Knuckles: options.knuckles_action_stage_missions,
        Character.Amy: options.amy_action_stage_missions,
        Character.Big: options.big_action_stage_missions,
        Character.Gamma: options.gamma_action_stage_missions
    }
    return character_action_stage_missions.get(character)


def is_level_playable(level: LevelLocation, options: SonicAdventureDXOptions) -> bool:
    if not is_character_playable(level.character, options):
        return False
    character_missions = get_character_action_stage_missions(level.character, options)
    if character_missions == 3:
        return level.levelMission in {LevelMission.C, LevelMission.B, LevelMission.A}
    if character_missions == 2:
        return level.levelMission in {LevelMission.C, LevelMission.B}
    if character_missions == 1:
        return level.levelMission == LevelMission.C
    return False
