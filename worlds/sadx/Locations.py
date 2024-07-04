from typing import List, TypedDict


class LocationInfo(TypedDict):
    id: int
    name: str
    needItem: int


location_table: List[LocationInfo] = [
    {"id": 2, "name": "Unlock Tails' Story", "needItem": -1},
    {"id": 3, "name": "Unlock Knuckles' Story", "needItem": 10},
    {"id": 4, "name": "Unlock Amy's Story", "needItem": 10},
    {"id": 5, "name": "Unlock Gamma's Story", "needItem": 12},
    {"id": 6, "name": "Unlock Big's Story", "needItem": 12},

    {"id": 10, "name": "Light shoes upgrade (Sonic)", "needItem": -1},
    {"id": 11, "name": "Crystal ring upgrade (Sonic)", "needItem": 10},
    {"id": 12, "name": "Ancient light upgrade (Sonic)", "needItem": 10},

    {"id": 20, "name": "Jet Ankle upgrade (Tails)", "needItem": 2},
    {"id": 21, "name": "Rhythm Badge upgrade (Tails)", "needItem": 2},

    {"id": 30, "name": "Shovel claw upgrade (Knuckles)", "needItem": 3},
    {"id": 31, "name": "Fighting gloves upgrade (Knuckles)", "needItem": 30},

    {"id": 40, "name": "Long Hammer upgrade (Amy)", "needItem": 4},
    {"id": 41, "name": "Warrior feather upgrade (Amy)", "needItem": 4},

    {"id": 50, "name": "Laser Blaster upgrade (Gamma)", "needItem": 51},
    {"id": 51, "name": "Jet booster upgrade (Gamma)", "needItem": 5},

    {"id": 60, "name": "Life belt upgrade (Big)", "needItem": 6},
    {"id": 61, "name": "Power rod upgrade (Big)", "needItem": 6},

]
