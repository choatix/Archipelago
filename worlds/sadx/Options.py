from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, DefaultOnToggle
from Options import PerGameCommonOptions
from worlds.ladx.Options import DefaultOffToggle


class FieldEmblemsChecks(DefaultOnToggle):
    """Determines whether collecting field emblems grants checks
    (12 Locations)"""
    display_name = "Field Emblems Checks"


class LifeSanity(DefaultOffToggle):
    """Determines whether collecting life capsules grants checks
    (100 Locations)"""
    display_name = "Life Capsule Checks"


class SubLevelChecks(DefaultOnToggle):
    """Determines whether beating a sublevel grants checks
    (4 Locations)"""
    display_name = "Sub-Level Checks"


class RandomizeUpgrades(DefaultOnToggle):
    """Determines whether the upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Upgrades"


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


class SonicMissions(BaseMissionChoice):
    """Choose what missions will be a location check for Sonic."""
    display_name = "Sonic's Missions"


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
    field_emblems_checks: FieldEmblemsChecks
    life_sanity: LifeSanity
    sub_level_checks: SubLevelChecks
    randomized_upgrades: RandomizeUpgrades
    sonic_missions: SonicMissions
    tails_missions: TailsMissions
    knuckles_missions: KnucklesMissions
    amy_missions: AmyMissions
    gamma_missions: GammaMissions
    big_missions: BigMissions
    emblems_percentage: EmblemPercentage


sadx_option_groups = [
    OptionGroup("Main Options", [
        EmblemPercentage,
        FieldEmblemsChecks,
        LifeSanity,
        SubLevelChecks,
        RandomizeUpgrades,
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
