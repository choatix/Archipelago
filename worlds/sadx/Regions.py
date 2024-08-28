from dataclasses import dataclass
from typing import Dict, Tuple, List

from BaseClasses import Region
from .CharacterUtils import character_has_life_sanity, is_level_playable, \
    get_playable_characters, get_playable_character_item, is_any_character_playable
from .CharacterUtils import is_character_playable
from .Enums import Area, Character, SubLevelMission, SubLevel, pascal_to_space
from .Locations import SonicAdventureDXLocation, life_capsule_location_table, \
    upgrade_location_table, level_location_table, mission_location_table, boss_location_table, sub_level_location_table, \
    field_emblem_location_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from .StartingSetup import StarterSetup
from ..AutoWorld import World


@dataclass
class AreaConnection:
    areaFrom: Area
    areaTo: Area
    character: Character
    item: str


created_regions: Dict[Tuple[Character, Area], Region] = {}

area_connections: Dict[Tuple[Character, Area, Area], Tuple[List[str], List[str], List[str]]] = {
    (Character.Sonic, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Sonic, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Sonic, Area.Casino, Area.Casinopolis): ([ItemName.Sonic.LightShoes], [ItemName.Sonic.LightShoes], []),
    (Character.Sonic, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    (Character.Sonic, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Sonic, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Sonic, Area.AngelIsland, Area.RedMountain): (
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight],
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight],
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight]),
    (Character.Sonic, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Sonic, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Sonic, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Sonic, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Tails, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Tails, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Tails, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Tails, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    (Character.Tails, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Tails, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Tails, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Tails, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Tails, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Tails, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Tails, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Knuckles, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Knuckles, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Knuckles, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone], [ItemName.KeyItem.IceStone], [ItemName.KeyItem.IceStone]),
    (Character.Knuckles, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Knuckles, Area.StationSquareMain, Area.SpeedHighway): ([], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.RedMountain): (
        [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    (Character.Knuckles, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Knuckles, Area.Jungle, Area.LostWorld): (
        [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    (Character.Knuckles, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Knuckles, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Amy, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Amy, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Amy, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Amy, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone], [ItemName.KeyItem.IceStone], [ItemName.KeyItem.IceStone]),
    (Character.Amy, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Amy, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Amy, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Amy, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Amy, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Amy, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Amy, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Big, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Big, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Big, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Big, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    (Character.Big, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Big, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Big, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Big, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Big, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Big, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Big, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Gamma, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Gamma, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Gamma, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Gamma, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone], [ItemName.KeyItem.IceStone], [ItemName.KeyItem.IceStone]),
    (Character.Gamma, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Gamma, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Gamma, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Gamma, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Gamma, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Gamma, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Gamma, Area.EggCarrierMain, Area.HotShelter): ([], [], []),

    (Character.Sonic, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], []),
    (Character.Sonic, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Sonic, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Sonic, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], []),
    (Character.Sonic, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Sonic, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Sonic, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Sonic, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Sonic, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Sonic, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Sonic, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Sonic, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Sonic, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Sonic, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Sonic, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Sonic, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Tails, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Tails, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Tails, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Tails, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Tails, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Tails, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Tails, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Tails, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Tails, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Tails, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Tails, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Tails, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Tails, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Tails, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Tails, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Tails, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Knuckles, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Knuckles, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Knuckles, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Knuckles, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Knuckles, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Knuckles, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Knuckles, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Knuckles, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Knuckles, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Knuckles, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Knuckles, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Amy, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Amy, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Amy, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Amy, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Amy, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Amy, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Amy, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Amy, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Amy, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Amy, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Amy, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Amy, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Amy, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Amy, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Amy, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Amy, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Big, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Big, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Big, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Big, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Big, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.StationSquareMain, Area.TwinkleParkLobby): ([], [], []),
    (Character.Big, Area.TwinkleParkLobby, Area.StationSquareMain): ([], [], []),
    (Character.Big, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Big, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Big, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Big, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Big, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Big, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Big, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Big, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Big, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Big, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Gamma, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Gamma, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Gamma, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Gamma, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Gamma, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Gamma, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Gamma, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Gamma, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Gamma, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Gamma, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Gamma, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Gamma, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Gamma, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Gamma, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Gamma, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Gamma, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
}


def get_region_name(character: Character, area: Area) -> str:
    return "{} ({})".format(pascal_to_space(area.name), character.name)


def get_entrance_name(character: Character, area: Area) -> str:
    return "{} Entrance ({})".format(pascal_to_space(area.name), character.name)


def create_sadx_regions(world: World, starter_setup: StarterSetup, options: SonicAdventureDXOptions):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    # Create regions for each character in each area
    for area in Area:
        for character in get_playable_characters(options):
            region = Region(get_region_name(character, area), world.player, world.multiworld)
            world.multiworld.regions.append(region)
            add_locations_to_region(region, area, character, world.player, options)
            created_regions[(character, area)] = region
            if area == starter_setup.get_starting_area(character):
                menu_region.connect(region, None,
                                    lambda state, item=get_playable_character_item(character): state.has(item,
                                                                                                         world.player))

    # Connect regions based on area connections rules
    for (character, area_from, area_to), (
            casual_logic_items, normal_logic_items, hard_logic_items) in area_connections.items():

        if options.entrance_randomizer:
            actual_area = starter_setup.level_mapping.get(area_to, area_to)
        else:
            actual_area = area_to

        region_from = created_regions.get((character, area_from))
        region_to = created_regions.get((character, actual_area))

        if options.logic_level.value == 2:
            key_items = hard_logic_items
        elif options.logic_level.value == 1:
            key_items = normal_logic_items
        else:
            key_items = casual_logic_items

        if Area.EmeraldCoast.value <= area_to.value <= Area.HotShelter.value:
            entrance_name = get_entrance_name(character, area_to)
        else:
            entrance_name = None

        if region_from and region_to:
            if key_items:
                region_from.connect(region_to, entrance_name,
                                    lambda state, items=key_items: all(state.has(item, world.player) for item in items))
            else:
                region_from.connect(region_to, entrance_name)

    common_region = Region("Common region", world.player, world.multiworld)
    world.multiworld.regions.append(common_region)
    add_locations_to_common_region(common_region, world.player, options)
    menu_region.connect(common_region)

    perfect_chaos_area = Region("Perfect Chaos Fight", world.player, world.multiworld)
    perfect_chaos_fight = SonicAdventureDXLocation(world.player, 9, menu_region)
    perfect_chaos_fight.locked = True
    perfect_chaos_area.locations.append(perfect_chaos_fight)
    menu_region.connect(perfect_chaos_area)
    created_regions.clear()


def add_locations_to_region(region: Region, area: Area, character: Character, player: int,
                            options: SonicAdventureDXOptions):
    location_ids = get_location_ids_for_area(area, character, options)
    for location_id in location_ids:
        location = SonicAdventureDXLocation(player, location_id, region)
        region.locations.append(location)


def get_location_ids_for_area(area: Area, character: Character, options: SonicAdventureDXOptions):
    location_ids = []
    for level in level_location_table:
        if level.area == area and level.character == character:
            if is_level_playable(level, options):
                location_ids.append(level.locationId)
    for upgrade in upgrade_location_table:
        if upgrade.area == area and upgrade.character == character:
            if is_character_playable(upgrade.character, options):
                location_ids.append(upgrade.locationId)

    if options.life_sanity:
        for life_capsule in life_capsule_location_table:
            if life_capsule.area == area and life_capsule.character == character:
                if is_character_playable(life_capsule.character, options):
                    if character_has_life_sanity(life_capsule.character, options):
                        if life_capsule.locationId == 1211 or life_capsule.locationId == 1212:
                            if options.pinball_life_capsules:
                                location_ids.append(life_capsule.locationId)
                        else:
                            location_ids.append(life_capsule.locationId)
    if options.boss_checks:
        for boss_fight in boss_location_table:
            if boss_fight.area == area and len(boss_fight.characters) == 1 and boss_fight.characters[0] == character:
                if options.unify_chaos4 and boss_fight.boss == LocationName.Boss.Chaos4 and not boss_fight.unified:
                    continue
                if options.unify_chaos6 and boss_fight.boss == LocationName.Boss.Chaos6 and not boss_fight.unified:
                    continue
                if options.unify_egg_hornet and boss_fight.boss == LocationName.Boss.EggHornet and not boss_fight.unified:
                    continue
                if is_any_character_playable(boss_fight.characters, options):
                    location_ids.append(boss_fight.locationId)

    if options.mission_mode_checks:
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if mission.objectiveArea == area and mission.character == character:
                if is_character_playable(mission.character, options):
                    location_ids.append(mission.locationId)

    return location_ids


def add_locations_to_common_region(region: Region, player: int, options: SonicAdventureDXOptions):
    location_ids = get_location_ids_for_common_region(options)
    for location_id in location_ids:
        location = SonicAdventureDXLocation(player, location_id, region)
        region.locations.append(location)


def get_location_ids_for_common_region(options):
    location_ids = []
    if options.sub_level_checks:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SandHill or sub_level.subLevel == SubLevel.TwinkleCircuit:
                if is_any_character_playable(sub_level.characters, options):
                    if ((options.sub_level_checks_hard and sub_level.subLevelMission == SubLevelMission.A)
                            or sub_level.subLevelMission == SubLevelMission.B):
                        location_ids.append(sub_level.locationId)
    if options.sky_chase_checks:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SkyChaseAct1 or sub_level.subLevel == SubLevel.SkyChaseAct2:
                if is_any_character_playable(sub_level.characters, options):
                    if ((options.sky_chase_checks_hard and sub_level.subLevelMission == SubLevelMission.A)
                            or sub_level.subLevelMission == SubLevelMission.B):
                        location_ids.append(sub_level.locationId)

    if options.field_emblems_checks:
        for field_emblem in field_emblem_location_table:
            if is_any_character_playable(field_emblem.get_logic_characters(options), options):
                location_ids.append(field_emblem.locationId)

    if options.boss_checks:
        for boss_fight in boss_location_table:
            if not boss_fight.unified:
                continue
            if not options.unify_chaos4 and boss_fight.boss == LocationName.Boss.Chaos4 and boss_fight.unified:
                continue
            if not options.unify_chaos6 and boss_fight.boss == LocationName.Boss.Chaos6 and boss_fight.unified:
                continue
            if not options.unify_egg_hornet and boss_fight.boss == LocationName.Boss.EggHornet and boss_fight.unified:
                continue
            if is_any_character_playable(boss_fight.characters, options):
                location_ids.append(boss_fight.locationId)

    return location_ids
