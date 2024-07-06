from worlds.sadx.test import SonicAdventureDXWorldTest


class TestLevelAccess(SonicAdventureDXWorldTest):
    def test_tails_levels(self) -> None:
        self.collect_all_but(["Story unlock (Tails)"])
        self.assertFalse(self.can_reach_location("Windy Valley (Tails - Mission C)"))

        self.collect_by_name("Story unlock (Tails)")
        self.assertTrue(self.can_reach_location("Windy Valley (Tails - Mission C)"))

    def test_Knuckles_upgrades(self) -> None:
        self.collect_all_but(["Story unlock (Knuckles)", "Shovel claw (Knuckles)"])
        self.assertFalse(self.can_reach_location("Shovel claw upgrade (Knuckles)"))
        self.assertFalse(self.can_reach_location("Fighting gloves upgrade (Knuckles)"))

        self.collect_by_name("Story unlock (Knuckles)")
        self.assertTrue(self.can_reach_location("Shovel claw upgrade (Knuckles)"))
        self.assertFalse(self.can_reach_location("Fighting gloves upgrade (Knuckles)"))

        self.collect_by_name("Shovel claw (Knuckles)")
        self.assertTrue(self.can_reach_location("Fighting gloves upgrade (Knuckles)"))
