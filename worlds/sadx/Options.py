from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, DefaultOnToggle
from Options import PerGameCommonOptions, Toggle


class StoryUnlockRandomized(DefaultOnToggle):
    """Are the story unlock randomized?"""
    display_name = "Story unlocks are randomized"


class EmblemPercentage(Range):
    """What percentage of the available emblems do you need to unlock the final story"""
    display_name = "Emblem Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 50


class BaseMissionChoice(Choice):
    """Base class for mission options"""
    option_none = 0
    option_c = 1
    option_c_b = 2
    option_c_b_a = 3
    default = 1


class SonicMissions(Choice):
    """Choose what missions will be a location check for Sonic. You need at least the Sonic C's mission activated"""
    display_name = "Sonic's Missions"
    option_c = 1
    option_c_b = 2
    option_c_b_a = 3
    default = 1


class TailsMissions(BaseMissionChoice):
    """Choose what missions will be a location check for Tails."""
    display_name = "Tail's Missions"


class KnucklesMissions(BaseMissionChoice):
    """Choose what missions will be a location check for Knuckles."""
    display_name = "Knuckles's Missions"


class AmyMissions(BaseMissionChoice):
    """Choose what missions will be a location check for Amy."""
    display_name = "Amy's Missions"


class GammaMissions(BaseMissionChoice):
    """Choose what missions will be a location check for Gamma."""
    display_name = "Gamma's Missions"


class BigMissions(BaseMissionChoice):
    """Choose what missions will be a location check for Big."""
    display_name = "Big's Missions"


@dataclass
class SonicAdventureDXOptions(PerGameCommonOptions):
    story_unlock_randomized: StoryUnlockRandomized
    sonic_missions: SonicMissions
    tails_missions: TailsMissions
    knuckles_missions: KnucklesMissions
    amy_missions: AmyMissions
    gamma_missions: GammaMissions
    big_missions: BigMissions
    emblems_percentage: EmblemPercentage


sadx_option_groups = [
    OptionGroup("Story Options", [
        StoryUnlockRandomized,
        EmblemPercentage
    ]),
    OptionGroup("Missions Options", [
        SonicMissions,
        TailsMissions,
        KnucklesMissions,
        AmyMissions,
        GammaMissions,
        BigMissions
    ])

]
