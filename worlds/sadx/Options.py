from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, DefaultOnToggle, Toggle, DeathLink
from Options import PerGameCommonOptions


class FieldEmblemsChecks(DefaultOnToggle):
    """Determines whether collecting field emblems grants checks
    (12 Locations)"""
    display_name = "Field Emblems Checks"


class RingLoss(Choice):
    """
    How taking damage is handled
    Classic: You lose all of your rings when hit
    Modern: You lose 20 rings when hit
    One Hit K.O.: You die immediately when hit
    """
    display_name = "Ring Loss"
    option_classic = 0
    option_modern = 1
    option_one_hit_k_o = 2
    default = 0


class RingLink(Toggle):
    """
    Whether your in-level ring gain/loss is linked to other players
    """
    display_name = "Ring Link"


class LifeSanity(Toggle):
    """Determines whether collecting life capsules grants checks
    (102 Locations)"""
    default = 0
    display_name = "Life Sanity"


class PinballLifeCapsules(Toggle):
    """Determines whether casinopolis life capsules grant checks
    (2 Locations)"""
    default = 0
    display_name = "Include Casinopolis Life Capsules"


class SubLevelChecks(DefaultOnToggle):
    """Determines whether beating a sublevel grants checks
    (4 Locations)"""
    display_name = "Sub-Level Checks"


class EmblemPercentage(Range):
    """What percentage of the available emblems do you need to unlock the final story"""
    display_name = "Emblem Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 80


class BaseMissionChoice(Choice):
    """Base class for mission options"""
    option_none = 0
    option_c = 1
    option_c_b = 2
    option_c_b_a = 3
    default = 1


class RandomizedSonicUpgrades(DefaultOnToggle):
    """Determines whether Sonic's upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Sonic's Upgrades"


class RandomizedTailsUpgrades(DefaultOnToggle):
    """Determines whether Tails' upgrades are randomized and sent to the item pool
    If you turn this off, Tails will never get the Rhythm Badge"""
    display_name = "Randomize Tails' Upgrades"


class RandomizedKnucklesUpgrades(DefaultOnToggle):
    """Determines whether Knuckles' upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Knuckles' Upgrades"


class RandomizedAmyUpgrades(DefaultOnToggle):
    """Determines whether Amy's upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Amy's Upgrades"


class RandomizedBigUpgrades(DefaultOnToggle):
    """Determines whether Big's upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Big's Upgrades"


class RandomizedGammaUpgrades(DefaultOnToggle):
    """Determines whether Gamma's upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Gamma's Upgrades"


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
    death_link: DeathLink
    ring_link: RingLink
    ring_loss: RingLoss
    life_sanity: LifeSanity
    pinball_life_capsules: PinballLifeCapsules
    sub_level_checks: SubLevelChecks
    randomized_sonic_upgrades: RandomizedSonicUpgrades
    randomized_tails_upgrades: RandomizedTailsUpgrades
    randomized_knuckles_upgrades: RandomizedKnucklesUpgrades
    randomized_amy_upgrades: RandomizedAmyUpgrades
    randomized_big_upgrades: RandomizedBigUpgrades
    randomized_gamma_upgrades: RandomizedGammaUpgrades
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
        RingLoss,
        FieldEmblemsChecks,
        LifeSanity,
        SubLevelChecks,
        RandomizedSonicUpgrades,
        RandomizedTailsUpgrades,
        RandomizedKnucklesUpgrades,
        RandomizedAmyUpgrades,
        RandomizedBigUpgrades,
        RandomizedGammaUpgrades,
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
