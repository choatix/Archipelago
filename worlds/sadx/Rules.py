from worlds.generic.Rules import add_rule
from worlds.sadx import Character, StartingArea
from worlds.sadx.Locations import get_location_by_name, LocationInfo, level_location_table, LevelLocation, \
    upgrade_location_table, UpgradeLocation, sub_level_location_table, SubLevelLocation, field_emblem_location_table, \
    EmblemLocation, life_capsule_location_table, LifeCapsuleLocation, boss_location_table, BossFightLocation
from worlds.sadx.Names import ItemName


def add_level_rules(self, location_name: str, level: LevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location,
             lambda state, item=level.character.get_playable_character_item(): state.has(item, self.player))
    for need in level.extraItems:
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_upgrade_rules(self, location_name: str, upgrade: UpgradeLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location,
             lambda state, item=upgrade.character.get_playable_character_item(): state.has(item, self.player))
    for need in upgrade.extraItems:
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_sub_level_rules(self, location_name: str, sub_level: SubLevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.has(character.get_playable_character_item(), self.player) for character in sub_level.characters))


def add_field_emblem_rules(self, location_name: str, field_emblem: EmblemLocation):
    location = self.multiworld.get_location(location_name, self.player)
    # For the City Hall Emblem, Knuckles needs the Shovel Claw
    add_rule(location, lambda state: any(
        state.has(character.get_playable_character_item(), self.player) and
        (state.has(ItemName.Knuckles.ShovelClaw,
                   self.player) if character == Character.Knuckles and field_emblem.emblemName == "City Hall Emblem" else True)
        for character in field_emblem.characters))


def add_life_capsule_rules(self, location_name: str, life_capsule: LifeCapsuleLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location,
             lambda state, item=life_capsule.character.get_playable_character_item(): state.has(item, self.player))
    for need in life_capsule.extraItems:
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_boss_fight_rules(self, location_name: str, boss_fight: BossFightLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.has(character.get_playable_character_item(), self.player) for character in boss_fight.characters))


def calculate_rules(self, location: LocationInfo):
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


def create_rules(self):
    for ap_location in self.multiworld.get_locations(self.player):
        loc = get_location_by_name(ap_location.name)
        if loc is not None:
            calculate_rules(self, loc)

    self.multiworld.get_location("Perfect Chaos Fight", self.player).place_locked_item(
        self.create_item(ItemName.Progression.ChaosPeace))

    emblem_count = self.get_emblems_needed()

    add_rule(self.multiworld.get_location("Perfect Chaos Fight", self.player),
             lambda state: state.has(ItemName.Progression.Emblem, self.player, max(emblem_count, 1)))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)


starting_area_items = {
    Character.Sonic: {
        StartingArea.StationSquare: [ItemName.KeyItem.TwinkleParkTicket,
                                     ItemName.KeyItem.EmployeeCard],
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.WindStone],
        StartingArea.EggCarrier: []
    },
    Character.Tails: {
        StartingArea.StationSquare: [ItemName.KeyItem.EmployeeCard],
        StartingArea.Casino: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.WindStone],
        StartingArea.EggCarrier: []
    },
    Character.Knuckles: {
        StartingArea.StationSquare: [],
        StartingArea.Casino: [],
    },
    Character.Amy: {
        StartingArea.StationSquare: [ItemName.KeyItem.TwinkleParkTicket],
        StartingArea.Jungle: [],
        StartingArea.EggCarrier: []
    },
    Character.Gamma: {
        StartingArea.StationSquare: [ItemName.KeyItem.HotelKeys],
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.Dynamite, ItemName.KeyItem.WindStone],
        StartingArea.Jungle: [],
    },
    Character.Big: {
        StartingArea.Hotel: [],
        StartingArea.StationSquare: [],
        StartingArea.EggCarrier: []
    }
}

starting_area_no_items = {
    Character.Sonic: {
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [],
        StartingArea.EggCarrier: []
    },
    Character.Tails: {
        StartingArea.Casino: [],
        StartingArea.MysticRuins: [],
        StartingArea.EggCarrier: []
    },
    Character.Knuckles: {
        StartingArea.StationSquare: [],
        StartingArea.Casino: [],
    },
    Character.Amy: {
        StartingArea.Jungle: [],
        StartingArea.EggCarrier: []
    },
    Character.Gamma: {
        StartingArea.Hotel: [],
        StartingArea.Jungle: [],
    },
    Character.Big: {
        StartingArea.Hotel: [],
        StartingArea.StationSquare: [],
        StartingArea.EggCarrier: []
    }
}
