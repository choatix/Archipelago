import re
from typing import List, TextIO

from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters, are_character_upgrades_randomized
from .Enums import Character, StartingArea, Area
from .Locations import level_location_table, upgrade_location_table, sub_level_location_table, \
    field_emblem_location_table, boss_location_table
from .Names import ItemName
from .Options import SonicAdventureDXOptions


class StarterSetup:
    def __init__(self, character: Character = None, area: StartingArea = None, item: str = None):
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
        if options.random_starting_location:
            starter_setup.area = StartingArea.StationSquareMain
        possible_starting_items = starting_area_items[starter_setup.character][starter_setup.area]
        if len(possible_starting_items) > 0:
            starter_setup.item = world.random.choice(possible_starting_items)
    else:
        possible_starter_areas = get_possible_starting_areas(world, starter_setup.character)
        starter_setup.area = world.random.choice(possible_starter_areas)

    return starter_setup


def get_possible_starting_areas(world, character: Character) -> List[StartingArea]:
    possible_starting_areas = []
    if has_locations_without_items(character, Area.StationSquareMain, world.options):
        possible_starting_areas += [StartingArea.StationSquareMain]
    if has_locations_without_items(character, Area.Station, world.options):
        possible_starting_areas += [StartingArea.Station]
    if has_locations_without_items(character, Area.Hotel, world.options):
        possible_starting_areas += [StartingArea.Hotel]
    if has_locations_without_items(character, Area.Casino, world.options):
        possible_starting_areas += [StartingArea.Casino]
    if has_locations_without_items(character, Area.MysticRuinsMain, world.options):
        possible_starting_areas += [StartingArea.MysticRuins]
    if has_locations_without_items(character, Area.Jungle, world.options):
        possible_starting_areas += [StartingArea.Jungle]
    if has_locations_without_items(character, Area.EggCarrierMain, world.options):
        possible_starting_areas += [StartingArea.EggCarrier]

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
        StartingArea.StationSquareMain: [ItemName.KeyItem.TwinkleParkTicket,
                                         ItemName.KeyItem.EmployeeCard],
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.WindStone],
        StartingArea.EggCarrier: []
    },
    Character.Tails: {
        StartingArea.StationSquareMain: [ItemName.KeyItem.EmployeeCard],
        StartingArea.Casino: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.WindStone],
        StartingArea.EggCarrier: []
    },
    Character.Knuckles: {
        StartingArea.StationSquareMain: [],
        StartingArea.Casino: [],
    },
    Character.Amy: {
        StartingArea.StationSquareMain: [ItemName.KeyItem.TwinkleParkTicket],
        StartingArea.Jungle: [],
        StartingArea.EggCarrier: []
    },
    Character.Gamma: {
        StartingArea.StationSquareMain: [ItemName.KeyItem.HotelKeys],
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.Dynamite, ItemName.KeyItem.WindStone],
        StartingArea.Jungle: [],
    },
    Character.Big: {
        StartingArea.StationSquareMain: [],
        StartingArea.Hotel: [],
        StartingArea.EggCarrier: []
    }
}
