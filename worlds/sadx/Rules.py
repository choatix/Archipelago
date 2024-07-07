from worlds.generic.Rules import add_rule
from .Locations import get_location_by_name
from .Names import ItemName
from .Names import LocationName


def create_rules(self):
    for ap_location in self.multiworld.get_locations(self.player):
        loc = get_location_by_name(ap_location.name)
        if loc is not None and "needs" in loc and len(loc["needs"]) > 0:
            location = self.multiworld.get_location(loc["name"], self.player)
            for itemNeeded in loc["needs"]:
                add_rule(location, lambda state, item=itemNeeded: state.has(item, self.player))

    if not self.options.story_unlock_randomized:
        if self.options.tails_missions > 0:
            self.multiworld.get_location(LocationName.Story.Meet.Tails, self.player).place_locked_item(
                self.create_item(ItemName.Tails.StoryUnlock))
        if self.options.knuckles_missions > 0:
            self.multiworld.get_location(LocationName.Story.Meet.Knuckles, self.player).place_locked_item(
                self.create_item(ItemName.Knuckles.StoryUnlock))
        if self.options.amy_missions > 0:
            self.multiworld.get_location(LocationName.Story.Meet.Amy, self.player).place_locked_item(
                self.create_item(ItemName.Amy.StoryUnlock))
        if self.options.gamma_missions > 0:
            self.multiworld.get_location(LocationName.Story.Meet.Gamma, self.player).place_locked_item(
                self.create_item(ItemName.Gamma.StoryUnlock))
        if self.options.big_missions > 0:
            self.multiworld.get_location(LocationName.Story.Meet.Big, self.player).place_locked_item(
                self.create_item(ItemName.Big.StoryUnlock))

    self.multiworld.get_location(LocationName.Story.Fight.PerfectChaos, self.player).place_locked_item(
        self.create_item(ItemName.Progression.ChaosPeace))

    emblem_count = int(round(self.get_emblem_count() * self.options.emblems_percentage / 100))

    add_rule(self.multiworld.get_location(LocationName.Story.Fight.PerfectChaos, self.player),
             lambda state: state.has(ItemName.Progression.Emblem, self.player, max(emblem_count, 1)))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)
