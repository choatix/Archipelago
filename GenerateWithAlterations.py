import os

import yaml

import Generate
from Utils import parse_yaml
import CustomiseYaml
import settings

from worlds import network_data_package

settings = settings.get_settings()
if "generator" in settings:
    generator_settings = settings["generator"]
    if "players_unmodified_path" in generator_settings:
        unmodified_path = generator_settings["players_unmodified_path"]
        players_path = generator_settings["player_files_path"]
        files = os.listdir(unmodified_path)
        for file in files:
            unmodified_file = unmodified_path+"/"+file
            end_file = players_path+"/"+file
            with (open(unmodified_file, encoding="utf-8-sig") as f):
                options = parse_yaml(f.read())

                game = options["game"]
                game_options = options[game]
                if "alters" in game_options:

                    game_lookup = network_data_package["games"][game]
                    location_names = list(game_lookup["location_name_to_id"].keys())

                    #print(location_names)

                    alter_exclusions = {}
                    alter_priorities = {}
                    if "exclusions" in game_options["alters"]:
                        alter_exclusions = game_options["alters"]["exclusions"]

                    if "priorities" in game_options["alters"]:
                        alter_priorities = game_options["alters"]["priorities"]

                    priorities,exclusions = CustomiseYaml\
                        .GetCustomWeightings(location_names, alter_priorities, alter_exclusions)

                    game_options["exclude_locations"].extend(exclusions)
                    game_options["priority_locations"].extend(priorities)

                with open(end_file, "w") as yaml_file:
                    yaml.dump(options, yaml_file, default_flow_style=False)

print("test complete")

from Main import main as ERmain
erargs, seed = Generate.main()
multiworld = ERmain(erargs, seed)