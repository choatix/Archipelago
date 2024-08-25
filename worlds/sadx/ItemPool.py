import math
from typing import List

from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_character_item, is_character_playable, are_character_upgrades_randomized, \
    get_character_upgrades_item
from .Enums import Character, Goal
from .Items import filler_item_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from .StartingSetup import StarterSetup


class ItemDistribution:
    def __init__(self, emblem_count_progressive=0, emblem_count_non_progressive=0, filler_count=0, trap_count=0):
        self.emblem_count_progressive = emblem_count_progressive
        self.emblem_count_non_progressive = emblem_count_non_progressive
        self.filler_count = filler_count
        self.trap_count = trap_count


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
        itempool.append(world.create_item(world.random.choice(filler_item_table).name))

    # Traps
    trap_weights = (
            [ItemName.Traps.IceTrap] * options.ice_trap_weight.value +
            [ItemName.Traps.SpringTrap] * options.spring_trap_weight.value +
            [ItemName.Traps.PoliceTrap] * options.police_trap_weight.value +
            [ItemName.Traps.BuyonTrap] * options.buyon_trap_weight.value
    )

    for _ in range(item_distribution.trap_count):
        itempool.append(world.create_item(world.random.choice(trap_weights)))

    world.multiworld.push_precollected(world.create_item(get_playable_character_item(starter_setup.character)))

    if starter_setup.item:
        world.multiworld.push_precollected(world.create_item(starter_setup.item))

    world.multiworld.itempool += itempool


def get_item_distribution(world: World, starting_item_count: int, needed_emblems: int,
                          options: SonicAdventureDXOptions) -> ItemDistribution:
    location_count = sum(1 for location in world.multiworld.get_locations(world.player) if not location.locked)
    extra_items = max(0, location_count - (needed_emblems + starting_item_count))
    if options.goal.value in {Goal.Emblems, Goal.EmblemsAndEmeraldHunt}:
        # If Emblems are enabled, we calculate how many progressive emblems and filler emblems we need
        junk_count = math.floor(extra_items * (options.junk_fill_percentage.value / 100.0))
    else:
        # If not, all the remaining locations are filler
        junk_count = extra_items
    return ItemDistribution(
        emblem_count_progressive=needed_emblems,
        emblem_count_non_progressive=extra_items - junk_count,
        filler_count=junk_count - math.floor(junk_count * (options.trap_fill_percentage.value / 100.0)),
        trap_count=math.floor(junk_count * (options.trap_fill_percentage.value / 100.0))
    )


def get_item_names(options: SonicAdventureDXOptions, starter_setup: StarterSetup) -> List[str]:
    item_names = sum((get_item_for_options_per_character(character, options) for character in Character), [])
    item_names += [
        ItemName.KeyItem.Train, ItemName.KeyItem.Boat, ItemName.KeyItem.Raft, ItemName.KeyItem.StationKeys,
        ItemName.KeyItem.HotelKeys, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.TwinkleParkTicket,
        ItemName.KeyItem.EmployeeCard, ItemName.KeyItem.Dynamite, ItemName.KeyItem.JungleCart,
        ItemName.KeyItem.IceStone, ItemName.KeyItem.WindStone
    ]

    if options.goal.value in {Goal.EmeraldHunt, Goal.EmblemsAndEmeraldHunt, Goal.LevelsAndEmeraldHunt}:
        item_names += [
            ItemName.Progression.WhiteEmerald, ItemName.Progression.RedEmerald, ItemName.Progression.CyanEmerald,
            ItemName.Progression.PurpleEmerald, ItemName.Progression.GreenEmerald, ItemName.Progression.YellowEmerald,
            ItemName.Progression.BlueEmerald
        ]

    item_names.remove(get_playable_character_item(starter_setup.character))
    if starter_setup.item:
        item_names.remove(starter_setup.item)
    return item_names


def get_item_for_options_per_character(character: Character, options: SonicAdventureDXOptions) -> List[str]:
    if not is_character_playable(character, options):
        return []
    return [get_playable_character_item(character)] + get_character_upgrades_item(character)


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
