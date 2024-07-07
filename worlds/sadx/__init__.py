from typing import ClassVar, Dict, Any, Type

from BaseClasses import Region, Location, Item, Tutorial
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Items import item_table, get_item
from .Locations import location_table
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

    def create_items(self) -> None:
        itempool = []
        for item in item_table:
            count = item["count"]

            if count <= 0:
                continue
            else:
                for i in range(count):
                    itempool.append(self.create_item(item["name"]))

        self.multiworld.itempool += itempool

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_region = Region("Sonic Adventure World", self.player, self.multiworld)

        for loc in self.location_name_to_id.keys():
            main_region.locations.append(
                SonicAdventureDXLocation(self.player, loc, self.location_name_to_id[loc], main_region))

        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

    def set_rules(self):
        create_rules(self, location_table)

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options

        settings = {
            "storyRandomized": int(options.story_unlock_randomized),
        }

        slot_data = {
            "settings": settings,
        }

        return slot_data


class SonicAdventureDXItem(Item):
    game: str = "Sonic Adventure DX"


class SonicAdventureDXLocation(Location):
    game: str = "Sonic Adventure DX"
