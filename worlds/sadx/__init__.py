from typing import ClassVar, Dict, Any, Type

from BaseClasses import Region, Location, Item, Tutorial
from Options import PerGameCommonOptions, Choice
from worlds.AutoWorld import WebWorld, World
from .Items import item_table, get_item, ItemDict
from .Locations import location_table
from .Names import LocationName, ItemName
from .Options import SonicAdventureDXOptions, sadx_option_groups
from .Rules import create_rules

base_id = 5438000


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

    item_name_to_id = {item["name"]: (item["id"] + base_id) for item in item_table}
    location_name_to_id = {loc["name"]: (loc["id"] + base_id) for loc in location_table}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = SonicAdventureDXOptions

    options: SonicAdventureDXOptions

    def create_item(self, name: str) -> "SonicAdventureDXItem":
        item_id: int = self.item_name_to_id[name]
        item = get_item(item_id - base_id)

        classification = item["classification"]

        return SonicAdventureDXItem(name, classification, item_id, player=self.player)

    def create_items(self):
        itempool = []

        self.add_character_item(itempool, "Sonic", self.options.sonic_missions)
        self.add_character_item(itempool, "Tails", self.options.tails_missions)
        self.add_character_item(itempool, "Knuckles", self.options.knuckles_missions)
        self.add_character_item(itempool, "Amy", self.options.amy_missions)
        self.add_character_item(itempool, "Gamma", self.options.gamma_missions)
        self.add_character_item(itempool, "Big", self.options.big_missions)

        emblem_count = self.get_emblem_count()

        emblem_count = range(emblem_count)
        for _ in emblem_count:
            itempool.append(self.create_item(ItemName.Progression.Emblem))

        # itempool.append(self.create_item(ItemName.Progression.ChaosPeace))
        self.multiworld.itempool += itempool

    def get_emblem_count(self):
        emblem_count = 0
        emblem_count += len(self.get_character_level_locations("Sonic", self.options.sonic_missions))
        emblem_count += len(self.get_character_level_locations("Tails", self.options.tails_missions))
        emblem_count += len(self.get_character_level_locations("Knuckles", self.options.knuckles_missions))
        emblem_count += len(self.get_character_level_locations("Amy", self.options.amy_missions))
        emblem_count += len(self.get_character_level_locations("Gamma", self.options.gamma_missions))
        emblem_count += len(self.get_character_level_locations("Big", self.options.big_missions))
        return emblem_count

    def get_emblems_needed(self):
        return int(round(self.get_emblem_count() * self.options.emblems_percentage / 100))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        sonic_story = Region("Sonic's Story", self.player, self.multiworld)
        self.add_character_location(sonic_story, "Sonic", self.options.sonic_missions)

        self.add_character_region("Tails", "Tails' Story", self.options.tails_missions,
                                  LocationName.Story.Meet.Tails, sonic_story, menu_region)
        self.add_character_region("Knuckles", "Knuckles' Story", self.options.knuckles_missions,
                                  LocationName.Story.Meet.Knuckles, sonic_story, menu_region)
        self.add_character_region("Amy", "Amy's Story", self.options.amy_missions,
                                  LocationName.Story.Meet.Amy, sonic_story, menu_region)
        self.add_character_region("Gamma", "Gamma's Story", self.options.gamma_missions,
                                  LocationName.Story.Meet.Gamma, sonic_story, menu_region)
        self.add_character_region("Big", "Big's Story", self.options.big_missions,
                                  LocationName.Story.Meet.Big, sonic_story, menu_region)

        perfect_chaos = SonicAdventureDXLocation(self.player, LocationName.Story.Fight.PerfectChaos,
                                                 self.location_name_to_id[LocationName.Story.Fight.PerfectChaos],
                                                 sonic_story)
        sonic_story.locations.append(perfect_chaos)

        self.multiworld.regions.append(sonic_story)
        menu_region.connect(sonic_story)

    def add_character_region(self, character_name: str, story_name: str, mission_choice: Choice, meet_loc: str,
                             sonic_story: Region, menu_region: Region):
        if mission_choice > 0:
            # We add meeting the character as a location check
            game_loc = SonicAdventureDXLocation(self.player, meet_loc, self.location_name_to_id[meet_loc], sonic_story)
            sonic_story.locations.append(game_loc)
            # We create a character's story as a region
            character_story = Region(story_name, self.player, self.multiworld)
            # We add its levels and upgrades as checks
            self.add_character_location(character_story, character_name, mission_choice)
            self.multiworld.regions.append(character_story)
            menu_region.connect(character_story)

    def add_character_location(self, region: Region, character: str, missions: Choice):
        level_locations = self.get_character_level_locations(character, missions)
        upgrade_locations = self.get_character_upgrade_location(character, missions)

        character_locations = level_locations + upgrade_locations

        for location in character_locations:
            level_location = SonicAdventureDXLocation(self.player, location, self.location_name_to_id[location], region)
            region.locations.append(level_location)

    def get_character_level_locations(self, character_name: str, missions):
        level_location = []
        for loc in self.location_name_to_id.keys():
            if (missions > 0 and (character_name + " - Mission C") in loc
                    or missions > 1 and (character_name + " - Mission B") in loc
                    or missions > 2 and (character_name + " - Mission A") in loc):
                level_location.append(loc)
        return level_location

    def get_character_upgrade_location(self, character_name: str, missions):
        upgrade_location = []
        for loc in self.location_name_to_id.keys():
            if missions > 0 and "upgrade (" + character_name in loc:
                upgrade_location.append(loc)
        return upgrade_location

    def add_character_item(self, itempool: [], character_name: str, missions: Choice):

        if missions < 1:
            return
        # We add all the upgrades and the story unlock
        for item in item_table:
            if ("(" + character_name + ")") not in item["name"]:
                continue
            if not self.options.story_unlock_randomized and item["name"] == "Story unlock (" + character_name + ")":
                continue
            if item["count"] <= 0:
                continue
            for i in range(item["count"]):
                itempool.append(self.create_item(item["name"]))

    def set_rules(self):
        create_rules(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "ModVersion": "0.1.0",
            "EmblemsForPerfectChaos": self.get_emblems_needed(),
            "SonicMissions": self.options.sonic_missions.value,
            "TailsMissions": self.options.tails_missions.value,
            "KnucklesMissions": self.options.knuckles_missions.value,
            "AmyMissions": self.options.amy_missions.value,
            "GammaMissions": self.options.gamma_missions.value,
            "BigMissions": self.options.big_missions.value
        }


class SonicAdventureDXItem(Item):
    game: str = "Sonic Adventure DX"


class SonicAdventureDXLocation(Location):
    game: str = "Sonic Adventure DX"
