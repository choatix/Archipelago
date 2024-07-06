from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle


class StoryRandomized(Toggle):
    display_name = "Story unlocks are randomized"
    default = True


@dataclass
class SonicAdventureDXOptions(PerGameCommonOptions):
    story_unlock_randomized: StoryRandomized
