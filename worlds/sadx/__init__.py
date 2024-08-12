import math
import re
import typing
from typing import ClassVar, Type, Dict, Any, List

from BaseClasses import Tutorial, ItemClassification
from Options import PerGameCommonOptions, OptionError
from worlds.AutoWorld import WebWorld, World
from .CharacterUtils import character_has_life_sanity, are_character_upgrades_randomized, get_playable_character_item, \
    get_character_missions, get_playable_characters, is_level_playable, is_character_playable
from .Enums import Character, LevelMission, Area, StartingArea, AdventureField, KeyItem, SADX_BASE_ID
from .Items import all_item_table, get_item, get_item_by_name, SonicAdventureDXItem, ItemInfo, \
    key_item_table, character_unlock_item_table, character_upgrade_item_table, filler_item_table, trap_item_table
from .Locations import all_location_table, SonicAdventureDXLocation, \
    field_emblem_location_table, sub_level_location_table, level_location_table, LevelLocation, \
    upgrade_location_table, life_capsule_location_table, boss_location_table
from .Names import ItemName, LocationName
from .Options import sadx_option_groups, SonicAdventureDXOptions, BaseMissionChoice
from .Regions import create_sadx_regions, get_location_ids_for_area
from .Rules import create_rules, starting_area_items, starting_area_no_items


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
        itempool = []

        # Keys and Characters Items
        item_names = self.get_item_names()
        for itemName in item_names:
            itempool.append(self.create_item(itemName))

        self.place_not_randomized_upgrades()

        # One less for the Perfect Chaos location
        location_count = sum(1 for location in self.multiworld.get_locations(self.player) if not location.locked) - 1
        emblem_count = max(1, location_count - len(item_names))

        needed_emblems = self.get_emblems_needed()
        filler_items = emblem_count - needed_emblems

        for _ in range(needed_emblems):
            itempool.append(self.create_item(ItemName.Progression.Emblem))

        junk_count = math.floor(filler_items * (self.options.junk_fill_percentage.value / 100.0))

        trap_count = math.floor(junk_count * (self.options.trap_fill_percentage.value / 100.0))

        if trap_count > 0:
            trap_weights = []
            trap_weights += [ItemName.Traps.IceTrap] * self.options.ice_trap_weight.value
            trap_weights += [ItemName.Traps.SpringTrap] * self.options.spring_trap_weight.value
            trap_weights += [ItemName.Traps.PoliceTrap] * self.options.police_trap_weight.value
            trap_weights += [ItemName.Traps.BuyonTrap] * self.options.buyon_trap_weight.value
            for _ in range(trap_count):
                trap_item_name = self.random.choice(trap_weights)
                itempool.append(self.create_item(trap_item_name))

        for _ in range(junk_count - trap_count):
            filler_item = self.random.choice(filler_item_table)
            itempool.append(self.create_item(filler_item.name))

        for _ in range(filler_items - junk_count):
            itempool.append(self.create_item(ItemName.Progression.Emblem, True))

        starter_character_name = get_playable_character_item(self.starter_character)
        self.multiworld.push_precollected(self.create_item(starter_character_name))
        if self.starter_item is not None:
            self.multiworld.push_precollected(self.create_item(self.starter_item))

        self.multiworld.itempool += itempool

    def place_not_randomized_upgrades(self):
        if is_character_playable(Character.Sonic, self.options) and not self.options.randomized_sonic_upgrades:
            self.multiworld.get_location(LocationName.Sonic.LightShoes, self.player).place_locked_item(
                self.create_item(ItemName.Sonic.LightShoes))
            self.multiworld.get_location(LocationName.Sonic.CrystalRing, self.player).place_locked_item(
                self.create_item(ItemName.Sonic.CrystalRing))
            self.multiworld.get_location(LocationName.Sonic.AncientLight, self.player).place_locked_item(
                self.create_item(ItemName.Sonic.AncientLight))
        if is_character_playable(Character.Tails, self.options) and not self.options.randomized_tails_upgrades:
            self.multiworld.get_location(LocationName.Tails.JetAnklet, self.player).place_locked_item(
                self.create_item(ItemName.Tails.JetAnklet))
        if is_character_playable(Character.Knuckles, self.options) and not self.options.randomized_knuckles_upgrades:
            self.multiworld.get_location(LocationName.Knuckles.ShovelClaw, self.player).place_locked_item(
                self.create_item(ItemName.Knuckles.ShovelClaw))
            self.multiworld.get_location(LocationName.Knuckles.FightingGloves, self.player).place_locked_item(
                self.create_item(ItemName.Knuckles.FightingGloves))
        if is_character_playable(Character.Amy, self.options) and not self.options.randomized_amy_upgrades:
            self.multiworld.get_location(LocationName.Amy.WarriorFeather, self.player).place_locked_item(
                self.create_item(ItemName.Amy.WarriorFeather))
            self.multiworld.get_location(LocationName.Amy.LongHammer, self.player).place_locked_item(
                self.create_item(ItemName.Amy.LongHammer))
        if is_character_playable(Character.Big, self.options) and not self.options.randomized_big_upgrades:
            self.multiworld.get_location(LocationName.Big.LifeBelt, self.player).place_locked_item(
                self.create_item(ItemName.Big.LifeBelt))
            self.multiworld.get_location(LocationName.Big.PowerRod, self.player).place_locked_item(
                self.create_item(ItemName.Big.PowerRod))
            self.multiworld.get_location(LocationName.Big.Lure1, self.player).place_locked_item(
                self.create_item(ItemName.Big.Lure1))
            self.multiworld.get_location(LocationName.Big.Lure2, self.player).place_locked_item(
                self.create_item(ItemName.Big.Lure2))
            self.multiworld.get_location(LocationName.Big.Lure3, self.player).place_locked_item(
                self.create_item(ItemName.Big.Lure3))
            self.multiworld.get_location(LocationName.Big.Lure4, self.player).place_locked_item(
                self.create_item(ItemName.Big.Lure4))
        if is_character_playable(Character.Gamma, self.options) and not self.options.randomized_gamma_upgrades:
            self.multiworld.get_location(LocationName.Gamma.JetBooster, self.player).place_locked_item(
                self.create_item(ItemName.Gamma.JetBooster))
            self.multiworld.get_location(LocationName.Gamma.LaserBlaster, self.player).place_locked_item(
                self.create_item(ItemName.Gamma.LaserBlaster))

    def set_rules(self):
        create_rules(self)

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
        item_names = self.get_item_names()
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

    def get_item_names(self) -> List[str]:
        item_names = []
        item_names += self.get_item_for_options_per_character(Character.Sonic)
        item_names += self.get_item_for_options_per_character(Character.Tails)
        item_names += self.get_item_for_options_per_character(Character.Knuckles)
        item_names += self.get_item_for_options_per_character(Character.Amy)
        item_names += self.get_item_for_options_per_character(Character.Big)
        item_names += self.get_item_for_options_per_character(Character.Gamma)
        # We don't add key items that aren't used for the randomizer

        item_names.append(ItemName.KeyItem.Train)
        item_names.append(ItemName.KeyItem.Boat)
        item_names.append(ItemName.KeyItem.Raft)
        if len(get_location_ids_for_area(Area.Hotel, self.options)) > 0:
            item_names.append(ItemName.KeyItem.HotelKeys)
        if len(get_location_ids_for_area(Area.Casino, self.options)) > 0:
            item_names.append(ItemName.KeyItem.CasinoKeys)
        if len(get_location_ids_for_area(Area.TwinklePark, self.options)) > 0:
            item_names.append(ItemName.KeyItem.TwinkleParkTicket)
        if len(get_location_ids_for_area(Area.SpeedHighway, self.options)) > 0:
            item_names.append(ItemName.KeyItem.EmployeeCard)
        if len(get_location_ids_for_area(Area.AngelIsland, self.options)) > 0:
            item_names.append(ItemName.KeyItem.Dynamite)
        if len(get_location_ids_for_area(Area.Jungle, self.options)) > 0:
            item_names.append(ItemName.KeyItem.JungleCart)
        # Don't include the ice stone for characters that aren't sonic/tails/big
        if is_character_playable(Character.Sonic, self.options) or is_character_playable(
                Character.Tails, self.options) or is_character_playable(Character.Big, self.options):
            item_names.append(ItemName.KeyItem.IceStone)

        if self.starter_item is not None:
            item_names.remove(self.starter_item)
        return item_names

    def get_item_for_options_per_character(self, character: Character) -> List[str]:
        item_names = []
        if not is_character_playable(character, self.options):
            return item_names

        if character != self.starter_character:
            for unlock_character in character_unlock_item_table:
                if unlock_character.character == character:
                    item_names.append(unlock_character.name)

        if are_character_upgrades_randomized(character, self.options):
            for character_upgrade in character_upgrade_item_table:
                if character_upgrade.character == character:
                    item_names.append(character_upgrade.name)

        return item_names
