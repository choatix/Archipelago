import json

import worlds.smw.Levels as Levels
import worlds.smw.Items as Items
import worlds.smw.Locations as Locations
from worlds.smw.Names import LocationName

stage = "yoshi2"
open_value = '{'
close_value = '}'

stage_info = Levels.level_info_dict
warp_items = Items.stage_item_table.items()
#location_items = Locations.warp_location_names


map_file = ("C:/Users/Alex/Downloads/poptracker_0-28-0_win64/poptracker/packs/"
            "super_mario_world_randomizer_clean - Copy/super_mario_world_randomizer_p_c/locations/map.json")
f = open(map_file).read()
loaded_map_file = json.loads(f)

map_data = loaded_map_file[0]
if map_data["name"] != "Map":
    print("Map not found")

map_stage_info = map_data["children"]

tracker_item_lines = []
tracker_mapping_lines = []

for stage in stage_info.values():
    base_stage_name = stage.levelName
    stage_name = stage.levelName

    if stage_name in [LocationName.front_door, LocationName.back_door]:
        continue

    if stage_name in ["Yoshi's House", "Top Secret Area"]:
        continue

    if stage_name == "Cheese Bridge":
        stage_name = "Cheese Bridge Area"

    if stage_name == "Choco-Ghost House":
        stage_name = "Choco Ghost House"

    if stage_name == "Forest Secret":
        stage_name = "Forest Secret Area"

    if " - Star Road" in stage_name or "Star Road - " in stage_name:
        #print("Is skippable Star Road",stage_name)
        continue

    map_entry = [l for l in map_stage_info if l["name"] == stage_name]

    if len(map_entry) == 0:
        print("Cannot find map entry for", stage_name)
        continue

    map_entry = map_entry[0]
    stage_short = stage_name.lower().replace("\'", "").replace(" ","").replace("#", "")
    print(stage_short)

    if len([ x for x in map_entry["access_rules"] if x != ""]) == 0:
        map_entry["access_rules"] = [stage_short]
        print("Add access rule for", stage_name)
    else:
        print("Existing access rule for", stage_name)

    stage_item_code = [ s[1].code for s in warp_items if s[0] == "Warp:" + base_stage_name][0]
    #stage_location = [ s for s in location_items if s == "Enter " + stage.levelName][0]

    hex_value = '0x'+('{:x}'.format(stage_item_code).upper())

    json_item_mapping_line = f"[{hex_value}] = {open_value}\"{stage_short}\", \"toggle\"{close_value},"
    tracker_mapping_lines.append(json_item_mapping_line)

    json_item_line = (f"{open_value}\n\t\"name\": \"{stage_name}\",\n\t"
                      f"\"type\": \"toggle\"\n\t"
                      f"\"img\": \"images/items/special_world.png\"\n\t"
                      f"\"codes\": \"{stage_short}\"\n{close_value},")
    tracker_item_lines.append(json_item_line)

for line in tracker_item_lines:
    print(line)

print("---")

for line in tracker_mapping_lines:
    print(line)



f_out = open(map_file+"safe.json", "w")
f_out.write(json.dumps(loaded_map_file, indent=4))



