from worlds.sadx.Names import ItemName
from worlds.sadx.Names import LocationName
from worlds.sadx.test import SonicAdventureDXWorldTest


class TestLevelAccess(SonicAdventureDXWorldTest):
    def test_tails_levels(self) -> None:
        self.collect_all_but([ItemName.Tails.StoryUnlock])
        self.assertFalse(self.can_reach_location(LocationName.Tails.WindyValley.C))

        self.collect_by_name(ItemName.Tails.StoryUnlock)
        self.assertTrue(self.can_reach_location(LocationName.Tails.WindyValley.C))

    def test_Knuckles_upgrades(self) -> None:
        self.collect_all_but([ItemName.Knuckles.StoryUnlock, ItemName.Knuckles.ShovelClaw])
        self.assertFalse(self.can_reach_location(LocationName.Knuckles.Upgrades.ShovelClaw))
        self.assertFalse(self.can_reach_location(LocationName.Knuckles.Upgrades.FightingGloves))

        self.collect_by_name(ItemName.Knuckles.StoryUnlock)
        self.assertTrue(self.can_reach_location(LocationName.Knuckles.Upgrades.ShovelClaw))
        self.assertFalse(self.can_reach_location(LocationName.Knuckles.Upgrades.FightingGloves))

        self.collect_by_name(ItemName.Knuckles.ShovelClaw)
        self.assertTrue(self.can_reach_location(LocationName.Knuckles.Upgrades.FightingGloves))
