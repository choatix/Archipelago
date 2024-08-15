from worlds.generic.Rules import add_rule
from . import SonicAdventureDXOptions
from .CharacterUtils import get_playable_character_item, is_character_playable, are_character_upgrades_randomized
from .Enums import Character, Goal
from .Locations import get_location_by_name, LocationInfo, level_location_table, LevelLocation, \
    upgrade_location_table, UpgradeLocation, sub_level_location_table, SubLevelLocation, field_emblem_location_table, \
    EmblemLocation, life_capsule_location_table, LifeCapsuleLocation, boss_location_table, BossFightLocation
from .Names import ItemName, LocationName
from ..AutoWorld import World


def add_level_rules(self, location_name: str, level: LevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location,
             lambda state, item=get_playable_character_item(level.character): state.has(item, self.player))
    for need in level.extraItems:
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_upgrade_rules(self, location_name: str, upgrade: UpgradeLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location,
             lambda state, item=get_playable_character_item(upgrade.character): state.has(item, self.player))
    for need in upgrade.extraItems:
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_sub_level_rules(self, location_name: str, sub_level: SubLevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.has(get_playable_character_item(character), self.player) for character in sub_level.characters))


def add_field_emblem_rules(self, location_name: str, field_emblem: EmblemLocation):
    location = self.multiworld.get_location(location_name, self.player)
    # For the City Hall Emblem, Knuckles needs the Shovel Claw
    add_rule(location, lambda state: any(
        state.has(get_playable_character_item(character), self.player) and
        (state.has(ItemName.Knuckles.ShovelClaw,
                   self.player) if character == Character.Knuckles and field_emblem.emblemName == "City Hall Emblem" else True)
        for character in field_emblem.characters))


def add_life_capsule_rules(self, location_name: str, life_capsule: LifeCapsuleLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location,
             lambda state, item=get_playable_character_item(life_capsule.character): state.has(item, self.player))
    for need in life_capsule.extraItems:
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_boss_fight_rules(self, location_name: str, boss_fight: BossFightLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.has(get_playable_character_item(character), self.player) for character in boss_fight.characters))


def calculate_rules(self, location: LocationInfo):
    if location is None:
        return
    for level in level_location_table:
        if location["id"] == level.locationId:
            add_level_rules(self, location["name"], level)
    for upgrade in upgrade_location_table:
        if location["id"] == upgrade.locationId:
            add_upgrade_rules(self, location["name"], upgrade)
    for sub_level in sub_level_location_table:
        if location["id"] == sub_level.locationId:
            add_sub_level_rules(self, location["name"], sub_level)
    for life_capsule in life_capsule_location_table:
        if location["id"] == life_capsule.locationId:
            add_life_capsule_rules(self, location["name"], life_capsule)
    for field_emblem in field_emblem_location_table:
        if location["id"] == field_emblem.locationId:
            add_field_emblem_rules(self, location["name"], field_emblem)
    for boss_fight in boss_location_table:
        if location["id"] == boss_fight.locationId:
            add_boss_fight_rules(self, location["name"], boss_fight)


def create_sadx_rules(self, needed_emblems: int):
    for ap_location in self.multiworld.get_locations(self.player):
        calculate_rules(self, get_location_by_name(ap_location.name))

    perfect_chaos_fight = self.multiworld.get_location("Perfect Chaos Fight", self.player)
    perfect_chaos_fight.place_locked_item(self.create_item(ItemName.Progression.ChaosPeace))

    if self.options.goal in {Goal.Emblems, Goal.EmblemsAndEmeraldHunt}:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.Emblem, self.player, needed_emblems))

    if self.options.goal in {Goal.EmeraldHunt, Goal.EmblemsAndEmeraldHunt}:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.WhiteEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.RedEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.CyanEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.PurpleEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.GreenEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.YellowEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.BlueEmerald, self.player))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)

