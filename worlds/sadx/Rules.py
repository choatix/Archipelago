from worlds.generic.Rules import add_rule
from worlds.sadx.Items import get_item_name
from .Names import ItemName
from .Names import LocationName


def create_rules(self, location_table):
    for loc in location_table:
        if "needItems" in loc and len(loc["needItems"]) > 0:
            location = self.multiworld.get_location(loc["name"], self.player)
            for itemNeeded in loc["needItems"]:
                item_name = get_item_name(itemNeeded)
                add_rule(location, lambda state, item=item_name: state.has(item, self.player))

    self.multiworld.get_location(LocationName.Story.Fight.PerfectChaos, self.player).place_locked_item(
        self.create_item(ItemName.Progression.ChaosPeace))

    # TODO: Calculate the emblem requirement as a percentage of emblems (as an option
    add_rule(self.multiworld.get_location(LocationName.Story.Fight.PerfectChaos, self.player),
             lambda state: state.has(ItemName.Progression.Emblem, self.player, 32))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)
