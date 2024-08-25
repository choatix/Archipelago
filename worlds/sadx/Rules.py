from worlds.generic.Rules import add_rule
from .CharacterUtils import get_playable_characters, is_level_playable
from .Enums import Goal, LevelMission
from .Locations import (
    get_location_by_name, level_location_table, LevelLocation, upgrade_location_table, UpgradeLocation,
    sub_level_location_table, SubLevelLocation, field_emblem_location_table, EmblemLocation,
    life_capsule_location_table, LifeCapsuleLocation, boss_location_table, BossFightLocation,
    mission_location_table, MissionLocation, CharacterUpgrade, LocationInfo
)
from .Names import ItemName
from .Regions import get_region_name


def add_level_rules(self, location_name: str, level: LevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in level.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_upgrade_rules(self, location_name: str, upgrade: UpgradeLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in upgrade.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_sub_level_rules(self, location_name: str, sub_level: SubLevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.can_reach_region(get_region_name(character, sub_level.area), self.player) for character in
        sub_level.characters if character in get_playable_characters(self.options)))


def add_field_emblem_rules(self, location_name: str, field_emblem: EmblemLocation):
    location = self.multiworld.get_location(location_name, self.player)
    # We check if the player has any of the character / character+upgraded needed
    add_rule(location, lambda state: any(
        (state.can_reach_region(
            get_region_name(character.character if isinstance(character, CharacterUpgrade) else character,
                            field_emblem.area), self.player) and
         (state.has(character.upgrade, self.player) if isinstance(character, CharacterUpgrade) else True))
        for character in field_emblem.get_logic_characters_upgrades(self.options) if
        character in get_playable_characters(self.options) or
        (isinstance(character, CharacterUpgrade) and character.character in get_playable_characters(self.options))))


def add_life_capsule_rules(self, location_name: str, life_capsule: LifeCapsuleLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in life_capsule.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_boss_fight_rules(self, location_name: str, boss_fight: BossFightLocation):
    location = self.multiworld.get_location(location_name, self.player)
    if not boss_fight.unified:
        return
    add_rule(location, lambda state: any(
        state.can_reach_region(get_region_name(character, boss_fight.area), self.player) for character in
        boss_fight.characters if character in get_playable_characters(self.options)))


def add_mission_rules(self, location_name: str, mission: MissionLocation):
    location = self.multiworld.get_location(location_name, self.player)
    card_area_name = get_region_name(mission.character, mission.cardArea)
    if not self.options.auto_start_missions:
        add_rule(location, lambda state, card_area=card_area_name: state.can_reach_region(card_area, self.player))
    for need in mission.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


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
    for mission in mission_location_table:
        if location["id"] == mission.locationId:
            add_mission_rules(self, location["name"], mission)


def create_sadx_rules(self, needed_emblems: int):
    for ap_location in self.multiworld.get_locations(self.player):
        calculate_rules(self, get_location_by_name(ap_location.name))

    perfect_chaos_fight = self.multiworld.get_location("Perfect Chaos Fight", self.player)
    perfect_chaos_fight.place_locked_item(self.create_item(ItemName.Progression.ChaosPeace))

    if self.options.goal.value in {Goal.Emblems, Goal.EmblemsAndEmeraldHunt}:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.Emblem, self.player, needed_emblems))

    if self.options.goal.value in {Goal.Levels, Goal.LevelsAndEmeraldHunt}:
        for level in level_location_table:
            if is_level_playable(level, self.options) and level.levelMission == LevelMission.C:
                location = self.multiworld.get_location(level.get_level_name(), self.player)
                add_rule(perfect_chaos_fight, lambda state: location.can_reach(state))

    if self.options.goal.value in {Goal.EmeraldHunt, Goal.LevelsAndEmeraldHunt, Goal.EmblemsAndEmeraldHunt}:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.WhiteEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.RedEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.CyanEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.PurpleEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.GreenEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.YellowEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.BlueEmerald, self.player))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)
