from BaseClasses import Region
from .CharacterUtils import is_any_character_playable, character_has_life_sanity, is_level_playable
from .CharacterUtils import is_character_playable
from .Enums import Area, StartingArea, SubLevelMission
from .Locations import SonicAdventureDXLocation, boss_location_table, life_capsule_location_table, \
    field_emblem_location_table, upgrade_location_table, level_location_table, sub_level_location_table, \
    mission_location_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from ..AutoWorld import World


def create_sadx_regions(world: World, starter_area: StartingArea, options: SonicAdventureDXOptions):
    def create_region_with_locations(area: Area) -> Region:
        region = Region(area.value, world.player, world.multiworld)
        world.multiworld.regions.append(region)
        add_locations_to_region(region, area, world.player, options)
        return region

    def connect_two_way(area1: Region, area2: Region, key_item: str):
        area1.connect(area2, None, lambda state: state.has(key_item, world.player))
        area2.connect(area1, None, lambda state: state.has(key_item, world.player))

    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    station_square_main_area = create_region_with_locations(Area.StationSquareMain)
    station_area = create_region_with_locations(Area.Station)
    hotel_area = create_region_with_locations(Area.Hotel)
    casino_area = create_region_with_locations(Area.Casino)
    twinkle_park_area = create_region_with_locations(Area.TwinklePark)
    mystic_ruins_area = create_region_with_locations(Area.MysticRuinsMain)
    angel_island_area = create_region_with_locations(Area.AngelIsland)
    jungle_area = create_region_with_locations(Area.Jungle)
    egg_carrier_area = create_region_with_locations(Area.EggCarrierMain)

    connect_two_way(station_square_main_area, station_area, ItemName.KeyItem.StationKeys)
    connect_two_way(station_square_main_area, hotel_area, ItemName.KeyItem.HotelKeys)
    connect_two_way(station_area, casino_area, ItemName.KeyItem.CasinoKeys)
    connect_two_way(hotel_area, casino_area, ItemName.KeyItem.CasinoKeys)
    connect_two_way(station_square_main_area, twinkle_park_area, ItemName.KeyItem.TwinkleParkTicket)
    connect_two_way(mystic_ruins_area, angel_island_area, ItemName.KeyItem.Dynamite)
    connect_two_way(mystic_ruins_area, jungle_area, ItemName.KeyItem.JungleCart)
    connect_two_way(station_area, mystic_ruins_area, ItemName.KeyItem.Train)
    connect_two_way(station_square_main_area, egg_carrier_area, ItemName.KeyItem.Boat)
    connect_two_way(mystic_ruins_area, egg_carrier_area, ItemName.KeyItem.Raft)

    if starter_area == StartingArea.StationSquareMain:
        menu_region.connect(station_square_main_area)
    elif starter_area == StartingArea.Station:
        menu_region.connect(station_area)
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
    perfect_chaos_fight = SonicAdventureDXLocation(world.player, 9, menu_region)
    perfect_chaos_fight.locked = True
    perfect_chaos_area.locations.append(perfect_chaos_fight)

    menu_region.connect(perfect_chaos_area)


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
                    if ((options.sub_level_checks_hard and sub_level.subLevelMission == SubLevelMission.A)
                            or sub_level.subLevelMission == SubLevelMission.B):
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

    if options.mission_mode_checks:
        for mission in mission_location_table:
            if not options.non_stop_missions and mission.locationId in [49, 53, 54, 58]:
                continue
            if mission.objectiveArea == area:
                if is_character_playable(mission.character, options):
                    location_ids.append(mission.locationId)

    return location_ids
