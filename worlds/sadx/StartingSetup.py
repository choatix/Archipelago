from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters
from .Enums import Character, StartingArea
from .Names import ItemName
from .Options import SonicAdventureDXOptions


class StarterSetup:
    def __init__(self, character: Character = None, area: StartingArea = None, item: str = None):
        self.character = character
        self.area = area
        self.item = item


def generate_early_sadx(world: World, options: SonicAdventureDXOptions) -> StarterSetup:
    starter_character: Character = None
    starter_area: StartingArea = None
    starter_item: str = None
    possible_characters = get_playable_characters(options)
    if len(possible_characters) == 0:
        raise OptionError("You need at least one playable character")

    starter_character = world.random.choice(possible_characters)

    # Random starting location
    if options.random_starting_location == 0:
        starter_area = world.random.choice(list(starting_area_items[starter_character].keys()))
        possible_starting_items = starting_area_items[starter_character][starter_area]
        if len(possible_starting_items) > 0:
            starter_item = world.random.choice(possible_starting_items)
    # Random starting location no items
    elif options.random_starting_location == 1:
        starter_area = world.random.choice(list(starting_area_no_items[starter_character].keys()))
    # Station Square
    elif options.random_starting_location == 2:
        starter_area = StartingArea.StationSquare
        possible_starting_items = starting_area_items[starter_character][starter_area]
        if len(possible_starting_items) > 0:
            starter_item = world.random.choice(possible_starting_items)
    # Station Square no items
    elif options.random_starting_location == 3:
        starter_area = StartingArea.StationSquare

    return StarterSetup(starter_character, starter_area, starter_item)


starting_area_items = {
    Character.Sonic: {
        StartingArea.StationSquare: [ItemName.KeyItem.TwinkleParkTicket,
                                     ItemName.KeyItem.EmployeeCard],
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.WindStone],
        StartingArea.EggCarrier: []
    },
    Character.Tails: {
        StartingArea.StationSquare: [ItemName.KeyItem.EmployeeCard],
        StartingArea.Casino: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.WindStone],
        StartingArea.EggCarrier: []
    },
    Character.Knuckles: {
        StartingArea.StationSquare: [],
        StartingArea.Casino: [],
    },
    Character.Amy: {
        StartingArea.StationSquare: [ItemName.KeyItem.TwinkleParkTicket],
        StartingArea.Jungle: [],
        StartingArea.EggCarrier: []
    },
    Character.Gamma: {
        StartingArea.StationSquare: [ItemName.KeyItem.HotelKeys],
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [ItemName.KeyItem.Dynamite, ItemName.KeyItem.WindStone],
        StartingArea.Jungle: [],
    },
    Character.Big: {
        StartingArea.Hotel: [],
        StartingArea.StationSquare: [],
        StartingArea.EggCarrier: []
    }
}

starting_area_no_items = {
    Character.Sonic: {
        StartingArea.Hotel: [],
        StartingArea.MysticRuins: [],
        StartingArea.EggCarrier: []
    },
    Character.Tails: {
        StartingArea.Casino: [],
        StartingArea.MysticRuins: [],
        StartingArea.EggCarrier: []
    },
    Character.Knuckles: {
        StartingArea.StationSquare: [],
        StartingArea.Casino: [],
    },
    Character.Amy: {
        StartingArea.Jungle: [],
        StartingArea.EggCarrier: []
    },
    Character.Gamma: {
        StartingArea.Hotel: [],
        StartingArea.Jungle: [],
    },
    Character.Big: {
        StartingArea.Hotel: [],
        StartingArea.StationSquare: [],
        StartingArea.EggCarrier: []
    }
}
