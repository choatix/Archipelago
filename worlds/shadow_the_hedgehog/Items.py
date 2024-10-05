import copy
from dataclasses import dataclass
from typing import List, Dict, Optional

from BaseClasses import Item, ItemClassification, MultiWorld, CollectionState
from worlds.AutoWorld import World
from worlds.shadow_the_hedgehog.Levels import LEVEL_ID_TO_LEVEL, ALL_STAGES
from worlds.shadow_the_hedgehog.Locations import MissionClearLocations, GetAlignmentsForStage

BASE_ID = 1743800000

@dataclass
class ItemInfo:
    itemId: int
    name: str
    classification: ItemClassification
    stageId: Optional[int | None]
    alignmentId: Optional[int | None]
    type: str


class Progression:
    GoodbyeForever = "Goodbye Forever"
    WhiteEmerald = "White Chaos Emerald"
    RedEmerald = "Red Chaos Emerald"
    CyanEmerald = "Cyan Chaos Emerald"
    PurpleEmerald = "Purple Chaos Emerald"
    GreenEmerald = "Green Chaos Emerald"
    YellowEmerald = "Damn Fourth Chaos Emerald"
    BlueEmerald = "Blue Chaos Emerald"

class Filler:
    Nothing = "Sorry, nothing."

def PopulateLevelUnlockItems():
    level_unlock_items = []
    count = 100
    for stageId in ALL_STAGES:
        item = ItemInfo(count, GetStageUnlockItem(stageId), ItemClassification.progression, stageId=stageId,
                        alignmentId=None, type="level_unlock")
        count += 1
        level_unlock_items.append(item)

    return level_unlock_items


def PopulateLevelObjectItems():
    level_object_items = []
    count = 1000
    for stageId in ALL_STAGES:
        # TODO: handling for stages without a particular mission type
        alignment_ids = GetAlignmentsForStage(stageId)
        for alignment in alignment_ids:
            alignment_object = GetStageAlignmentObject(stageId, alignment)
            if alignment_object is None:
                continue
            item = ItemInfo(count, alignment_object, ItemClassification.progression,
                            stageId=stageId, alignmentId=alignment, type="level_object")
            count += 1
            level_object_items.append(item)

    return level_object_items

def GetStageAlignmentObject(stageId, alignmentId):
    i = [ m for m in MissionClearLocations if m.stageId == stageId and m.alignmentId == alignmentId]
    if len(i) == 0:
        return None

    item = i[0]
    if item.mission_object_name is None:
        return None

    return LEVEL_ID_TO_LEVEL[stageId] + " " + item.mission_object_name

def GetStageUnlockItem(stageId):
    return "Stage:"+LEVEL_ID_TO_LEVEL[stageId]



class ShadowTheHedgehogItem(Item):
    game: str = "Shadow The Hedgehog"

    def __init__(self, item: ItemInfo, player):
        #item = item_name_to_info[name]
        super().__init__(item.name, item.classification, item.itemId + BASE_ID, player)


def GetFinalItem():
    info = ItemInfo(1, Progression.GoodbyeForever, ItemClassification.progression, None, None, type="final")
    return info

def GetFillerItems():
    fillers: List[ItemInfo] = [
        ItemInfo(2, Filler.Nothing, ItemClassification.filler, None, None, type="filler")
    ]

    return fillers

def GetEmeraldItems():
    emeralds: List[ItemInfo] = [
        ItemInfo(10, Progression.WhiteEmerald, ItemClassification.progression, None, None, type="emerald"),
        ItemInfo(11, Progression.CyanEmerald, ItemClassification.progression, None, None, type="emerald"),
        ItemInfo(12, Progression.RedEmerald, ItemClassification.progression, None, None, type="emerald"),
        ItemInfo(13, Progression.GreenEmerald, ItemClassification.progression, None, None, type="emerald"),
        ItemInfo(14, Progression.BlueEmerald, ItemClassification.progression, None, None, type="emerald"),
        ItemInfo(15, Progression.PurpleEmerald, ItemClassification.progression, None, None, type="emerald"),
        ItemInfo(16, Progression.YellowEmerald, ItemClassification.progression, None, None, type="emerald")
    ]

    return emeralds


def GetItemDict():
    all_items = GetAllItemInfo()

    result = {}
    for item_type in all_items:
        for item in item_type:
            result[item.name] = item.itemId + BASE_ID

    return result

def GetItemLookupDict():
    all_items = GetAllItemInfo()

    result = {}
    for item_type in all_items:
        for item in item_type:
            result[item.itemId + BASE_ID] = item

    return result


def GetAllItemInfo():
    level_unlocks_item_table: List[ItemInfo] = PopulateLevelUnlockItems()
    stage_progression_item_table: List[ItemInfo] = PopulateLevelObjectItems()

    emerald_items = GetEmeraldItems()

    filler_items = GetFillerItems()

    level_unlock_items = []
    for unlock in level_unlocks_item_table:
        level_unlock_items.append(unlock)

    stage_items = []
    for item in stage_progression_item_table:
        reference_stage = item.stageId
        reference_alignment = item.alignmentId

        lookup = [x for x in MissionClearLocations
                  if x.stageId == reference_stage and x.alignmentId == reference_alignment][0]

        for i in range(0, lookup.requirement_count):
            stage_items.append(item)

    return emerald_items, level_unlock_items, stage_items, filler_items

def PopulateItemPool(world : World, first_regions):
    total_locations = len(world.multiworld.get_unfilled_locations(world.player))
    item_pool = []
    # TODO: Do not add item for stages you start with
    emerald_items, level_unlock_items, stage_items, filler_items = GetAllItemInfo()

    # Don't use level unlocks for stages you start with!
    use_level_unlock_items = [ l for l in level_unlock_items if l.stageId not in first_regions]

    # Convert to multiworld items
    mw_em_items = [ ShadowTheHedgehogItem(e, world.player) for e in emerald_items]
    mw_level_unlock_items = [ ShadowTheHedgehogItem(l, world.player) for l in use_level_unlock_items ]
    mw_stage_items =  [ ShadowTheHedgehogItem(s, world.player) for s in stage_items]
    mw_filler_items = [ ShadowTheHedgehogItem(f, world.player) for f in filler_items]

    item_pool += mw_em_items
    item_pool += mw_level_unlock_items
    item_pool += mw_stage_items
    while len(item_pool) < total_locations:
        item_pool += mw_filler_items
    world.multiworld.itempool += item_pool
