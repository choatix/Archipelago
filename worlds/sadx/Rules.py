from worlds.generic.Rules import add_rule
from worlds.sadx.Items import get_item_name


def create_rules(self, location_table):
    multiworld = self.multiworld
    player = self.player
    options = self.options

    for loc in location_table:
        if loc["needItem"] and loc["needItem"] >= 0:
            add_rule(multiworld.get_location(loc["name"], player), lambda state: state.has(get_item_name(loc["id"]), player))
