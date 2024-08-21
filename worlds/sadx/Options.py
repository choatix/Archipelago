from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, DefaultOnToggle, Toggle, DeathLink, OptionSet
from Options import PerGameCommonOptions


class Goal(Choice):
    """
    Determines the goal of the seed
    Emblems (0): You have to collect a certain number of emblems to unlock the Perfect Chaos Fight.
    Chaos Emerald Hunt (1): You have to collect all 7 Chaos Emeralds to unlock the Perfect Chaos Fight.
        There won't be any emblems in the item pool, only filler items and traps depending on your options
    Emblems and Chaos Emerald Hunt (2): You have to collect both emblems and the emeralds to fight Perfect Chaos.

    Keep in mind select emerald hunt will require enough checks to add the 7 emeralds to the pool,
        some options will fail to generate a seed if there are not enough checks to add the emeralds.
    """
    display_name = "Goal"
    option_emblems = 0
    option_emerald_hunt = 1
    option_emblems_and_emerald_hunt = 2
    default = 0


class LogicLevel(Choice):
    """
    What kind of logic the randomizer will use
    Casual Logic (0): Very forgiving, ideal if you are not used to this game or its location checks.
    Normal Logic (1): Less forgiving logic, some checks require to do spindash jumps or dying to get the check.
    Hard Logic (2): The most unforgiving logic, some checks require to do precise jumps or glitches.
    """
    display_name = "Logic Level"
    option_casual_logic = 0
    option_normal_logic = 1
    option_hard_logic = 2
    default = 0


class EmblemPercentage(Range):
    """What percentage of the available emblems do you need to unlock the final story"""
    display_name = "Emblem Requirement Percentage"
    range_start = 1
    range_end = 100
    default = 80


class RandomStartingLocation(DefaultOnToggle):
    """Randomize starting location, if false, you will start at Station Square"""
    display_name = "Random Starting location"


class RandomStartingLocationPerCharacter(DefaultOnToggle):
    """If Randomize starting location is enabled, each character will start in a random location"""
    display_name = "Random Starting location per character"


class GuaranteedLevel(Toggle):
    """Ensures access to a level from the start, even if it means giving you an item"""
    display_name = "Guaranteed Level Access"


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


class PlayableSonic(DefaultOnToggle):
    """Determines whether Sonic is playable"""
    display_name = "Playable Sonic"


class PlayableTails(DefaultOnToggle):
    """Determines whether Tails is playable"""
    display_name = "Playable Tails"


class PlayableKnuckles(DefaultOnToggle):
    """Determines whether Knuckles is playable"""
    display_name = "Playable Knuckles"


class PlayableAmy(DefaultOnToggle):
    """Determines whether Amy is playable"""
    display_name = "Playable Amy"


class PlayableGamma(DefaultOnToggle):
    """Determines whether Gamma is playable"""
    display_name = "Playable Gamma"


class PlayableBig(DefaultOnToggle):
    """Determines whether Big is playable"""
    display_name = "Playable Big"


class BaseActionStageMissionChoice(Choice):
    """
        For missions, the options go from 3 to 0
        3 means Missions A, B and C
        2 means Missions B and C
        1 means Missions C
        0 means no missions at all (You can still play the character if they are enabled)
    """
    option_none = 0
    option_c = 1
    option_c_b = 2
    option_c_b_a = 3
    default = 1


class SonicActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Sonic."""
    display_name = "Sonic's Action Stage Missions"


class TailsActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Tails."""
    display_name = "Tail's Action Stage Missions"


class KnucklesActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Knuckles."""
    display_name = "Knuckles's Action Stage Missions"


class AmyActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Amy."""
    display_name = "Amy's Action Stage Missions"


class GammaActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Gamma."""
    display_name = "Gamma's Action Stage Missions"


class BigActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Big."""
    display_name = "Big's Action Stage Missions"


class RandomizedSonicUpgrades(DefaultOnToggle):
    """Determines whether Sonic's upgrades are randomized and sent to the item pool"""
    display_name = "Randomize Sonic's Upgrades"


class RandomizedTailsUpgrades(DefaultOnToggle):
    """Determines whether Tails' upgrades are randomized and sent to the item pool"""
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


class FieldEmblemsChecks(DefaultOnToggle):
    """Determines whether collecting field emblems grants checks
    (12 Locations)"""
    display_name = "Field Emblems Checks"


class MissionChecks(Toggle):
    """Determines whether completing missions grants checks (60 Locations)"""
    display_name = "Enable Mission Checks"


class MissionBlackList(OptionSet):
    """Determines what missions are blacklisted, the default are:
    Mission 49 (Flags in the Kart section of Twinkle Park )
    Mission 53 (Triple Jump in the Snowboard section of Ice Cap)
    Mission 54 (Flags in the Snowboard section of Ice Cap)
    Mission 58 (Flags in the rolling bounce section of Lost World)
    """
    display_name = "Mission Blacklist"
    default = {49, 53, 54, 58}
    valid_keys = [str(i) for i in range(1, 61)]


class SubLevelChecks(DefaultOnToggle):
    """Determines whether beating the default sublevel mission  grants checks (4 Locations)
    Current sublevels are: Twinkle Circuit, Sand Hill and Sky Chase Act 1 and 2"""
    display_name = "Sub-Level Checks"


class SubLevelChecksHard(Toggle):
    """
    Determines whether beating the harder (points based) sublevel mission grants checks (4 Locations)
    Only works if sublevel checks are enabled
    """
    display_name = "Sub-Level Checks"


class LifeSanity(Toggle):
    """Determines whether collecting life capsules grants checks
    (102 Locations)"""
    display_name = "Life Sanity"


class PinballLifeCapsules(Toggle):
    """Determines whether pinball's life capsules grant checks
    (2 Locations)"""
    display_name = "Include pinball's Life Capsules"


class SonicLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Sonic's life capsules are part of the randomizer"""
    display_name = "Sonic's Life Sanity"


class TailsLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Tails' life capsules are part of the randomizer"""
    display_name = "Tails' Life Sanity"


class KnucklesLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Knuckles' life capsules are part of the randomizer"""
    display_name = "Knuckles' Life Sanity"


class AmyLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Amy's life capsules are part of the randomizer"""
    display_name = "Amy's Life Sanity"


class BigLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Big's life capsules are part of the randomizer"""
    display_name = "Big's Life Sanity"


class GammaLifeSanity(DefaultOnToggle):
    """If life-sanity is on, determines whether Gamma's life capsules are part of the randomizer"""
    display_name = "Gamma's Life Sanity"


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required emblems in the item pool with random junk items
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 50


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    The available options are 0 (off), 1 (low), 2 (medium) and 4 (high)
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which freeze the player in place
    """
    display_name = "Ice Trap Weight"


class SpringTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which spawns a spring that sends the player flying to the opposite direction
    """
    display_name = "Spring Trap Weight"


class PoliceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which spawns a lot of Cop Speeder enemies
    """
    display_name = "Police Trap Weight"


class BuyonTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which spawns a lot of Buyon enemies
    """
    display_name = "Buyon Trap Weight"


@dataclass
class SonicAdventureDXOptions(PerGameCommonOptions):
    goal: Goal
    logic_level: LogicLevel
    emblems_percentage: EmblemPercentage
    random_starting_location: RandomStartingLocation
    random_starting_location_per_character: RandomStartingLocationPerCharacter
    guaranteed_level: GuaranteedLevel
    death_link: DeathLink
    ring_link: RingLink
    hard_ring_link: HardRingLink
    ring_loss: RingLoss

    playable_sonic: PlayableSonic
    playable_tails: PlayableTails
    playable_knuckles: PlayableKnuckles
    playable_amy: PlayableAmy
    playable_gamma: PlayableGamma
    playable_big: PlayableBig

    sonic_action_stage_missions: SonicActionStageMissions
    tails_action_stage_missions: TailsActionStageMissions
    knuckles_action_stage_missions: KnucklesActionStageMissions
    amy_action_stage_missions: AmyActionStageMissions
    gamma_action_stage_missions: GammaActionStageMissions
    big_action_stage_missions: BigActionStageMissions

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
    mission_mode_checks: MissionChecks
    mission_blacklist: MissionBlackList
    sub_level_checks: SubLevelChecks
    sub_level_checks_hard: SubLevelChecksHard
    life_sanity: LifeSanity
    pinball_life_capsules: PinballLifeCapsules
    sonic_life_sanity: SonicLifeSanity
    tails_life_sanity: TailsLifeSanity
    knuckles_life_sanity: KnucklesLifeSanity
    amy_life_sanity: AmyLifeSanity
    big_life_sanity: BigLifeSanity
    gamma_life_sanity: GammaLifeSanity

    junk_fill_percentage: JunkFillPercentage
    trap_fill_percentage: TrapFillPercentage
    ice_trap_weight: IceTrapWeight
    spring_trap_weight: SpringTrapWeight
    police_trap_weight: PoliceTrapWeight
    buyon_trap_weight: BuyonTrapWeight


sadx_option_groups = [
    OptionGroup("General Options", [
        Goal,
        LogicLevel,
        EmblemPercentage,
        RandomStartingLocation,
        RandomStartingLocationPerCharacter,
        GuaranteedLevel,
        RingLink,
        HardRingLink,
        RingLoss,
    ]),
    OptionGroup("Characters Options", [
        PlayableSonic,
        PlayableTails,
        PlayableKnuckles,
        PlayableAmy,
        PlayableGamma,
        PlayableBig,
    ]),
    OptionGroup("Stage Options", [
        SonicActionStageMissions,
        TailsActionStageMissions,
        KnucklesActionStageMissions,
        AmyActionStageMissions,
        GammaActionStageMissions,
        BigActionStageMissions
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
        MissionChecks,
        MissionBlackList,
        SubLevelChecks,
        SubLevelChecksHard,
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
        TrapFillPercentage,
        IceTrapWeight,
        SpringTrapWeight,
        PoliceTrapWeight,
        BuyonTrapWeight
    ]),

]
