import typing
from math import ceil, floor

from BaseClasses import MultiWorld, Region, Entrance, Item, ItemClassification
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from . import Items, Levels, LEVEL_ID_TO_LEVEL, CharacterToLevel, ITEM_TOKEN_TYPE_FINAL, \
    MISSION_ALIGNMENT_DARK, MISSION_ALIGNMENT_HERO, ITEM_TOKEN_TYPE_OBJECTIVE, \
    ITEM_TOKEN_TYPE_STANDARD, ITEM_TOKEN_TYPE_ALIGNMENT, Utils, REGION_RESTRICTION_TYPES, Weapons, Regions, LevelRegion, \
    GetLevelObjectNames, Vehicle, Options, Locations, ITEM_TOKEN_TYPE_BOSS, ITEM_TOKEN_TYPE_FINAL_BOSS, \
    REGION_RESTRICTION_REFERENCE_TYPES, GetEnemyLocationName, Names
from .Items import ShadowTheHedgehogItem, GetLevelTokenItems
from .Locations import MissionClearLocations, LocationInfo, BossClearLocations
from .Options import LevelProgression
from .Regions import character_name_to_region, stage_id_to_region, region_name_for_character, weapon_name_to_region, \
    region_name_for_weapon
from . import Utils as ShadowUtils

def GetKeyRule(stage, player):
    rule = lambda state: True
    for keyData in [ k for k in Locations.KeyLocations if k.stageId == stage]:
        regions = set(keyData.region)
        for region in regions:
            region_name = Regions.stage_id_to_region(stage, region)
            rule = lambda state, r=rule, r_name=region_name: r(
                state) and state.can_reach_region(
                r_name, player)

    return rule

def GetRelevantTokenItem(token: LocationInfo):
    level_token_items = GetLevelTokenItems()

    if token.other == ITEM_TOKEN_TYPE_FINAL:
        level_token_items = [ t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_FINAL ]
    elif token.other == ITEM_TOKEN_TYPE_OBJECTIVE:
        level_token_items = [ t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_OBJECTIVE ]
    elif token.other == ITEM_TOKEN_TYPE_STANDARD:
        level_token_items = [t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_STANDARD]
    elif token.other == ITEM_TOKEN_TYPE_ALIGNMENT:
        level_token_items = [t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_ALIGNMENT]
        if token.alignmentId == MISSION_ALIGNMENT_DARK:
            level_token_items = [ t for t in level_token_items if t.alignmentId == MISSION_ALIGNMENT_DARK]
        elif token.alignmentId == MISSION_ALIGNMENT_HERO:
            level_token_items = [ t for t in level_token_items if t.alignmentId == MISSION_ALIGNMENT_HERO]
    elif token.other == ITEM_TOKEN_TYPE_BOSS:
        level_token_items = [t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_BOSS]
    elif token.other == ITEM_TOKEN_TYPE_FINAL_BOSS:
        level_token_items = [t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_FINAL_BOSS]

    if len(level_token_items) == 0:
        return None

    return level_token_items[0]

def handle_path_rules(options, player, additional_level_region, path_type):
    rule = lambda state: True

    logic_level = None
    if path_type == REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic:
        logic_level = options.logic_level
    elif path_type == REGION_RESTRICTION_REFERENCE_TYPES.BossLogic:
        logic_level = options.boss_logic_level
    elif path_type == REGION_RESTRICTION_REFERENCE_TYPES.CraftLogic:
        logic_level = options.craft_logic_level

    region_restriction = additional_level_region.restrictionType

    if region_restriction == REGION_RESTRICTION_TYPES.HardLogicOnly:
        if options.logic_level != Options.LogicLevel.option_hard:
            rule = lambda state: False

    if additional_level_region.logicType == Options.LogicLevel.option_easy and \
            logic_level != Options.LogicLevel.option_easy:
        return rule

    if additional_level_region.logicType == Options.LogicLevel.option_hard and \
            logic_level == Options.LogicLevel.option_hard:
        return rule

    if region_restriction == REGION_RESTRICTION_TYPES.ShootOrTurret:
        if options.weapon_sanity_unlock and options.vehicle_logic:
            rule_weapon = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region.stageId,
                                                      additional_level_region.fromRegions)

            rule_vehicle = Vehicle.GetRuleByVehicleRequirement(player, "Gun Turret")

            rule = (rule_weapon or rule_vehicle)
            return rule

        # If weapon or vehicle is not on, then it will always be available to use the other method

        #elif options.weapon_sanity_unlock:
        #    region_restriction = REGION_RESTRICTION_TYPES.LongRangeGun
        #elif options.vehicle_logic:
        #    region_restriction = REGION_RESTRICTION_TYPES.GunTurret


    # TODO: Complete this restriction - with weapon type and Unit access
    elif region_restriction == REGION_RESTRICTION_TYPES.Explosion:
        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.EXPLOSION,
                                                  additional_level_region.stageId, additional_level_region.fromRegions)

        weapon_available = False
        bombs_available = True
        if weapon_rule is not None:
            weapon_available = True

        bomb_rule = lambda state: state.has("Bombs", player)

        if additional_level_region.stageId == Levels.STAGE_DEATH_RUINS:
            bombs_available = False

        if weapon_available and options.weapon_sanity_unlock and \
            (not bombs_available):
            rule = weapon_rule
        elif bombs_available and weapon_available and options.weapon_sanity_unlock and \
            options.object_units:
            rule = lambda state: weapon_rule(state) or bomb_rule(state)
        elif not weapon_available and options.object_units:
            rule = bomb_rule

    elif region_restriction == REGION_RESTRICTION_TYPES.Heal:
        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.HEAL,
                                                         additional_level_region.stageId,
                                                         additional_level_region.fromRegions)

        weapon_available = False
        units_available = False
        if weapon_rule is not None:
            weapon_available = True

        unit_rule = lambda state: state.has("Heal Units", player)

        if additional_level_region.stageId == Levels.STAGE_THE_DOOM:
            units_available = True

        if weapon_available and \
                (not units_available):
            rule = weapon_rule
        elif units_available and weapon_available and \
                options.object_units:
            rule = lambda state: weapon_rule(state) or unit_rule(state)
        elif not weapon_available and options.object_units:
            rule = unit_rule

    elif options.weapon_sanity_unlock and Levels.IsWeaponsanityRestriction(region_restriction):
        if region_restriction == REGION_RESTRICTION_TYPES.Torch:
            rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.TORCH,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        elif region_restriction == REGION_RESTRICTION_TYPES.LongRangeGun:
            rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        elif region_restriction == REGION_RESTRICTION_TYPES.Vacuum:
            rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        elif region_restriction == REGION_RESTRICTION_TYPES.Gun:
            rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.SHOT,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        elif region_restriction == REGION_RESTRICTION_TYPES.Heal:
           pass

        elif region_restriction == REGION_RESTRICTION_TYPES.AnyStageWeapon:
            rule = Weapons.GetRuleByWeaponRequirement(player, None, additional_level_region.stageId, additional_level_region.fromRegions)

        else:
            print("Unhandled restriction",region_restriction, additional_level_region )

    elif options.vehicle_logic and Levels.IsVeichleSanityRestriction(additional_level_region.restrictionType):
        if region_restriction == REGION_RESTRICTION_TYPES.BlackArmsTurret:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Turret")
        elif region_restriction == REGION_RESTRICTION_TYPES.Car:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Standard Car")
        elif region_restriction == REGION_RESTRICTION_TYPES.BlackVolt:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Volt")
        elif region_restriction == REGION_RESTRICTION_TYPES.BlackHawk:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Hawk")
        elif region_restriction == REGION_RESTRICTION_TYPES.GunJumper:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Jumper")
        elif region_restriction == REGION_RESTRICTION_TYPES.AirSaucer:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Air Saucer")
        elif region_restriction == REGION_RESTRICTION_TYPES.GunLift:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Lift")
        elif region_restriction == REGION_RESTRICTION_TYPES.GunTurret:
            rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Turret")

    elif region_restriction == REGION_RESTRICTION_TYPES.ShadowRifle:
        rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.SHADOW_RIFLE,
                                                         additional_level_region.stageId,
                                                         additional_level_region.fromRegions)


    elif options.object_unlocks and Levels.IsObjectRestriction(region_restriction):
        if region_restriction == REGION_RESTRICTION_TYPES.Zipwire and options.object_ziplines:
            rule = lambda state: state.has("Zipwire", player)
        if region_restriction == REGION_RESTRICTION_TYPES.LightDash and options.object_light_dashes:
            rule = lambda state: state.has("Air Shoes", player)
        if region_restriction == REGION_RESTRICTION_TYPES.WarpHole and options.object_warp_holes:
            rule = lambda state: state.has("Warp Holes", player)
        if region_restriction == REGION_RESTRICTION_TYPES.Rocket and options.object_rockets:
            rule = lambda state: state.has("Rocket", player)
        if region_restriction == REGION_RESTRICTION_TYPES.Pulley and options.object_pulleys:
            rule = lambda state: state.has("Pulley", player)

    return rule


def lock_warp_items(multiworld, world, player):

    if world.options.level_progression == Options.LevelProgression.option_select or not world.options.secret_story_progression:
        return

    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = Locations.GetAllLocationInfo()

    warpItemInfos = Items.PopulateLevelWarpPoints()

    for warp in warp_locations:
        if warp.stageId in Levels.LAST_STORY_STAGES and not world.options.include_last_way_shuffle:
            continue

        if warp.stageId in Levels.BOSS_STAGES and world.options.level_progression == Options.LevelProgression.option_select:
            continue

        if warp.stageId not in world.available_levels:
            continue

        warp_story_region = Regions.stage_id_to_story_region(warp.stageId)
        location = multiworld.get_location(warp.name, player)
        i = [ w for w in warpItemInfos if w.stageId == warp.stageId][0]
        mw_token_item = ShadowTheHedgehogItem(i, player)
        new_access_rule = lambda state, r=location.access_rule, s=warp_story_region: r(state) and state.can_reach_region(
            s, player)

        location.access_rule = new_access_rule

        location.place_locked_item(
            mw_token_item)

def CountRegionAccessibility(state, keys, data, ix, player):
    #sum(
    #    [data[r] for r in GetReachableRegions(state, keys) if r in keys]) >= ix)

    # This method uses events but they show up in spoiler log and look bad so use other method
    # Which uses reachable regions instead of events

    #keys = list(keys)
    # all_regions = [ a.name for a in  state.reachable_regions[player]]
    # matching_counts = [ data[r] for r in all_regions if r in keys]
    #total_accessible = sum(matching_counts)
    #return total_accessible >= ix

    keys = list(keys)

    total = 0
    for key in keys:
        #print("Does player have", key)
        if state.has(key, player):
            total += data[key]

    #print("total is", total)
    return total >= ix

def set_rules(multiworld: MultiWorld, world: World, player: int):

    token_assignments = {}

    if world.options.level_progression != LevelProgression.option_select:
        Regions.connect_by_story_mode(multiworld, world, player, world.shuffled_story_mode)

    for stage in Levels.ALL_STAGES:
        if stage in Levels.BOSS_STAGES:
            continue

        if stage not in world.available_levels:
            continue

        view_name = Names.GetDistributionRegionEventName(stage, 0)

        event_location = multiworld.get_location(view_name, player)
        event_location.access_rule = lambda state, r=stage_id_to_region(stage,
                                                                        0): \
            state.can_reach_region(r, player)

        event_location.place_locked_item(Item(view_name,
                                              ItemClassification.progression, None, player))

    for additional_level_region in Levels.INDIVIDUAL_LEVEL_REGIONS:
        if additional_level_region.stageId not in world.available_levels:
            continue

        if world.options.logic_level != Options.LogicLevel.option_hard \
            and additional_level_region.restrictionType == REGION_RESTRICTION_TYPES.HardLogicOnly:
            #print("Skip--", additional_level_region)
            continue

        from_regions = additional_level_region.fromRegions
        new_region_name = stage_id_to_region(additional_level_region.stageId, additional_level_region.regionIndex)

        for region_from in from_regions:
            base_region_name = stage_id_to_region(additional_level_region.stageId, region_from)


            base_region = world.get_region(base_region_name)
            new_region = world.get_region(new_region_name)

            rule = lambda state: True

            if additional_level_region.restrictionType == REGION_RESTRICTION_TYPES.KeyDoor:
                key_rule = GetKeyRule(additional_level_region.stageId, player)
                connect(world.player, base_region_name + ">" + new_region_name,
                        base_region, new_region, key_rule)
                continue

            path_rule = handle_path_rules(world.options, player, additional_level_region,
                                          REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic)
            if path_rule is not None:
                rule = path_rule

            connect(world.player, base_region_name+ ">" + "(" + str(additional_level_region.restrictionType) + ")" + new_region_name,
                    base_region, new_region, rule)

        view_name = Names.GetDistributionRegionEventName(additional_level_region.stageId, additional_level_region.regionIndex)

        event_location = multiworld.get_location(view_name, player)
        event_location.access_rule = lambda state, r=stage_id_to_region(additional_level_region.stageId,
                                                                        additional_level_region.regionIndex): \
            state.can_reach_region(r, player)

        event_location.place_locked_item(Item(view_name,
                                              ItemClassification.progression, None, player))

            # TODO: Add logic here for obtaining access

    override_settings = world.options.percent_overrides
    lock_warp_items(multiworld, world, world.player)


    for clear in MissionClearLocations:

        if clear.stageId not in world.available_levels:
            continue

        id, name = Levels.GetLevelCompletionNames(clear.stageId, clear.alignmentId)
        try:
            req_rule = lambda state: True
            level_rule = lambda state: True
            rule_change = False

            if clear.requirements is not None:
                for req in clear.requirements:
                    lr = LevelRegion(clear.stageId, None, req)
                    lr.setLogicType(clear.logicType)

                    logic_type = REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic

                    req_rule_a = handle_path_rules(world.options, player, lr,
                                                 logic_type)
                    if req_rule_a is not None:
                        req_rule = lambda state, z=req_rule, a=req_rule_a: \
                            z(state) and a(state)
                        level_rule = lambda state, r_rule=req_rule, l_rule=level_rule: (
                                r_rule(state) and l_rule(state))

                        rule_change = True
            if clear.craft_requirements is not None:
                for req in clear.craft_requirements:
                    lr = LevelRegion(clear.stageId, None, req)
                    lr.setLogicType(clear.logicType)

                    logic_type = REGION_RESTRICTION_REFERENCE_TYPES.CraftLogic

                    req_rule_b = handle_path_rules(world.options, player, lr,
                                                 logic_type)
                    if req_rule_b is not None:
                        req_rule = lambda state, z=req_rule, b=req_rule_b: \
                            z(state) and b(state)
                        level_rule = lambda state, r_rule=req_rule, l_rule=level_rule: (
                                r_rule(state) and l_rule(state))
                        rule_change = True

            if clear.getDistribution() is not None:

                # This functionality requires access to ALL to complete which is inflating
                # When logically you can find with access to either
                # But this also needs handling for objective-less
                #for region_id in clear.getDistribution().keys():
                #    required_region = Regions.stage_id_to_region(clear.stageId, region_id)
                ##    new_rule = lambda state, r_region=required_region: state.can_reach_region(r_region, player)
                #    level_rule = lambda state, l_rule=level_rule, n_rule=new_rule: n_rule(state) and l_rule(state)
                #    rule_change = True

                if clear.requirement_count is not None and world.options.objective_sanity:

                    max_required = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                  clear.mission_object_name, world.options),
                        clear.requirement_count, clear.stageId, clear.alignmentId,
                        override_settings)

                    frequency_required = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                                  clear.mission_object_name, world.options),
                        100, clear.stageId, clear.alignmentId,
                        override_settings)

                    progress_distribution = clear.getDistribution().items()
                    progress_dist_by_name = {}

                    total = 0
                    for region, count in progress_distribution:
                        progress_dist_by_name[Names.GetDistributionRegionEventName(clear.stageId, region)] = count
                        total += count

                    for l in range(1, total + 1):
                        if l > max_required:
                            break

                        if l % frequency_required != 0 and max_required != l:
                            continue

                        prog_rule = lambda state, ix=l, data=progress_dist_by_name, keys=progress_dist_by_name.keys() \
                            : CountRegionAccessibility(state, keys, data, ix, player)

                        location_id, objective_location_name = (
                            GetLevelObjectNames(clear.stageId, clear.alignmentId, clear.mission_object_name,
                                                l))
                        location = multiworld.get_location(objective_location_name, player)

                        progression_rule = lambda state, p_rule=prog_rule, r_rule=req_rule : \
                            p_rule(state) and r_rule(state)

                        add_rule(location, progression_rule)

                        if l > max_required:
                            break


            if clear.requirement_count is not None:
                location = multiworld.get_location(name, player)
                item_name = Items.GetStageAlignmentObject(clear.stageId, clear.alignmentId)
                if world.options.objective_sanity:

                    max_required = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                                  clear.mission_object_name, world.options),
                        clear.requirement_count, clear.stageId, clear.alignmentId,
                        override_settings)

                    new_rule = lambda state, itemname=item_name, count=max_required: state.has(itemname, player, count=count)

                    progress_distribution = clear.getDistribution().items()
                    progress_dist_by_name = {}

                    total = 0
                    for region, count in progress_distribution:
                        progress_dist_by_name[Names.GetDistributionRegionEventName(clear.stageId, region)] = count
                        total += count

                    finish_count = 1
                    if not world.options.objective_sanity:
                        finish_count = max_required
                        if finish_count == 0:
                            finish_count = 1

                    # Enemy stage clears don't require completing objectives
                    if clear.mission_object_name in ("Soldier", "Artificial Chaos", "Alien"):
                        finish_count = 0

                    prog_rule = lambda state, keys=progress_dist_by_name.keys(), data=progress_dist_by_name,\
                                       ix=finish_count\
                        : CountRegionAccessibility(state, keys, data, ix, player)

                    # Does this work as an AND or an OR?
                    level_rule = lambda state, l_rule=level_rule, n_rule=new_rule, p_rule=prog_rule:\
                        l_rule(state) and n_rule(state) and p_rule(state)
                    add_rule(location, level_rule)
                    rule_change = True
            else:

                # if equal to 1 there should only be one, and we need that region to finish
                # e.g. goal ring, core, etc.
                if clear.getDistribution() is not None:

                    # This functionality requires access to ALL to complete which is inflating
                    # When logically you can find with access to either
                    # But this also needs handling for objective-less
                    for region_id in clear.getDistribution().keys():
                        required_region = Regions.stage_id_to_region(clear.stageId, region_id)
                        new_rule = lambda state, r_region=required_region: state.can_reach_region(r_region, player)
                        level_rule = lambda state, l_rule=level_rule, n_rule=new_rule: n_rule(state) and l_rule(state)
                        rule_change = True

                location = multiworld.get_location(name, player)
                if rule_change:
                    add_rule(location, level_rule)

            associated_tokens = [t for t in world.token_locations if
                                 t.alignmentId == clear.alignmentId and
                                 t.stageId == clear.stageId and t.other != ITEM_TOKEN_TYPE_BOSS]

            for token in associated_tokens:
                location = multiworld.get_location(token.name, player)
                if rule_change:
                    add_rule(location, level_rule)
                allocated_item = GetRelevantTokenItem(token)
                if allocated_item is None:
                    print("Could not resolve:", token)
                    continue
                if allocated_item.name not in token_assignments:
                    token_assignments[allocated_item.name] = []
                token_assignments[allocated_item.name].append(location)
                mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
                location.place_locked_item(
                    mw_token_item)

        except KeyError as e:
            # Do nothing for mission locations that do not exist
            print("Key error in handling!", e)
            pass

    for boss in BossClearLocations:
        if boss.stageId not in world.available_levels:
            continue

        if boss.stageId == Levels.BOSS_DEVIL_DOOM:
            continue

        boss_id, boss_name = Locations.GetBossLocationName(boss.name, boss.stageId)
        location = multiworld.get_location(boss_name, player)

        boss_rule = None
        if boss.requirements is not None:
            if boss.stageId not in world.available_levels:
                continue
            lr = LevelRegion(boss.stageId, None, boss.requirements)
            lr.setLogicType(boss.logicType)
            req_rule = handle_path_rules(world.options, player, lr, REGION_RESTRICTION_REFERENCE_TYPES.BossLogic)
            if req_rule is not None:
                boss_rule = lambda state, r_rule=req_rule: r_rule(state)
                boss_id, boss_name = Locations.GetBossLocationName(boss.name, boss.stageId)
                location = multiworld.get_location(boss_name, player)
                add_rule(location, boss_rule)


        associated_tokens = [t for t in world.token_locations if
                             t.stageId == boss.stageId and
                             (t.other == ITEM_TOKEN_TYPE_BOSS or t.other == ITEM_TOKEN_TYPE_FINAL_BOSS)]
        for token in associated_tokens:
            allocated_item = GetRelevantTokenItem(token)
            if allocated_item.name not in token_assignments:
                token_assignments[allocated_item.name] = []
            token_location = multiworld.get_location(token.name, player)
            if boss_rule is not None:
                add_rule(token_location, boss_rule)
            token_assignments[allocated_item.name].append(location)
            mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
            token_location.place_locked_item(
                mw_token_item)

    for character,stages in CharacterToLevel.items():
        if character in world.available_characters:
            region_name = character_name_to_region(character)
            region = world.get_region(region_name)
            for stage in stages:
                region_index = 0
                if type(stage) is tuple:
                    region_index = stage[1]
                    stage = stage[0]
                    pass

                if stage not in world.available_levels:
                    continue
                region_stage = world.get_region(stage_id_to_region(stage, region_index))
                region_stage.connect(region, region_name_for_character(LEVEL_ID_TO_LEVEL[stage], character))

    for weapon in Weapons.WEAPON_INFO:
        if weapon.name in world.available_weapons:
            region_name = weapon_name_to_region(weapon.name)
            region = world.get_region(region_name)
            for stage in weapon.available_stages:
                region_index = 0
                if type(stage) is tuple:
                    region_index = stage[1]
                    stage = stage[0]
                    pass

                if stage not in world.available_levels:
                    continue

                rule = lambda state: True

                if (world.options.weapon_sanity_unlock and
                    world.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked) or \
                    Weapons.WeaponAttributes.SPECIAL in weapon.attributes:
                        rule = Weapons.GetRuleByWeaponRequirement(player, weapon.name, None, None)

                region_stage = world.get_region(stage_id_to_region(stage, region_index))
                region_stage.connect(region, region_name_for_weapon(LEVEL_ID_TO_LEVEL[stage], weapon.name),
                                     rule=rule)

    if world.options.enemy_sanity:
        for enemy in Locations.GetEnemySanityLocations():

            if enemy.stageId not in world.available_levels:
                continue

            max_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, world.options),
                enemy.total_count, enemy.stageId, enemy.enemyClass,
                override_settings)

            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                          enemy.mission_object_name, world.options),
                100, enemy.stageId, enemy.enemyClass,
                override_settings)


            enemy_distribution = enemy.getDistribution().items()
            enemy_dist_by_name = {}

            total = 0
            for region, count in enemy_distribution:
                enemy_dist_by_name[Names.GetDistributionRegionEventName(enemy.stageId, region)] = count
                total += count

            for l in range(1, total+1):
                if l > max_required:
                    break

                if l % frequency_required != 0 and max_required != l:
                    continue

                new_rule = lambda state, ix=l, data=enemy_dist_by_name, keys=enemy_dist_by_name.keys()\
                    : CountRegionAccessibility(state, keys, data, ix, player)
                location_id, objective_location_name = (
                    GetEnemyLocationName(enemy.stageId, enemy.enemyClass, enemy.mission_object_name,
                                        l))
                location = multiworld.get_location(objective_location_name, player)
                add_rule(location, new_rule)

                if l > max_required:
                    break

    e = multiworld.get_entrance("final-story-unlock", player)
    goal_has = []
    item_dict = Items.GetItemDict()
    if world.options.goal_chaos_emeralds:
        emeralds = Items.GetEmeraldItems()
        goal_has.extend([ (ce.name,1) for ce in emeralds ])
    if world.options.goal_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardMissionToken, token_assignments, world.options.goal_missions)
        goal_has.append(tokens)
    if world.options.goal_hero_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardHeroToken, token_assignments, world.options.goal_hero_missions)
        goal_has.append(tokens)
    if world.options.goal_dark_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardDarkToken, token_assignments, world.options.goal_dark_missions)
        goal_has.append(tokens)
    if world.options.goal_final_missions > 0:
        tokens = get_token_count(world, Items.Progression.FinalToken, token_assignments, world.options.goal_final_missions)
        goal_has.append(tokens)
    if world.options.goal_objective_missions > 0:
        tokens = get_token_count(world, Items.Progression.ObjectiveToken, token_assignments, world.options.goal_objective_missions)
        goal_has.append(tokens)
    if world.options.goal_bosses > 0:
        tokens = get_token_count(world, Items.Progression.BossToken, token_assignments, world.options.goal_bosses)
        goal_has.append(tokens)
    if world.options.goal_final_bosses > 0:
        tokens = get_token_count(world, Items.Progression.FinalBossToken, token_assignments, world.options.goal_final_bosses)
        goal_has.append(tokens)
    if world.options.include_last_way_shuffle:
        pass

    e.access_rule = lambda state, g_has=goal_has: len([ x for x in g_has if state.has(x[0], player, count=x[1]) ]) == len(g_has)

    if (world.options.level_progression != Options.LevelProgression.option_select and
            world.options.include_last_way_shuffle and world.options.story_shuffle == Options.StoryShuffle.option_chaos):

        # handle requirement that DD must be found in the level shuffle!
        devil_doom_story_region = Regions.stage_id_to_story_region(Levels.BOSS_DEVIL_DOOM)
        e.access_rule = lambda state, er=e.access_rule : er(state) and state.can_reach_region(devil_doom_story_region, player)
        multiworld.register_indirect_condition(multiworld.get_region(devil_doom_story_region, player),
                                               multiworld.get_entrance('devil-doom-fight', player))

    else:
        # Ensure TLW is beatable
        tlw_location_id, tlw_location_name = Levels.GetLevelCompletionNames(Levels.STAGE_THE_LAST_WAY, Levels.MISSION_ALIGNMENT_NEUTRAL)
        last_way_region = multiworld.get_region(Regions.get_max_stage_region_id(Levels.STAGE_THE_LAST_WAY), player)
        e.access_rule = lambda state, er=e.access_rule: er(state)

        devil_doom = multiworld.get_entrance("devil-doom-fight", player)
        devil_doom_region = multiworld.get_region('DevilDoom', player)
        devil_doom.access_rule = lambda state, er=e.access_rule: er(state) and state.can_reach_location(tlw_location_name, player)
        multiworld.register_indirect_condition(devil_doom_region,devil_doom)
        multiworld.register_indirect_condition(last_way_region, devil_doom)

    #else:
    #    e = multiworld.get_entrance("final-story-unlock-tlw", player)
        pass

        #e.access_rule = lambda state, : state.has(, player) and state.has(emeralds[1].name, player) \
        #        and state.has(emeralds[2].name, player) and state.has(emeralds[3].name, player) \
        #        and state.has(emeralds[4].name, player) and state.has(emeralds[5].name, player) \
        #        and state.has(emeralds[6].name, player)
    #if world.options.goal_missions:
    #    e.access_rule = lambda state: state.has(emeralds[0].name, player)


    final_item = Items.GetFinalItem()
    mw_final_item = ShadowTheHedgehogItem(final_item, world.player)
    multiworld.get_location(Levels.DevilDoom_Name, world.player).place_locked_item(
        mw_final_item)

    if world.options.rifle_components:
        location = multiworld.get_location("Complete Shadow Rifle", player)
        shadow_rifle = Items.GetShadowRifle()
        mw_shadow_rifle = ShadowTheHedgehogItem(shadow_rifle, world.player)
        location.place_locked_item(mw_shadow_rifle)

        rifle_components = Items.GetRifleComponents()
        rifle_rule = lambda state: True

        for component in rifle_components:
            new_rifle_part = lambda state, cn=component.name: state.has(cn, player)
            rifle_rule = lambda state, rr=rifle_rule, nrp=new_rifle_part: rr(state) and nrp(state)

        add_rule(location, rifle_rule)

    multiworld.completion_condition[player] = lambda state: state.has(Items.Progression.GoodbyeForever, player)


def get_token_count(world, type, token_assignments, goal_value):
    if type not in token_assignments:
        return (type, 0)
    count = len(token_assignments[type])
    goal_req = Utils.getRequiredCount(count, goal_value, ceil)
    world.required_tokens[type] = goal_req
    return (type, goal_req)

def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):

    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)