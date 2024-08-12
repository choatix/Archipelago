from BaseClasses import Region
from .CharacterUtils import is_any_character_playable, character_has_life_sanity, is_level_playable
from .CharacterUtils import is_character_playable
from .Enums import Area, StartingArea
from .Locations import SonicAdventureDXLocation, boss_location_table, life_capsule_location_table, \
    field_emblem_location_table, upgrade_location_table, level_location_table, sub_level_location_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from ..AutoWorld import World


def create_sadx_regions(world: World, starter_area: StartingArea,
                        emblems_needed: int, options: SonicAdventureDXOptions):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    station_square_area = Region("Station Square", world.player, world.multiworld)
    world.multiworld.regions.append(station_square_area)
    add_locations_to_region(station_square_area, Area.StationSquareMain, world.player, options)

    hotel_area = Region("Hotel Area", world.player, world.multiworld)
    world.multiworld.regions.append(hotel_area)
    add_locations_to_region(hotel_area, Area.Hotel, world.player, options)
    # We don't add regions that aren't used for the randomizer
    if len(hotel_area.locations) > 0:
        station_square_area.connect(hotel_area, None,
                                    lambda state: state.has(ItemName.KeyItem.HotelKeys, world.player))

        hotel_area.connect(station_square_area, None,
                           lambda state: state.has(ItemName.KeyItem.HotelKeys, world.player))

    casino_area = Region("Casino Area", world.player, world.multiworld)
    world.multiworld.regions.append(casino_area)
    add_locations_to_region(casino_area, Area.Casino, world.player, options)
    if len(casino_area.locations) > 0:
        station_square_area.connect(casino_area, None,
                                    lambda state: state.has(ItemName.KeyItem.CasinoKeys, world.player))

        casino_area.connect(station_square_area, None,
                            lambda state: state.has(ItemName.KeyItem.CasinoKeys, world.player))

    twinkle_park_area = Region("Twinkle Park Area", world.player, world.multiworld)
    world.multiworld.regions.append(twinkle_park_area)
    add_locations_to_region(twinkle_park_area, Area.TwinklePark, world.player, options)
    if len(twinkle_park_area.locations) > 0:
        station_square_area.connect(twinkle_park_area, None,
                                    lambda state: state.has(ItemName.KeyItem.TwinkleParkTicket, world.player))

    speed_highway_area = Region("Speed Highway Area", world.player, world.multiworld)
    world.multiworld.regions.append(speed_highway_area)
    add_locations_to_region(speed_highway_area, Area.SpeedHighway, world.player, options)
    if len(speed_highway_area.locations) > 0:
        station_square_area.connect(speed_highway_area, None,
                                    lambda state: state.has(ItemName.KeyItem.EmployeeCard, world.player))

    mystic_ruins_area = Region("Mystic Ruins", world.player, world.multiworld)
    world.multiworld.regions.append(mystic_ruins_area)
    add_locations_to_region(mystic_ruins_area, Area.MysticRuinsMain, world.player, options)

    angel_island_area = Region("Angel Island", world.player, world.multiworld)
    world.multiworld.regions.append(angel_island_area)
    add_locations_to_region(angel_island_area, Area.AngelIsland, world.player, options)
    if len(angel_island_area.locations) > 0:
        mystic_ruins_area.connect(angel_island_area, None,
                                  lambda state: state.has(ItemName.KeyItem.Dynamite, world.player))

    jungle_area = Region("Jungle", world.player, world.multiworld)
    world.multiworld.regions.append(jungle_area)
    add_locations_to_region(jungle_area, Area.Jungle, world.player, options)
    if len(jungle_area.locations) > 0:
        mystic_ruins_area.connect(jungle_area, None,
                                  lambda state: state.has(ItemName.KeyItem.JungleCart, world.player))
        jungle_area.connect(mystic_ruins_area, None,
                            lambda state: state.has(ItemName.KeyItem.JungleCart, world.player))

    egg_carrier_area = Region("Egg Carrier", world.player, world.multiworld)
    world.multiworld.regions.append(egg_carrier_area)
    add_locations_to_region(egg_carrier_area, Area.EggCarrierMain, world.player, options)

    # We connect the main regions
    station_square_area.connect(mystic_ruins_area, None, lambda state: state.has(
        ItemName.KeyItem.Train, world.player))
    mystic_ruins_area.connect(station_square_area, None, lambda state: state.has(
        ItemName.KeyItem.Train, world.player))

    station_square_area.connect(egg_carrier_area, None, lambda state: state.has(
        ItemName.KeyItem.Boat, world.player))
    egg_carrier_area.connect(station_square_area, None, lambda state: state.has(
        ItemName.KeyItem.Boat, world.player))

    mystic_ruins_area.connect(egg_carrier_area, None, lambda state: state.has(
        ItemName.KeyItem.Raft, world.player))
    egg_carrier_area.connect(mystic_ruins_area, None, lambda state: state.has(
        ItemName.KeyItem.Raft, world.player))

    if starter_area == StartingArea.StationSquare:
        menu_region.connect(station_square_area)
    elif starter_area == StartingArea.Hotel:
        menu_region.connect(hotel_area)
    elif starter_area == StartingArea.Casino:
        menu_region.connect(casino_area)
    elif starter_area == StartingArea.MysticRuins:
        menu_region.connect(mystic_ruins_area)
    elif starter_area == StartingArea.Jungle:
        menu_region.connect(jungle_area)
    elif starter_area == StartingArea.EggCarrier:
        menu_region.connect(egg_carrier_area)

    perfect_chaos_area = Region("Perfect Chaos Fight", world.player, world.multiworld)
    perfect_chaos = SonicAdventureDXLocation(world.player, 9, menu_region)
    perfect_chaos_area.locations.append(perfect_chaos)

    menu_region.connect(perfect_chaos_area, None,
                        lambda state: state.has(ItemName.Progression.ChaosPeace, world.player, emblems_needed))


def add_locations_to_region(region: Region, area: Area, player: int, options: SonicAdventureDXOptions):
    location_ids = get_location_ids_for_area(area, options)
    for location_id in location_ids:
        location = SonicAdventureDXLocation(player, location_id, region)
        region.locations.append(location)


def get_location_ids_for_area(area: Area, options: SonicAdventureDXOptions):
    location_ids = []
    for level in level_location_table:
        if level.area == area:
            if is_level_playable(level, options):
                location_ids.append(level.locationId)
    for upgrade in upgrade_location_table:
        if upgrade.area == area:
            if is_character_playable(upgrade.character, options):
                location_ids.append(upgrade.locationId)
    if options.sub_level_checks:
        for sub_level in sub_level_location_table:
            if sub_level.area == area:
                if is_any_character_playable(sub_level.characters, options):
                    location_ids.append(sub_level.locationId)

    if options.field_emblems_checks:
        for field_emblem in field_emblem_location_table:
            if field_emblem.area == area:
                if is_any_character_playable(field_emblem.characters, options):
                    location_ids.append(field_emblem.locationId)

    if options.life_sanity:
        for life_capsule in life_capsule_location_table:
            if life_capsule.area == area:
                if is_character_playable(life_capsule.character, options):
                    if character_has_life_sanity(life_capsule.character, options):
                        if life_capsule.locationId == 1211 or life_capsule.locationId == 1212:
                            if options.pinball_life_capsules:
                                location_ids.append(life_capsule.locationId)
                        else:
                            location_ids.append(life_capsule.locationId)
    if options.boss_checks:
        for boss_fight in boss_location_table:
            if boss_fight.area == area:
                if options.unify_chaos4 and boss_fight.boss == LocationName.Boss.Chaos4 and not boss_fight.unified:
                    continue
                if not options.unify_chaos4 and boss_fight.boss == LocationName.Boss.Chaos4 and boss_fight.unified:
                    continue
                if options.unify_chaos6 and boss_fight.boss == LocationName.Boss.Chaos6 and not boss_fight.unified:
                    continue
                if not options.unify_chaos6 and boss_fight.boss == LocationName.Boss.Chaos6 and boss_fight.unified:
                    continue
                if options.unify_egg_hornet and boss_fight.boss == LocationName.Boss.EggHornet and not boss_fight.unified:
                    continue
                if not options.unify_egg_hornet and boss_fight.boss == LocationName.Boss.EggHornet and boss_fight.unified:
                    continue

                if is_any_character_playable(boss_fight.characters, options):
                    location_ids.append(boss_fight.locationId)

    return location_ids
