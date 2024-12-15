import random
from dataclasses import dataclass

from . import Levels

@dataclass
class PathInfo:
    start_stage_id: int
    alignment_id: int
    end_stage_id: int
    cutscenes: []
    boss = None

    def __init__(self, o_id, alignment, n_id, cutscenes):
        self.start_stage_id = o_id
        self.alignment_id = alignment
        self.end_stage_id = n_id
        self.cutscenes = cutscenes
        self.boss = None

    def via_boss(self, boss):
        self.boss = boss
        return self

    def __str__(self):
        start = "START" if self.start_stage_id is None else Levels.LEVEL_ID_TO_LEVEL[self.start_stage_id]
        end = "END" if self.end_stage_id is None else Levels.LEVEL_ID_TO_LEVEL[self.end_stage_id]
        alignment = self.alignment_id
        boss = "" if self.boss is None else Levels.LEVEL_ID_TO_LEVEL[self.boss] + ">"

        return f"{start} {alignment} > {boss}{end}"


def StoryToOrder(StoryMode):

    ordered_data = []
    set_data = set()

    starting_stages = [ s.end_stage_id for s in StoryMode if s.start_stage_id is None ]
    set_data = set_data.union(set(starting_stages))
    ordered_data.extend(list(set_data))

    while True:
        story_nodes = [ s for s in StoryMode if s.start_stage_id in set_data]
        if len(story_nodes) == 0:
            break
        b_len = len(set_data)
        set_data = set_data.union(set([s.end_stage_id for s in story_nodes if s.end_stage_id is not None and s.end_stage_id not in set_data]))
        set_data = set_data.union(set([s.boss for s in story_nodes if s.boss not in set_data and s.boss is not None and s.boss not in set_data]))
        if b_len == len(set_data):
            break
        else:
            missing = [ x for x in set_data if x not in ordered_data]
            ordered_data.extend(missing)

    return ordered_data


def ChaosShuffle(world):
    ModifiedStoryMode = DefaultStoryMode.copy()

    include_last_way = world.options.include_last_way_shuffle

    stages_to_assign = [ l for l in Levels.ALL_STAGES if l not in world.options.excluded_stages and l
                         not in Levels.BOSS_STAGES and l not in Levels.LAST_STORY_STAGES
                         and l != Levels.STAGE_WESTOPOLIS]

    if include_last_way:
        stages_to_assign.append(Levels.STAGE_THE_LAST_WAY)

    possible_stages = stages_to_assign.copy()

    final_bosses = [boss.boss for boss in ModifiedStoryMode if boss.end_stage_id is None]
    if include_last_way:
        final_bosses.append(Levels.BOSS_DEVIL_DOOM)

    bosses_to_assign = [ b for b in Levels.BOSS_STAGES if b not in world.options.excluded_stages and b not in final_bosses]

    # Potentially duplicate some bosses for more clarity

    steps_to_randomise = [ s for s in ModifiedStoryMode if s.start_stage_id is not None ]
    steps_to_randomise.append(PathInfo(Levels.STAGE_THE_LAST_WAY, Levels.MISSION_ALIGNMENT_NEUTRAL, None, []))

    untouched_steps = [ s for s in ModifiedStoryMode if s not in steps_to_randomise ]

    new_story = []
    new_story.extend(untouched_steps)

    bosses_by_alignment = {}

    random.shuffle(steps_to_randomise)
    for step in steps_to_randomise:
        if len(final_bosses) > 0:
            step.end_stage_id = None
            step.boss = final_bosses.pop()
        else:
            boss_assigned = False
            if len(bosses_to_assign) > 0:
                possible_boss = random.choice(bosses_to_assign)

                if possible_boss not in bosses_by_alignment:
                    bosses_by_alignment[possible_boss] = []

                if step.alignment_id not in bosses_by_alignment[possible_boss]:
                    step.boss = possible_boss
                    bosses_by_alignment[possible_boss].append(step.alignment_id)
                    bosses_to_assign.remove(step.boss)
                    boss_assigned = True

            if not boss_assigned:
                step.boss = None

            if len(stages_to_assign) > 0:
                step.end_stage_id = stages_to_assign.pop()
                if step.end_stage_id == step.start_stage_id:
                    stages_to_assign.append(step.end_stage_id)
            else:
                step.end_stage_id = random.choice(possible_stages)

    new_story.extend(steps_to_randomise)

    return new_story




def ShuffleStoryMode(world):
    ModifiedStoryMode = DefaultStoryMode.copy()
    story_stages = []
    for step in ModifiedStoryMode:
        if step.end_stage_id is not None and step.end_stage_id not in story_stages and \
                step.end_stage_id not in world.options.excluded_stages:
            if step.end_stage_id == Levels.STAGE_WESTOPOLIS:
                continue
            story_stages.append(step.end_stage_id)

    story_base = story_stages.copy()
    random.shuffle(story_stages)

    for step in ModifiedStoryMode:
        if step.end_stage_id in story_base:
            index = story_base.index(step.end_stage_id)
            new_stage = story_stages[index]
            step.end_stage_id = new_stage
            print("")

    print(ModifiedStoryMode)
    return ModifiedStoryMode



def GenerateStoryMode(world):
    ModifiedStoryMode = DefaultStoryMode.copy()
    ModifiedStoryMode[0].end_stage_id = world.random.choice(
        [s for s in Levels.ALL_STAGES if s not in Levels.BOSS_STAGES and s not in Levels.LAST_STORY_STAGES
         and s not in Levels.FINAL_STAGES and s not in world.options.excluded_stages])
    return ModifiedStoryMode

def GetStoryMode(world):
    if world.options.story_shuffle == 1:
        return GenerateStoryMode(world)
    elif world.options.story_shuffle == 2:
        return ShuffleStoryMode(world)
    elif world.options.story_shuffle == 3:
        return ChaosShuffle(world)
    else:
        return DefaultStoryMode


def StoryToString(Story):
    string = ""
    for item in Story:
        start_id = item.start_stage_id
        end_id = item.end_stage_id
        alignment = item.alignment_id
        boss = item.boss
        cutscenes = item.cutscenes
        cutscene_count = len(cutscenes)

        if start_id is None:
            start_id = -1

        if end_id is None:
            end_id = -1

        if boss is None:
            boss = -1

        if alignment is None:
            alignment = -1

        cutscene_string = "" if cutscene_count == 0 else "&".join([str(c) for c in cutscenes])

        string += f"{start_id}&{end_id}&{alignment}&{boss}&{cutscene_count}{cutscene_string}/"

    return string

def StringToStory(string):
    story = []
    items = string.split("/")
    for item in items:
        if len(item) == 0:
            continue
        split = item.split("&")
        start_id = int(split[0])
        end_id = int(split[1])
        alignment = int(split[2])
        boss = int(split[3])
        cutscene_count = int(split[4])

        if start_id == -1:
            start_id = None

        if end_id == -1:
            end_id = None

        if alignment == -1:
            alignment = None

        if boss == -1:
            boss = None

        step = PathInfo(start_id, alignment, end_id, [])

        if cutscene_count > 0:
            cutscenes = [ int(x) for x in split[5].split(",")]
            step.cutscenes = cutscenes

        if boss is not None:
            step.boss = boss

        story.append(step)

    return story



DefaultStoryMode = \
[
    PathInfo(None, None, Levels.STAGE_WESTOPOLIS, []),

    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_DIGITAL_CIRCUIT, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_GLYPHIC_CANYON, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LETHAL_HIGHWAY, [])
    ,
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_PRISON_ISLAND, []),

    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_PRISON_ISLAND, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, []),

    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_PRISON_ISLAND, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),
    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),

    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CENTRAL_CITY, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_THE_DOOM, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SKY_TROOPS, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),

    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_DOOM, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_MAD_MATRIX, []),

    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_MAD_MATRIX, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_DEATH_RUINS, []),

    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, []),
    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_AIR_FLEET, []),

    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_AIR_FLEET, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),

    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_AIR_FLEET, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_IRON_JUNGLE, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SPACE_GADGET, []),

    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),

    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),
    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),

    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),
    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),

    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LAVA_SHELTER, []),

    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_LAVA_SHELTER, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_COSMIC_FALL, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),

    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_LAVA_SHELTER, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_GF),
    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_GF),

    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_BC),
    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_BC),

    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),
    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),

    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_CF),
    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_CF),

    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_FH),
    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_FH),

]
