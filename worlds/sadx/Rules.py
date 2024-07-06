from worlds.generic.Rules import add_rule
from worlds.sadx.Items import get_item_name


def create_rules(self, location_table):
    for loc in location_table:
        if "needItems" in loc and len(loc["needItems"]) > 0:
            location = self.multiworld.get_location(loc["name"], self.player)
            for itemNeeded in loc["needItems"]:
                item_name = get_item_name(itemNeeded)
                add_rule(location, lambda state: state.has(item_name, self.player))

    self.multiworld.get_location("Perfect Chaos Fight", self.player).place_locked_item(
        self.create_item("Chaos' Peace"))
    add_rule(self.multiworld.get_location("Perfect Chaos Fight", self.player),
             lambda state: state.has("Emblem", self.player, 32))
    self.multiworld.completion_condition[self.player] = lambda state: state.has("Chaos' Peace", self.player)
