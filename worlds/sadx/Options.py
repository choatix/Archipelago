from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, DefaultOnToggle, Toggle, DeathLink
from Options import PerGameCommonOptions


class RandomStartingLocation(Choice):
    """
    Select starting Location
    Random location: You'll start at a random location, and you could get an item to ensure access to a level.
    Random location no items: Same as Random, but locations that need items to access a level them are excluded.
    Station Square: You'll start at Station Square, and you could get an item to ensure access to a level.
    Station Square no items: Same as Station Square, but you won't get an item.
    """
    display_name = "Ring Loss"
    option_random_location = 0
    option_random_location_no_items = 1
    option_station_square = 2
    option_station_square_no_items = 3
    default = 0


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


class HardRingLink(Toggle):
    """
    If Ring Link is enabled, sends and receives rings in more situations.
    Particularly it will subtract rings when finishing a level and during the Perfect Chaos fight.
    """
    display_name = "Hard Ring Link"


class LifeSanity(Toggle):
    """Determines whether collecting life capsules grants checks
    (102 Locations)"""
    display_name = "Life Sanity"


class SonicLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Sonic's life capsules are part of the randomizer"""
    display_name = "Randomize Sonic's Upgrades"


class TailsLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Tails' life capsules are part of the randomizer"""
    display_name = "Randomize Tails' Upgrades"


class KnucklesLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Knuckles' life capsules are part of the randomizer"""
    display_name = "Randomize Knuckles' Upgrades"


class AmyLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Amy's life capsules are part of the randomizer"""
    display_name = "Randomize Amy's Upgrades"


class BigLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Big's life capsules are part of the randomizer"""
    display_name = "Randomize Big's Upgrades"


class GammaLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Gamma's life capsules are part of the randomizer"""
    display_name = "Randomize Gamma's Upgrades"


class PinballLifeCapsules(Toggle):
    """Determines whether casinopolis life capsules grant checks
    (2 Locations)"""
    display_name = "Include Casinopolis Life Capsules"


class SubLevelChecks(DefaultOnToggle):
    """Determines whether beating a sublevel grants checks
    (4 Locations)"""
    display_name = "Sub-Level Checks"


class BossChecks(DefaultOnToggle):
    """Determines whether beating a boss grants a check
    (15 Locations)"""
    display_name = "Boss Checks"


class UnifyChaos4(DefaultOnToggle):
    """Determines whether the Chaos 4 fight counts as a single location or three (Sonic, Tails and Knuckles)"""
    display_name = "Unify Chaos 4"


class UnifyChaos6(Toggle):
    """Determines whether the Chaos 6 fight counts as a single location or three (Sonic, Big and Knuckles)"""
    display_name = "Unify Chaos 6"


class UnifyEggHornet(Toggle):
    """Determines whether the Egg Hornet fight counts as a single location or two (Sonic, Tails)"""
    display_name = "Unify Egg Hornet"


class EmblemPercentage(Range):
    """What percentage of the available emblems do you need to unlock the final story"""
    display_name = "Emblem Requirement Percentage"
    range_start = 1
    range_end = 100
    default = 80


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required emblems in the item pool with random junk items
    """
    display_name = "Junk Fill Percentage"
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
    emblems_percentage: EmblemPercentage
    random_starting_location: RandomStartingLocation
    death_link: DeathLink
    ring_link: RingLink
    hard_ring_link: HardRingLink
    ring_loss: RingLoss

    sonic_missions: SonicMissions
    tails_missions: TailsMissions
    knuckles_missions: KnucklesMissions
    amy_missions: AmyMissions
    gamma_missions: GammaMissions
    big_missions: BigMissions

    randomized_sonic_upgrades: RandomizedSonicUpgrades
    randomized_tails_upgrades: RandomizedTailsUpgrades
    randomized_knuckles_upgrades: RandomizedKnucklesUpgrades
    randomized_amy_upgrades: RandomizedAmyUpgrades
    randomized_big_upgrades: RandomizedBigUpgrades
    randomized_gamma_upgrades: RandomizedGammaUpgrades

    boss_checks: BossChecks
    unify_chaos4: UnifyChaos4
    unify_chaos6: UnifyChaos6
    unify_egg_hornet: UnifyEggHornet

    field_emblems_checks: FieldEmblemsChecks
    sub_level_checks: SubLevelChecks
    life_sanity: LifeSanity
    pinball_life_capsules: PinballLifeCapsules
    sonic_life_sanity: SonicLifeSanity
    tails_life_sanity: TailsLifeSanity
    knuckles_life_sanity: KnucklesLifeSanity
    amy_life_sanity: AmyLifeSanity
    big_life_sanity: BigLifeSanity
    gamma_life_sanity: GammaLifeSanity

    junk_fill_percentage: JunkFillPercentage


sadx_option_groups = [
    OptionGroup("General Options", [
        EmblemPercentage,
        RandomStartingLocation,
        RingLink,
        HardRingLink,
        RingLoss,
    ]),
    OptionGroup("Stage Options", [
        SonicMissions,
        TailsMissions,
        KnucklesMissions,
        AmyMissions,
        GammaMissions,
        BigMissions
    ]),
    OptionGroup("Upgrade Options", [
        RandomizedSonicUpgrades,
        RandomizedTailsUpgrades,
        RandomizedKnucklesUpgrades,
        RandomizedAmyUpgrades,
        RandomizedBigUpgrades,
        RandomizedGammaUpgrades,
    ]),
    OptionGroup("Bosses Options", [
        BossChecks,
        UnifyChaos4,
        UnifyChaos6,
        UnifyEggHornet,
    ]),
    OptionGroup("Extra locations", [
        FieldEmblemsChecks,
        SubLevelChecks,
        LifeSanity,
        PinballLifeCapsules,
        SonicLifeSanity,
        TailsLifeSanity,
        KnucklesLifeSanity,
        AmyLifeSanity,
        BigLifeSanity,
        GammaLifeSanity,
    ]),
    OptionGroup("Junk Options", [
        JunkFillPercentage,
    ]),

]
