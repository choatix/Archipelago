import re
from dataclasses import dataclass, field
from typing import List, TextIO

from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters, are_character_upgrades_randomized
from .Enums import Character, Area
from .Locations import level_location_table, upgrade_location_table, sub_level_location_table, \
    field_emblem_location_table, boss_location_table, life_capsule_location_table, mission_location_table
from .Names import ItemName
from .Options import SonicAdventureDXOptions


@dataclass
class CharacterArea:
    character: Character
    area: Area = None


@dataclass
class StarterSetup:
    character = None
    area = None
    item = None
    charactersWithArea: List[CharacterArea] = field(default_factory=list)

    def get_starting_area(self, character: Character) -> Area:
        for char_area in self.charactersWithArea:
            if char_area.character == character:
                return char_area.area
        return self.area


def generate_early_sadx(world: World, options: SonicAdventureDXOptions) -> StarterSetup:
    starter_setup = StarterSetup()
    possible_characters = get_playable_characters(options)
    if len(possible_characters) == 0:
        raise OptionError("You need at least one playable character")

    starter_setup.character = world.random.choice(possible_characters)

    if options.guaranteed_level:
        if options.random_starting_location:
            starter_setup.area = world.random.choice(list(starting_area_items[starter_setup.character].keys()))
        else:
            starter_setup.area = Area.StationSquareMain
        possible_starting_items = starting_area_items[starter_setup.character][starter_setup.area]
        if len(possible_starting_items) > 0:
            starter_setup.item = world.random.choice(possible_starting_items)
    else:
        if options.random_starting_location:
            possible_starter_areas = get_possible_starting_areas(world, starter_setup.character)
            starter_setup.area = world.random.choice(possible_starter_areas)
        else:
            starter_setup.area = Area.StationSquareMain

    # We set different starting areas for each character, and we try to don't repeat them
    if options.random_starting_location_per_character and options.random_starting_location:
        used_areas = {starter_setup.area}
        starter_setup.charactersWithArea.append(CharacterArea(starter_setup.character, starter_setup.area))
        possible_areas_dict = {char: get_possible_starting_areas(world, char) for char in possible_characters}
        characters_sorted_by_areas = sorted(possible_characters, key=lambda char: len(possible_areas_dict[char]))

        for character in characters_sorted_by_areas:
            if character == starter_setup.character:
                continue
            unused_areas = [area for area in possible_areas_dict[character] if area not in used_areas]
            if unused_areas:
                area = world.random.choice(unused_areas)
            else:
                area = world.random.choice(possible_areas_dict[character])
            used_areas.add(area)
            starter_setup.charactersWithArea.append(CharacterArea(character, area))

    return starter_setup


def get_possible_starting_areas(world, character: Character) -> List[Area]:
    possible_starting_areas = []
    if has_locations_without_items(character, Area.StationSquareMain, world.options):
        possible_starting_areas += [Area.StationSquareMain]
    if has_locations_without_items(character, Area.Station, world.options):
        possible_starting_areas += [Area.Station]
    if has_locations_without_items(character, Area.Hotel, world.options):
        possible_starting_areas += [Area.Hotel]
    if has_locations_without_items(character, Area.Casino, world.options):
        possible_starting_areas += [Area.Casino]
    if has_locations_without_items(character, Area.MysticRuinsMain, world.options):
        possible_starting_areas += [Area.MysticRuinsMain]
    if has_locations_without_items(character, Area.Jungle, world.options):
        possible_starting_areas += [Area.Jungle]
    if has_locations_without_items(character, Area.EggCarrierMain, world.options):
        possible_starting_areas += [Area.EggCarrierMain]

    return possible_starting_areas


def has_locations_without_items(character: Character, area: Area, options: SonicAdventureDXOptions) -> bool:
    for level in level_location_table:
        if level.character == character and level.area == area and not level.extraItems:
            return True
    if are_character_upgrades_randomized(character, options):
        for upgrade in upgrade_location_table:
            if upgrade.character == character and upgrade.area == area and not upgrade.extraItems:
                return True
    if options.sub_level_checks:
        for sub_level in sub_level_location_table:
            if character in sub_level.characters and sub_level.area == area:
                return True
    if options.field_emblems_checks:
        for field_emblem in field_emblem_location_table:
            if character in field_emblem.characters and field_emblem.area == area:
                return True
    if options.boss_checks:
        for boss_fight in boss_location_table:
            if character in boss_fight.characters and boss_fight.area == area:
                return True

    if options.life_sanity:
        for life_capsule in life_capsule_location_table:
            if life_capsule.character == character and life_capsule.area == area and not life_capsule.extraItems:
                return True
    if options.mission_mode_checks:
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if mission.character == character and mission.cardArea == area and mission.objectiveArea == area and not mission.extraItems:
                return True


def write_sadx_spoiler(world: World, spoiler_handle: TextIO, starter_setup: StarterSetup):
    spoiler_handle.write("\n")
    header_text = f"Sonic Adventure starting setup for {world.multiworld.player_name[world.player]}:\n"
    spoiler_handle.write(header_text)

    starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', starter_setup.area.name)
    if starter_setup.item:
        text = "- Will start as {0} in the {1} area with {2}.\n"
        text = text.format(starter_setup.character.name, starting_area_name, starter_setup.item)
    else:
        text = "- Will start as {0} in the {1} area.\n"
        text = text.format(starter_setup.character.name, starting_area_name)

    for characterArea in starter_setup.charactersWithArea:
        if characterArea.character == starter_setup.character:
            continue
        starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', characterArea.area.name)
        text += "- {0} will spawn in the {1} area.\n".format(characterArea.character.name, starting_area_name)

    spoiler_handle.writelines(text)


starting_area_items = {
    Character.Sonic: {
        Area.StationSquareMain: [ItemName.KeyItem.TwinkleParkTicket, ItemName.KeyItem.EmployeeCard],
        Area.Hotel: [],
        Area.MysticRuinsMain: [ItemName.KeyItem.WindStone],
        Area.EggCarrierMain: []
    },
    Character.Tails: {
        Area.StationSquareMain: [ItemName.KeyItem.EmployeeCard],
        Area.Casino: [],
        Area.MysticRuinsMain: [ItemName.KeyItem.WindStone],
        Area.EggCarrierMain: []
    },
    Character.Knuckles: {
        Area.StationSquareMain: [],
        Area.Casino: [],
    },
    Character.Amy: {
        Area.StationSquareMain: [ItemName.KeyItem.TwinkleParkTicket],
        Area.Jungle: [],
        Area.EggCarrierMain: []
    },
    Character.Gamma: {
        Area.StationSquareMain: [ItemName.KeyItem.HotelKeys],
        Area.Hotel: [],
        Area.MysticRuinsMain: [ItemName.KeyItem.Dynamite],
        Area.Jungle: [],
    },
    Character.Big: {
        Area.StationSquareMain: [],
        Area.Hotel: [],
        Area.EggCarrierMain: []
    }
}
