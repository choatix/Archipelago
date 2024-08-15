import math
from typing import List

from worlds.AutoWorld import World
from .CharacterUtils import get_playable_character_item, is_character_playable, are_character_upgrades_randomized
from .Enums import Character, Area, Goal
from .Items import filler_item_table, playable_character_item_table, character_upgrade_item_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from .Regions import get_location_ids_for_area
from .StartingSetup import StarterSetup


class ItemCount:
    emblem_count_progressive: int = 0
    emblem_count_non_progressive: int = 0
    filler_count: int = 0
    trap_count: int = 0


def create_sadx_items(world: World, starter_setup: StarterSetup,
                      needed_emblems: int, options: SonicAdventureDXOptions):
    itempool = []
    item_names = get_item_names(options, starter_setup)
    # Calculate the number of items per type
    item_count = get_item_count(world, len(item_names), needed_emblems, options)

    # Keys and Characters Items
    itempool.extend(world.create_item(item_name) for item_name in item_names)

    # Character Upgrades
    place_not_randomized_upgrades(world, options)

    # Emblems
    for _ in range(item_count.emblem_count_progressive):
        itempool.append(world.create_item(ItemName.Progression.Emblem))
    for _ in range(item_count.emblem_count_non_progressive):
        itempool.append(world.create_item(ItemName.Progression.Emblem, True))

    # Filler
    for _ in range(item_count.filler_count):
        filler_item = world.random.choice(filler_item_table)
        itempool.append(world.create_item(filler_item.name))

    # Traps
    trap_weights = []
    trap_weights += [ItemName.Traps.IceTrap] * options.ice_trap_weight.value
    trap_weights += [ItemName.Traps.SpringTrap] * options.spring_trap_weight.value
    trap_weights += [ItemName.Traps.PoliceTrap] * options.police_trap_weight.value
    trap_weights += [ItemName.Traps.BuyonTrap] * options.buyon_trap_weight.value
    for _ in range(item_count.trap_count):
        trap_item_name = world.random.choice(trap_weights)
        itempool.append(world.create_item(trap_item_name))

    # Push the starter items
    starter_character_name = get_playable_character_item(starter_setup.character)
    world.multiworld.push_precollected(world.create_item(starter_character_name))
    if starter_setup.item is not None:
        world.multiworld.push_precollected(world.create_item(starter_setup.item))

    world.multiworld.itempool += itempool


def get_item_count(world: World, stating_item_count: int, needed_emblems: int,
                   options: SonicAdventureDXOptions) -> ItemCount:
    item_count = ItemCount()

    location_count = sum(1 for location in world.multiworld.get_locations(world.player) if not location.locked)
    extra_items = max(0, location_count - (needed_emblems + stating_item_count))

    if options.goal in {Goal.Emblems, Goal.EmblemsAndEmeraldHunt}:
        # If Emblems are enabled, we calculate how many progressive emblems and filler emblems we need
        junk_count = math.floor(extra_items * (options.junk_fill_percentage.value / 100.0))
    else:
        # If not, all the remaining locations are filler
        junk_count = extra_items

    item_count.emblem_count_progressive = needed_emblems
    item_count.emblem_count_non_progressive = extra_items - junk_count
    item_count.trap_count = math.floor(junk_count * (options.trap_fill_percentage.value / 100.0))
    item_count.filler_count = junk_count - item_count.trap_count

    return item_count


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
    if len(get_location_ids_for_area(Area.SpeedHighway, options)) > 0:
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

    if options.goal in {Goal.EmeraldHunt, Goal.EmblemsAndEmeraldHunt}:
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

    if are_character_upgrades_randomized(character, options):
        for character_upgrade in character_upgrade_item_table:
            if character_upgrade.character == character:
                item_names.append(character_upgrade.name)

    return item_names


def place_not_randomized_upgrades(world: World, options: SonicAdventureDXOptions):
    if is_character_playable(Character.Sonic, options) and not options.randomized_sonic_upgrades:
        world.multiworld.get_location(LocationName.Sonic.LightShoes, world.player).place_locked_item(
            world.create_item(ItemName.Sonic.LightShoes))
        world.multiworld.get_location(LocationName.Sonic.CrystalRing, world.player).place_locked_item(
            world.create_item(ItemName.Sonic.CrystalRing))
        world.multiworld.get_location(LocationName.Sonic.AncientLight, world.player).place_locked_item(
            world.create_item(ItemName.Sonic.AncientLight))
    if is_character_playable(Character.Tails, options) and not options.randomized_tails_upgrades:
        world.multiworld.get_location(LocationName.Tails.JetAnklet, world.player).place_locked_item(
            world.create_item(ItemName.Tails.JetAnklet))
        world.multiworld.get_location(LocationName.Tails.RhythmBadge, world.player).place_locked_item(
            world.create_item(ItemName.Tails.RhythmBadge))
    if is_character_playable(Character.Knuckles, options) and not options.randomized_knuckles_upgrades:
        world.multiworld.get_location(LocationName.Knuckles.ShovelClaw, world.player).place_locked_item(
            world.create_item(ItemName.Knuckles.ShovelClaw))
        world.multiworld.get_location(LocationName.Knuckles.FightingGloves, world.player).place_locked_item(
            world.create_item(ItemName.Knuckles.FightingGloves))
    if is_character_playable(Character.Amy, options) and not options.randomized_amy_upgrades:
        world.multiworld.get_location(LocationName.Amy.WarriorFeather, world.player).place_locked_item(
            world.create_item(ItemName.Amy.WarriorFeather))
        world.multiworld.get_location(LocationName.Amy.LongHammer, world.player).place_locked_item(
            world.create_item(ItemName.Amy.LongHammer))
    if is_character_playable(Character.Big, options) and not options.randomized_big_upgrades:
        world.multiworld.get_location(LocationName.Big.LifeBelt, world.player).place_locked_item(
            world.create_item(ItemName.Big.LifeBelt))
        world.multiworld.get_location(LocationName.Big.PowerRod, world.player).place_locked_item(
            world.create_item(ItemName.Big.PowerRod))
        world.multiworld.get_location(LocationName.Big.Lure1, world.player).place_locked_item(
            world.create_item(ItemName.Big.Lure1))
        world.multiworld.get_location(LocationName.Big.Lure2, world.player).place_locked_item(
            world.create_item(ItemName.Big.Lure2))
        world.multiworld.get_location(LocationName.Big.Lure3, world.player).place_locked_item(
            world.create_item(ItemName.Big.Lure3))
        world.multiworld.get_location(LocationName.Big.Lure4, world.player).place_locked_item(
            world.create_item(ItemName.Big.Lure4))
    if is_character_playable(Character.Gamma, options) and not options.randomized_gamma_upgrades:
        world.multiworld.get_location(LocationName.Gamma.JetBooster, world.player).place_locked_item(
            world.create_item(ItemName.Gamma.JetBooster))
        world.multiworld.get_location(LocationName.Gamma.LaserBlaster, world.player).place_locked_item(
            world.create_item(ItemName.Gamma.LaserBlaster))
