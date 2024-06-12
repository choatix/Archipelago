import random
import typing
import math
import logging

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World

from .AestheticData import chao_name_conversion, sample_chao_names, totally_real_item_names, \
                           all_exits, all_destinations, multi_rooms, single_rooms, room_to_exits_map, exit_to_room_map, valid_kindergarten_exits
from .GateBosses import get_gate_bosses, get_boss_rush_bosses, get_boss_name
from .Items import SA2BItem, ItemData, item_table, upgrades_table, emeralds_table, junk_table, trap_table, item_groups, \
                   eggs_table, fruits_table, seeds_table, hats_table, animals_table, chaos_drives_table
from .Locations import SA2BLocation, all_locations, setup_locations, chao_animal_event_location_table, black_market_location_table
from .Missions import get_mission_table, get_mission_count_table, get_first_and_last_cannons_core_missions
from .Names import ItemName, LocationName
from .Options import SA2BOptions, sa2b_option_groups
from .Regions import create_regions, shuffleable_regions, connect_regions, LevelGate, gate_0_whitelist_regions, \
    gate_0_blacklist_regions
from .Rules import set_rules


class SA2BWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Sonic Adventure 2: Battle randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RaspberrySpaceJam", "PoryGone", "Entiss"]
    )

    tutorials = [setup_en]
    option_groups = sa2b_option_groups


def check_for_impossible_shuffle(shuffled_levels: typing.List[int], gate_0_range: int, multiworld: MultiWorld):
    blacklist_level_count = 0

    for i in range(gate_0_range):
        if shuffled_levels[i] in gate_0_blacklist_regions:
            blacklist_level_count += 1

    if blacklist_level_count == gate_0_range:
        index_to_swap = multiworld.random.randint(0, gate_0_range)
        for i in range(len(shuffled_levels)):
            if shuffled_levels[i] in gate_0_whitelist_regions:
                shuffled_levels[i], shuffled_levels[index_to_swap] = shuffled_levels[index_to_swap], shuffled_levels[i]
                break


class SA2BWorld(World):
    """
    Sonic Adventure 2 Battle is an action platforming game. Play as Sonic, Tails, Knuckles, Shadow, Rouge, and Eggman across 31 stages and prevent the destruction of the earth.
    """
    game: str = "Sonic Adventure 2 Battle"
    options_dataclass = SA2BOptions
    options: SA2BOptions
    topology_present = False

    item_name_groups = item_groups
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    location_table: typing.Dict[str, int]

    mission_map: typing.Dict[int, int]
    mission_count_map: typing.Dict[int, int]
    emblems_for_cannons_core: int
    region_emblem_map: typing.Dict[int, int]
    gate_costs: typing.Dict[int, int]
    gate_bosses: typing.Dict[int, int]
    boss_rush_map: typing.Dict[int, int]
    black_market_costs: typing.Dict[int, int]

    web = SA2BWeb()

    def fill_slot_data(self) -> dict:
        return {
            "ModVersion": 203,
            "Goal": self.options.goal.value,
            "MusicMap": self.generate_music_data(),
            "VoiceMap": self.generate_voice_data(),
            "DefaultEggMap": self.generate_chao_egg_data(),
            "DefaultChaoNameMap": self.generate_chao_name_data(),
            "MissionMap": self.mission_map,
            "MissionCountMap": self.mission_count_map,
            "MusicShuffle": self.options.music_shuffle.value,
            "Narrator": self.options.narrator.value,
            "MinigameTrapDifficulty": self.options.minigame_trap_difficulty.value,
            "RingLoss": self.options.ring_loss.value,
            "RingLink": self.options.ring_link.value,
            "RequiredRank": self.options.required_rank.value,
            "ChaoKeys": self.options.keysanity.value,
            "Whistlesanity": self.options.whistlesanity.value,
            "GoldBeetles": self.options.beetlesanity.value,
            "OmochaoChecks": self.options.omosanity.value,
            "AnimalChecks": self.options.animalsanity.value,
            "KartRaceChecks": self.options.kart_race_checks.value,
            "ChaoStadiumChecks": self.options.chao_stadium_checks.value,
            "ChaoRaceDifficulty": self.options.chao_race_difficulty.value,
            "ChaoKarateDifficulty": self.options.chao_karate_difficulty.value,
            "ChaoStats": self.options.chao_stats.value,
            "ChaoStatsFrequency": self.options.chao_stats_frequency.value,
            "ChaoStatsStamina": self.options.chao_stats_stamina.value,
            "ChaoStatsHidden": self.options.chao_stats_hidden.value,
            "ChaoAnimalParts": self.options.chao_animal_parts.value,
            "ChaoKindergarten": self.options.chao_kindergarten.value,
            "BlackMarketSlots": self.options.black_market_slots.value,
            "BlackMarketData": self.generate_black_market_data(),
            "BlackMarketUnlockCosts": self.black_market_costs,
            "BlackMarketUnlockSetting": self.options.black_market_unlock_costs.value,
            "ChaoERLayout": self.generate_er_layout(),
            "DeathLink": self.options.death_link.value,
            "EmblemPercentageForCannonsCore": self.options.emblem_percentage_for_cannons_core.value,
            "RequiredCannonsCoreMissions": self.options.required_cannons_core_missions.value,
            "NumberOfLevelGates": self.options.number_of_level_gates.value,
            "LevelGateDistribution": self.options.level_gate_distribution.value,
            "EmblemsForCannonsCore": self.emblems_for_cannons_core,
            "RegionEmblemMap": self.region_emblem_map,
            "GateCosts": self.gate_costs,
            "GateBosses": self.gate_bosses,
            "BossRushMap": self.boss_rush_map,
            "PlayerNum": self.player,
        }

    def generate_early(self):
        if self.options.goal.value == 3:
            # Turn off everything else for Grand Prix goal
            self.options.number_of_level_gates.value = 0
            self.options.emblem_percentage_for_cannons_core.value = 0

            self.options.chao_race_difficulty.value = 0
            self.options.chao_karate_difficulty.value = 0
            self.options.chao_stats.value = 0
            self.options.chao_animal_parts.value = 0
            self.options.chao_kindergarten.value = 0
            self.options.black_market_slots.value = 0

            self.options.junk_fill_percentage.value = 100
            self.options.trap_fill_percentage.value = 100
            self.options.omochao_trap_weight.value = 0
            self.options.timestop_trap_weight.value = 0
            self.options.confusion_trap_weight.value = 0
            self.options.tiny_trap_weight.value = 0
            self.options.gravity_trap_weight.value = 0
            self.options.ice_trap_weight.value = 0
            self.options.slow_trap_weight.value = 0
            self.options.cutscene_trap_weight.value = 0

            valid_trap_weights = self.options.exposition_trap_weight.value + \
                                 self.options.reverse_trap_weight.value + \
                                 self.options.pong_trap_weight.value

            if valid_trap_weights == 0:
                self.options.exposition_trap_weight.value = 4
                self.options.reverse_trap_weight.value = 4
                self.options.pong_trap_weight.value = 4

            if self.options.kart_race_checks.value == 0:
                self.options.kart_race_checks.value = 2

            self.gate_bosses = {}
            self.boss_rush_map = {}
        else:
            self.gate_bosses   = get_gate_bosses(self.multiworld, self)
            self.boss_rush_map = get_boss_rush_bosses(self.multiworld, self)

    def create_regions(self):
        self.mission_count_map = get_mission_count_table(self.multiworld, self, self.player)
        self.mission_map       = get_mission_table(self.multiworld, self, self.player, self.mission_count_map)

        self.location_table = setup_locations(self, self.player, self.mission_map, self.mission_count_map)
        create_regions(self.multiworld, self, self.player, self.location_table)

        # Not Generate Basic
        self.black_market_costs = dict()

        if self.options.goal.value in [0, 2, 4, 5, 6]:
            self.multiworld.get_location(LocationName.finalhazard, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.options.goal.value == 1:
            self.multiworld.get_location(LocationName.green_hill, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.options.goal.value == 3:
            self.multiworld.get_location(LocationName.grand_prix, self.player).place_locked_item(self.create_item(ItemName.maria))
        elif self.options.goal.value == 7:
            self.multiworld.get_location(LocationName.chaos_chao, self.player).place_locked_item(self.create_item(ItemName.maria))

            for animal_name in chao_animal_event_location_table.keys():
                animal_region = self.multiworld.get_region(animal_name, self.player)
                animal_event_location = SA2BLocation(self.player, animal_name, None, animal_region)
                animal_region.locations.append(animal_event_location)
                animal_event_item = SA2BItem(animal_name, ItemClassification.progression, None, self.player)
                self.multiworld.get_location(animal_name, self.player).place_locked_item(animal_event_item)

        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = len(self.location_table)
        total_required_locations -= 1; # Locked Victory Location

        if self.options.goal.value != 3:
            # Fill item pool with all required items
            for item in {**upgrades_table}:
                itempool += [self.create_item(item, False, self.options.goal.value)]

            if self.options.goal.value in [1, 2, 6]:
                # Some flavor of Chaos Emerald Hunt
                for item in {**emeralds_table}:
                    itempool.append(self.create_item(item))

            # Black Market
            itempool += [self.create_item(ItemName.market_token) for _ in range(self.options.black_market_slots.value)]

            black_market_unlock_mult = 1.0
            if self.options.black_market_unlock_costs.value == 0:
                black_market_unlock_mult = 0.5
            elif self.options.black_market_unlock_costs.value == 1:
                black_market_unlock_mult = 0.75

            for i in range(self.options.black_market_slots.value):
                self.black_market_costs[i] = math.floor((i + 1) * black_market_unlock_mult)

        # Cap at player-specified Emblem count
        raw_emblem_count = total_required_locations - len(itempool)
        total_emblem_count = min(raw_emblem_count, self.options.max_emblem_cap.value)
        extra_junk_count = raw_emblem_count - total_emblem_count

        self.emblems_for_cannons_core = math.floor(
            total_emblem_count * (self.options.emblem_percentage_for_cannons_core.value / 100.0))

        gate_cost_mult = 1.0
        if self.options.level_gate_costs.value == 0:
            gate_cost_mult = 0.6
        elif self.options.level_gate_costs.value == 1:
            gate_cost_mult = 0.8

        shuffled_region_list = list(range(30))
        emblem_requirement_list = list()
        self.multiworld.random.shuffle(shuffled_region_list)
        levels_per_gate = self.get_levels_per_gate()

        check_for_impossible_shuffle(shuffled_region_list, math.ceil(levels_per_gate[0]), self.multiworld)
        levels_added_to_gate = 0
        total_levels_added = 0
        current_gate = 0
        current_gate_emblems = 0
        self.gate_costs = dict()
        self.gate_costs[0] = 0
        self.gates = list()
        gates = self.gates
        gates.append(LevelGate(0))
        for i in range(30):
            gates[current_gate].gate_levels.append(shuffled_region_list[i])
            emblem_requirement_list.append(current_gate_emblems)
            levels_added_to_gate += 1
            total_levels_added += 1
            if levels_added_to_gate >= levels_per_gate[current_gate]:
                current_gate += 1
                if current_gate > self.options.number_of_level_gates.value:
                    current_gate = self.options.number_of_level_gates.value
                else:
                    current_gate_emblems = max(
                        math.floor(total_emblem_count * math.pow(total_levels_added / 30.0, 2.0) * gate_cost_mult), current_gate)
                    gates.append(LevelGate(current_gate_emblems))
                    self.gate_costs[current_gate] = current_gate_emblems
                levels_added_to_gate = 0

        self.region_emblem_map = dict(zip(shuffled_region_list, emblem_requirement_list))

        first_cannons_core_mission, final_cannons_core_mission = get_first_and_last_cannons_core_missions(self.mission_map, self.mission_count_map)

        connect_regions(self.multiworld, self, self.player, gates, self.emblems_for_cannons_core, self.gate_bosses, self.boss_rush_map, first_cannons_core_mission, final_cannons_core_mission)

        max_required_emblems = max(max(emblem_requirement_list), self.emblems_for_cannons_core)
        itempool += [self.create_item(ItemName.emblem) for _ in range(max_required_emblems)]

        non_required_emblems = (total_emblem_count - max_required_emblems)
        junk_count = math.floor(non_required_emblems * (self.options.junk_fill_percentage.value / 100.0))
        itempool += [self.create_item(ItemName.emblem, True) for _ in range(non_required_emblems - junk_count)]

        # Carve Traps out of junk_count
        trap_weights = []
        trap_weights += ([ItemName.omochao_trap] * self.options.omochao_trap_weight.value)
        trap_weights += ([ItemName.timestop_trap] * self.options.timestop_trap_weight.value)
        trap_weights += ([ItemName.confuse_trap] * self.options.confusion_trap_weight.value)
        trap_weights += ([ItemName.tiny_trap] * self.options.tiny_trap_weight.value)
        trap_weights += ([ItemName.gravity_trap] * self.options.gravity_trap_weight.value)
        trap_weights += ([ItemName.exposition_trap] * self.options.exposition_trap_weight.value)
        #trap_weights += ([ItemName.darkness_trap] * self.options.darkness_trap_weight.value)
        trap_weights += ([ItemName.ice_trap] * self.options.ice_trap_weight.value)
        trap_weights += ([ItemName.slow_trap] * self.options.slow_trap_weight.value)
        trap_weights += ([ItemName.cutscene_trap] * self.options.cutscene_trap_weight.value)
        trap_weights += ([ItemName.reverse_trap] * self.options.reverse_trap_weight.value)
        trap_weights += ([ItemName.pong_trap] * self.options.pong_trap_weight.value)

        junk_count += extra_junk_count
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.options.trap_fill_percentage.value / 100.0))
        junk_count -= trap_count

        chao_active = self.any_chao_locations_active()
        junk_pool = []
        junk_keys = list(junk_table.keys())

        # Chao Junk
        if chao_active and self.options.chaos_drives_enabled:
            junk_keys += list(chaos_drives_table.keys())

        eggs_keys = list(eggs_table.keys())
        fruits_keys = list(fruits_table.keys())
        seeds_keys = list(seeds_table.keys())
        hats_keys = list(hats_table.keys())
        eggs_count = 0
        seeds_count = 0
        hats_count = 0

        for i in range(junk_count):
            junk_type = self.random.randint(0, len(junk_keys) + 3)

            if chao_active and junk_type == len(junk_keys) + 0 and eggs_count < 20:
                junk_item = self.multiworld.random.choice(eggs_keys)
                junk_pool.append(self.create_item(junk_item))
                eggs_count += 1
            elif chao_active and junk_type == len(junk_keys) + 1:
                junk_item = self.multiworld.random.choice(fruits_keys)
                junk_pool.append(self.create_item(junk_item))
            elif chao_active and junk_type == len(junk_keys) + 2 and seeds_count < 12:
                junk_item = self.multiworld.random.choice(seeds_keys)
                junk_pool.append(self.create_item(junk_item))
                seeds_count += 1
            elif chao_active and junk_type == len(junk_keys) + 3 and hats_count < 20:
                junk_item = self.multiworld.random.choice(hats_keys)
                junk_pool.append(self.create_item(junk_item))
                hats_count += 1
            else:
                junk_item = self.multiworld.random.choice(junk_keys)
                junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.multiworld.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        itempool += trap_pool

        self.multiworld.itempool += itempool



    def create_item(self, name: str, force_non_progression=False, goal=0) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif name == ItemName.emblem or \
             name in emeralds_table.keys() or \
             (name == ItemName.knuckles_shovel_claws and goal in [4, 5]):
            classification = ItemClassification.progression_skip_balancing
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        created_item = SA2BItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        junk_keys = list(junk_table.keys())

        # Chao Junk
        if self.any_chao_locations_active():
            junk_keys += list(chaos_drives_table.keys())

        return self.multiworld.random.choice(junk_keys)

    def set_rules(self):
        set_rules(self.multiworld, self, self.player, self.gate_bosses, self.boss_rush_map, self.mission_map, self.mission_count_map, self.black_market_costs)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        if self.options.number_of_level_gates.value > 0 or self.options.goal.value in [4, 5, 6]:
            spoiler_handle.write("\n")
            header_text = "Sonic Adventure 2 Bosses for {}:\n"
            header_text = header_text.format(self.multiworld.player_name[self.player])
            spoiler_handle.write(header_text)

            if self.options.number_of_level_gates.value > 0:
                for x in range(len(self.gate_bosses.values())):
                    text = "Gate {0} Boss: {1}\n"
                    text = text.format((x + 1), get_boss_name(self.gate_bosses[x + 1]))
                    spoiler_handle.writelines(text)
                spoiler_handle.write("\n")

            if self.options.goal.value in [4, 5, 6]:
                for x in range(len(self.boss_rush_map.values())):
                    text = "Boss Rush Boss {0}: {1}\n"
                    text = text.format((x + 1), get_boss_name(self.boss_rush_map[x]))
                    spoiler_handle.writelines(text)
                spoiler_handle.write("\n")

        header_text = "Sonic Adventure 2 Level Gates for {}:\n"
        header_text = header_text.format(self.multiworld.player_name[self.player])
        spoiler_handle.write(header_text)

        for i in self.gates:
            index = self.gates.index(i)
            emblem_count = i.gate_emblem_count
            levels = i.gate_levels

            levels_list = [ Missions.stage_name_prefixes[level].replace(" - ", "") for level in levels ]

            text = "Gate: {0}, Unlock: {1}\n Levels {2}\n"
            text = text.format(index, emblem_count, levels_list)
            spoiler_handle.writelines(text)


        if self.options.mission_shuffle:
            header_text = "Sonic Adventure 2 Missions for {}:\n"
            header_text = header_text.format(self.multiworld.player_name[self.player])
            spoiler_handle.write(header_text)

            #self.mission_count_map = get_mission_count_table(self.multiworld, self, self.player)
            #self.mission_map       = get_mission_table(self.multiworld, self, self.player, self.mission_count_map)

            counter = self.mission_count_map
            missions = self.mission_map

            for missionKey in missions.keys():
                level_name = Missions.stage_name_prefixes[missionKey].replace(" - ", "")
                count = counter[missionKey]
                missionOrder = missions[missionKey]
                missionOrderIndex = Missions.mission_orders[missionOrder]

                possibleMissions = missionOrderIndex[0:count]
                text = "Level: {0} Missions: {1}\n"
                text = text.format(level_name, possibleMissions)
                spoiler_handle.writelines(text)

            # mission_table[level] = level_mission_index



    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        gate_names = [
            LocationName.gate_0_region,
            LocationName.gate_1_region,
            LocationName.gate_2_region,
            LocationName.gate_3_region,
            LocationName.gate_4_region,
            LocationName.gate_5_region,
        ]
        no_hint_region_names = [
            LocationName.cannon_core_region,
            LocationName.chao_race_beginner_region,
            LocationName.chao_race_intermediate_region,
            LocationName.chao_race_expert_region,
            LocationName.chao_karate_beginner_region,
            LocationName.chao_karate_intermediate_region,
            LocationName.chao_karate_expert_region,
            LocationName.chao_karate_super_region,
            LocationName.kart_race_beginner_region,
            LocationName.kart_race_standard_region,
            LocationName.kart_race_expert_region,
            LocationName.chao_kindergarten_region,
            LocationName.black_market_region,
        ]
        er_hint_data = {}
        for i in range(self.options.number_of_level_gates.value + 1):
            gate_name = gate_names[i]
            gate_region = self.multiworld.get_region(gate_name, self.player)
            if not gate_region:
                continue
            for exit in gate_region.exits:
                if exit.connected_region.name in gate_names or exit.connected_region.name in no_hint_region_names:
                    continue
                level_region = exit.connected_region
                for location in level_region.locations:
                    er_hint_data[location.address] = gate_name

        for i in range(self.options.black_market_slots.value):
            location = self.multiworld.get_location(LocationName.chao_black_market_base + str(i + 1), self.player)
            er_hint_data[location.address] = str(self.black_market_costs[i]) + " " + str(ItemName.market_token)


        hint_data[self.player] = er_hint_data

    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool, usefulitempool, filleritempool, fill_locations):
        if multiworld.get_game_players("Sonic Adventure 2 Battle"):
            progitempool.sort(
                key=lambda item: 0 if (item.name != 'Emblem') else 1)

    def get_levels_per_gate(self) -> list:
        levels_per_gate = list()
        max_gate_index = self.options.number_of_level_gates
        average_level_count = 30 / (max_gate_index + 1)
        levels_added = 0

        for i in range(max_gate_index + 1):
            levels_per_gate.append(average_level_count)
            levels_added += average_level_count
        additional_count_iterator = 0
        while levels_added < 30:
            levels_per_gate[additional_count_iterator] += 1
            levels_added += 1
            additional_count_iterator += 1 if additional_count_iterator < max_gate_index else -max_gate_index

        if self.options.level_gate_distribution == 0 or self.options.level_gate_distribution == 2:
            early_distribution = self.options.level_gate_distribution == 0
            levels_to_distribute = 5
            gate_index_offset = 0
            while levels_to_distribute > 0:
                if levels_per_gate[0 + gate_index_offset] == 1 or \
                        levels_per_gate[max_gate_index - gate_index_offset] == 1:
                    break
                if early_distribution:
                    levels_per_gate[0 + gate_index_offset] += 1
                    levels_per_gate[max_gate_index - gate_index_offset] -= 1
                else:
                    levels_per_gate[0 + gate_index_offset] -= 1
                    levels_per_gate[max_gate_index - gate_index_offset] += 1
                gate_index_offset += 1
                if gate_index_offset > math.floor(max_gate_index / 2):
                    gate_index_offset = 0
                levels_to_distribute -= 1

        return levels_per_gate

    def any_chao_locations_active(self) -> bool:
        if self.options.chao_race_difficulty.value > 0 or \
           self.options.chao_karate_difficulty.value > 0 or \
           self.options.chao_stats.value > 0 or \
           self.options.chao_animal_parts or \
           self.options.chao_kindergarten or \
           self.options.black_market_slots.value > 0:
            return True;

        return False

    def generate_music_data(self) -> typing.Dict[int, int]:
        if self.options.music_shuffle == "levels":
            musiclist_o = list(range(0, 47))
            musiclist_s = musiclist_o.copy()
            self.random.shuffle(musiclist_s)
            musiclist_o.extend(range(47, 78))
            musiclist_s.extend(range(47, 78))

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                for i in range(len(musiclist_s)):
                    if self.random.randint(0,1):
                        musiclist_s[i] += 100

            return dict(zip(musiclist_o, musiclist_s))
        elif self.options.music_shuffle == "full":
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()
            self.random.shuffle(musiclist_s)

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                for i in range(len(musiclist_s)):
                    if self.random.randint(0,1):
                        musiclist_s[i] += 100

            return dict(zip(musiclist_o, musiclist_s))
        elif self.options.music_shuffle == "singularity":
            musiclist_o = list(range(0, 78))
            musiclist_s = [self.random.choice(musiclist_o)] * len(musiclist_o)

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                if self.random.randint(0,1):
                    musiclist_s = [x+100 for x in musiclist_s]

            return dict(zip(musiclist_o, musiclist_s))
        else:
            musiclist_o = list(range(0, 78))
            musiclist_s = musiclist_o.copy()

            if self.options.sadx_music.value == 1:
                musiclist_s = [x+100 for x in musiclist_s]
            elif self.options.sadx_music.value == 2:
                for i in range(len(musiclist_s)):
                    if self.random.randint(0,1):
                        musiclist_s[i] += 100

            return dict(zip(musiclist_o, musiclist_s))

    def voice_charater_map(self):
        return \
            {'Pilot': [0, 2, 4, 5], 'Radio': [1, 3, 6, 1744, 2010],
             'Sonic': [7, 8, 9, 10, 11, 12, 13, 16, 18, 19, 20, 21, 23, 24, 25, 27, 29, 30, 31, 62, 64, 67, 69, 71, 74,
                       77, 78, 80, 82, 84, 85, 92, 94, 95, 98, 102, 104, 119, 123, 125, 128, 131, 132, 133, 136, 140,
                       142, 144, 151, 153, 158, 162, 163, 166, 168, 169, 172, 173, 180, 187, 189, 194, 219, 221, 224,
                       228, 233, 234, 241, 245, 248, 249, 251, 252, 255, 258, 260, 269, 277, 283, 341, 342, 345, 346,
                       347, 348, 349, 351, 352, 353, 355, 357, 358, 359, 408, 409, 411, 413, 415, 453, 455, 458, 459,
                       466, 507, 509, 512, 516, 526, 547, 549, 560, 580, 582, 583, 602, 625, 627, 629, 631, 649, 657,
                       658, 666, 681, 683, 684, 879, 890, 901, 912, 923, 934, 945, 956, 967, 978, 989, 1000, 1011, 1022,
                       1033, 1044, 1054, 1065, 1076, 1087, 1098, 1109, 1120, 1131, 1142, 1320, 1326, 1403, 1409, 1443,
                       1445, 1447, 1449, 1451, 1453, 1455, 1457, 1459, 1461, 1463, 1465, 1467, 1469, 1471, 1473, 1475,
                       1477, 1479, 1481, 1483, 1485, 1487, 1489, 1491, 1493, 1495, 1497, 1499, 1501, 1503, 1505, 1507,
                       1509, 1511, 1513, 1515, 1517, 1519, 1521, 1523, 1525, 1527, 1529, 1531, 1533, 1535, 1537, 1539,
                       1541, 1543, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1688, 1689, 1723, 1728, 1733, 1748, 1749,
                       1833, 1834, 1839, 1840, 1858, 1859, 1924, 1925, 2049, 2051, 2055, 2057, 2061, 2063, 2068, 2069,
                       2072, 2073, 2074, 2078, 2079, 2144, 2151, 2152, 2153, 2154, 2155, 2156, 2157, 2158, 2162, 2163,
                       2164, 2165, 2166, 2167, 2168, 2169, 2170, 2201, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 2332,
                       2333, 2334, 2352, 2353, 2354, 2355, 2356, 2357, 2358, 2359, 2360, 2361, 2362, 2363, 2483, 2484,
                       2485, 2495, 2496, 2497, 2498, 2499, 2520, 2521, 2522, 2523, 2524, 2525, 2530, 2531, 2532, 2533,
                       2534, 2539, 2540, 2541, 2542, 2543, 2544, 2545, 2555, 2556],
             'Shadow': [14, 15, 22, 26, 79, 81, 250, 253, 254, 256, 267, 270, 280, 284, 297, 298, 300, 303, 305, 330,
                        331, 334, 336, 339, 340, 343, 344, 350, 354, 364, 365, 368, 369, 370, 372, 399, 404, 405, 406,
                        407, 410, 412, 416, 418, 420, 421, 424, 429, 431, 435, 443, 447, 448, 528, 530, 532, 534, 536,
                        541, 543, 545, 546, 548, 550, 608, 616, 621, 623, 630, 632, 639, 656, 659, 660, 876, 887, 898,
                        909, 920, 931, 942, 953, 965, 975, 986, 997, 1008, 1019, 1030, 1042, 1052, 1062, 1073, 1084,
                        1095, 1106, 1117, 1128, 1139, 1324, 1330, 1402, 1408, 1442, 1444, 1446, 1448, 1450, 1452, 1454,
                        1456, 1458, 1460, 1462, 1464, 1466, 1468, 1470, 1472, 1474, 1476, 1478, 1480, 1482, 1484, 1486,
                        1488, 1490, 1492, 1494, 1496, 1498, 1500, 1502, 1504, 1506, 1508, 1510, 1512, 1514, 1516, 1518,
                        1520, 1522, 1524, 1526, 1528, 1530, 1532, 1534, 1536, 1538, 1540, 1542, 1544, 1831, 1832, 1868,
                        1869, 1872, 1873, 1967, 1968, 2040, 2048, 2050, 2054, 2056, 2060, 2062, 2070, 2071, 2075, 2076,
                        2077, 2080, 2081, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2139, 2140, 2141, 2142, 2143,
                        2145, 2200, 2374, 2375, 2376, 2377, 2378, 2389, 2390, 2391, 2392, 2424, 2425, 2426, 2427, 2428,
                        2429, 2430, 2435, 2436, 2437, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471, 2516, 2517,
                        2518, 2519, 2553, 2554], 'G.U.N.': [28],
             'Rouge': [32, 35, 39, 42, 43, 46, 195, 198, 200, 201, 203, 204, 206, 208, 210, 213, 215, 216, 217, 272,
                       276, 286, 307, 310, 314, 317, 318, 321, 360, 361, 362, 374, 375, 377, 379, 381, 383, 385, 401,
                       402, 403, 422, 423, 425, 428, 430, 433, 434, 436, 438, 442, 444, 445, 446, 467, 468, 469, 470,
                       471, 472, 473, 476, 478, 479, 481, 482, 484, 486, 488, 491, 493, 494, 495, 529, 531, 533, 535,
                       537, 538, 539, 542, 544, 562, 564, 565, 566, 584, 586, 587, 591, 597, 598, 645, 652, 664, 665,
                       667, 677, 678, 679, 875, 886, 897, 908, 919, 930, 941, 952, 963, 974, 985, 996, 1007, 1018, 1029,
                       1041, 1051, 1061, 1072, 1083, 1094, 1105, 1116, 1127, 1138, 1174, 1176, 1178, 1180, 1182, 1184,
                       1186, 1188, 1190, 1192, 1194, 1196, 1198, 1200, 1202, 1204, 1206, 1208, 1210, 1212, 1214, 1216,
                       1218, 1220, 1222, 1224, 1226, 1228, 1230, 1232, 1234, 1236, 1238, 1240, 1242, 1244, 1246, 1248,
                       1250, 1252, 1254, 1256, 1258, 1260, 1262, 1264, 1266, 1268, 1270, 1272, 1274, 1276, 1278, 1280,
                       1282, 1284, 1286, 1288, 1290, 1292, 1293, 1325, 1331, 1401, 1407, 1722, 1727, 1737, 1738, 1739,
                       1741, 1742, 1743, 1772, 1773, 1791, 1792, 1895, 1896, 1963, 1964, 2052, 2067, 2086, 2088, 2111,
                       2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2199, 2379, 2380, 2381, 2382, 2383,
                       2384, 2393, 2394, 2395, 2396, 2397, 2415, 2416, 2417, 2418, 2419, 2420, 2421, 2422, 2423, 2431,
                       2432, 2433, 2434, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2449, 2551, 2552],
             'Knuckles': [33, 34, 36, 38, 41, 44, 47, 86, 101, 108, 109, 134, 137, 143, 145, 146, 147, 148, 165, 167,
                          196, 197, 199, 202, 205, 207, 209, 211, 212, 214, 243, 244, 246, 247, 274, 279, 308, 309, 311,
                          313, 316, 319, 322, 450, 474, 475, 477, 480, 483, 485, 487, 489, 490, 492, 559, 561, 563, 567,
                          575, 578, 599, 624, 628, 634, 635, 638, 640, 642, 676, 680, 873, 884, 895, 906, 917, 928, 939,
                          950, 961, 972, 983, 994, 1005, 1016, 1027, 1039, 1049, 1059, 1070, 1081, 1092, 1103, 1114,
                          1125, 1136, 1173, 1175, 1177, 1179, 1181, 1183, 1185, 1187, 1189, 1191, 1193, 1195, 1197,
                          1199, 1201, 1203, 1205, 1207, 1209, 1211, 1213, 1215, 1217, 1219, 1221, 1223, 1225, 1227,
                          1229, 1231, 1233, 1235, 1237, 1239, 1241, 1243, 1245, 1247, 1249, 1251, 1253, 1255, 1257,
                          1259, 1261, 1263, 1265, 1267, 1269, 1271, 1273, 1275, 1277, 1279, 1281, 1283, 1285, 1287,
                          1289, 1291, 1322, 1328, 1400, 1406, 1420, 1421, 1721, 1726, 1760, 1761, 1781, 1782, 1909,
                          1910, 1911, 1938, 1939, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035,
                          2058, 2085, 2090, 2198, 2335, 2336, 2337, 2338, 2339, 2340, 2364, 2365, 2366, 2367, 2455,
                          2456, 2457, 2458, 2459, 2486, 2487, 2488, 2489, 2490, 2491, 2492, 2493, 2494, 2505, 2506,
                          2507, 2508, 2526, 2527, 2528, 2529, 2548, 2549, 2550],
             'Eggman': [37, 40, 45, 48, 54, 83, 87, 88, 89, 90, 116, 118, 121, 150, 154, 192, 218, 220, 222, 225, 226,
                        227, 229, 235, 237, 239, 242, 268, 281, 289, 290, 291, 292, 293, 294, 295, 296, 299, 301, 302,
                        304, 306, 312, 315, 320, 323, 324, 325, 327, 329, 363, 366, 367, 371, 373, 376, 378, 380, 382,
                        384, 386, 387, 388, 389, 390, 393, 395, 396, 400, 414, 426, 427, 432, 437, 439, 440, 441, 449,
                        452, 456, 457, 460, 461, 462, 496, 497, 498, 499, 500, 501, 503, 505, 506, 508, 510, 513, 514,
                        515, 517, 520, 522, 524, 527, 540, 551, 552, 556, 557, 558, 577, 579, 581, 585, 592, 595, 601,
                        603, 641, 651, 668, 671, 673, 674, 872, 883, 894, 905, 916, 927, 938, 949, 960, 971, 982, 993,
                        1004, 1015, 1026, 1038, 1048, 1058, 1069, 1080, 1091, 1102, 1113, 1124, 1135, 1323, 1329, 1399,
                        1405, 1564, 1566, 1568, 1570, 1572, 1574, 1576, 1578, 1580, 1582, 1584, 1586, 1588, 1590, 1592,
                        1594, 1596, 1598, 1600, 1602, 1604, 1606, 1608, 1610, 1612, 1614, 1616, 1618, 1620, 1622, 1624,
                        1626, 1628, 1630, 1632, 1634, 1636, 1638, 1640, 1642, 1644, 1646, 1648, 1650, 1652, 1654, 1656,
                        1658, 1660, 1662, 1664, 1666, 1668, 1670, 1673, 1674, 1675, 1677, 1690, 1691, 1692, 1693, 1694,
                        1698, 1700, 1701, 1702, 1720, 1725, 1740, 1850, 1851, 1883, 1884, 1945, 1946, 1947, 1948, 1949,
                        1950, 1971, 1972, 1980, 1981, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2059, 2082, 2087, 2197, 2368, 2369, 2370, 2371, 2372, 2373,
                        2385, 2386, 2387, 2388, 2398, 2399, 2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2438,
                        2439, 2440, 2441, 2450, 2451, 2452, 2453, 2454, 2460, 2461, 2462, 2546, 2547],
             'Tails': [49, 50, 51, 52, 53, 56, 58, 60, 93, 96, 99, 103, 111, 113, 126, 127, 138, 139, 141, 149, 152,
                       157, 164, 171, 174, 176, 177, 178, 181, 182, 184, 185, 186, 190, 191, 193, 223, 230, 232, 238,
                       240, 257, 259, 271, 282, 398, 451, 454, 465, 511, 518, 523, 525, 594, 596, 600, 650, 669, 670,
                       672, 675, 880, 891, 902, 913, 924, 935, 946, 957, 968, 979, 990, 1001, 1012, 1023, 1034, 1045,
                       1055, 1066, 1077, 1088, 1099, 1110, 1121, 1132, 1143, 1321, 1327, 1404, 1410, 1565, 1567, 1569,
                       1571, 1573, 1575, 1577, 1579, 1581, 1583, 1585, 1587, 1589, 1591, 1593, 1595, 1597, 1599, 1601,
                       1603, 1605, 1607, 1609, 1611, 1613, 1615, 1617, 1619, 1621, 1623, 1625, 1627, 1629, 1631, 1633,
                       1635, 1637, 1639, 1641, 1643, 1645, 1647, 1649, 1651, 1653, 1655, 1657, 1659, 1661, 1663, 1665,
                       1667, 1669, 1671, 1672, 1699, 1724, 1729, 1730, 1731, 1732, 1734, 1735, 1736, 1825, 1826, 1863,
                       1864, 1917, 1918, 1943, 1944, 2064, 2084, 2089, 2174, 2175, 2176, 2177, 2178, 2179, 2180, 2181,
                       2185, 2186, 2187, 2188, 2189, 2190, 2191, 2202, 2341, 2342, 2343, 2344, 2345, 2346, 2347, 2348,
                       2349, 2350, 2351, 2409, 2410, 2411, 2412, 2413, 2414, 2472, 2473, 2474, 2475, 2476, 2477, 2478,
                       2479, 2480, 2481, 2482, 2500, 2501, 2502, 2503, 2504, 2535, 2536, 2537, 2538, 2557, 2558],
             'Amy': [55, 57, 59, 61, 63, 65, 66, 68, 70, 72, 73, 75, 76, 91, 100, 106, 107, 110, 112, 135, 155, 156,
                     170, 175, 179, 183, 188, 231, 236, 261, 262, 273, 278, 285, 391, 392, 394, 397, 463, 464, 502, 504,
                     519, 521, 576, 593, 604, 605, 606, 607, 609, 610, 611, 612, 613, 614, 622, 648, 653, 682, 870, 881,
                     892, 903, 914, 925, 936, 947, 958, 969, 980, 991, 1002, 1013, 1024, 1036, 1046, 1056, 1067, 1078,
                     1089, 1100, 1111, 1122, 1133, 2053, 2065, 2066, 2083, 2091, 2509, 2510, 2511, 2512, 2513, 2514,
                     2515, 2559, 2560, 2561, 2562, 2563, 2564, 2565, 2566, 2567, 2568, 2569, 2570, 2571, 2572, 2573,
                     2574, 2575, 2576, 2577, 2578, 2579, 2580, 2581, 2582], 'Police': [97, 105],
             'Secretary': [114, 130, 643, 646, 661, 663, 877, 878, 888, 889, 899, 900, 910, 911, 921, 922, 932, 933,
                           943, 944, 954, 955, 964, 966, 976, 977, 987, 988, 998, 999, 1009, 1010, 1020, 1021, 1031,
                           1032, 1035, 1043, 1053, 1063, 1064, 1074, 1075, 1085, 1086, 1096, 1097, 1107, 1108, 1118,
                           1119, 1129, 1130, 1140, 1141], 'President': [115, 117, 120, 122, 124, 129, 644, 647, 662],
             'Announcer': [159, 160, 161, 288, 1676, 1695, 1696, 1697, 1841, 1842, 1843, 1844, 1845, 1846, 1852, 1853,
                           1854],
             'Narrator': [263, 264, 265, 287, 553, 554, 555, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859,
                          860, 861, 862, 863, 864, 865, 866, 867, 868, 869],
             'Maria': [266, 275, 332, 335, 337, 338, 417, 419, 615, 617, 618, 619, 620, 654, 655, 874, 885, 896, 907,
                       918, 929, 940, 951, 962, 973, 984, 995, 1006, 1017, 1028, 1040, 1050, 1060, 1071, 1082, 1093,
                       1104, 1115, 1126, 1137], 'Reporter': [326, 328],
             'Soldier': [333, 356, 572, 573, 2009, 2011, 2012, 2016, 2017, 2018, 2021, 2022, 2023],
             'Gerald': [568, 569, 570, 571, 574, 588, 589, 590, 626], 'Biolizard': [633, 636, 637],
             'Omochao': [685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703,
                         704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722,
                         723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741,
                         742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760,
                         761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779,
                         780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798,
                         799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817,
                         818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836,
                         837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 871, 882, 893, 904, 915, 926, 937, 948,
                         959, 970, 981, 992, 1003, 1014, 1025, 1037, 1047, 1057, 1068, 1079, 1090, 1101, 1112, 1123,
                         1134, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158,
                         1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1294, 1295,
                         1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311,
                         1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339,
                         1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355,
                         1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1370, 1371,
                         1372, 1373, 1374, 1375, 1376, 1377, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387,
                         1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1411, 1412, 1413, 1414, 1415,
                         1416, 1417, 1418, 1419, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433,
                         1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1559,
                         1560, 1561, 1562, 1563, 1678, 1679, 1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1703, 1704,
                         1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1745,
                         1746, 1747, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1762, 1763, 1764, 1765,
                         1766, 1767, 1768, 1769, 1770, 1771, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1783, 1784, 1785,
                         1786, 1787, 1788, 1789, 1790, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803,
                         1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819,
                         1820, 1821, 1822, 1823, 1824, 1827, 1828, 1829, 1830, 1835, 1836, 1837, 1838, 1847, 1848, 1849,
                         1855, 1856, 1857, 1860, 1861, 1862, 1865, 1866, 1867, 1870, 1871, 1874, 1875, 1876, 1877, 1878,
                         1879, 1880, 1881, 1882, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1897, 1898,
                         1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1912, 1913, 1914, 1915, 1916, 1919,
                         1920, 1921, 1922, 1923, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937,
                         1940, 1941, 1942, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1965,
                         1966, 1969, 1970, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1982, 1993, 1994, 1995, 1996, 2004,
                         2005, 2006, 2007, 2008, 2013, 2014, 2015, 2019, 2020, 2024, 2036, 2037, 2038, 2039, 2041, 2042,
                         2043, 2044, 2045, 2046, 2047, 2108, 2109, 2110, 2122, 2123, 2124, 2125, 2126, 2135, 2136, 2137,
                         2138, 2146, 2147, 2148, 2149, 2150, 2159, 2160, 2161, 2171, 2172, 2173, 2182, 2183, 2184, 2192,
                         2193, 2194, 2195, 2196, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214,
                         2215, 2216, 2217, 2218, 2219, 2220, 2221, 2222, 2223, 2224, 2225, 2226, 2227, 2228, 2229, 2230,
                         2231, 2232, 2233, 2234, 2235, 2236, 2237, 2238, 2239, 2240, 2241, 2242, 2243, 2244, 2245, 2246,
                         2247, 2248, 2249, 2250, 2251, 2252, 2253, 2254, 2255, 2256, 2257, 2258, 2259, 2260, 2261, 2262,
                         2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278,
                         2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294,
                         2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309, 2310,
                         2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324],
             'King Boom Boo': [2092, 2093, 2094, 2095, 2096, 2097, 2098, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106,
                               2107], 'Chaos Zero': [2583, 2584, 2585],
             'Chao': [2586, 2587, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2595, 2596],
             'Dark Chao': [2597, 2598, 2599, 2600, 2601, 2602, 2603, 2604, 2605, 2606, 2607],
             'Metal Sonic': [2608, 2609, 2610, 2611],
             'Tikal': [2612, 2613, 2614, 2615, 2616, 2617, 2618, 2619, 2620, 2621, 2622]}

    def generate_voice_data_no_omochao(self):

        valid_characters = []
        invalid_characters = ["Omochao"]

        vmap = self.voice_charater_map()
        voicelist_o = list(range(0, 2623))

        voicelist_s = []
        for char in vmap.keys():
            if len(valid_characters) > 0:
                if char not in valid_characters:
                    continue

            if len(invalid_characters) > 0:
                if char in invalid_characters:
                    continue

            voicelist_s.extend(vmap[char])

        while len(voicelist_o) != len(voicelist_s):
            sizeToAdd = len(voicelist_o) - len(voicelist_s)
            if sizeToAdd > len(voicelist_s):
                sizeToAdd = len(voicelist_s)
            voicelist_s.extend(random.sample(voicelist_s, sizeToAdd))

        return voicelist_s


    def generate_voice_data(self) -> typing.Dict[int, int]:
        if self.options.voice_shuffle == "shuffled_no_omochao":
            voicelist_o = list(range(0, 2623))
            voicelist_s = self.generate_voice_data_no_omochao()
            self.random.shuffle(voicelist_s)
            return dict(zip(voicelist_o, voicelist_s))

        if self.options.voice_shuffle == "shuffled":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.random.shuffle(voicelist_s)
            return dict(zip(voicelist_o, voicelist_s))
        elif self.options.voice_shuffle == "rude":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.random.shuffle(voicelist_s)

            for i in range(len(voicelist_s)):
                if self.random.randint(1,100) > 80:
                    voicelist_s[i] = 17

            return dict(zip(voicelist_o, voicelist_s))
        elif self.options.voice_shuffle == "chao":
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()
            self.random.shuffle(voicelist_s)

            for i in range(len(voicelist_s)):
                voicelist_s[i] = self.random.choice(range(2586, 2608))

            return dict(zip(voicelist_o, voicelist_s))
        elif self.options.voice_shuffle == "singularity":
            voicelist_o = list(range(0, 2623))
            voicelist_s = [self.random.choice(voicelist_o)] * len(voicelist_o)

            return dict(zip(voicelist_o, voicelist_s))
        else:
            voicelist_o = list(range(0, 2623))
            voicelist_s = voicelist_o.copy()

            return dict(zip(voicelist_o, voicelist_s))

    def generate_chao_egg_data(self) -> typing.Dict[int, int]:
        if self.options.shuffle_starting_chao_eggs:
            egglist_o = list(range(0, 4))
            egglist_s = self.random.sample(range(0,54), 4)

            return dict(zip(egglist_o, egglist_s))
        else:
            # Indicate these are not shuffled
            egglist_o = [0, 1, 2, 3]
            egglist_s = [255, 255, 255, 255]

            return dict(zip(egglist_o, egglist_s))

    def generate_chao_name_data(self) -> typing.Dict[int, int]:
        number_of_names = 30
        name_list_o = list(range(number_of_names * 7))
        name_list_s = []

        name_list_base = []
        name_list_copy = list(self.multiworld.player_name.values())
        name_list_copy.remove(self.multiworld.player_name[self.player])

        if self.options.replace_chao_names.value:
            chao_name_options = []
        else:
            chao_name_options = sample_chao_names.copy()

        chao_name_options.extend(list(self.options.additional_chao_names.value))

        if len(name_list_copy) >= number_of_names:
            name_list_base = self.random.sample(name_list_copy, number_of_names)
        else:
            name_list_base = name_list_copy
            self.random.shuffle(name_list_base)

            while len(chao_name_options) < number_of_names - len(name_list_base):
                chao_name_options.append(random.choice(chao_name_options))

            name_list_base += self.random.sample(chao_name_options, number_of_names - len(name_list_base))

        for name in name_list_base:
            for char_idx in range(7):
                if char_idx < len(name):
                    name_list_s.append(chao_name_conversion.get(name[char_idx], 0x5F))
                else:
                    name_list_s.append(0x00)

        return dict(zip(name_list_o, name_list_s))

    def generate_black_market_data(self) -> typing.Dict[int, int]:
        if self.options.black_market_slots.value == 0:
            return {}

        ring_costs = [50, 75, 100]

        market_data = {}
        item_names = []
        player_names = []
        progression_flags = []

        if self.options.replace_trap_names:
            totally_real_item_names_copy = []
        else:
            totally_real_item_names_copy = totally_real_item_names.copy()

        totally_real_item_names_copy.extend(list(self.options.additional_trap_names.value))

        location_names = [(LocationName.chao_black_market_base + str(i)) for i in range(1, self.options.black_market_slots.value + 1)]
        locations = [self.multiworld.get_location(location_name, self.player) for location_name in location_names]
        for location in locations:
            if location.item.classification & ItemClassification.trap:
                item_name = self.random.choice(totally_real_item_names_copy)
                totally_real_item_names_copy.remove(item_name)
                item_names.append(item_name)
            else:
                item_names.append(location.item.name)
            player_names.append(self.multiworld.player_name[location.item.player])

            if location.item.classification & ItemClassification.progression or location.item.classification & ItemClassification.trap:
                progression_flags.append(2)
            elif location.item.classification & ItemClassification.useful:
                progression_flags.append(1)
            else:
                progression_flags.append(0)

        for item_idx in range(self.options.black_market_slots.value):
            for chr_idx in range(len(item_names[item_idx][:26])):
                market_data[(item_idx * 46) + chr_idx] = ord(item_names[item_idx][chr_idx])
            for chr_idx in range(len(player_names[item_idx][:16])):
                market_data[(item_idx * 46) + 26 + chr_idx] = ord(player_names[item_idx][chr_idx])

            # TODO: This feature could do with more configuration
            multiplier_min = self.options.black_market_price_multiplier_min
            random_multiplier = random.choice(range(multiplier_min, self.options.black_market_price_multiplier.value))
            item_price = math.floor(ring_costs[progression_flags[item_idx]] * random_multiplier)
            market_data[(item_idx * 46) + 42] = item_price

        return market_data

    def generate_er_layout(self) -> typing.Dict[int, int]:
        if not self.options.chao_entrance_randomization:
            return {}

        er_layout = {}

        start_exit = self.random.randint(0, 3)
        accessible_rooms = []

        multi_rooms_copy      = multi_rooms.copy()
        single_rooms_copy     = single_rooms.copy()
        all_exits_copy        = all_exits.copy()
        all_destinations_copy = all_destinations.copy()

        multi_rooms_copy.remove(0x07)
        accessible_rooms.append(0x07)

        # Place Kindergarten somewhere sane
        exit_choice = self.random.choice(valid_kindergarten_exits)
        exit_room = exit_to_room_map[exit_choice]
        all_exits_copy.remove(exit_choice)
        multi_rooms_copy.remove(exit_room)

        destination = 0x06
        single_rooms_copy.remove(destination)
        all_destinations_copy.remove(destination)

        er_layout[exit_choice] = destination

        reverse_exit = self.random.choice(room_to_exits_map[destination])

        er_layout[reverse_exit] = exit_to_room_map[exit_choice]

        all_exits_copy.remove(reverse_exit)
        all_destinations_copy.remove(exit_room)

        # Connect multi-exit rooms
        loop_guard = 0
        while len(multi_rooms_copy) > 0:
            loop_guard += 1
            if loop_guard > 2000:
                logging.warning(f"Failed to generate Chao Entrance Randomization for player: {self.multiworld.player_name[self.player]}")
                return {}

            exit_room = self.random.choice(accessible_rooms)
            possible_exits = [exit for exit in room_to_exits_map[exit_room] if exit in all_exits_copy]
            if len(possible_exits) == 0:
                continue
            exit_choice = self.random.choice(possible_exits)
            all_exits_copy.remove(exit_choice)

            destination = self.random.choice(multi_rooms_copy)
            multi_rooms_copy.remove(destination)
            all_destinations_copy.remove(destination)
            accessible_rooms.append(destination)

            er_layout[exit_choice] = destination

            reverse_exit = self.random.choice(room_to_exits_map[destination])

            er_layout[reverse_exit] = exit_room

            all_exits_copy.remove(reverse_exit)
            all_destinations_copy.remove(exit_room)

        # Connect dead-end rooms
        loop_guard = 0
        while len(single_rooms_copy) > 0:
            loop_guard += 1
            if loop_guard > 2000:
                logging.warning(f"Failed to generate Chao Entrance Randomization for player: {self.multiworld.player_name[self.player]}")
                return {}

            exit_room = self.random.choice(accessible_rooms)
            possible_exits = [exit for exit in room_to_exits_map[exit_room] if exit in all_exits_copy]
            if len(possible_exits) == 0:
                continue
            exit_choice = self.random.choice(possible_exits)
            all_exits_copy.remove(exit_choice)

            destination = self.random.choice(single_rooms_copy)
            single_rooms_copy.remove(destination)
            all_destinations_copy.remove(destination)

            er_layout[exit_choice] = destination

            reverse_exit = self.random.choice(room_to_exits_map[destination])

            er_layout[reverse_exit] = exit_room

            all_exits_copy.remove(reverse_exit)
            all_destinations_copy.remove(exit_room)

        # Connect remaining exits
        loop_guard = 0
        while len(all_exits_copy) > 0:
            loop_guard += 1
            if loop_guard > 2000:
                logging.warning(f"Failed to generate Chao Entrance Randomization for player: {self.multiworld.player_name[self.player]}")
                return {}

            exit_room = self.random.choice(all_destinations_copy)
            possible_exits = [exit for exit in room_to_exits_map[exit_room] if exit in all_exits_copy]
            if len(possible_exits) == 0:
                continue
            exit_choice = self.random.choice(possible_exits)
            all_exits_copy.remove(exit_choice)
            all_destinations_copy.remove(exit_room)

            destination = self.random.choice(all_destinations_copy)
            all_destinations_copy.remove(destination)

            er_layout[exit_choice] = destination

            possible_reverse_exits = [exit for exit in room_to_exits_map[destination] if exit in all_exits_copy]
            reverse_exit = self.random.choice(possible_reverse_exits)

            er_layout[reverse_exit] = exit_room

            all_exits_copy.remove(reverse_exit)

        return er_layout
