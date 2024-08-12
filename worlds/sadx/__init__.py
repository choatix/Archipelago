import re
import typing
from typing import ClassVar, Type, Dict, Any

from BaseClasses import Tutorial, ItemClassification
from Options import PerGameCommonOptions, OptionError
from worlds.AutoWorld import WebWorld, World
from .CharacterUtils import get_playable_characters
from .Enums import Character, StartingArea, SADX_BASE_ID
from .ItemPool import create_sadx_items, get_item_names
from .Items import all_item_table, SonicAdventureDXItem, get_item_by_name
from .Locations import all_location_table
from .Names import ItemName, LocationName
from .Options import sadx_option_groups, SonicAdventureDXOptions, BaseMissionChoice
from .Regions import create_sadx_regions, get_location_ids_for_area
from .Rules import create_sadx_rules, starting_area_items, starting_area_no_items


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
    starter_character: Character = None
    starter_area: StartingArea = None
    starter_item: str = None

    item_name_to_id = {item["name"]: (item["id"] + SADX_BASE_ID) for item in all_item_table}
    location_name_to_id = {loc["name"]: (loc["id"] + SADX_BASE_ID) for loc in all_location_table}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = SonicAdventureDXOptions

    options: SonicAdventureDXOptions

    def generate_early(self):
        possible_characters = get_playable_characters(self.options)
        if len(possible_characters) == 0:
            raise OptionError("You need at least one playable character")

        self.starter_character = self.random.choice(possible_characters)

        # Random starting location
        if self.options.random_starting_location == 0:
            self.starter_area = self.random.choice(list(starting_area_items[self.starter_character].keys()))
            possible_starting_items = starting_area_items[self.starter_character][self.starter_area]
            if len(possible_starting_items) > 0:
                self.starter_item = self.random.choice(possible_starting_items)
        # Random starting location no items
        elif self.options.random_starting_location == 1:
            self.starter_area = self.random.choice(list(starting_area_no_items[self.starter_character].keys()))
        # Station Square
        elif self.options.random_starting_location == 2:
            self.starter_area = StartingArea.StationSquare
            possible_starting_items = starting_area_items[self.starter_character][self.starter_area]
            if len(possible_starting_items) > 0:
                self.starter_item = self.random.choice(possible_starting_items)
        # Station Square no items
        elif self.options.random_starting_location == 3:
            self.starter_area = StartingArea.StationSquare

        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Sonic Adventure DX" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Sonic Adventure DX"]
                self.starter_character = Character(passthrough["StartingCharacter"])
                self.starter_area = StartingArea(passthrough["StartingArea"])
                self.starter_item = passthrough["StartingItem"]

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data

    def create_item(self, name: str, force_non_progression=False) -> SonicAdventureDXItem:
        item = get_item_by_name(name)
        classification = ItemClassification.filler if force_non_progression else None
        return SonicAdventureDXItem(item, self.player, classification)

    def create_regions(self) -> None:
        create_sadx_regions(self.multiworld, self.player, self.starter_area,
                            self.get_emblems_needed(), self.options)

    def create_items(self):
        self.multiworld.itempool += create_sadx_items(self, self.starter_character, self.starter_item,
                                                      self.get_emblems_needed(), self.options)

    def set_rules(self):
        create_sadx_rules(self, self.get_emblems_needed())

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        spoiler_handle.write("\n")
        header_text = "Sonic Adventure starting setup for {}:\n"
        header_text = header_text.format(self.multiworld.player_name[self.player])
        spoiler_handle.write(header_text)

        starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', self.starter_area.name)
        if self.starter_item is not None:
            text = "Will start as {0} in the {1} area with {2}.\n"
            text = text.format(self.starter_character.name, starting_area_name, self.starter_item)
        else:
            text = "Will start as {0} in the {1} area.\n"
            text = text.format(self.starter_character.name, starting_area_name)
        spoiler_handle.writelines(text)

    def get_emblems_needed(self) -> int:
        item_names = get_item_names(self.options, self.starter_item, self.starter_character)
        location_count = sum(1 for location in self.multiworld.get_locations(self.player) if not location.locked) - 1
        emblem_count = max(1, location_count - len(item_names))
        return int(round(emblem_count * self.options.emblems_percentage / 100))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "ModVersion": "0.4.3",
            "EmblemsForPerfectChaos": self.get_emblems_needed(),
            "StartingCharacter": self.starter_character.value,
            "StartingArea": self.starter_area.value,
            "StartingItem": self.starter_item,
            "RandomStartingLocation": self.options.random_starting_location.value,
            "FieldEmblemChecks": self.options.field_emblems_checks.value,

            "LifeSanity": self.options.life_sanity.value,
            "PinballLifeCapsules": self.options.pinball_life_capsules.value,
            "SonicLifeSanity": self.options.sonic_life_sanity.value,
            "TailsLifeSanity": self.options.tails_life_sanity.value,
            "KnucklesLifeSanity": self.options.knuckles_life_sanity.value,
            "AmyLifeSanity": self.options.amy_life_sanity.value,
            "BigLifeSanity": self.options.big_life_sanity.value,
            "GammaLifeSanity": self.options.gamma_life_sanity.value,

            "DeathLink": self.options.death_link.value,
            "RingLink": self.options.ring_link.value,
            "HardRingLink": self.options.hard_ring_link.value,
            "RingLoss": self.options.ring_loss.value,
            "SubLevelChecks": self.options.sub_level_checks.value,

            "BossChecks": self.options.boss_checks.value,
            "UnifyChaos4": self.options.unify_chaos4.value,
            "UnifyChaos6": self.options.unify_chaos6.value,
            "UnifyEggHornet": self.options.unify_egg_hornet.value,

            "RandomizedSonicUpgrades": self.options.randomized_sonic_upgrades.value,
            "RandomizedTailsUpgrades": self.options.randomized_tails_upgrades.value,
            "RandomizedKnucklesUpgrades": self.options.randomized_knuckles_upgrades.value,
            "RandomizedAmyUpgrades": self.options.randomized_amy_upgrades.value,
            "RandomizedGammaUpgrades": self.options.randomized_big_upgrades.value,
            "RandomizedBigUpgrades": self.options.randomized_gamma_upgrades.value,

            "SonicMissions": self.options.sonic_missions.value,
            "TailsMissions": self.options.tails_missions.value,
            "KnucklesMissions": self.options.knuckles_missions.value,
            "AmyMissions": self.options.amy_missions.value,
            "GammaMissions": self.options.gamma_missions.value,
            "BigMissions": self.options.big_missions.value,

            "JunkFillPercentage": self.options.junk_fill_percentage.value
        }
