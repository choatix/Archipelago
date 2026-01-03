import importlib
import os
import pkgutil
import sys

from . import Levels, Names
from .Items import GetAllItemInfo
from .Locations import GetAllLocationInfo


def TestItemIds():
    items = GetAllItemInfo()

    result = {}
    error_count = 0
    for i_set in items:
        for item in i_set:
            if item.itemId in result:
                print("Duplicate item ID", result[item.itemId].name, item.name, item.itemId)
                error_count += 1
            else:
                result[item.itemId] = item

    return error_count


def TestLocationStageReference():
    locations = GetAllLocationInfo()
    error_count = 0
    for l_set in locations:
        for location in l_set:
            if location.stageId is not None:
                if Levels.LEVEL_ID_TO_LEVEL[location.stageId] not in location.name:
                    print("Suspicious name for ", location.name, "for stage", Levels.LEVEL_ID_TO_LEVEL[location.stageId])

    return error_count

def TestLocationIds():
    locations = GetAllLocationInfo()
    result = {}
    error_count = 0
    for l_set in locations:
        for location in l_set:
            if location.locationId in result:
                print("Duplicate location ID", result[location.locationId].name, location.name, location.locationId)
                error_count += 1
            else:
                result[location.locationId] = location

            if location.stageId is not None:
                if Levels.LEVEL_ID_TO_LEVEL[location.stageId] not in location.name:
                    print("Suspicious name for ", location.name, "for stage", Levels.LEVEL_ID_TO_LEVEL[location.stageId])

    return error_count

def TestLevelRegions():
    print("TLR")
    region_definitions = Levels.INDIVIDUAL_LEVEL_REGIONS

    last_region = None
    for region in region_definitions:
        if last_region is None:
            last_region = region
            continue

        if region.stageId != last_region.stageId:
            last_region = region
            continue

        if region.regionIndex != (last_region.regionIndex + 1):
            print("Error with", region)

        last_region = region

    region_indicies = Names.REGION_INDICIES


    pass

errors =  TestItemIds()
errors += TestLocationIds()
errors += TestLocationStageReference()

if errors > 0:
    sys.exit(1)