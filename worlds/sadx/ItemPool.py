import math
from typing import List

from worlds.AutoWorld import World
from .CharacterUtils import get_playable_character_item, is_character_playable, are_character_upgrades_randomized
from .Enums import Character, Area
from .Items import filler_item_table, character_unlock_item_table, character_upgrade_item_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from .Regions import get_location_ids_for_area
from .StartingSetup import StarterSetup


def create_sadx_items(world: World, starter_setup: StarterSetup,
                      needed_emblems: int, options: SonicAdventureDXOptions):
    itempool = []

    # Keys and Characters Items
    item_names = get_item_names(options, starter_setup.item, starter_setup.character)
    for itemName in item_names:
        itempool.append(world.create_item(itemName))

    place_not_randomized_upgrades(world, options)

    # One less for the Perfect Chaos location
    location_count = sum(1 for location in world.multiworld.get_locations(world.player) if not location.locked) - 1
    emblem_count = max(1, location_count - len(item_names))

    filler_items = emblem_count - needed_emblems

    for _ in range(needed_emblems):
        itempool.append(world.create_item(ItemName.Progression.Emblem))

    junk_count = math.floor(filler_items * (options.junk_fill_percentage.value / 100.0))

    trap_count = math.floor(junk_count * (options.trap_fill_percentage.value / 100.0))

    if trap_count > 0:
        trap_weights = []
        trap_weights += [ItemName.Traps.IceTrap] * options.ice_trap_weight.value
        trap_weights += [ItemName.Traps.SpringTrap] * options.spring_trap_weight.value
        trap_weights += [ItemName.Traps.PoliceTrap] * options.police_trap_weight.value
        trap_weights += [ItemName.Traps.BuyonTrap] * options.buyon_trap_weight.value
        for _ in range(trap_count):
            trap_item_name = world.random.choice(trap_weights)
            itempool.append(world.create_item(trap_item_name))

    for _ in range(junk_count - trap_count):
        filler_item = world.random.choice(filler_item_table)
        itempool.append(world.create_item(filler_item.name))

    for _ in range(filler_items - junk_count):
        itempool.append(world.create_item(ItemName.Progression.Emblem, True))

    starter_character_name = get_playable_character_item(starter_setup.character)
    world.multiworld.push_precollected(world.create_item(starter_character_name))
    if starter_setup.item is not None:
        world.multiworld.push_precollected(world.create_item(starter_setup.item))

    world.multiworld.itempool += itempool


def get_item_names(options: SonicAdventureDXOptions, starter_item: str, starter_character: Character) -> List[str]:
    item_names = []
    item_names += get_item_for_options_per_character(Character.Sonic, starter_character, options)
    item_names += get_item_for_options_per_character(Character.Tails, starter_character, options)
    item_names += get_item_for_options_per_character(Character.Knuckles, starter_character, options)
    item_names += get_item_for_options_per_character(Character.Amy, starter_character, options)
    item_names += get_item_for_options_per_character(Character.Big, starter_character, options)
    item_names += get_item_for_options_per_character(Character.Gamma, starter_character, options)
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
    # Don't include the wind stone for characters that aren't sonic/tails/big
    if is_character_playable(Character.Sonic, options) or is_character_playable(
            Character.Tails, options) or is_character_playable(Character.Gamma, options):
        item_names.append(ItemName.KeyItem.WindStone)

    if options.goal == 1 or options.goal == 2:
        item_names.append(ItemName.Progression.WhiteEmerald)
        item_names.append(ItemName.Progression.RedEmerald)
        item_names.append(ItemName.Progression.CyanEmerald)
        item_names.append(ItemName.Progression.PurpleEmerald)
        item_names.append(ItemName.Progression.GreenEmerald)
        item_names.append(ItemName.Progression.YellowEmerald)
        item_names.append(ItemName.Progression.BlueEmerald)

    if starter_item is not None:
        item_names.remove(starter_item)
    return item_names


def get_item_for_options_per_character(character: Character, starter_character: Character,
                                       options: SonicAdventureDXOptions) -> List[str]:
    item_names = []
    if not is_character_playable(character, options):
        return item_names

    if character != starter_character:
        for unlock_character in character_unlock_item_table:
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
