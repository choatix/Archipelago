import random
import re

from Main import main as M
from Generate import main as G
from BaseClasses import CollectionState

def SetupMulti():
    multi = M(*G())

    return multi
    #for l in locations:
    #    print(l)

def GetCustomWeights():
    contains_weightings_crystalSA2 = \
        {
            "^Gate \\d Boss$": (75, 0),
            "^(?!Black Market - \\d$)[A-Za-z ]+ - \\d$": (10, 0),
            "^Chao Stat - [A-Za-z0-9- ]+": (0, 50)
        }

    player_weightings = {}

    # Chance for exclude, chance for excluded
    contains_weightings_choatixShadow = \
        {
            "^Charactersanity:[A-Za-z ]+$": (75, 0),
            "^Held Weapon:Weapon:[A-Za-z ]+$": (33, 0),
            "^Boss:[A-Za-z ]+$": (100, 0),
            "^[A-Za-z ]+-Soldier \\d$": (0, 50),
            "^[A-Za-z ]+-Alien \\d$": (0, 50),
            "^[A-Za-z ]+ Key \\d$": (50, 0),

        }

    player_weightings["ChoatixShadow"] = contains_weightings_choatixShadow
    player_weightings["CrystalSA2"] = contains_weightings_crystalSA2

    return player_weightings


def GetCustomWeightings(locations, priorities, exclusions):
    random_exclusions = []
    random_priorities = []

    for l in locations:
        for p_key in priorities.keys():
            priority_weight = priorities[p_key]

            if re.match(p_key, l):
                if priority_weight > 0:
                    r = random.randrange(0, 100)
                    if r < priority_weight:
                        random_priorities.append(l)
        if l not in random_exclusions:
            for e_key in exclusions.keys():
                exclusion_weight = exclusions[e_key]

                if re.match(e_key, l):
                    if exclusion_weight > 0:
                        r = random.randrange(0, 100)
                        if r < exclusion_weight:
                            random_exclusions.append(l)
    print("Exclusions")
    print("\n    - ".join(random_exclusions))

    print("Priorities")
    print("\n    - ".join(random_priorities))

    return random_priorities, random_exclusions


#SetupMulti()