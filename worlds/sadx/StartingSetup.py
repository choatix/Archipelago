import re
from typing import List, TextIO

from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters, are_character_upgrades_randomized
from .Enums import Character, Area
from .Locations import level_location_table, upgrade_location_table, sub_level_location_table, \
    field_emblem_location_table, boss_location_table, life_capsule_location_table, mission_location_table
from .Names import ItemName
from .Options import SonicAdventureDXOptions


class StarterSetup:
    def __init__(self, character: Character = None, area: Area = None, item: str = None):
        self.character = character
        self.area = area
        self.item = item


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
    # non_stop_missions
    if options.mission_mode_checks:
        for mission in mission_location_table:
            if not options.non_stop_missions and mission.locationId in [49, 53, 54, 58]:
                continue
            if mission.character == character and mission.cardArea == area and mission.objectiveArea == area and not mission.extraItems:
                return True


def write_sadx_spoiler(world: World, spoiler_handle: TextIO, starter_setup: StarterSetup):
    spoiler_handle.write("\n")
    header_text = "Sonic Adventure starting setup for {}:\n"
    header_text = header_text.format(world.multiworld.player_name[world.player])
    spoiler_handle.write(header_text)

    starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', starter_setup.area.name)
    if starter_setup.item is not None:
        text = "Will start as {0} in the {1} area with {2}.\n"
        text = text.format(starter_setup.character.name, starting_area_name, starter_setup.item)
    else:
        text = "Will start as {0} in the {1} area.\n"
        text = text.format(starter_setup.character.name, starting_area_name)
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
