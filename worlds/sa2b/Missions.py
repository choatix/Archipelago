import ast
import json
import random
import typing
import copy

from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from worlds.sa2b.Options import BaseLevelCount

def get_mission_orders():
    return mission_orders

mission_orders: typing.List[typing.List[int]] = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 5, 4],
    [1, 2, 4, 3, 5],
    [1, 2, 4, 5, 3],
    [1, 2, 5, 3, 4],
    [1, 2, 5, 4, 3],

    [1, 3, 2, 4, 5],
    [1, 3, 2, 5, 4],
    [1, 3, 4, 2, 5],
    [1, 3, 4, 5, 2],
    [1, 3, 5, 2, 4],
    [1, 3, 5, 4, 2],

    [1, 4, 2, 3, 5],
    [1, 4, 2, 5, 3],
    [1, 4, 3, 2, 5],
    [1, 4, 3, 5, 2],
    [1, 4, 5, 2, 3],
    [1, 4, 5, 3, 2],

    [1, 5, 2, 3, 4],
    [1, 5, 2, 4, 3],
    [1, 5, 3, 2, 4],
    [1, 5, 3, 4, 2],
    [1, 5, 4, 2, 3],
    [1, 5, 4, 3, 2],

    [2, 1, 3, 4, 5],
    [2, 1, 3, 5, 4],
    [2, 1, 4, 3, 5],
    [2, 1, 4, 5, 3],
    [2, 1, 5, 3, 4],
    [2, 1, 5, 4, 3],

    [2, 3, 1, 4, 5],
    [2, 3, 1, 5, 4],
    [2, 3, 4, 1, 5],
    [2, 3, 4, 5, 1],
    [2, 3, 5, 1, 4],
    [2, 3, 5, 4, 1],

    [2, 4, 1, 3, 5],
    [2, 4, 1, 5, 3],
    [2, 4, 3, 1, 5],
    [2, 4, 3, 5, 1],
    [2, 4, 5, 1, 3],
    [2, 4, 5, 3, 1],

    [2, 5, 1, 3, 4],
    [2, 5, 1, 4, 3],
    [2, 5, 3, 1, 4],
    [2, 5, 3, 4, 1],
    [2, 5, 4, 1, 3],
    [2, 5, 4, 3, 1],

    [3, 1, 2, 4, 5],
    [3, 1, 2, 5, 4],
    [3, 1, 4, 2, 5],
    [3, 1, 4, 5, 2],
    [3, 1, 5, 4, 2],
    [3, 1, 5, 2, 4],

    [3, 2, 1, 4, 5],
    [3, 2, 1, 5, 4],
    [3, 2, 4, 1, 5],
    [3, 2, 4, 5, 1],
    [3, 2, 5, 1, 4],
    [3, 2, 5, 4, 1],

    [3, 4, 1, 2, 5],
    [3, 4, 1, 5, 2],
    [3, 4, 2, 1, 5],
    [3, 4, 2, 5, 1],
    [3, 4, 5, 1, 2],
    [3, 4, 5, 2, 1],

    [3, 5, 1, 4, 2],
    [3, 5, 1, 2, 4],
    [3, 5, 2, 1, 4],
    [3, 5, 2, 4, 1],
    [3, 5, 4, 1, 2],
    [3, 5, 4, 2, 1],

    [4, 1, 2, 3, 5],
    [4, 1, 2, 5, 3],
    [4, 1, 3, 2, 5],
    [4, 1, 3, 5, 2],
    [4, 1, 5, 3, 2],
    [4, 1, 5, 2, 3],

    [4, 2, 1, 3, 5],
    [4, 2, 1, 5, 3],
    [4, 2, 3, 1, 5],
    [4, 2, 3, 5, 1],
    [4, 2, 5, 1, 3],
    [4, 2, 5, 3, 1],

    [4, 3, 1, 2, 5],
    [4, 3, 1, 5, 2],
    [4, 3, 2, 1, 5],
    [4, 3, 2, 5, 1],
    [4, 3, 5, 1, 2],
    [4, 3, 5, 2, 1],

    [4, 5, 1, 3, 2],
    [4, 5, 1, 2, 3],
    [4, 5, 2, 1, 3],
    [4, 5, 2, 3, 1],
    [4, 5, 3, 1, 2],
    [4, 5, 3, 2, 1],
]

SPEED_LEVEL_STYLE = 0
MECH_LEVEL_STYLE = 1
HUNT_LEVEL_STYLE = 2
KART_LEVEL_STYLE = 3
CANNONS_CORE_LEVEL_STYLE = 4

### 0: Speed
### 1: Mech
### 2: Hunt
### 3: Kart
### 4: Cannon's Core
level_styles: typing.List[int] = [
    SPEED_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    KART_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,

    MECH_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    KART_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,
    HUNT_LEVEL_STYLE,
    MECH_LEVEL_STYLE,
    SPEED_LEVEL_STYLE,

    CANNONS_CORE_LEVEL_STYLE
]

def get_stage_name_prefixes():
    return stage_name_prefixes

stage_name_prefixes: typing.List[str] = [
    "City Escape - ",
    "Wild Canyon - ",
    "Prison Lane - ",
    "Metal Harbor - ",
    "Green Forest - ",
    "Pumpkin Hill - ",
    "Mission Street - ",
    "Aquatic Mine - ",
    "Route 101 - ",
    "Hidden Base - ",
    "Pyramid Cave - ",
    "Death Chamber - ",
    "Eternal Engine - ",
    "Meteor Herd - ",
    "Crazy Gadget - ",
    "Final Rush - ",
    "Iron Gate - ",
    "Dry Lagoon - ",
    "Sand Ocean - ",
    "Radical Highway - ",
    "Egg Quarters - ",
    "Lost Colony - ",
    "Weapons Bed - ",
    "Security Hall - ",
    "White Jungle - ",
    "Route 280 - ",
    "Sky Rail - ",
    "Mad Space - ",
    "Cosmic Wall - ",
    "Final Chase - ",
    "Cannon's Core - ",
]

def get_mission_count_table(multiworld: MultiWorld, world: World, player: int):
    mission_count_table: typing.Dict[int, int] = {}

    excluded_set = multiworld.exclude_locations[player].value
    excluded = {}
    if excluded_set is not None:
        for stage_name in stage_name_prefixes:
            for i in range(1, 6):
                if stage_name + str(i) in excluded_set:
                    level_name = stage_name.replace(" - ", "")
                    if level_name not in excluded:
                        excluded[level_name] = []
                    excluded[level_name].append(i)

    excluded_styles = []

    if world.options.goal == 3:
        for level in range(31):
            mission_count_table[level] = 0
    else:
        speed_active_missions = 1
        mech_active_missions = 1
        hunt_active_missions = 1
        kart_active_missions = 1
        cannons_core_active_missions = 1

        for i in range(2,6):
            if getattr(world.options, "speed_mission_" + str(i), None):
                speed_active_missions += 1
            else:
                excluded_styles.append(str(SPEED_LEVEL_STYLE) + " - " + str(i))

            if getattr(world.options, "mech_mission_" + str(i), None):
                mech_active_missions += 1
            else:
                excluded_styles.append(str(MECH_LEVEL_STYLE) + " - " + str(i))

            if getattr(world.options, "hunt_mission_" + str(i), None):
                hunt_active_missions += 1
            else:
                excluded_styles.append(str(HUNT_LEVEL_STYLE) + " - " + str(i))

            if getattr(world.options, "kart_mission_" + str(i), None):
                kart_active_missions += 1
            else:
                excluded_styles.append(str(KART_LEVEL_STYLE) + " - " + str(i))

            if getattr(world.options, "cannons_core_mission_" + str(i), None):
                cannons_core_active_missions += 1
            else:
                excluded_styles.append(str(CANNONS_CORE_LEVEL_STYLE) + " - " + str(i))

        speed_active_missions        = min(speed_active_missions, world.options.speed_mission_count.value)
        mech_active_missions         = min(mech_active_missions, world.options.mech_mission_count.value)
        hunt_active_missions         = min(hunt_active_missions, world.options.hunt_mission_count.value)
        kart_active_missions         = min(kart_active_missions, world.options.kart_mission_count.value)
        cannons_core_active_missions = min(cannons_core_active_missions, world.options.cannons_core_mission_count.value)

        active_missions: typing.List[typing.List[int]] = [
            speed_active_missions,
            mech_active_missions,
            hunt_active_missions,
            kart_active_missions,
            cannons_core_active_missions
        ]

        use_level_weights = False
        use_level_weight = getattr(world.options, "level_weights")
        if use_level_weight:
            use_level_weights = True

        for level in range(31):
            level_style = level_styles[level]
            level_mission_count = active_missions[level_style]

            level_name = stage_name_prefixes[level].replace(" - ", "")
            max_non_excluded = 5

            level_name_variable = level_name.lower().replace(" ","_")+"_levels"
            if hasattr(world.options, level_name_variable) and use_level_weights:

                if level_name in excluded:
                    disabled_styles = 0
                    excluded_for_level = excluded[level_name]
                    for i in range(1, 6):
                        if str(level_style) + " - " + str(i) in excluded_styles:
                            disabled_styles += 1
                        elif i in excluded_for_level:
                            disabled_styles += 1

                    max_missions_with_excluded = 5 - disabled_styles
                    if level_mission_count > max_missions_with_excluded:
                        level_mission_count = max_missions_with_excluded

                count = getattr(world.options, level_name_variable)
                if not isinstance(count,BaseLevelCount):
                    print("Count unknown for::", level_name_variable, type(count))
                if count == 0:
                    count = level_mission_count

                if count > level_mission_count:
                    count = level_mission_count
                if count > max_non_excluded:
                    count = max_non_excluded

                # Levels CANNOT be disabled, always set to 1
                if count == 0:
                    count = 1

                if type(count) == int:
                    print("Issue with processing field:", level_name_variable)
                    mission_count_table[level] = count
                else:
                    mission_count_table[level] = count.value



            else:
                mission_count_table[level] = level_mission_count

    return mission_count_table


def get_mission_table(multiworld: MultiWorld, world: World, player: int, mission_count_map: typing.Dict[int, int]):
    mission_table: typing.Dict[int, int] = {}

    if world.options.goal == 3:
        for level in range(31):
            mission_table[level] = 0
    else:
        speed_active_missions: typing.List[int] = [1]
        mech_active_missions: typing.List[int] = [1]
        hunt_active_missions: typing.List[int] = [1]
        kart_active_missions: typing.List[int] = [1]
        cannons_core_active_missions: typing.List[int] = [1]

        # Add included missions
        for i in range(2,6):
            if getattr(world.options, "speed_mission_" + str(i), None):
                speed_active_missions.append(i)

            if getattr(world.options, "mech_mission_" + str(i), None):
                mech_active_missions.append(i)

            if getattr(world.options, "hunt_mission_" + str(i), None):
                hunt_active_missions.append(i)

            if getattr(world.options, "kart_mission_" + str(i), None):
                kart_active_missions.append(i)

            if getattr(world.options, "cannons_core_mission_" + str(i), None):
                cannons_core_active_missions.append(i)

        active_missions: typing.List[typing.List[int]] = [
            speed_active_missions,
            mech_active_missions,
            hunt_active_missions,
            kart_active_missions,
            cannons_core_active_missions
        ]

        excluded_set = multiworld.exclude_locations[player].value
        excluded = {}
        if excluded_set is not None:
            for stage_name in stage_name_prefixes:
                for i in range(1, 6):
                    if stage_name + str(i) in excluded_set:
                        level_name = stage_name.replace(" - ", "")
                        if level_name not in excluded:
                            excluded[level_name] = []
                        excluded[level_name].append(i)

        required_in_shuffle = getattr(world.options, "required_missions", None)
        required = {}
        if required_in_shuffle is not None:
            for stage_name in stage_name_prefixes:
                for i in range(1, 6):
                    if stage_name + str(i) in required_in_shuffle:
                        level_name = stage_name.replace(" - ", "")
                        if level_name not in required:
                            required[level_name] = []
                        required[level_name].append(i)

        force_mission_position = {}
        mission_shuffle_params = getattr(world.options, "mission_shuffle_parameters", None)
        if mission_shuffle_params is not None:
            for stage_name in stage_name_prefixes:
                for i in range(1, 6):
                    stage_mission = stage_name + str(i)
                    level_name = stage_name.replace(" - ", "")
                    for j in range(1,6):
                        level_name_plus_position_positive = stage_mission + " / " + str(j)
                        level_name_plus_position_negative = stage_mission + " / !" + str(j)

                        if level_name_plus_position_positive in mission_shuffle_params:
                            if level_name not in force_mission_position:
                                force_mission_position[level_name] = {}
                            force_mission_position[level_name][i] = (j,True)

                        if level_name_plus_position_negative in mission_shuffle_params:
                            if level_name not in force_mission_position:
                                force_mission_position[level_name] = {}
                            force_mission_position[level_name][i] = (j,False)

        disallow_only_M2 = getattr(world.options, "disallow_only_M2", None)

        for level in range(31):

            mission_count = mission_count_map[level]

            level_style = level_styles[level]

            level_active_missions: typing.List[int] = copy.deepcopy(active_missions[level_style])
            level_chosen_missions: typing.List[int] = []

            # The first mission must be M1, M2, M3, or M4
            first_mission = 1
            first_mission_options = [1, 2, 3]

            level_name = stage_name_prefixes[level].replace(" - ", "")
            excluded_missions = []
            if level_name in excluded:
                excluded_missions = excluded[level_name]

            required_missions = []
            if level_name in required:
                required_missions = required[level_name]

            if disallow_only_M2:
                if mission_count == 1 and level_style != 3:
                    first_mission_options.remove(2)

            if not world.options.animalsanity:
                first_mission_options.append(4)

            if level_name in force_mission_position:
                forces = force_mission_position[level_name]
                for f in forces.items():
                    force_mission = f[0]
                    force_position_tuple = f[1]
                    force_position_value = force_position_tuple[0]
                    force_position_route = force_position_tuple[1]

                    if force_position_value == 1 and force_position_route and force_mission in first_mission_options:
                        first_mission_options = [force_mission]
                    elif force_mission in first_mission_options:
                        first_mission_options.remove(force_mission)


            use_required = False
            if len(required_missions) > mission_count:
                print("There is an issue with your required count settings...")
                use_required = True
            elif len(required_missions) == mission_count:
                # First mission must be a required mission
                use_required = True

                pass

            if world.options.mission_shuffle:
                valid_options = [mission for mission in level_active_missions if mission in first_mission_options
                                                          and mission not in excluded_missions and
                                                         (mission in required_missions if use_required else True)]
                if len(valid_options) == 0:
                    valid_options = [1]
                    print("Error, invalid pick for:", mission_count, required_missions, use_required, level_name)
                first_mission = multiworld.random.choice(valid_options)
                if first_mission in required_missions:
                    required_missions.remove(first_mission)

            level_active_missions.remove(first_mission)

            for mission in required_missions:
                if mission not in level_chosen_missions and mission not in excluded_missions:
                    level_chosen_missions.append(mission)

            multiworld.random.shuffle(level_active_missions)

            #forces = force_mission_position[level_name]
            #for f in forces.items():
            #    force_mission = f[0]
            #    force_position_tuple = f[1]
            #    force_position_value = force_position_tuple[0] - 1
            #    force_position_route = force_position_tuple[1]

            #    if force_position_value == 1:
            #        continue

            #    if force_position_value == 1 and force_position_route:
            #        pass
            #    else:
            #        pass

            # Place Active Missions in the chosen mission list
            for mission in level_active_missions:
                mission_number = len(level_chosen_missions) + 1

                if mission_number == mission_count:
                    break

                if mission not in level_chosen_missions and mission not in excluded_missions:
                    level_chosen_missions.append(mission)


            #if world.options.mission_shuffle:
            #    multiworld.random.shuffle(level_chosen_missions)

            level_chosen_missions.insert(0, first_mission)

            # Fill in the non-included missions
            for i in range(1,6):
                if i not in level_chosen_missions:
                    level_chosen_missions.append(i)

            # Determine which mission order index we have, for conveying to the mod
            for i in range(len(mission_orders)):
                if mission_orders[i] == level_chosen_missions:
                    level_mission_index = i
                    break

            mission_table[level] = level_mission_index

    return mission_table


def get_first_and_last_cannons_core_missions(mission_map: typing.Dict[int, int], mission_count_map: typing.Dict[int, int]):
        mission_count = mission_count_map[30]
        mission_order: typing.List[int] = mission_orders[mission_map[30]]
        stage_prefix: str = stage_name_prefixes[30]

        first_mission_number = mission_order[0]
        last_mission_number = mission_order[mission_count - 1]
        first_location_name: str = stage_prefix + str(first_mission_number)
        last_location_name: str = stage_prefix + str(last_mission_number)

        return first_location_name, last_location_name
