from typing import ClassVar, Type, Dict, Any, List

from BaseClasses import Tutorial, Region
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Enums import Character, LevelMission, Area
from .Items import all_item_table, get_item, get_item_by_name, SonicAdventureDXItem, ItemInfo, \
    key_item_table, character_unlock_item_table, character_upgrade_item_table
from .Locations import all_location_table, SonicAdventureDXLocation, \
    field_emblem_location_table, sub_level_location_table, level_location_table, LevelLocation, \
    upgrade_location_table, life_capsule_location_table
from .Names import ItemName
from .Options import sadx_option_groups, SonicAdventureDXOptions, BaseMissionChoice
from .Rules import create_rules

base_id = 543800000


class SonicAdventureDXWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Sonic Adventure DX randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["ClassicSpeed"]
    )]
    option_groups = sadx_option_groups


class SonicAdventureDXWorld(World):
    game = "Sonic Adventure DX"
    web = SonicAdventureDXWeb()
    starter_character = None

    item_name_to_id = {item["name"]: (item["id"] + base_id) for item in all_item_table}
    location_name_to_id = {loc["name"]: (loc["id"] + base_id) for loc in all_location_table}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = SonicAdventureDXOptions

    options: SonicAdventureDXOptions

    def create_item(self, name: str) -> "SonicAdventureDXItem":
        item: ItemInfo = get_item_by_name(name)
        return SonicAdventureDXItem(item, base_id, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        station_square_area = Region("Station Square", self.player, self.multiworld)
        self.multiworld.regions.append(station_square_area)
        self.add_locations_to_region(station_square_area, Area.StationSquareMain)
        # no logic for now, will add random adventure field later
        menu_region.connect(station_square_area)

        hotel_area = Region("Hotel Area", self.player, self.multiworld)
        self.multiworld.regions.append(hotel_area)
        self.add_locations_to_region(hotel_area, Area.Hotel)
        # We don't add regions that aren't used for the randomizer
        if len(hotel_area.locations) > 0:
            station_square_area.connect(hotel_area, None,
                                        lambda state: state.has(ItemName.KeyItem.HotelKeys, self.player))

        casino_area = Region("Casino Area", self.player, self.multiworld)
        self.multiworld.regions.append(casino_area)
        self.add_locations_to_region(casino_area, Area.Casino)
        if len(casino_area.locations) > 0:
            station_square_area.connect(casino_area, None,
                                        lambda state: state.has(ItemName.KeyItem.CasinoKeys, self.player))

        twinkle_park_area = Region("Twinkle Park Area", self.player, self.multiworld)
        self.multiworld.regions.append(twinkle_park_area)
        self.add_locations_to_region(twinkle_park_area, Area.TwinklePark)
        if len(twinkle_park_area.locations) > 0:
            station_square_area.connect(twinkle_park_area, None,
                                        lambda state: state.has(ItemName.KeyItem.TwinkleParkTicket, self.player))

        speed_highway_area = Region("Speed Highway Area", self.player, self.multiworld)
        self.multiworld.regions.append(speed_highway_area)
        self.add_locations_to_region(speed_highway_area, Area.SpeedHighway)
        if len(speed_highway_area.locations) > 0:
            station_square_area.connect(speed_highway_area, None,
                                        lambda state: state.has(ItemName.KeyItem.EmployeeCard, self.player))

        mystic_ruins_area = Region("Mystic Ruins", self.player, self.multiworld)
        self.multiworld.regions.append(mystic_ruins_area)
        self.add_locations_to_region(mystic_ruins_area, Area.MysticRuinsMain)
        station_square_area.connect(mystic_ruins_area, None, lambda state: state.has(
            ItemName.KeyItem.Train or (
                    state.has(ItemName.KeyItem.Boat, self.player) and state.has(ItemName.KeyItem.Raft,
                                                                                self.player)), self.player))

        angel_island_area = Region("Angel Island", self.player, self.multiworld)
        self.multiworld.regions.append(angel_island_area)
        self.add_locations_to_region(angel_island_area, Area.AngelIsland)
        if len(angel_island_area.locations) > 0:
            mystic_ruins_area.connect(angel_island_area, None,
                                      lambda state: state.has(ItemName.KeyItem.Dynamite, self.player))

        jungle_area = Region("Jungle", self.player, self.multiworld)
        self.multiworld.regions.append(jungle_area)
        self.add_locations_to_region(jungle_area, Area.Jungle)
        if len(jungle_area.locations) > 0:
            mystic_ruins_area.connect(jungle_area, None,
                                      lambda state: state.has(ItemName.KeyItem.JungleKart, self.player))

        egg_carrier_area = Region("Egg Carrier", self.player, self.multiworld)
        self.multiworld.regions.append(egg_carrier_area)
        self.add_locations_to_region(egg_carrier_area, Area.EggCarrierMain)
        station_square_area.connect(egg_carrier_area, None, lambda state: state.has(
            ItemName.KeyItem.Boat or (
                    state.has(ItemName.KeyItem.Train, self.player) and state.has(ItemName.KeyItem.Raft,
                                                                                 self.player)), self.player))

        perfect_chaos = SonicAdventureDXLocation(self.player, 9, base_id, menu_region)
        menu_region.locations.append(perfect_chaos)

    def create_items(self):
        itempool = []

        # Keys and Characters Items
        self.starter_character = self.get_starter_character()
        item_names = self.get_items_for_options(self.options, self.starter_character)
        for itemName in item_names:
            itempool.append(self.create_item(itemName))

        # One less for the Perfect Chaos location
        location_count = sum(1 for _ in self.multiworld.get_locations(self.player)) - 1
        emblem_count = max(1, location_count - len(item_names))

        for _ in range(emblem_count):
            itempool.append(self.create_item(ItemName.Progression.Emblem))

        starter_character_name = self.get_character_item_from_enum(self.starter_character)
        self.multiworld.push_precollected(self.create_item(starter_character_name))

        self.multiworld.itempool += itempool

    def set_rules(self):
        create_rules(self)

    def get_emblems_needed(self):

        item_names = self.get_items_for_options(self.options, self.starter_character)
        location_count = sum(1 for _ in self.multiworld.get_locations(self.player)) - 1
        emblem_count = max(1, location_count - len(item_names))
        return int(round(emblem_count * self.options.emblems_percentage / 100))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "ModVersion": "0.3.1",
            "EmblemsForPerfectChaos": self.get_emblems_needed(),
            "FieldEmblemChecks": self.options.field_emblems_checks.value,
            "LifeSanity": self.options.life_sanity.value,
            "PinballLifeCapsules": self.options.pinball_life_capsules.value,
            "SubLevelChecks": self.options.sub_level_checks.value,
            "RandomizeUpgrades": self.options.randomized_upgrades.value,
            "SonicMissions": self.options.sonic_missions.value,
            "TailsMissions": self.options.tails_missions.value,
            "KnucklesMissions": self.options.knuckles_missions.value,
            "AmyMissions": self.options.amy_missions.value,
            "GammaMissions": self.options.gamma_missions.value,
            "BigMissions": self.options.big_missions.value,
        }

    def get_starter_character(self) -> Character:
        possible_characters = self.get_playable_characters()
        assert len(possible_characters) > 0, "You need at least one playable character"
        return self.random.choice(possible_characters)

    @staticmethod
    def get_character_item_from_enum(character: Character) -> str:
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

    def get_items_for_options(self, options: SonicAdventureDXOptions, starter_character: Character) -> List[str]:
        item_names = []
        item_names += self.get_item_for_options_per_character(Character.Sonic, starter_character,
                                                              options.sonic_missions)
        item_names += self.get_item_for_options_per_character(Character.Tails, starter_character,
                                                              options.tails_missions)
        item_names += self.get_item_for_options_per_character(Character.Knuckles, starter_character,
                                                              options.knuckles_missions)
        item_names += self.get_item_for_options_per_character(Character.Amy, starter_character, options.amy_missions, )
        item_names += self.get_item_for_options_per_character(Character.Big, starter_character, options.big_missions)
        item_names += self.get_item_for_options_per_character(Character.Gamma, starter_character,
                                                              options.gamma_missions)
        # We don't add key items that aren't used for the randomizer

        item_names.append(ItemName.KeyItem.Train)
        item_names.append(ItemName.KeyItem.Boat)
        item_names.append(ItemName.KeyItem.Raft)
        if len(self.get_location_ids_for_area(Area.Hotel)) > 0:
            item_names.append(ItemName.KeyItem.HotelKeys)
        if len(self.get_location_ids_for_area(Area.Casino)) > 0:
            item_names.append(ItemName.KeyItem.CasinoKeys)
        if len(self.get_location_ids_for_area(Area.TwinklePark)) > 0:
            item_names.append(ItemName.KeyItem.TwinkleParkTicket)
        if len(self.get_location_ids_for_area(Area.SpeedHighway)) > 0:
            item_names.append(ItemName.KeyItem.EmployeeCard)
        if len(self.get_location_ids_for_area(Area.AngelIsland)) > 0:
            item_names.append(ItemName.KeyItem.Dynamite)
        if len(self.get_location_ids_for_area(Area.Jungle)) > 0:
            item_names.append(ItemName.KeyItem.JungleKart)
        # Don't include the ice stone for characters that aren't sonic/tails/big
        if self.is_character_playable(Character.Sonic) or self.is_character_playable(
                Character.Tails) or self.is_character_playable(Character.Big):
            item_names.append(ItemName.KeyItem.IceStone)

        return item_names

    def get_item_for_options_per_character(self, character: Character, starter_character: Character,
                                           missions: BaseMissionChoice) -> []:
        item_names = []
        if missions == 0:
            return item_names

        if character != starter_character:
            for unlock_character in character_unlock_item_table:
                if unlock_character.character == character:
                    item_names.append(unlock_character.name)

        if self.options.randomized_upgrades:
            for character_upgrade in character_upgrade_item_table:
                if character_upgrade.character == character:
                    item_names.append(character_upgrade.name)

        return item_names

    def get_character_missions(self, character: Character) -> BaseMissionChoice:
        character_missions = {
            Character.Sonic: self.options.sonic_missions,
            Character.Tails: self.options.tails_missions,
            Character.Knuckles: self.options.knuckles_missions,
            Character.Amy: self.options.amy_missions,
            Character.Big: self.options.big_missions,
            Character.Gamma: self.options.gamma_missions
        }
        return character_missions.get(character)

    def get_playable_characters(self) -> List[Character]:
        character_list: List[Character] = []
        if self.options.sonic_missions > 0:
            character_list.append(Character.Sonic)
        if self.options.tails_missions > 0:
            character_list.append(Character.Tails)
        if self.options.knuckles_missions > 0:
            character_list.append(Character.Knuckles)
        if self.options.amy_missions > 0:
            character_list.append(Character.Amy)
        if self.options.big_missions > 0:
            character_list.append(Character.Big)
        if self.options.gamma_missions > 0:
            character_list.append(Character.Gamma)

        return character_list

    def is_level_playable(self, level: LevelLocation) -> bool:
        character_missions = self.get_character_missions(level.character)
        if character_missions == 3 and (
                level.levelMission == LevelMission.C or level.levelMission == LevelMission.B or level.levelMission == LevelMission.A):
            return True
        if character_missions == 2 and (level.levelMission == LevelMission.C or level.levelMission == LevelMission.B):
            return True
        if character_missions == 1 and level.levelMission == LevelMission.C:
            return True
        return False

    def is_character_playable(self, character: Character) -> bool:
        return self.get_character_missions(character) > 0

    def is_any_character_playable(self, characters: List[Character]) -> bool:
        for character in characters:
            if self.is_character_playable(character):
                return True
        return False

    def get_location_ids_for_area(self, area: Area):
        location_ids = []
        for level in level_location_table:
            if level.area == area:
                if self.is_level_playable(level):
                    location_ids.append(level.locationId)
        if self.options.randomized_upgrades:
            for upgrade in upgrade_location_table:
                if upgrade.area == area:
                    if self.is_character_playable(upgrade.character):
                        location_ids.append(upgrade.locationId)
        if self.options.sub_level_checks:
            for sub_level in sub_level_location_table:
                if sub_level.area == area:
                    if self.is_any_character_playable(sub_level.characters):
                        location_ids.append(sub_level.locationId)

        if self.options.field_emblems_checks:
            for field_emblem in field_emblem_location_table:
                if field_emblem.area == area:
                    if self.is_any_character_playable(field_emblem.characters):
                        location_ids.append(field_emblem.locationId)

        if self.options.life_sanity:
            for life_capsule in life_capsule_location_table:
                if life_capsule.area == area:
                    if self.is_character_playable(life_capsule.character):
                        if life_capsule.character == Character.Sonic and life_capsule.area == Area.Casino:
                            if self.options.pinball_life_capsules:
                                location_ids.append(life_capsule.locationId)
                        else:
                            location_ids.append(life_capsule.locationId)
        return location_ids

    def add_locations_to_region(self, region: Region, area: Area):

        location_ids = self.get_location_ids_for_area(area)
        for location_id in location_ids:
            location = SonicAdventureDXLocation(self.player, location_id, base_id, region)
            region.locations.append(location)
