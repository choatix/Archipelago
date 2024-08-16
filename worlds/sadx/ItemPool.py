import math
from typing import List

from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_character_item, is_character_playable, are_character_upgrades_randomized
from .Enums import Character, Area, Goal
from .Items import filler_item_table, playable_character_item_table, character_upgrade_item_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from .Regions import get_location_ids_for_area
from .StartingSetup import StarterSetup


class ItemDistribution:
    emblem_count_progressive: int = 0
    emblem_count_non_progressive: int = 0
    filler_count: int = 0
    trap_count: int = 0


def create_sadx_items(world: World, starter_setup: StarterSetup, needed_emblems: int, options: SonicAdventureDXOptions):
    item_names = get_item_names(options, starter_setup)

    # Calculate the number of items per type
    item_distribution = get_item_distribution(world, len(item_names), needed_emblems, options)

    # Character Upgrades and removal of from the item pool
    place_not_randomized_upgrades(world, options, item_names)

    # Keys and Characters Items
    itempool = [world.create_item(item_name) for item_name in item_names]

    # Emblems
    for _ in range(item_distribution.emblem_count_progressive):
        itempool.append(world.create_item(ItemName.Progression.Emblem))
    for _ in range(item_distribution.emblem_count_non_progressive):
        item = world.create_item(ItemName.Progression.Emblem)
        item.classification = ItemClassification.filler
        itempool.append(item)

    # Filler
    for _ in range(item_distribution.filler_count):
        filler_item = world.random.choice(filler_item_table)
        itempool.append(world.create_item(filler_item.name))

    # Traps
    trap_weights = []
    trap_weights += [ItemName.Traps.IceTrap] * options.ice_trap_weight.value
    trap_weights += [ItemName.Traps.SpringTrap] * options.spring_trap_weight.value
    trap_weights += [ItemName.Traps.PoliceTrap] * options.police_trap_weight.value
    trap_weights += [ItemName.Traps.BuyonTrap] * options.buyon_trap_weight.value
    for _ in range(item_distribution.trap_count):
        trap_item_name = world.random.choice(trap_weights)
        itempool.append(world.create_item(trap_item_name))

    # Push the starter items
    starter_character_name = get_playable_character_item(starter_setup.character)
    world.multiworld.push_precollected(world.create_item(starter_character_name))
    if starter_setup.item is not None:
        world.multiworld.push_precollected(world.create_item(starter_setup.item))

    world.multiworld.itempool += itempool


def get_item_distribution(world: World, stating_item_count: int, needed_emblems: int,
                          options: SonicAdventureDXOptions) -> ItemDistribution:
    distribution = ItemDistribution()

    location_count = sum(1 for location in world.multiworld.get_locations(world.player) if not location.locked)
    extra_items = max(0, location_count - (needed_emblems + stating_item_count))

    if options.goal.value in {Goal.Emblems, Goal.EmblemsAndEmeraldHunt}:
        # If Emblems are enabled, we calculate how many progressive emblems and filler emblems we need
        junk_count = math.floor(extra_items * (options.junk_fill_percentage.value / 100.0))
    else:
        # If not, all the remaining locations are filler
        junk_count = extra_items

    distribution.emblem_count_progressive = needed_emblems
    distribution.emblem_count_non_progressive = extra_items - junk_count
    distribution.trap_count = math.floor(junk_count * (options.trap_fill_percentage.value / 100.0))
    distribution.filler_count = junk_count - distribution.trap_count

    return distribution


def get_item_names(options: SonicAdventureDXOptions, starter_setup: StarterSetup) -> List[str]:
    item_names = []
    item_names += get_item_for_options_per_character(Character.Sonic, options)
    item_names += get_item_for_options_per_character(Character.Tails, options)
    item_names += get_item_for_options_per_character(Character.Knuckles, options)
    item_names += get_item_for_options_per_character(Character.Amy, options)
    item_names += get_item_for_options_per_character(Character.Big, options)
    item_names += get_item_for_options_per_character(Character.Gamma, options)
    # We don't add key items that aren't used for the randomizer

    item_names.append(ItemName.KeyItem.Train)
    item_names.append(ItemName.KeyItem.Boat)
    item_names.append(ItemName.KeyItem.Raft)
    item_names.append(ItemName.KeyItem.StationKeys)

    if len(get_location_ids_for_area(Area.Hotel, options)) > 0:
        item_names.append(ItemName.KeyItem.HotelKeys)
    if len(get_location_ids_for_area(Area.Casino, options)) > 0:
        item_names.append(ItemName.KeyItem.CasinoKeys)
    if len(get_location_ids_for_area(Area.TwinklePark, options)) > 0:
        item_names.append(ItemName.KeyItem.TwinkleParkTicket)
    if is_character_playable(Character.Sonic, options) or is_character_playable(Character.Tails, options):
        item_names.append(ItemName.KeyItem.EmployeeCard)
    if len(get_location_ids_for_area(Area.AngelIsland, options)) > 0:
        item_names.append(ItemName.KeyItem.Dynamite)
    if len(get_location_ids_for_area(Area.Jungle, options)) > 0:
        item_names.append(ItemName.KeyItem.JungleCart)
    # Don't include the ice stone for characters that aren't sonic/tails/big
    if is_character_playable(Character.Sonic, options) or is_character_playable(
            Character.Tails, options) or is_character_playable(Character.Big, options):
        item_names.append(ItemName.KeyItem.IceStone)
    # Don't include the wind stone for characters that aren't sonic/tails/gamma
    if is_character_playable(Character.Sonic, options) or is_character_playable(
            Character.Tails, options) or is_character_playable(Character.Gamma, options):
        item_names.append(ItemName.KeyItem.WindStone)

    if options.goal.value in {Goal.EmeraldHunt, Goal.EmblemsAndEmeraldHunt}:
        item_names.append(ItemName.Progression.WhiteEmerald)
        item_names.append(ItemName.Progression.RedEmerald)
        item_names.append(ItemName.Progression.CyanEmerald)
        item_names.append(ItemName.Progression.PurpleEmerald)
        item_names.append(ItemName.Progression.GreenEmerald)
        item_names.append(ItemName.Progression.YellowEmerald)
        item_names.append(ItemName.Progression.BlueEmerald)

    item_names.remove(get_playable_character_item(starter_setup.character))
    if starter_setup.item is not None:
        item_names.remove(starter_setup.item)
    return item_names


def get_item_for_options_per_character(character: Character, options: SonicAdventureDXOptions) -> List[str]:
    item_names = []
    if not is_character_playable(character, options):
        return item_names

    for unlock_character in playable_character_item_table:
        if unlock_character.character == character:
            item_names.append(unlock_character.name)

    for character_upgrade in character_upgrade_item_table:
        if character_upgrade.character == character:
            item_names.append(character_upgrade.name)

    return item_names


def place_not_randomized_upgrades(world: World, options: SonicAdventureDXOptions, item_names: List[str]):
    upgrades = {
        Character.Sonic: [
            (LocationName.Sonic.LightShoes, ItemName.Sonic.LightShoes),
            (LocationName.Sonic.CrystalRing, ItemName.Sonic.CrystalRing),
            (LocationName.Sonic.AncientLight, ItemName.Sonic.AncientLight)
        ],
        Character.Tails: [
            (LocationName.Tails.JetAnklet, ItemName.Tails.JetAnklet),
            (LocationName.Tails.RhythmBadge, ItemName.Tails.RhythmBadge)
        ],
        Character.Knuckles: [
            (LocationName.Knuckles.ShovelClaw, ItemName.Knuckles.ShovelClaw),
            (LocationName.Knuckles.FightingGloves, ItemName.Knuckles.FightingGloves)
        ],
        Character.Amy: [
            (LocationName.Amy.WarriorFeather, ItemName.Amy.WarriorFeather),
            (LocationName.Amy.LongHammer, ItemName.Amy.LongHammer)
        ],
        Character.Big: [
            (LocationName.Big.LifeBelt, ItemName.Big.LifeBelt),
            (LocationName.Big.PowerRod, ItemName.Big.PowerRod),
            (LocationName.Big.Lure1, ItemName.Big.Lure1),
            (LocationName.Big.Lure2, ItemName.Big.Lure2),
            (LocationName.Big.Lure3, ItemName.Big.Lure3),
            (LocationName.Big.Lure4, ItemName.Big.Lure4)
        ],
        Character.Gamma: [
            (LocationName.Gamma.JetBooster, ItemName.Gamma.JetBooster),
            (LocationName.Gamma.LaserBlaster, ItemName.Gamma.LaserBlaster)
        ]
    }

    for character, upgrades in upgrades.items():
        if is_character_playable(character, options) and not are_character_upgrades_randomized(character, options):
            for location_name, item_name in upgrades:
                world.multiworld.get_location(location_name, world.player).place_locked_item(
                    world.create_item(item_name))
                item_names.remove(item_name)
