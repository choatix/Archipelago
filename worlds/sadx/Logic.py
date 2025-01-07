from dataclasses import dataclass
from typing import Dict, Tuple, List, Union

from .Enums import Character, Area, SubLevel, LevelMission, pascal_to_space, SubLevelMission, EVERYONE, SONIC_TAILS, \
    Capsule, Enemy
from .Names import ItemName, LocationName
from .Names.LocationName import Boss
from .Options import SonicAdventureDXOptions


@dataclass
class LevelLocation:
    locationId: int
    area: Area
    character: Character
    levelMission: LevelMission
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_level_name(self) -> str:
        return f"{pascal_to_space(self.area.name)} ({self.character.name}) - Mission {self.levelMission.name}"

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class UpgradeLocation:
    locationId: int
    locationName: str
    area: Area
    character: Character
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class CharacterUpgrade:
    character: Character
    upgrade: str


@dataclass
class EmblemLocation:
    locationId: int
    area: Area
    normalLogicCharacters: List[Union[CharacterUpgrade, Character]]
    hardLogicCharacters: List[Union[CharacterUpgrade, Character]]
    expertLogicCharacters: List[Union[CharacterUpgrade, Character]]
    emblemName: str

    def get_logic_characters_upgrades(self, options: SonicAdventureDXOptions) -> (
            List)[Union[CharacterUpgrade, Character]]:
        if options.logic_level.value == 2:
            return self.expertLogicCharacters
        elif options.logic_level.value == 1:
            return self.hardLogicCharacters
        else:
            return self.normalLogicCharacters

    def get_logic_characters(self, options: SonicAdventureDXOptions) -> List[Character]:
        if options.logic_level.value == 2:
            return self._get_characters(self.expertLogicCharacters)
        elif options.logic_level.value == 1:
            return self._get_characters(self.hardLogicCharacters)
        else:
            return self._get_characters(self.normalLogicCharacters)

    @staticmethod
    def _get_characters(logic: List[Union[CharacterUpgrade, Character]]) -> List[Character]:
        return [item.character if isinstance(item, CharacterUpgrade) else item for item in logic]


@dataclass
class CapsuleLocation:
    locationId: int
    area: Area
    character: Character
    capsuleNumber: int
    type: Capsule
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class EnemyLocation:
    locationId: int
    area: Area
    character: Character
    enemyNumber: int
    type: Enemy
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class MissionLocation:
    locationId: int
    cardArea: Area
    objectiveArea: Area
    character: Character
    missionNumber: int
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_mission_name(self) -> str:
        return f"Mission {self.missionNumber} ({self.character.name})"

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class SubLevelLocation:
    locationId: int
    area: Area
    characters: List[Character]
    subLevel: SubLevel
    subLevelMission: SubLevelMission


@dataclass
class BossFightLocation:
    locationId: int
    area: Area
    characters: List[Character]
    boss: Boss
    unified: bool

    def get_boss_name(self) -> str:
        if self.unified:
            return f"{self.boss} Boss Fight"
        else:
            return f"{self.boss} Boss Fight ({self.characters[0].name})"


@dataclass
class ChaoEggLocation:
    locationId: int
    eggName: str
    area: Area
    characters: List[Character]
    requirements: List[List[str]]


@dataclass
class ChaoRaceLocation:
    locationId: int
    name: str
    area: Area


area_connections: Dict[Tuple[Character, Area, Area], Tuple[List[str], List[str], List[str]]] = {
    (Character.Sonic, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Sonic, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Sonic, Area.Casino, Area.Casinopolis): ([ItemName.Sonic.LightShoes], [ItemName.Sonic.LightShoes], []),
    (Character.Sonic, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite]),
    (Character.Sonic, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Sonic, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], []),
    (Character.Sonic, Area.AngelIsland, Area.RedMountain): (
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight],
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight],
        []),
    (Character.Sonic, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Sonic, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Sonic, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Sonic, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Tails, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Tails, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Tails, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Tails, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite]),
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
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite], [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Knuckles, Area.StationSquareMain, Area.SpeedHighway): ([], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.RedMountain): (
        [ItemName.Knuckles.ShovelClaw, ItemName.KeyItem.Dynamite],
        [ItemName.Knuckles.ShovelClaw, ItemName.KeyItem.Dynamite],
        [ItemName.Knuckles.ShovelClaw, ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Knuckles, Area.Jungle, Area.LostWorld): (
        [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw], []),
    (Character.Knuckles, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Knuckles, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Amy, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Amy, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Amy, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Amy, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite], [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite]),
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
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite]),
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
    (Character.Gamma, Area.AngelIsland, Area.IceCap): ([ItemName.KeyItem.IceStone,
                                                        ItemName.KeyItem.Dynamite], [ItemName.KeyItem.IceStone,
                                                                                     ItemName.KeyItem.Dynamite],
                                                       [ItemName.KeyItem.IceStone,
                                                        ItemName.KeyItem.Dynamite]),
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
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], []),
    (Character.Sonic, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Sonic, Area.Station, Area.Casino): ([ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], []),
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
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], []),
    (Character.Tails, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Tails, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.Casino, Area.Station): ([ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], []),
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
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
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
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
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
    (Character.Big, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
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
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
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

level_location_table: List[LevelLocation] = [
    LevelLocation(6002, Area.TwinklePark, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6001, Area.TwinklePark, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6000, Area.TwinklePark, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4]),
    LevelLocation(3002, Area.SpeedHighway, Character.Knuckles, LevelMission.C, [], [], []),
    LevelLocation(3001, Area.SpeedHighway, Character.Knuckles, LevelMission.B, [], [], []),
    LevelLocation(3000, Area.SpeedHighway, Character.Knuckles, LevelMission.A, [], [], []),
    LevelLocation(1002, Area.EmeraldCoast, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1001, Area.EmeraldCoast, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1000, Area.EmeraldCoast, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(6202, Area.EmeraldCoast, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6201, Area.EmeraldCoast, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6200, Area.EmeraldCoast, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4]),
    LevelLocation(5102, Area.EmeraldCoast, Character.Gamma, LevelMission.C, [], [], []),
    LevelLocation(5101, Area.EmeraldCoast, Character.Gamma, LevelMission.B, [], [], []),
    LevelLocation(5100, Area.EmeraldCoast, Character.Gamma, LevelMission.A, [], [], []),
    LevelLocation(1202, Area.Casinopolis, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1201, Area.Casinopolis, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1200, Area.Casinopolis, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2102, Area.Casinopolis, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2101, Area.Casinopolis, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2100, Area.Casinopolis, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(3102, Area.Casinopolis, Character.Knuckles, LevelMission.C, [], [], []),
    LevelLocation(3101, Area.Casinopolis, Character.Knuckles, LevelMission.B, [], [], []),
    LevelLocation(3100, Area.Casinopolis, Character.Knuckles, LevelMission.A, [], [], []),
    LevelLocation(1402, Area.TwinklePark, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1401, Area.TwinklePark, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1400, Area.TwinklePark, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(4002, Area.TwinklePark, Character.Amy, LevelMission.C, [], [], []),
    LevelLocation(4001, Area.TwinklePark, Character.Amy, LevelMission.B, [], [], []),
    LevelLocation(4000, Area.TwinklePark, Character.Amy, LevelMission.A, [], [], []),
    LevelLocation(1502, Area.SpeedHighway, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1501, Area.SpeedHighway, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1500, Area.SpeedHighway, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2402, Area.SpeedHighway, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2401, Area.SpeedHighway, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2400, Area.SpeedHighway, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(1102, Area.WindyValley, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1101, Area.WindyValley, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1100, Area.WindyValley, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2002, Area.WindyValley, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2001, Area.WindyValley, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2000, Area.WindyValley, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(5202, Area.WindyValley, Character.Gamma, LevelMission.C, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], []),
    LevelLocation(5201, Area.WindyValley, Character.Gamma, LevelMission.B, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], []),
    LevelLocation(5200, Area.WindyValley, Character.Gamma, LevelMission.A, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], []),
    LevelLocation(1302, Area.IceCap, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1301, Area.IceCap, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1300, Area.IceCap, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2202, Area.IceCap, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2201, Area.IceCap, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2200, Area.IceCap, Character.Tails, LevelMission.A, [], [], []),
    LevelLocation(6102, Area.IceCap, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6101, Area.IceCap, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6100, Area.IceCap, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4]),
    LevelLocation(1602, Area.RedMountain, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1601, Area.RedMountain, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1600, Area.RedMountain, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(3202, Area.RedMountain, Character.Knuckles, LevelMission.C, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3201, Area.RedMountain, Character.Knuckles, LevelMission.B, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3200, Area.RedMountain, Character.Knuckles, LevelMission.A, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(5302, Area.RedMountain, Character.Gamma, LevelMission.C, [], [], []),
    LevelLocation(5301, Area.RedMountain, Character.Gamma, LevelMission.B, [], [], []),
    LevelLocation(5300, Area.RedMountain, Character.Gamma, LevelMission.A, [], [], []),
    LevelLocation(1802, Area.LostWorld, Character.Sonic, LevelMission.C, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1801, Area.LostWorld, Character.Sonic, LevelMission.B, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1800, Area.LostWorld, Character.Sonic, LevelMission.A, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(3302, Area.LostWorld, Character.Knuckles, LevelMission.C, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3301, Area.LostWorld, Character.Knuckles, LevelMission.B, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3300, Area.LostWorld, Character.Knuckles, LevelMission.A, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(1902, Area.FinalEgg, Character.Sonic, LevelMission.C, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1901, Area.FinalEgg, Character.Sonic, LevelMission.B, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1900, Area.FinalEgg, Character.Sonic, LevelMission.A, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(4202, Area.FinalEgg, Character.Amy, LevelMission.C, [], [], []),
    LevelLocation(4201, Area.FinalEgg, Character.Amy, LevelMission.B, [], [], []),
    LevelLocation(4200, Area.FinalEgg, Character.Amy, LevelMission.A, [], [], []),
    LevelLocation(5002, Area.FinalEgg, Character.Gamma, LevelMission.C, [], [], []),
    LevelLocation(5001, Area.FinalEgg, Character.Gamma, LevelMission.B, [], [], []),
    LevelLocation(5000, Area.FinalEgg, Character.Gamma, LevelMission.A, [], [], []),
    LevelLocation(1702, Area.SkyDeck, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1701, Area.SkyDeck, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1700, Area.SkyDeck, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2302, Area.SkyDeck, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2301, Area.SkyDeck, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2300, Area.SkyDeck, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(3402, Area.SkyDeck, Character.Knuckles, LevelMission.C, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3401, Area.SkyDeck, Character.Knuckles, LevelMission.B, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3400, Area.SkyDeck, Character.Knuckles, LevelMission.A, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(4102, Area.HotShelter, Character.Amy, LevelMission.C, [], [], []),
    LevelLocation(4101, Area.HotShelter, Character.Amy, LevelMission.B, [], [], []),
    LevelLocation(4100, Area.HotShelter, Character.Amy, LevelMission.A, [], [], []),
    LevelLocation(6302, Area.HotShelter, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6301, Area.HotShelter, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6300, Area.HotShelter, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], []),
    LevelLocation(5402, Area.HotShelter, Character.Gamma, LevelMission.C, [ItemName.Gamma.JetBooster], [], []),
    LevelLocation(5401, Area.HotShelter, Character.Gamma, LevelMission.B, [ItemName.Gamma.JetBooster], [], []),
    LevelLocation(5400, Area.HotShelter, Character.Gamma, LevelMission.A, [ItemName.Gamma.JetBooster], [], []),
]

upgrade_location_table: List[UpgradeLocation] = [
    UpgradeLocation(100, LocationName.Sonic.LightShoes, Area.StationSquareMain, Character.Sonic, [], [], []),
    UpgradeLocation(200, LocationName.Tails.JetAnklet, Area.StationSquareMain, Character.Tails, [], [], []),
    UpgradeLocation(602, LocationName.Big.Lure1, Area.StationSquareMain, Character.Big, [], [], []),
    UpgradeLocation(101, LocationName.Sonic.CrystalRing, Area.Hotel, Character.Sonic, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], []),
    UpgradeLocation(300, LocationName.Knuckles.ShovelClaw, Area.MysticRuinsMain, Character.Knuckles, [], [], []),
    UpgradeLocation(604, LocationName.Big.Lure3, Area.IceCap, Character.Big, [], [], []),
    UpgradeLocation(600, LocationName.Big.LifeBelt, Area.AngelIsland, Character.Big,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    UpgradeLocation(102, LocationName.Sonic.AncientLight, Area.AngelIsland, Character.Sonic, [], [], []),
    UpgradeLocation(301, LocationName.Knuckles.FightingGloves, Area.Jungle, Character.Knuckles, [], [], []),
    UpgradeLocation(603, LocationName.Big.Lure2, Area.Jungle, Character.Big, [], [], []),
    UpgradeLocation(601, LocationName.Big.PowerRod, Area.Jungle, Character.Big, [], [], []),
    UpgradeLocation(400, LocationName.Amy.WarriorFeather, Area.EggCarrierMain, Character.Amy, [], [], []),
    UpgradeLocation(401, LocationName.Amy.LongHammer, Area.EggCarrierMain, Character.Amy, [], [], []),
    UpgradeLocation(500, LocationName.Gamma.JetBooster, Area.EggCarrierMain, Character.Gamma, [], [], []),
    UpgradeLocation(501, LocationName.Gamma.LaserBlaster, Area.EggCarrierMain, Character.Gamma, [], [], []),
    UpgradeLocation(605, LocationName.Big.Lure4, Area.EggCarrierMain, Character.Big, [], [], []),
    UpgradeLocation(201, LocationName.Tails.RhythmBadge, Area.AngelIsland, Character.Tails, [], [], []),
]

field_emblem_location_table: List[EmblemLocation] = [
    EmblemLocation(10, Area.Station,
                   [Character.Sonic, Character.Knuckles, Character.Tails, Character.Amy, Character.Big],
                   [Character.Sonic, Character.Knuckles, Character.Tails, Character.Amy, Character.Big],
                   [Character.Sonic, Character.Knuckles, Character.Tails, Character.Amy, Character.Big],
                   "Station Emblem"),
    EmblemLocation(11, Area.StationSquareMain,
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma], "Burger Shop Emblem"),
    EmblemLocation(12, Area.StationSquareMain,
                   [Character.Tails, CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)],
                   [Character.Tails, CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)],
                   [Character.Amy, Character.Tails, CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)],
                   "City Hall Emblem"),
    EmblemLocation(13, Area.Casino, [Character.Tails], [Character.Tails], [Character.Tails], "Casino Emblem"),
    EmblemLocation(20, Area.MysticRuinsMain,
                   [Character.Tails, Character.Knuckles, CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)],
                   [Character.Sonic, Character.Tails, Character.Knuckles,
                    CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)],
                   [Character.Sonic, Character.Tails, Character.Knuckles,
                    CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)], "Tails' Workshop Emblem"),
    EmblemLocation(21, Area.AngelIsland, [Character.Knuckles], [Character.Tails, Character.Knuckles,
                                                                CharacterUpgrade(Character.Gamma,
                                                                                 ItemName.Gamma.JetBooster)],
                   [Character.Sonic, Character.Tails, Character.Knuckles,
                    CharacterUpgrade(Character.Gamma,
                                     ItemName.Gamma.JetBooster)], "Shrine Emblem"),
    EmblemLocation(22, Area.Jungle, [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                                     Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma], "Jungle Path Emblem"),
    EmblemLocation(23, Area.Jungle, [Character.Tails, Character.Knuckles],
                   [Character.Sonic, Character.Tails, Character.Knuckles],
                   [Character.Sonic, Character.Tails, Character.Knuckles], "Tree Stump Emblem"),
    EmblemLocation(30, Area.EggCarrierMain, [Character.Tails, Character.Knuckles],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy], "Pool Emblem"),
    EmblemLocation(31, Area.EggCarrierMain, [Character.Tails], [Character.Tails, Character.Sonic],
                   [Character.Tails, Character.Sonic], "Spinning Platform Emblem"),
    EmblemLocation(32, Area.EggCarrierMain, [Character.Tails, Character.Sonic],
                   [Character.Tails, Character.Sonic, Character.Big], [Character.Tails, Character.Sonic, Character.Big],
                   "Hidden Bed Emblem"),
    EmblemLocation(33, Area.EggCarrierMain, [Character.Sonic], [Character.Sonic, Character.Big],
                   [Character.Sonic, Character.Big], "Main Platform Emblem"),
]

mission_location_table: List[MissionLocation] = [
    MissionLocation(801, Area.StationSquareMain, Area.StationSquareMain, Character.Sonic, 1, [], [], []),
    MissionLocation(802, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Sonic, 2, [], [], []),
    MissionLocation(803, Area.Hotel, Area.Hotel, Character.Sonic, 3, [ItemName.Sonic.LightShoes], [], []),
    MissionLocation(804, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 4, [], [], []),
    MissionLocation(805, Area.Casino, Area.Casino, Character.Knuckles, 5, [], [], []),
    MissionLocation(806, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Amy, 6, [], [], []),
    MissionLocation(807, Area.MysticRuinsMain, Area.Jungle, Character.Gamma, 7, [], [], []),
    MissionLocation(808, Area.StationSquareMain, Area.StationSquareMain, Character.Big, 8, [], [], []),
    MissionLocation(809, Area.StationSquareMain, Area.EmeraldCoast, Character.Sonic, 9, [], [], []),
    MissionLocation(810, Area.Hotel, Area.Hotel, Character.Tails, 10, [], [], []),
    MissionLocation(811, Area.MysticRuinsMain, Area.WindyValley, Character.Sonic, 11, [], [], []),
    MissionLocation(812, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Knuckles, 12,
                    [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(813, Area.Casino, Area.Casinopolis, Character.Sonic, 13, [], [], []),
    MissionLocation(814, Area.StationSquareMain, Area.Hotel, Character.Big, 14, [], [], []),
    MissionLocation(815, Area.MysticRuinsMain, Area.WindyValley, Character.Sonic, 15, [], [], []),
    MissionLocation(816, Area.MysticRuinsMain, Area.WindyValley, Character.Tails, 16, [], [], []),
    MissionLocation(817, Area.StationSquareMain, Area.Casinopolis, Character.Sonic, 17, [], [], []),
    MissionLocation(818, Area.Station, Area.TwinklePark, Character.Amy, 18, [], [], []),
    MissionLocation(819, Area.StationSquareMain, Area.TwinklePark, Character.Amy, 19, [], [], []),
    MissionLocation(820, Area.AngelIsland, Area.IceCap, Character.Sonic, 20,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    MissionLocation(821, Area.Jungle, Area.FinalEgg, Character.Gamma, 21, [], [], []),
    MissionLocation(822, Area.Hotel, Area.EmeraldCoast, Character.Big, 22, [], [], []),
    MissionLocation(823, Area.TwinkleParkLobby, Area.TwinklePark, Character.Sonic, 23, [], [], []),
    MissionLocation(824, Area.Casino, Area.Casinopolis, Character.Tails, 24, [], [], []),
    MissionLocation(825, Area.StationSquareMain, Area.Casinopolis, Character.Knuckles, 25, [], [], []),
    MissionLocation(826, Area.StationSquareMain, Area.Casinopolis, Character.Knuckles, 26, [], [], []),
    MissionLocation(827, Area.StationSquareMain, Area.SpeedHighway, Character.Sonic, 27, [], [], []),
    MissionLocation(828, Area.StationSquareMain, Area.SpeedHighway, Character.Sonic, 28, [], [], []),
    MissionLocation(829, Area.StationSquareMain, Area.StationSquareMain, Character.Big, 29, [ItemName.Big.LifeBelt], [],
                    []),
    MissionLocation(830, Area.Jungle, Area.RedMountain, Character.Sonic, 30, [], [], []),
    MissionLocation(831, Area.Station, Area.Casinopolis, Character.Tails, 31, [], [], []),
    MissionLocation(832, Area.AngelIsland, Area.AngelIsland, Character.Knuckles, 32, [], [], []),
    MissionLocation(833, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 33, [], [], []),
    MissionLocation(834, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 34, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], []),
    MissionLocation(835, Area.MysticRuinsMain, Area.AngelIsland, Character.Big, 35,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    MissionLocation(836, Area.EggCarrierMain, Area.SkyDeck, Character.Sonic, 36, [], [], []),
    MissionLocation(837, Area.Jungle, Area.Jungle, Character.Tails, 37, [ItemName.Tails.JetAnklet], [], []),
    MissionLocation(838, Area.Jungle, Area.LostWorld, Character.Knuckles, 38, [ItemName.Knuckles.ShovelClaw],
                    [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(839, Area.Hotel, Area.EmeraldCoast, Character.Gamma, 39, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    MissionLocation(840, Area.MysticRuinsMain, Area.LostWorld, Character.Sonic, 40, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], [ItemName.Sonic.LightShoes]),
    MissionLocation(841, Area.Jungle, Area.LostWorld, Character.Sonic, 41, [ItemName.Sonic.LightShoes], [], []),
    MissionLocation(842, Area.EggCarrierMain, Area.HotShelter, Character.Gamma, 42, [], [], []),
    MissionLocation(843, Area.EggCarrierMain, Area.HotShelter, Character.Amy, 43, [], [], []),
    MissionLocation(844, Area.EggCarrierMain, Area.EggCarrierMain, Character.Big, 44, [], [], []),
    MissionLocation(845, Area.Jungle, Area.FinalEgg, Character.Sonic, 45, [], [], []),
    MissionLocation(846, Area.Jungle, Area.FinalEgg, Character.Sonic, 46, [], [], []),
    MissionLocation(847, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 47, [], [], []),
    MissionLocation(848, Area.StationSquareMain, Area.Casinopolis, Character.Knuckles, 48, [], [], []),
    MissionLocation(849, Area.StationSquareMain, Area.TwinklePark, Character.Sonic, 49, [], [], []),
    MissionLocation(850, Area.Jungle, Area.FinalEgg, Character.Amy, 50, [], [], []),
    MissionLocation(851, Area.Jungle, Area.WindyValley, Character.Gamma, 51, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    MissionLocation(852, Area.Jungle, Area.Jungle, Character.Big, 52, [], [], []),
    MissionLocation(853, Area.AngelIsland, Area.IceCap, Character.Sonic, 53, [], [], []),
    MissionLocation(854, Area.AngelIsland, Area.IceCap, Character.Tails, 54, [], [], []),
    MissionLocation(855, Area.TwinkleParkLobby, Area.SpeedHighway, Character.Sonic, 55, [], [], []),
    MissionLocation(856, Area.MysticRuinsMain, Area.RedMountain, Character.Knuckles, 56, [ItemName.Knuckles.ShovelClaw],
                    [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(857, Area.AngelIsland, Area.RedMountain, Character.Sonic, 57, [], [], []),
    MissionLocation(858, Area.Jungle, Area.LostWorld, Character.Sonic, 58, [], [], []),
    MissionLocation(859, Area.EggCarrierMain, Area.SkyDeck, Character.Knuckles, 59, [], [], []),
    MissionLocation(860, Area.MysticRuinsMain, Area.IceCap, Character.Big, 60, [], [], []),
]

sub_level_location_table: List[SubLevelLocation] = [
    SubLevelLocation(15, Area.TwinkleParkLobby, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.B),
    SubLevelLocation(16, Area.TwinkleParkLobby, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.A),
    SubLevelLocation(25, Area.Jungle, SONIC_TAILS, SubLevel.SandHill, SubLevelMission.B),
    SubLevelLocation(26, Area.Jungle, SONIC_TAILS, SubLevel.SandHill, SubLevelMission.A),
    SubLevelLocation(27, Area.MysticRuinsMain, SONIC_TAILS, SubLevel.SkyChaseAct1, SubLevelMission.B),
    SubLevelLocation(28, Area.MysticRuinsMain, SONIC_TAILS, SubLevel.SkyChaseAct1, SubLevelMission.A),
    SubLevelLocation(35, Area.EggCarrierMain, SONIC_TAILS, SubLevel.SkyChaseAct2, SubLevelMission.B),
    SubLevelLocation(36, Area.EggCarrierMain, SONIC_TAILS, SubLevel.SkyChaseAct2, SubLevelMission.A),
]

boss_location_table: List[BossFightLocation] = [
    BossFightLocation(700, Area.StationSquareMain, [Character.Sonic], LocationName.Boss.Chaos0, False),
    BossFightLocation(710, Area.Hotel, [Character.Knuckles], LocationName.Boss.Chaos2, False),
    BossFightLocation(720, Area.Casino, [Character.Tails], LocationName.Boss.EggWalker, False),
    BossFightLocation(730, Area.MysticRuinsMain, [Character.Sonic], LocationName.Boss.EggHornet, False),
    BossFightLocation(731, Area.MysticRuinsMain, [Character.Tails], LocationName.Boss.EggHornet, False),
    BossFightLocation(739, Area.MysticRuinsMain, [Character.Sonic, Character.Tails], LocationName.Boss.EggHornet, True),
    BossFightLocation(740, Area.MysticRuinsMain, [Character.Sonic], LocationName.Boss.Chaos4, False),
    BossFightLocation(741, Area.MysticRuinsMain, [Character.Tails], LocationName.Boss.Chaos4, False),
    BossFightLocation(742, Area.MysticRuinsMain, [Character.Knuckles], LocationName.Boss.Chaos4, False),
    BossFightLocation(749, Area.MysticRuinsMain, [Character.Sonic, Character.Tails, Character.Knuckles],
                      LocationName.Boss.Chaos4, True),
    BossFightLocation(750, Area.Jungle, [Character.Sonic], LocationName.Boss.EggViper, False),
    BossFightLocation(760, Area.Jungle, [Character.Gamma], LocationName.Boss.E101Beta, False),
    BossFightLocation(770, Area.EggCarrierMain, [Character.Sonic], LocationName.Boss.Chaos6, False),
    BossFightLocation(771, Area.EggCarrierMain, [Character.Knuckles], LocationName.Boss.Chaos6, False),
    BossFightLocation(772, Area.EggCarrierMain, [Character.Big], LocationName.Boss.Chaos6, False),
    BossFightLocation(779, Area.EggCarrierMain, [Character.Sonic, Character.Knuckles, Character.Big],
                      LocationName.Boss.Chaos6, True),
    BossFightLocation(780, Area.EggCarrierMain, [Character.Gamma], LocationName.Boss.E101mkII, False),
    BossFightLocation(790, Area.EggCarrierMain, [Character.Amy], LocationName.Boss.Zero, False),
]

chao_egg_location_table: List[ChaoEggLocation] = [
    ChaoEggLocation(900, LocationName.Chao.GoldEgg, Area.StationSquareMain, EVERYONE,
                    [[ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.StationKeys, ItemName.KeyItem.CasinoKeys]]),
    ChaoEggLocation(901, LocationName.Chao.SilverEgg, Area.MysticRuinsMain, [Character.Sonic, Character.Tails,
                                                                             Character.Knuckles, Character.Amy,
                                                                             Character.Big], []),
    ChaoEggLocation(902, LocationName.Chao.BlackEgg, Area.EggCarrierMain,
                    [Character.Amy, Character.Gamma, Character.Big], []),
]
chao_race_location_table: List[ChaoRaceLocation] = [
    ChaoRaceLocation(905, LocationName.Chao.PearlCourse, Area.Hotel),
    ChaoRaceLocation(906, LocationName.Chao.AmethystCourse, Area.Hotel),
    ChaoRaceLocation(907, LocationName.Chao.SapphireCourse, Area.Hotel),
    ChaoRaceLocation(908, LocationName.Chao.RubyCourse, Area.Hotel),
    ChaoRaceLocation(909, LocationName.Chao.EmeraldCourse, Area.Hotel),
]

enemy_location_table: List[EnemyLocation] = [
    EnemyLocation(10001, Area.EmeraldCoast, Character.Sonic, 1, Enemy.Rhinotank, [], [], []),
    EnemyLocation(10002, Area.EmeraldCoast, Character.Sonic, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(10003, Area.EmeraldCoast, Character.Sonic, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(10004, Area.EmeraldCoast, Character.Sonic, 4, Enemy.Rhinotank, [], [], []),
    EnemyLocation(10005, Area.EmeraldCoast, Character.Sonic, 5, Enemy.Kiki, [], [], []),
    EnemyLocation(10006, Area.EmeraldCoast, Character.Sonic, 6, Enemy.Kiki, [], [], []),
    EnemyLocation(10007, Area.EmeraldCoast, Character.Sonic, 7, Enemy.Kiki, [], [], []),
    EnemyLocation(10008, Area.EmeraldCoast, Character.Sonic, 8, Enemy.Kiki, [], [], []),
    EnemyLocation(10009, Area.EmeraldCoast, Character.Sonic, 9, Enemy.Kiki, [], [], []),
    EnemyLocation(10010, Area.EmeraldCoast, Character.Sonic, 10, Enemy.Kiki, [], [], []),
    EnemyLocation(10011, Area.EmeraldCoast, Character.Sonic, 11, Enemy.Kiki, [], [], []),
    EnemyLocation(10012, Area.EmeraldCoast, Character.Sonic, 12, Enemy.Kiki, [], [], []),
    EnemyLocation(10013, Area.EmeraldCoast, Character.Sonic, 13, Enemy.Sweep, [], [], []),
    EnemyLocation(10014, Area.EmeraldCoast, Character.Sonic, 14, Enemy.Sweep, [], [], []),
    EnemyLocation(10015, Area.EmeraldCoast, Character.Sonic, 15, Enemy.Kiki, [], [], []),
    EnemyLocation(10016, Area.EmeraldCoast, Character.Sonic, 16, Enemy.Kiki, [], [], []),
    EnemyLocation(10017, Area.EmeraldCoast, Character.Sonic, 17, Enemy.Kiki, [], [], []),
    EnemyLocation(10018, Area.EmeraldCoast, Character.Sonic, 18, Enemy.Kiki, [], [], []),
    EnemyLocation(51001, Area.EmeraldCoast, Character.Gamma, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(51002, Area.EmeraldCoast, Character.Gamma, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(51003, Area.EmeraldCoast, Character.Gamma, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(51004, Area.EmeraldCoast, Character.Gamma, 4, Enemy.Kiki, [], [], []),
    EnemyLocation(51005, Area.EmeraldCoast, Character.Gamma, 5, Enemy.Kiki, [], [], []),
    EnemyLocation(51006, Area.EmeraldCoast, Character.Gamma, 6, Enemy.Rhinotank, [], [], []),
    EnemyLocation(51007, Area.EmeraldCoast, Character.Gamma, 7, Enemy.Rhinotank, [], [], []),
    EnemyLocation(51008, Area.EmeraldCoast, Character.Gamma, 8, Enemy.Rhinotank, [], [], []),
    EnemyLocation(51009, Area.EmeraldCoast, Character.Gamma, 9, Enemy.Kiki, [], [], []),
    EnemyLocation(51010, Area.EmeraldCoast, Character.Gamma, 10, Enemy.Kiki, [], [], []),
    EnemyLocation(51011, Area.EmeraldCoast, Character.Gamma, 11, Enemy.Rhinotank, [], [], []),
    EnemyLocation(51012, Area.EmeraldCoast, Character.Gamma, 12, Enemy.Kiki, [], [], []),
    EnemyLocation(51013, Area.EmeraldCoast, Character.Gamma, 13, Enemy.Kiki, [], [], []),
    EnemyLocation(51014, Area.EmeraldCoast, Character.Gamma, 14, Enemy.Rhinotank, [], [], []),
    EnemyLocation(51015, Area.EmeraldCoast, Character.Gamma, 15, Enemy.Kiki, [], [], []),
    EnemyLocation(51016, Area.EmeraldCoast, Character.Gamma, 16, Enemy.Kiki, [], [], []),
    EnemyLocation(51017, Area.EmeraldCoast, Character.Gamma, 17, Enemy.Kiki, [], [], []),
    EnemyLocation(51018, Area.EmeraldCoast, Character.Gamma, 18, Enemy.Kiki, [], [], []),
    EnemyLocation(51019, Area.EmeraldCoast, Character.Gamma, 19, Enemy.Kiki, [], [], []),
    EnemyLocation(51020, Area.EmeraldCoast, Character.Gamma, 20, Enemy.Kiki, [], [], []),
    EnemyLocation(51021, Area.EmeraldCoast, Character.Gamma, 21, Enemy.Kiki, [], [], []),
    EnemyLocation(51022, Area.EmeraldCoast, Character.Gamma, 22, Enemy.Kiki, [], [], []),
    EnemyLocation(51023, Area.EmeraldCoast, Character.Gamma, 23, Enemy.Rhinotank, [], [], []),
    EnemyLocation(51024, Area.EmeraldCoast, Character.Gamma, 24, Enemy.Kiki, [], [], []),
    EnemyLocation(51025, Area.EmeraldCoast, Character.Gamma, 25, Enemy.Kiki, [], [], []),
    EnemyLocation(51026, Area.EmeraldCoast, Character.Gamma, 26, Enemy.Kiki, [], [], []),
    EnemyLocation(51027, Area.EmeraldCoast, Character.Gamma, 27, Enemy.Kiki, [], [], []),
    EnemyLocation(51028, Area.EmeraldCoast, Character.Gamma, 28, Enemy.Kiki, [], [], []),
    EnemyLocation(51029, Area.EmeraldCoast, Character.Gamma, 29, Enemy.Kiki, [], [], []),
    EnemyLocation(62001, Area.EmeraldCoast, Character.Big, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(62002, Area.EmeraldCoast, Character.Big, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(62003, Area.EmeraldCoast, Character.Big, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(11001, Area.WindyValley, Character.Sonic, 1, Enemy.Leon, [], [], []),
    EnemyLocation(11002, Area.WindyValley, Character.Sonic, 2, Enemy.BoaBoa, [], [], []),
    EnemyLocation(11003, Area.WindyValley, Character.Sonic, 3, Enemy.Leon, [], [], []),
    EnemyLocation(11004, Area.WindyValley, Character.Sonic, 4, Enemy.Leon, [], [], []),
    EnemyLocation(11005, Area.WindyValley, Character.Sonic, 5, Enemy.BoaBoa, [], [], []),
    EnemyLocation(11006, Area.WindyValley, Character.Sonic, 6, Enemy.Leon, [], [], []),
    EnemyLocation(11007, Area.WindyValley, Character.Sonic, 7, Enemy.Leon, [], [], []),
    EnemyLocation(11008, Area.WindyValley, Character.Sonic, 8, Enemy.Rhinotank, [], [], []),
    EnemyLocation(11009, Area.WindyValley, Character.Sonic, 9, Enemy.Leon, [], [], []),
    EnemyLocation(11010, Area.WindyValley, Character.Sonic, 10, Enemy.Rhinotank, [], [], []),
    EnemyLocation(20001, Area.WindyValley, Character.Tails, 1, Enemy.Leon, [], [], []),
    EnemyLocation(20002, Area.WindyValley, Character.Tails, 2, Enemy.Rhinotank, [], [], []),
    EnemyLocation(20003, Area.WindyValley, Character.Tails, 3, Enemy.Rhinotank, [], [], []),
    EnemyLocation(52001, Area.WindyValley, Character.Gamma, 1, Enemy.BoaBoa, [], [], []),
    EnemyLocation(52002, Area.WindyValley, Character.Gamma, 2, Enemy.Rhinotank, [], [], []),
    EnemyLocation(52003, Area.WindyValley, Character.Gamma, 3, Enemy.BoaBoa, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52004, Area.WindyValley, Character.Gamma, 4, Enemy.BoaBoa, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52005, Area.WindyValley, Character.Gamma, 5, Enemy.Leon, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52006, Area.WindyValley, Character.Gamma, 6, Enemy.Leon, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52007, Area.WindyValley, Character.Gamma, 7, Enemy.BoaBoa, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52008, Area.WindyValley, Character.Gamma, 8, Enemy.BoaBoa, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52009, Area.WindyValley, Character.Gamma, 9, Enemy.BoaBoa, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52010, Area.WindyValley, Character.Gamma, 10, Enemy.BoaBoa, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(52011, Area.WindyValley, Character.Gamma, 11, Enemy.Rhinotank, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    EnemyLocation(14001, Area.TwinklePark, Character.Sonic, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(14002, Area.TwinklePark, Character.Sonic, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(14003, Area.TwinklePark, Character.Sonic, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(14004, Area.TwinklePark, Character.Sonic, 4, Enemy.Kiki, [], [], []),
    EnemyLocation(14005, Area.TwinklePark, Character.Sonic, 5, Enemy.Kiki, [], [], []),
    EnemyLocation(14006, Area.TwinklePark, Character.Sonic, 6, Enemy.Kiki, [], [], []),
    EnemyLocation(14007, Area.TwinklePark, Character.Sonic, 7, Enemy.Kiki, [], [], []),
    EnemyLocation(14008, Area.TwinklePark, Character.Sonic, 8, Enemy.Kiki, [], [], []),
    EnemyLocation(14009, Area.TwinklePark, Character.Sonic, 9, Enemy.Buyon, [], [], []),
    EnemyLocation(14010, Area.TwinklePark, Character.Sonic, 10, Enemy.Buyon, [], [], []),
    EnemyLocation(14011, Area.TwinklePark, Character.Sonic, 11, Enemy.Sweep, [], [], []),
    EnemyLocation(14012, Area.TwinklePark, Character.Sonic, 12, Enemy.Sweep, [], [], []),
    EnemyLocation(14013, Area.TwinklePark, Character.Sonic, 13, Enemy.Sweep, [], [], []),
    EnemyLocation(14014, Area.TwinklePark, Character.Sonic, 14, Enemy.Kiki, [], [], []),
    EnemyLocation(14015, Area.TwinklePark, Character.Sonic, 15, Enemy.Kiki, [], [], []),
    EnemyLocation(14016, Area.TwinklePark, Character.Sonic, 16, Enemy.Kiki, [], [], []),
    EnemyLocation(14017, Area.TwinklePark, Character.Sonic, 17, Enemy.Kiki, [], [], []),
    EnemyLocation(14018, Area.TwinklePark, Character.Sonic, 18, Enemy.Buyon, [], [], []),
    EnemyLocation(14019, Area.TwinklePark, Character.Sonic, 19, Enemy.Buyon, [], [], []),
    EnemyLocation(14020, Area.TwinklePark, Character.Sonic, 20, Enemy.Kiki, [], [], []),
    EnemyLocation(14021, Area.TwinklePark, Character.Sonic, 21, Enemy.Kiki, [], [], []),
    EnemyLocation(14022, Area.TwinklePark, Character.Sonic, 22, Enemy.Kiki, [], [], []),
    EnemyLocation(14023, Area.TwinklePark, Character.Sonic, 23, Enemy.Kiki, [], [], []),
    EnemyLocation(14024, Area.TwinklePark, Character.Sonic, 24, Enemy.Kiki, [], [], []),
    EnemyLocation(14025, Area.TwinklePark, Character.Sonic, 25, Enemy.Kiki, [], [], []),
    EnemyLocation(14026, Area.TwinklePark, Character.Sonic, 26, Enemy.Kiki, [], [], []),
    EnemyLocation(14027, Area.TwinklePark, Character.Sonic, 27, Enemy.Kiki, [], [], []),
    EnemyLocation(14028, Area.TwinklePark, Character.Sonic, 28, Enemy.Kiki, [], [], []),
    EnemyLocation(14029, Area.TwinklePark, Character.Sonic, 29, Enemy.Kiki, [], [], []),
    EnemyLocation(14030, Area.TwinklePark, Character.Sonic, 30, Enemy.Kiki, [], [], []),
    EnemyLocation(14031, Area.TwinklePark, Character.Sonic, 31, Enemy.Kiki, [], [], []),
    EnemyLocation(14032, Area.TwinklePark, Character.Sonic, 32, Enemy.Kiki, [], [], []),
    EnemyLocation(14033, Area.TwinklePark, Character.Sonic, 33, Enemy.Kiki, [], [], []),
    EnemyLocation(14034, Area.TwinklePark, Character.Sonic, 34, Enemy.Kiki, [], [], []),
    EnemyLocation(40001, Area.TwinklePark, Character.Amy, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(40002, Area.TwinklePark, Character.Amy, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(40003, Area.TwinklePark, Character.Amy, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(40004, Area.TwinklePark, Character.Amy, 4, Enemy.Kiki, [], [], []),
    EnemyLocation(40005, Area.TwinklePark, Character.Amy, 5, Enemy.Kiki, [], [], []),
    EnemyLocation(40006, Area.TwinklePark, Character.Amy, 6, Enemy.Kiki, [], [], []),
    EnemyLocation(40007, Area.TwinklePark, Character.Amy, 7, Enemy.Buyon, [], [], []),
    EnemyLocation(40008, Area.TwinklePark, Character.Amy, 8, Enemy.Kiki, [], [], []),
    EnemyLocation(40009, Area.TwinklePark, Character.Amy, 9, Enemy.Buyon, [], [], []),
    EnemyLocation(40010, Area.TwinklePark, Character.Amy, 10, Enemy.Buyon, [], [], []),
    EnemyLocation(40011, Area.TwinklePark, Character.Amy, 11, Enemy.Kiki, [], [], []),
    EnemyLocation(40012, Area.TwinklePark, Character.Amy, 12, Enemy.Kiki, [], [], []),
    EnemyLocation(40013, Area.TwinklePark, Character.Amy, 13, Enemy.Kiki, [], [], []),
    EnemyLocation(40014, Area.TwinklePark, Character.Amy, 14, Enemy.Kiki, [], [], []),
    EnemyLocation(40015, Area.TwinklePark, Character.Amy, 15, Enemy.Kiki, [], [], []),
    EnemyLocation(40016, Area.TwinklePark, Character.Amy, 16, Enemy.Buyon, [], [], []),
    EnemyLocation(60001, Area.TwinklePark, Character.Big, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(60002, Area.TwinklePark, Character.Big, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(60003, Area.TwinklePark, Character.Big, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(60004, Area.TwinklePark, Character.Big, 4, Enemy.Kiki, [], [], []),
]

capsule_location_table: List[CapsuleLocation] = [
    CapsuleLocation(10501, Area.EmeraldCoast, Character.Sonic, 1, Capsule.TenRings, [], [], []),
    CapsuleLocation(10502, Area.EmeraldCoast, Character.Sonic, 2, Capsule.TenRings, [], [], []),
    CapsuleLocation(10503, Area.EmeraldCoast, Character.Sonic, 3, Capsule.TenRings, [], [], []),
    CapsuleLocation(10504, Area.EmeraldCoast, Character.Sonic, 4, Capsule.RandomRings, [], [], []),
    CapsuleLocation(10505, Area.EmeraldCoast, Character.Sonic, 5, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(10506, Area.EmeraldCoast, Character.Sonic, 6, Capsule.TenRings, [], [], []),
    CapsuleLocation(10507, Area.EmeraldCoast, Character.Sonic, 7, Capsule.TenRings, [], [], []),
    CapsuleLocation(10508, Area.EmeraldCoast, Character.Sonic, 8, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(10509, Area.EmeraldCoast, Character.Sonic, 9, Capsule.RandomRings, [], [], []),
    CapsuleLocation(10510, Area.EmeraldCoast, Character.Sonic, 10, Capsule.RandomRings, [], [], []),
    CapsuleLocation(10511, Area.EmeraldCoast, Character.Sonic, 11, Capsule.RandomRings, [], [], []),
    CapsuleLocation(10512, Area.EmeraldCoast, Character.Sonic, 12, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(10513, Area.EmeraldCoast, Character.Sonic, 13, Capsule.TenRings, [], [], []),
    CapsuleLocation(10514, Area.EmeraldCoast, Character.Sonic, 14, Capsule.TenRings, [], [], []),
    CapsuleLocation(10515, Area.EmeraldCoast, Character.Sonic, 15, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(10516, Area.EmeraldCoast, Character.Sonic, 16, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(10517, Area.EmeraldCoast, Character.Sonic, 17, Capsule.FiveRings, [], [], []),
    CapsuleLocation(10518, Area.EmeraldCoast, Character.Sonic, 18, Capsule.FiveRings, [], [], []),
    CapsuleLocation(10519, Area.EmeraldCoast, Character.Sonic, 19, Capsule.FiveRings, [], [], []),
    CapsuleLocation(10520, Area.EmeraldCoast, Character.Sonic, 20, Capsule.RandomRings, [], [], []),
    CapsuleLocation(51501, Area.EmeraldCoast, Character.Gamma, 1, Capsule.TenRings, [], [], []),
    CapsuleLocation(51502, Area.EmeraldCoast, Character.Gamma, 2, Capsule.TenRings, [], [], []),
    CapsuleLocation(51503, Area.EmeraldCoast, Character.Gamma, 3, Capsule.TenRings, [], [], []),
    CapsuleLocation(51504, Area.EmeraldCoast, Character.Gamma, 4, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51505, Area.EmeraldCoast, Character.Gamma, 5, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51506, Area.EmeraldCoast, Character.Gamma, 6, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51507, Area.EmeraldCoast, Character.Gamma, 7, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51508, Area.EmeraldCoast, Character.Gamma, 8, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51509, Area.EmeraldCoast, Character.Gamma, 9, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51510, Area.EmeraldCoast, Character.Gamma, 10, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(51511, Area.EmeraldCoast, Character.Gamma, 11, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51512, Area.EmeraldCoast, Character.Gamma, 12, Capsule.FiveRings, [], [], []),
    CapsuleLocation(51513, Area.EmeraldCoast, Character.Gamma, 13, Capsule.RandomRings, [], [], []),
    CapsuleLocation(62501, Area.EmeraldCoast, Character.Big, 1, Capsule.TenRings, [], [], []),
    CapsuleLocation(62502, Area.EmeraldCoast, Character.Big, 2, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(11501, Area.WindyValley, Character.Sonic, 1, Capsule.TenRings, [], [], []),
    CapsuleLocation(11502, Area.WindyValley, Character.Sonic, 2, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(11503, Area.WindyValley, Character.Sonic, 3, Capsule.Shield, [], [], []),
    CapsuleLocation(11504, Area.WindyValley, Character.Sonic, 4, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(11505, Area.WindyValley, Character.Sonic, 5, Capsule.RandomRings, [], [], []),
    CapsuleLocation(11506, Area.WindyValley, Character.Sonic, 6, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(11507, Area.WindyValley, Character.Sonic, 7, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(11508, Area.WindyValley, Character.Sonic, 8, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(11509, Area.WindyValley, Character.Sonic, 9, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(11510, Area.WindyValley, Character.Sonic, 10, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(11511, Area.WindyValley, Character.Sonic, 11, Capsule.RandomRings, [], [], []),
    CapsuleLocation(11512, Area.WindyValley, Character.Sonic, 12, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(11513, Area.WindyValley, Character.Sonic, 13, Capsule.RandomRings, [], [], []),
    CapsuleLocation(11514, Area.WindyValley, Character.Sonic, 14, Capsule.RandomRings, [], [], []),
    CapsuleLocation(11515, Area.WindyValley, Character.Sonic, 15, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(11516, Area.WindyValley, Character.Sonic, 16, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(11517, Area.WindyValley, Character.Sonic, 17, Capsule.RandomRings, [], [], []),
    CapsuleLocation(20501, Area.WindyValley, Character.Tails, 1, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(20502, Area.WindyValley, Character.Tails, 2, Capsule.FiveRings, [], [], []),
    CapsuleLocation(20503, Area.WindyValley, Character.Tails, 3, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(20504, Area.WindyValley, Character.Tails, 4, Capsule.RandomRings, [], [], []),
    CapsuleLocation(20505, Area.WindyValley, Character.Tails, 5, Capsule.TenRings, [], [], []),
    CapsuleLocation(20506, Area.WindyValley, Character.Tails, 6, Capsule.TenRings, [], [], []),
    CapsuleLocation(20507, Area.WindyValley, Character.Tails, 7, Capsule.RandomRings, [], [], []),
    CapsuleLocation(20508, Area.WindyValley, Character.Tails, 8, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(20509, Area.WindyValley, Character.Tails, 9, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(20510, Area.WindyValley, Character.Tails, 10, Capsule.RandomRings, [], [], []),
    CapsuleLocation(52501, Area.WindyValley, Character.Gamma, 1, Capsule.ExtraLife, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52502, Area.WindyValley, Character.Gamma, 2, Capsule.SpeedUp, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52503, Area.WindyValley, Character.Gamma, 3, Capsule.TenRings, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52504, Area.WindyValley, Character.Gamma, 4, Capsule.FiveRings, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52505, Area.WindyValley, Character.Gamma, 5, Capsule.Invincibility, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52506, Area.WindyValley, Character.Gamma, 6, Capsule.MagneticShield, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52507, Area.WindyValley, Character.Gamma, 7, Capsule.RandomRings, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52508, Area.WindyValley, Character.Gamma, 8, Capsule.ExtraLife, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52509, Area.WindyValley, Character.Gamma, 9, Capsule.RandomRings, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(52510, Area.WindyValley, Character.Gamma, 10, Capsule.RandomRings, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    CapsuleLocation(14501, Area.TwinklePark, Character.Sonic, 1, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14502, Area.TwinklePark, Character.Sonic, 2, Capsule.TenRings, [], [], []),
    CapsuleLocation(14503, Area.TwinklePark, Character.Sonic, 3, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14504, Area.TwinklePark, Character.Sonic, 4, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14505, Area.TwinklePark, Character.Sonic, 5, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14506, Area.TwinklePark, Character.Sonic, 6, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14507, Area.TwinklePark, Character.Sonic, 7, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14508, Area.TwinklePark, Character.Sonic, 8, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(14509, Area.TwinklePark, Character.Sonic, 9, Capsule.Bomb, [], [], []),
    CapsuleLocation(14510, Area.TwinklePark, Character.Sonic, 10, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(14511, Area.TwinklePark, Character.Sonic, 11, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14512, Area.TwinklePark, Character.Sonic, 12, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14513, Area.TwinklePark, Character.Sonic, 13, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14514, Area.TwinklePark, Character.Sonic, 14, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14515, Area.TwinklePark, Character.Sonic, 15, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14516, Area.TwinklePark, Character.Sonic, 16, Capsule.TenRings, [], [], []),
    CapsuleLocation(14517, Area.TwinklePark, Character.Sonic, 17, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14518, Area.TwinklePark, Character.Sonic, 18, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14519, Area.TwinklePark, Character.Sonic, 19, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14520, Area.TwinklePark, Character.Sonic, 20, Capsule.Invincibility, [], [], []),
    CapsuleLocation(14521, Area.TwinklePark, Character.Sonic, 21, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14522, Area.TwinklePark, Character.Sonic, 22, Capsule.Invincibility, [], [], []),
    CapsuleLocation(14523, Area.TwinklePark, Character.Sonic, 23, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14524, Area.TwinklePark, Character.Sonic, 24, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14525, Area.TwinklePark, Character.Sonic, 25, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14526, Area.TwinklePark, Character.Sonic, 26, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(14527, Area.TwinklePark, Character.Sonic, 27, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14528, Area.TwinklePark, Character.Sonic, 28, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14529, Area.TwinklePark, Character.Sonic, 29, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14530, Area.TwinklePark, Character.Sonic, 30, Capsule.TenRings, [], [], []),
    CapsuleLocation(14531, Area.TwinklePark, Character.Sonic, 31, Capsule.Shield, [], [], []),
    CapsuleLocation(14532, Area.TwinklePark, Character.Sonic, 32, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(14533, Area.TwinklePark, Character.Sonic, 33, Capsule.FiveRings, [], [], []),
    CapsuleLocation(14534, Area.TwinklePark, Character.Sonic, 34, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14535, Area.TwinklePark, Character.Sonic, 35, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14536, Area.TwinklePark, Character.Sonic, 36, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14537, Area.TwinklePark, Character.Sonic, 37, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14538, Area.TwinklePark, Character.Sonic, 38, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14539, Area.TwinklePark, Character.Sonic, 39, Capsule.RandomRings, [], [], []),
    CapsuleLocation(14540, Area.TwinklePark, Character.Sonic, 40, Capsule.FiveRings, [], [], []),
    CapsuleLocation(40501, Area.TwinklePark, Character.Amy, 1, Capsule.RandomRings, [], [], []),
    CapsuleLocation(40502, Area.TwinklePark, Character.Amy, 2, Capsule.RandomRings, [], [], []),
    CapsuleLocation(40503, Area.TwinklePark, Character.Amy, 3, Capsule.RandomRings, [], [], []),
    CapsuleLocation(40504, Area.TwinklePark, Character.Amy, 4, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(40505, Area.TwinklePark, Character.Amy, 5, Capsule.Shield, [], [], []),
    CapsuleLocation(40506, Area.TwinklePark, Character.Amy, 6, Capsule.TenRings, [], [], []),
    CapsuleLocation(40507, Area.TwinklePark, Character.Amy, 7, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(40508, Area.TwinklePark, Character.Amy, 8, Capsule.RandomRings, [], [], []),
    CapsuleLocation(40509, Area.TwinklePark, Character.Amy, 9, Capsule.RandomRings, [], [], []),
    CapsuleLocation(60501, Area.TwinklePark, Character.Big, 1, Capsule.RandomRings, [], [], []),
    CapsuleLocation(60502, Area.TwinklePark, Character.Big, 2, Capsule.RandomRings, [], [], []),
]
