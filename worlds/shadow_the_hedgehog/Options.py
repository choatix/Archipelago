from dataclasses import dataclass
from Options import PerGameCommonOptions, Choice, DefaultOnToggle, Toggle, Range, OptionSet, OptionDict, OptionGroup, \
    NamedRange
from . import Names


class GoalChaosEmeralds(DefaultOnToggle):
    """
        Determines if chaos emeralds are required for completion.
        If enabled, you require the 7 chaos emeralds to unlock your goal.
    """
    display_name = "Goal: Chaos Emeralds"

class GoalMissions(Range):
    """
        Determines what percentage of general missions are required for completion, rounded up.
    """
    display_name = "Goal: Missions"
    range_start = 0
    range_end = 100
    default = 75

class GoalDarkMissions(Range):
    """
        Determines what percentage of dark missions are required for completion, rounded up.
    """
    display_name = "Goal: Dark Missions"
    range_start = 0
    range_end = 100
    default = 0

class GoalHeroMissions(Range):
    """
        Determines what percentage of hero missions are required for completion, rounded up.
    """
    display_name = "Goal: Hero Missions"
    range_start = 0
    range_end = 100
    default = 0

class GoalObjectiveMissions(Range):
    """
        Determines what percentage of objective missions are required for completion, rounded up.
    """
    display_name = "Goal: Objective Missions"
    range_start = 0
    range_end = 100
    default = 0


class GoalBosses(Range):
    """
        Determines what percentage of bosses are required for completion, rounded up.
    """
    display_name = "Goal: Bosses"
    range_start = 0
    range_end = 100
    default = 0

class GoalFinalBosses(Range):
    """
        Determines what percentage of final boss missions are required for completion, rounded up.
    """
    display_name = "Goal: Final Bosses"
    range_start = 0
    range_end = 100
    default = 0

class GoalFinalMissions(Range):
    """
        Determines what percentage of final missions are required for completion, rounded up.
    """
    display_name = "Goal: Final Missions"
    range_start = 0
    range_end = 100
    default = 0

class ObjectiveSanity(DefaultOnToggle):
    """
        Determines if objective based checks are enabled.
        Objectivesanity checks are all stage objectives for dark/hero missions.
        Please read the readme for more information.
    """
    display_name = "Objective Sanity"

class ObjectiveSanitySystem(Choice):
    """

    Option to determine what triggers objective sanity checks.
    Count Up, the original system, requires getting/maintaining a particular count.
    Individual, the new system, where each individual activation is a separate check, not requiring the count
        Due to technical limitations:
         - Currently disabled for Final Haunt Shields
         - GUN Soldiers work on despawn rather than defeat
    Both, checks for both in the system, if available

    """
    display_name = "Objective Sanity System"
    option_count_up = 0
    option_individual = 1
    option_both = 2
    default = option_individual

class ObjectiveSanityBehaviour(Choice):
    """
        When objective-sanity is enabled, how to operate clearing of stages
        Default: You require desired item count to finish stage, press Z to finish, then complete a goal
        Manual Clear: You require desired item count to finish stage, pressing Z when completable, sets count to 0, must be beaten normally
            (Must handle early accessible / update to current value detected in the stage)
        Base Clear: You do not need to collect items to progress stages, but as objectivesanity is on,
            required to still press Z to avoid inability to get checks.
    """

    display_name = "Objective Sanity Behaviour"
    option_default = 0
    option_manual_clear = 1
    option_base_clear = 2
    default = option_default

class ObjectivePercentage(Range):
    """Sets the objective percentage for each objective.
    When playing objective sanity count up, this removes the locations for anything after the percentage objective.
    Only affects locations, use available/completion for goal-related effects."""
    display_name = "Objective Percentage"
    range_start = 1
    range_end = 100
    default = 100

class EnemyObjectivePercentage(Range):
    """When playing Objective Sanity, determine the percentage of items required to finish stages for enemy objectives."""
    display_name = "Enemy Objective Percentage"
    range_start = 1
    range_end = 100
    default = 90

class ObjectiveCompletionPercentage(Range):
    """When playing Objective Sanity, determine the percentage of items required to finish stages.
    When playing non-objective, this is the amount required to complete the stage."""
    display_name = "Objective Completion Percentage"
    range_start = 1
    range_end = 100
    default = 100

class ObjectiveCompletionEnemyPercentage(Range):
    """
        When playing Enemy Objective Sanity, determine the percentage of items required to finish stages.
        This is specifically the enemy-based objectivesanity missions.
        For all enemies, refer to enemy sanity. These can be used in tandem.
    """
    display_name = "Objective Completion Enemy Percentage"
    range_start = 1
    range_end = 100
    default = 90


class ObjectiveItemPercentageAvailable(Range):
    """
        When playing Objective Sanity, determine the percentage of items required to finish stages added alongside
        your provided completion percentage.
    """
    display_name = "Objective Item Percentage"
    range_start = 0
    range_end = 900
    default = 0

class ObjectiveItemEnemyPercentageAvailable(Range):
    """When playing Objective Enemy Sanity, determine the percentage of items required to finish stages added alongside
        your provided completion percentage."""
    display_name = "Objective Item Enemy Percentage"
    range_start = 0
    range_end = 900
    default = 0

class EnemyObjectiveSanity(DefaultOnToggle):
    """Determines if enemy-based objective checks are enabled."""
    display_name = "Enemy Objective Sanity"

class Enemysanity(Toggle):
    """
        Determines whether standard enemy sanity is enabled.
        This can be used in tandem with enemy objective sanity.
    """
    display_name = "Enemy Sanity"


class BossEnemysanity(Toggle):
    """
        Determines whether boss enemy sanity is enabled.
        This can be used in tandem with enemy objective sanity.
    """
    display_name = "Boss Enemy Sanity"


class DifficultEnemysanity(Toggle):
    """
        Determines whether enemies marked as difficult are included as part of enemy sanity.
    """
    display_name = "Difficult Enemy Sanity"

class Keysanity(Toggle):
    """
        Determines whether key sanity is enabled.
        This enables checks as keys and does not add any items to the pool.
    """
    display_name = "Key Sanity"

class KeysRequiredForDoors(Range):
    """
        Determines how many keys are required to open doors. This works by providing fake keys to the player.
    """
    display_name = "Keys Required For Doors"
    range_start = 0
    range_end = 5
    default = 5

class KeyCollectionMethod(Choice):
    """
        Determines how keys can be collected.
        Local: Only the player collecting keys locally will collect keys for opening key doors.
            If keysanity is enabled, you will keep these keys when re-entering stages,
            but if disabled, you need to collect each time. Rare logic will require this.
        Arch: All keys must be obtained as archipelago items.
        Both: Arch items are included and local accessible keys also contribute to the key count.
    """
    display_name = "Key Collection Method"
    option_local = 0
    option_arch = 1
    option_both = 2
    default = option_local

class Checkpointsanity(DefaultOnToggle):
    """
        Determines whether checkpoint sanity is enabled.
        This only adds checks and does not add anything to the pool.
    """
    display_name = "Checkpoint Sanity"


class CheckpointShuffle(Choice):
    """
        Determines whether checkpoint shuffle is enabled.
        Off: Checkpoint behaviour acts as normal.
        Unlocks Only: All checkpoints are added as items into the multiworld,
            allowing you to jump to later in the stage when unlocking.
        Start And Unlock: Checkpoints spawns for stages are randomised to be other checkpoints.
            To access Checkpoint 0 when unlocked, for relevant stages,
            You must pause and press Y then restart the stage.
    """
    display_name = "Checkpoint Shuffle"
    option_off = 0
    option_unlocks_only = 1
    option_start_and_unlock = 2
    default = option_off

class CheckpointRules(OptionSet):
    """
        Specific settings for controlling which checkpoint items are included.
        Disable Goal Rings: Disables including the goal ring as a possible checkpoint / spawn point.
        Zero Start: If checkpoint zero cannot be backtracked to, always start at 0. Note, read readme for information on reaching if disabled.
        Minimal Checkpoints: Removes random checkpoints from the pool to prevent end-game bloat.
    """

    display_name = "Checkpoint Rules"
    valid_keys = Names.getValidCheckpointRules()
    default = ["Zero Start"]

class MinimalCheckpointPercentage(Range):
    """
            Percentage chance to include a checkpoint if Minimal Checkpoint rule is enabled.
    """
    display_name = "Minimal Checkpoint Percentage"
    default = 50
    range_start = 1
    range_end = 100

class CheckpointConvenience(DefaultOnToggle):
    """
        Determines whether checkpoint convenience is enabled, allowing warping back to a checkpoint
        On re-entering a stage if it has been enabled before.
        Requires Checkpoint sanity to function.
    """
    display_name = "Checkpoint Convenience"

class CharacterSanity(DefaultOnToggle):
    """
        Determines if character checks are enabled.
        The first time you meet a character, the cutscene will play and provide a check.
        Disabling is handling by overwriting the value and cutscene will never play.
    """
    display_name = "Character Sanity"

class WeaponsanityUnlock(Toggle):
    """
        Determines whether weapons are required to be obtained from the pool of items.
        This will change the logic of same stages.
        Can be used alongside Weapon Groups for more flexibility.
    """
    display_name = "Weapon Sanity Unlock"

class WeaponSanityMinAvailable(Range):
    """
        Minimum value for weapon copies to be in the item pool.
    """
    display_name = "Weapon Sanity Min Available"
    range_start = 1
    range_end = 5
    default = 1

class WeaponSanityMaxAvailable(Range):
    """
        Maximum value for weapon weapons to be in the item pool.
    """
    display_name = "Weapon Sanity Max Available"
    range_start = 1
    range_end = 5
    default = 1

class WeaponsanityHold(Choice):
    """Determines whether game contains checks for legally holding each weapon.
    If unlocked is chosen, you must unlock the weapon with unlock first.
    If on is chosen, you will still lose the item in this mode, but will get the check.
    """
    display_name = "Weapon Sanity Hold"
    option_off = 0  # No checks for holding weapons
    option_unlocked = 1  # Requires the item to be unlocked to get the check.
    option_on = 2  # Does not require the item to be unlocked to get the check.
    default = 0

class VehicleLogic(Toggle):
    """Determines if vehicle logic is active. Vehicles will not be avialable for use until found."""
    display_name = "Vehicle Logic"

class GaugeFiller(DefaultOnToggle):
    """Determines if gauge filler is included."""
    display_name = "Gauge Filler"

class RingFiller(DefaultOnToggle):
    """Determines if ring filler is included."""
    display_name = "Ring Filler"

class AmmoBoostFiller(DefaultOnToggle):
    """Determines if ammo boost filler is included."""
    display_name = "Ammo Boost Filler"

class EnemySanityPercentage(Range):
    """Determines the percentage of enemysanity checks in a stage to be included."""
    display_name = "Enemy Sanity Percentage"
    range_start = 0
    range_end = 100
    default = 50

class StartingStages(Range):
    """
        Determines the number of stages that start unlocked in Select mode.
    """
    display_name = "Starting Stages"
    range_start = 0
    range_end = 22
    default = 1

class SelectGates(Choice):
    """
        Determines distribution behaviour for select gates.
    """
    display_name = "Select Gates"
    option_off = 0
    option_early = 1
    option_medium = 2
    option_late = 3
    default = option_medium

class SelectGatesCount(Range):
    """
        Determines the number of select gates.
    """
    display_name = "Select Gates"
    range_start = 1
    range_end = 10
    default = 5

class GateUnlockRequirement(Choice):
    """
        Determines how gates are opened when using select gates.
        Items: Adds specific gate keys into the logic which open gates sequentially.
        Objective: Uses the objective items (e.g. Egg Balloon / Jungle Soldier)
        Chaos Emeralds: Each chaos emerald unlocks a gate. Forces gate count.
        Objective Available: Objective; but only uses stage items for levels previously available in gates.
    """
    display_name = "Gate Unlock Requirement"
    option_items = 0
    option_objective = 1
    option_chaos_emeralds = 2
    option_objective_available = 3
    default = option_objective_available

class GateDensity(Range):
    """
        Determines the density of objective items required for gates as per gate formula.
        Higher values will set the percentages higher to open gates.
    """
    display_name = "Gate Density"
    range_start = 0
    range_end = 100
    default = 0

class ForceObjectiveSanityChance(Range):
    """Determines the probability of a objective-sanity stage being force-added to Priority Locations"""
    display_name = "Force Objective Sanity Mission Chance"
    range_start = 0
    range_end = 100
    default = 25

class ForceObjectiveSanityMax(Range):
    """Determines the upper limit of total objectsanity items in priority locations."""
    display_name = "Force Objective Sanity Max"
    range_start = 0
    range_end = 60
    default = 10

class ForceObjectiveSanityMaxCounter(Range):
    """Determines the upper limit of stages to be forced into priority locations."""
    display_name = "Force Objective Sanity Max"
    range_start = 0
    range_end = 1000
    default = 1000

class ExcludedStages(OptionSet):
    """Stage names to exclude checks from."""
    display_name = "Excluded Stages"
    #default = {}
    valid_keys = [i for i in Names.getLevelNames() ]

class Itemsanity(Toggle):
    """
        Determines whether item box sanity is enabled.
    """
    display_name = "Item Sanity"

class ExceedingItemsFiller(Choice):
    """
        Determines whether game marks non-required items as progression or not.
        Off is only recommended for testing a yaml.
    """
    display_name = "Exceeding Items Filler"
    option_off = 0  # Never remove or convert exceeding items into filler. Only use to test yaml.
    option_minimise = 1  # Remove excess items to prevent failures.
    option_always = 2  # Always mark exceeding items as filler.
    option_chance = 3 # Sometimes mark exceeding items as filler.
    default = option_minimise

class ExceedingItemsFillerRandom(Range):
    """Determines chance of marking exceeding filler items as useful rather than progression"""
    display_name = "Exceeding Items Filler Random Chance"
    range_start = 0
    range_end = 100
    default = 25

class RingLink(Choice):
    """
    Whether your in-level ring gain/loss is linked to other players.
    Off disables the feature.
    On enables the feature excluding the special cases listed below.
    Unsafe enables ring link during Circus Park missions and during Devil Doom.

    """
    option_off = 0
    option_on = 1
    option_unsafe = 2

    display_name = "Ring Link"
    default = option_off

class AutoClearMissions(DefaultOnToggle):
    """
        Set automatic clears for missions once objective criteria is achieved. When playing story mode, ensure
        that the player has access to a new stage before auto-clearing to improve tracking behaviour.
        Auto clear is automatically disabled when playing on objective-less sanity.
    """
    display_name = "Auto Clear Missions"

class LevelProgression(Choice):
    """
        Which type of logic to use for progression through the game.
        Select will ignore story mode progression, and accessibility to stages will be given by items, based on gate options.
            See gates options for more information on gates.

        Story progression takes the story path and unlocks stages after clearing previous stages in story mode.
        Story mode stages will be available in select mode, and clearing in select mode
            will automatically follow the story path, sometimes leading to bosses blocking further stages.
            Use the /story command to see what stages are available in story and
            /story /s{stage} to set the story progression to where it needs to be.
    """
    display_name = "Level Progression"
    option_select = 0  # All stages will be unlocked through unlocks to Select Mode
    option_story = 1  # All stages will only be unlocked through story mode progression
    option_both = 2  # Stages can be unlocked through story mode progression or unlocked for Select Mode
    default = option_select

class SelectBosses(DefaultOnToggle):
    """
        Whether bosses can be unlocked via select mode.
        Note that mid-bosses require the ability to access the main stage
            in order to enter them but may be unlocked before they can be entered.
    """
    display_name = "Select Bosses"

class PercentOverrides(OptionDict):
    """
        Advanced YAML setting to provide keys to dictate percentage based overrides.
        Read the setup_en.yaml for more information.
    """
    display_name = "Percent Overrides"
    valid_keys = Names.getValidPercentOverrides()
    default = {}

class MusicShuffle(Toggle):
    """
        Toggle for shuffling the stage music upon entering a stage
    """
    display_name = "Music Shuffle"


class WeaponGroups(OptionSet):
    """
    Group together confirmed sets of weapon items to unlock them in given batches.

    - Stage Melee Weapons: Non-required Stage Melee Weapons
    - Environment Weapons: All Stage Melee Environment Weapons
    - Egg Pawn Weapons: Used by Egg Pawns
    - GUN Launcher Weapons: Launching GUN Weapons
    - Black Warrior Weapons: Held by standard Black Arms
    - Black Oak Weapons: Held by big Black Arm enemies
    - Worm Weapons:  Held by Black Arm Worm enemies
    - Gun Soldier Weapons: Held by GUN Soldiers
    - Gun Mech Weapons: Held by GUN Mechs
    - Laser Weapons: Laser-style weapons
    """
    display_name = "Weapon Groups"
    valid_keys = []
    default = ["Stage Melee Weapons"]


class LogicLevel(Choice):
    """
        Determines the logic level for play-through.
        Easy: Some requirements are dialled back to make for a smoother early experience.
        Normal: Standard logic.
        Hard: Skips expected of the player in order to make progress.
    """
    display_name = "Logic Level"
    option_easy = 0  # Logic adds in easier elements for completion
    option_normal = 1  # Standard logic
    option_hard = 2  # Requires skips to traverse regions.
    default = option_normal

class ChaosControlLogicLevel(Choice):
    """
        Determines the chaos control logic level for play-through.
        Note: This functionality may not work quite as intended yet with checkpoint shuffle.
        Off: Chaos Control is never required to make progress.
        Easy: Stages where the player will naturally have chaos control are included.
        Intermediate: Stages with workarounds that are not extremely complicated are included.
        Hard: Requires the player to work out building up and handling gauge.
    """
    display_name = "Chaos Control Logic Level"
    option_off = 0  # Disables requirements for chaos control logic
    option_easy = 1  # Enables chaos control as logic passes apart from those requiring intensive gauge management
    option_intermediate = 2 # Enabled some management of chaos control gauge
    option_hard = 3  # Requires intensive management of chaos control gauge to mark these areas
    default = option_off

class BossLogicLevel(Choice):
    """
        Determines the boss logic level for playthrough.
        Easy boss logic ensures the player has access to one of the weapons within the stage in order to beat it.
        All bosses can be beaten without any progression otherwise, apart from Iron Jungle Egg Breaker.
    """
    display_name = "Boss Logic Level"
    option_easy = 0  # Logic adds in easier elements for completion
    #option_normal = 1  # Standard logic
    option_hard = 2  # Requires skips to traverse regions.
    default = option_easy

class CraftLogicLevel(NamedRange):
    """
        Determines the craft logic level for playthrough - distinguishing a difference
        in logic for crafts in Iron Jungle, Lethal Highway and Air Fleet

        A divider for calculating amount of hits required to take down a craft.
        Option Shadow Rifle: Use lowest setting but explicitly require the Shadow Rifle
        Option Impossible: Logic does not take into consideration any multiplier
            The maximum hits (may) require infinite ammo
        Other:
            Apply reduction by that value to the total number of hits on the craft

    """
    display_name = "Craft Logic Level"
    option_shadow_rifle = 0
    default = 6
    range_start = 0
    range_end = 10
    special_range_names = {
        "shadow_rifle": 0,
        "impossible": 1,
        "hard": 3,
        "normal": 6,
        "easy": 8
    }

class StoryShuffle(Choice):
    """
    Determines method for shuffling story stages.
    Off will disable the story shuffle and will instead require vanilla order.
    Chaos mode will shuffle the story. For more information on chaos shuffle, please read the documentation.
    """
    display_name = "Story Shuffle"
    option_off = 0  # Story stages will be in vanilla order
    #option_basic = 1
    #option_shuffle = 2
    option_chaos = 3
    default = option_off

class IncludeLastStoryShuffle(Toggle):
    """
        Determines whether to include Last Way accessibility in the seed.

        In story mode:
        By enabling this, Devil Doom (the final fight) will be hidden in story mode and must be found
        in order to clear the game.
        Last Way goes to a random stage at the end, hence why Devil Doom MUST be shuffled in this way.

        In Select mode:
        Last Story will unlock early once the stage is unlocked via item or gate. Entering here plays as
        normal end game would,  and would lead to Devil Doom afterwards.

        Note, if you are in the Devil Doom stage without the required goal items unlocked, you will be unable to complete it,
        Shadow will run out of rings on a loop and the stage must be exited and returned to later.

    """
    display_name = "Include Last Story"


class SecretStoryProgression(Toggle):
    """
        When using UT, hide the progress of stages until the player has found them in the story mode.
    """
    display_name = "Secret Story Progression"

class StoryBossCount(Range):
    """
        How many copies of each standard boss to feature through the story chain.
    """
    display_name = "Story Boss Count"
    range_start = 0
    range_end = 3
    default = 1

class StartingLevelMethod(Choice):
    """
        Ensures clearable neutral stages are picked first for starting stages.
        None: Starting behaviour has no factors.
        Clear Stage: First stage non-objectivesanity mission can be cleared.
        Stage + Item: First stage, plus an item that progresses through that stage. Only picks one item.
    """
    display_name = "Starting Level Method"
    option_none = 0
    option_clear_stage = 1
    option_stage_and_item = 2
    default = option_none

class SingleEggDealer(Toggle):
    """
        Only include a single Egg Dealer of the available 3.
    """
    display_name = "Single Egg Dealer"

class SingleBlackDoom(Toggle):
    """
        Only include a single Black Doom of the available 3.
    """
    display_name = "Single Black Doom"

class SingleDiablon(Toggle):
    """
        Only include a single Sonic & Diablon of the available 3.
    """
    display_name = "Single Diablon"

class RifleComponents(Toggle):
    """
        Whether parts are required for the Shadow Rifle to be complete and available.
    """
    display_name = "Shadow Rfile Components"

class ObjectiveFrequency(Range):
    """
        Frequency of checks for objective checks, i.e. if set to 4, each 4 progress is 1 check.
        This will always include the final check as well as every 4.
    """
    display_name = "Objective Frequency"
    range_start = 1
    range_end = 10
    default = 1

class EnemyObjectiveFrequency(Range):
    """
        Frequency of checks for enemy objective checks as percentage.
    """
    display_name = "Enemy Objective Frequency"
    range_start = 1
    range_end = 10
    default = 1

class EnemyFrequency(Range):
    """
        Frequency of checks for enemy checks, i.e. if set to 4, each 4 progress is 1 check.
    """
    display_name = "Enemy Frequency"
    range_start = 1
    range_end = 10
    default = 1

class MinimumRank(Choice):
    """Minimum rank required to get the location clear check."""
    display_name = "Minimum Rank"
    option_a = "A"
    option_b = "B"
    option_c = "C"
    option_d = "D"
    option_e = "E"
    default = option_e

class StoryProgressionBalancing(Range):
    """
        Story progression balancing to determine sphering for story stages.
        Higher numbers choose routes leading to more stages available in one go.
        Lower numbers choose smaller story progression, but will stay lower progression for longer.
        Refer to the documentation for more information.
    """
    display_name = "Story Progression Balancing"
    range_start = 1
    range_end = 100
    default = 25 # Decide this value

class StoryProgressionBalancingPasses(Range):
    """
        Story progression balancing passes to make, using balancing value.
        Use 0 to disable story progression balancing.
        Each pass selects a route, reducing the counts required to progress through story missions.
        The lowest value from all passes will be used.
    """
    display_name = "Story Progression Balancing Passes"
    option_off = 0
    range_start = 0
    range_end = 5
    default = 1

class ShadowMod(Choice):
    """
        Shadow Mod intended to be used. In order to use a mod you accept that the game may not yet
        be fully supported and that bugs will occur.
        Only vanilla is officially supported.
        Only mods in the list have any testing or handling at all.
        Minor mods will not affect memory and are likely to be fine.
    """
    display_name = "Shadow Mod"
    option_vanilla = 0
    option_reloaded = 1
    option_sx = 2
    default = option_vanilla


class ObjectUnlocks(Toggle):
    """
    Overarching setting to enable/disable very object options.
    """
    display_name = "Object Unlocks"

class ObjectPulleys(DefaultOnToggle):
    """
        Whether pulleys need to be unlocked before they can be used.
    """
    display_name = "Objects: Pulleys"

class ObjectZiplines(DefaultOnToggle):
    """
        Whether ziplines need to be unlocked before they can be used.
    """
    display_name = "Objects: Ziplines"

class ObjectUnits(DefaultOnToggle):
    """
        Whether heal units and bombs, as associated servers need to be unlocked before they can be used.
    """
    display_name = "Objects: Units"

class ObjectRockets(DefaultOnToggle):
    """
        Whether rockets need to be unlocked before they can be used.
    """
    display_name = "Objects: Rockets"

class ObjectLightDashes(DefaultOnToggle):
    """
        Whether light dash trails of rings need to be unlocked before they can be used.
    """
    display_name = "Objects: Light Dashes"

class ObjectWarpHoles(DefaultOnToggle):
    """
        Whether warp holes need to be unlocked before they can be used.
    """
    display_name = "Objects: Warp Holes"

class ShadowBoxes(Toggle):
    """
        Whether or not Special Weapon Boxes (Shadow crates) reward a check.
    """
    display_name = "Shadow Boxes"

class GoldBeetleSanity(Toggle):
    """
        Whether or not Golden Beetles reward checks.
    """
    display_name = "Gold Beetle Sanity"

class DoorSanity(Toggle):
    """Determines whether key door sanity is enabled, i.e. opening the key door provides a check."""
    display_name = "Door Sanity"

class EnergyCores(Toggle):
    """
        Whether or not energy cores (Hero/Dark cores) reward a check.
    """
    display_name = "Energy Cores"

class PlandoStartingStages(OptionSet):
    """
        Force this selection of stages to be chosen first.
    """
    display_name = "Plando Starting Stages"
    valid_keys = [i for i in Names.getLevelNames()
                  if i not in Names.getBossNames() and i not in Names.getLastStoryNames()]


class StoryAndSelectStartTogether(DefaultOnToggle):
    """
        Force story mode's start point to be one of the starting select stages (for both mode)
    """

    display_name = "Story And Select Start Together"

class StartInventoryExcessItems(DefaultOnToggle):
    """
        Add items to start inventory if not enough locations found.
        Not recommended to disable as can lead to generate failures.
    """
    display_name = "Start Inventory Excess Items"

class SelectPercentage(Range):
    """
        Percent of stage unlock items to include in the item pool when playing
        on 'Both' story and select mode.
    """

    display_name = "Select Percentage"
    range_start = 0
    range_end = 100
    default_value = range_end

class ExcludeGoModeItems(DefaultOnToggle):
    """
        Excludes go-mode items from being checks, which is currently limited to
        - Checks within The Last Way on Select/Story Shuffle-less modes
    """
    display_name = "Exclude Go Mode Items"


class EnableTraps(Toggle):
    """
        Enables traps for the multiworld
    """
    display_name = "Enable Traps"

class PoisonTraps(Choice):
    """
        Enables traps for the multiworld
    """
    display_name = "Enable Poison Traps"
    option_off = 0
    option_low = 1
    option_medium = 2
    option_high = 3
    default = option_off

class AmmoTraps(Choice):
    """
        Enables traps for the multiworld
    """
    display_name = "Enable Ammo Traps"
    option_off = 0
    option_low = 1
    option_medium = 2
    option_high = 3
    default = option_off

class CheckpointTraps(Choice):
    """
        Enables traps for the multiworld
    """
    display_name = "Enable Checkpoint Traps"
    option_off = 0
    option_low = 1
    option_medium = 2
    option_high = 3
    default = option_off

class TrapFillPercentage(Range):
    """
        Enables traps for the multiworld
    """
    display_name = "Trap Fill Percentage"
    range_start = 1
    range_end = 100
    default = 5


class PlandoCheckpointSpawns(OptionDict):
    """
        Advanced YAML setting to provide keys to dictate percentage based overrides.
        Read the setup_en.yaml for more information.
    """
    display_name = "Plando Checkpoint Spawns"
    default = {}

class LastWayEnemysanity(DefaultOnToggle):
    """
        Toggle to disable enemy sanity for last way. Only applicable when enemysanity is enabled.
    """
    display_name = "Last Way Enemysanity"

@dataclass
class ShadowTheHedgehogOptions(PerGameCommonOptions):
    #goal: Goal
    #goal_percentage: GoalMissionPercentage
    goal_chaos_emeralds: GoalChaosEmeralds
    goal_missions: GoalMissions
    goal_final_missions: GoalFinalMissions
    goal_hero_missions: GoalHeroMissions
    goal_dark_missions: GoalDarkMissions
    goal_objective_missions: GoalObjectiveMissions
    goal_bosses: GoalBosses
    goal_final_bosses: GoalFinalBosses
    objective_sanity: ObjectiveSanity
    objective_sanity_system: ObjectiveSanitySystem
    objective_sanity_behaviour: ObjectiveSanityBehaviour
    objective_percentage: ObjectivePercentage
    objective_enemy_percentage: EnemyObjectivePercentage
    objective_completion_percentage: ObjectiveCompletionPercentage
    objective_completion_enemy_percentage: ObjectiveCompletionEnemyPercentage
    objective_item_percentage_available: ObjectiveItemPercentageAvailable
    objective_item_enemy_percentage_available: ObjectiveItemEnemyPercentageAvailable
    enemy_objective_sanity: EnemyObjectiveSanity
    character_sanity: CharacterSanity
    enemy_sanity: Enemysanity
    boss_enemy_sanity: BossEnemysanity
    item_sanity: Itemsanity
    enemy_sanity_percentage: EnemySanityPercentage
    difficult_enemy_sanity: DifficultEnemysanity
    key_sanity: Keysanity
    keys_required_for_doors: KeysRequiredForDoors
    key_collection_method: KeyCollectionMethod
    checkpoint_sanity: Checkpointsanity
    checkpoint_shuffle: CheckpointShuffle
    checkpoint_rules: CheckpointRules
    minimal_checkpoint_percentage: MinimalCheckpointPercentage
    checkpoint_convenience: CheckpointConvenience
    starting_stages: StartingStages
    select_gates: SelectGates
    select_gates_count: SelectGatesCount
    gate_unlock_requirement: GateUnlockRequirement
    force_objective_sanity_chance: ForceObjectiveSanityChance
    force_objective_sanity_max: ForceObjectiveSanityMax
    force_objective_sanity_max_counter: ForceObjectiveSanityMaxCounter
    excluded_stages: ExcludedStages
    weapon_sanity_unlock: WeaponsanityUnlock
    weapon_sanity_min_available: WeaponSanityMinAvailable
    weapon_sanity_max_available: WeaponSanityMaxAvailable
    weapon_sanity_hold: WeaponsanityHold
    vehicle_logic: VehicleLogic
    enable_gauge_items: GaugeFiller
    enable_ring_items: RingFiller
    enable_ammo_boost_items: AmmoBoostFiller
    ring_link: RingLink
    auto_clear_missions: AutoClearMissions
    level_progression: LevelProgression
    percent_overrides: PercentOverrides
    logic_level: LogicLevel
    boss_logic_level: BossLogicLevel
    craft_logic_level: CraftLogicLevel
    chaos_control_logic_level: ChaosControlLogicLevel
    story_shuffle: StoryShuffle
    include_last_way_shuffle: IncludeLastStoryShuffle
    secret_story_progression: SecretStoryProgression
    story_boss_count: StoryBossCount
    starting_level_method: StartingLevelMethod
    single_egg_dealer: SingleEggDealer
    single_black_doom: SingleBlackDoom
    single_diablon: SingleDiablon
    rifle_components: RifleComponents
    objective_frequency: ObjectiveFrequency
    enemy_objective_frequency: EnemyObjectiveFrequency
    enemy_frequency: EnemyFrequency
    select_bosses: SelectBosses
    minimum_rank: MinimumRank
    weapon_groups: WeaponGroups
    story_progression_balancing: StoryProgressionBalancing
    story_progression_balancing_passes: StoryProgressionBalancingPasses
    shadow_mod: ShadowMod
    object_unlocks: ObjectUnlocks
    object_pulleys: ObjectPulleys
    object_ziplines: ObjectZiplines
    object_units: ObjectUnits
    object_rockets: ObjectRockets
    object_light_dashes: ObjectLightDashes
    object_warp_holes: ObjectWarpHoles
    shadow_boxes: ShadowBoxes
    energy_cores: EnergyCores
    door_sanity: DoorSanity
    gold_beetle_sanity: GoldBeetleSanity
    plando_starting_stages: PlandoStartingStages
    story_and_select_start_together: StoryAndSelectStartTogether
    select_percentage: SelectPercentage
    gate_density: GateDensity
    #exceeding_items_filler: ExceedingItemsFiller
    start_inventory_excess_items: StartInventoryExcessItems
    exclude_go_mode_items: ExcludeGoModeItems
    enable_traps: EnableTraps
    ammo_trap_enabled: AmmoTraps
    checkpoint_trap_enabled: CheckpointTraps
    poison_trap_enabled: PoisonTraps
    trap_fill_percentage: TrapFillPercentage

    plando_checkpoint_spawns: PlandoCheckpointSpawns
    music_shuffle: MusicShuffle
    last_way_enemysanity: LastWayEnemysanity


shadow_option_groups = [

    OptionGroup("Sanities", [ObjectiveSanity, EnemyObjectiveSanity,
                             CharacterSanity, Checkpointsanity,
                             Keysanity, Enemysanity,
                             WeaponsanityUnlock, WeaponsanityHold,
                             VehicleLogic, ObjectUnlocks,
                             ShadowBoxes, EnergyCores, GoldBeetleSanity,
                             DoorSanity, KeyCollectionMethod, Itemsanity,
                             CheckpointShuffle, CheckpointRules, MinimalCheckpointPercentage]),

    OptionGroup("Progression", [StartingStages, LevelProgression, SelectGates,
                                SelectGatesCount, GateUnlockRequirement,
                                GateDensity, SelectBosses, StoryShuffle,
                                SelectPercentage, StoryBossCount,
                                IncludeLastStoryShuffle,
                                ExcludeGoModeItems]),

    OptionGroup("Difficulty", [LogicLevel, BossLogicLevel, CraftLogicLevel,
                               ChaosControlLogicLevel]),

    OptionGroup("Goal", [GoalChaosEmeralds, GoalMissions,
                         GoalObjectiveMissions, GoalFinalMissions,
                         GoalHeroMissions, GoalDarkMissions,
                         GoalBosses, GoalFinalBosses]),

    OptionGroup("Objective Configuration", [
        ObjectiveSanitySystem, ObjectiveSanityBehaviour, KeysRequiredForDoors,
        ObjectivePercentage, ObjectiveCompletionPercentage, ObjectiveItemPercentageAvailable, ObjectiveFrequency,
        EnemyObjectivePercentage, ObjectiveCompletionEnemyPercentage, ObjectiveItemEnemyPercentageAvailable, EnemyObjectiveFrequency,
        EnemySanityPercentage, EnemyFrequency, PercentOverrides
        ]),

    OptionGroup("Configuration", [
        RifleComponents, ExcludedStages,
        ObjectZiplines, ObjectPulleys, ObjectRockets, ObjectUnits, ObjectWarpHoles, ObjectLightDashes,
        SingleDiablon, SingleBlackDoom, SingleEggDealer,
        BossEnemysanity, DifficultEnemysanity, LastWayEnemysanity,
        StoryAndSelectStartTogether, StoryProgressionBalancing, StoryProgressionBalancingPasses,
        ForceObjectiveSanityChance, ForceObjectiveSanityMax, ForceObjectiveSanityMaxCounter,
        StartingLevelMethod, SecretStoryProgression, CheckpointConvenience, MinimumRank, AutoClearMissions,
        StartInventoryExcessItems

    ]),

    OptionGroup("Extra Items", [RingFiller, GaugeFiller, AmmoBoostFiller,
                                EnableTraps, TrapFillPercentage,
                                PoisonTraps, AmmoTraps, CheckpointTraps,
                                WeaponSanityMinAvailable, WeaponSanityMaxAvailable, WeaponGroups]),

    OptionGroup("Other", [RingLink, MusicShuffle, ShadowMod, ExceedingItemsFiller]),

    OptionGroup("Plando", [PlandoStartingStages, PlandoCheckpointSpawns])

]