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
    EnemyLocation(15001, Area.SpeedHighway, Character.Sonic, 1, Enemy.Spinner, [], [], []),
    EnemyLocation(15002, Area.SpeedHighway, Character.Sonic, 2, Enemy.Spinner, [], [], []),
    EnemyLocation(15003, Area.SpeedHighway, Character.Sonic, 3, Enemy.Spinner, [], [], []),
    EnemyLocation(15004, Area.SpeedHighway, Character.Sonic, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(15005, Area.SpeedHighway, Character.Sonic, 5, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15006, Area.SpeedHighway, Character.Sonic, 6, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15007, Area.SpeedHighway, Character.Sonic, 7, Enemy.Spinner, [], [], []),
    EnemyLocation(15008, Area.SpeedHighway, Character.Sonic, 8, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15009, Area.SpeedHighway, Character.Sonic, 9, Enemy.Spinner, [], [], []),
    EnemyLocation(15010, Area.SpeedHighway, Character.Sonic, 10, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(15011, Area.SpeedHighway, Character.Sonic, 11, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15012, Area.SpeedHighway, Character.Sonic, 12, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(15013, Area.SpeedHighway, Character.Sonic, 13, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(15014, Area.SpeedHighway, Character.Sonic, 14, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15015, Area.SpeedHighway, Character.Sonic, 15, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15016, Area.SpeedHighway, Character.Sonic, 16, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15017, Area.SpeedHighway, Character.Sonic, 17, Enemy.Spinner, [], [], []),
    EnemyLocation(15018, Area.SpeedHighway, Character.Sonic, 18, Enemy.Spinner, [], [], []),
    EnemyLocation(15019, Area.SpeedHighway, Character.Sonic, 19, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15020, Area.SpeedHighway, Character.Sonic, 20, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15021, Area.SpeedHighway, Character.Sonic, 21, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15022, Area.SpeedHighway, Character.Sonic, 22, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15023, Area.SpeedHighway, Character.Sonic, 23, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15024, Area.SpeedHighway, Character.Sonic, 24, Enemy.Spinner, [], [], []),
    EnemyLocation(15025, Area.SpeedHighway, Character.Sonic, 25, Enemy.Spinner, [], [], []),
    EnemyLocation(15026, Area.SpeedHighway, Character.Sonic, 26, Enemy.Spinner, [], [], []),
    EnemyLocation(15027, Area.SpeedHighway, Character.Sonic, 27, Enemy.Spinner, [], [], []),
    EnemyLocation(15028, Area.SpeedHighway, Character.Sonic, 28, Enemy.Spinner, [], [], []),
    EnemyLocation(15029, Area.SpeedHighway, Character.Sonic, 29, Enemy.Spinner, [], [], []),
    EnemyLocation(15030, Area.SpeedHighway, Character.Sonic, 30, Enemy.Spinner, [], [], []),
    EnemyLocation(15031, Area.SpeedHighway, Character.Sonic, 31, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15032, Area.SpeedHighway, Character.Sonic, 32, Enemy.Spinner, [], [], []),
    EnemyLocation(15033, Area.SpeedHighway, Character.Sonic, 33, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15034, Area.SpeedHighway, Character.Sonic, 34, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15035, Area.SpeedHighway, Character.Sonic, 35, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15036, Area.SpeedHighway, Character.Sonic, 36, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15037, Area.SpeedHighway, Character.Sonic, 37, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(15038, Area.SpeedHighway, Character.Sonic, 38, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(15039, Area.SpeedHighway, Character.Sonic, 39, Enemy.Spinner, [], [], []),
    EnemyLocation(15040, Area.SpeedHighway, Character.Sonic, 40, Enemy.Spinner, [], [], []),
    EnemyLocation(15041, Area.SpeedHighway, Character.Sonic, 41, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15042, Area.SpeedHighway, Character.Sonic, 42, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15043, Area.SpeedHighway, Character.Sonic, 43, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15044, Area.SpeedHighway, Character.Sonic, 44, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15045, Area.SpeedHighway, Character.Sonic, 45, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15046, Area.SpeedHighway, Character.Sonic, 46, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15047, Area.SpeedHighway, Character.Sonic, 47, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(15048, Area.SpeedHighway, Character.Sonic, 48, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24001, Area.SpeedHighway, Character.Tails, 1, Enemy.Spinner, [], [], []),
    EnemyLocation(24002, Area.SpeedHighway, Character.Tails, 2, Enemy.Spinner, [], [], []),
    EnemyLocation(24003, Area.SpeedHighway, Character.Tails, 3, Enemy.Spinner, [], [], []),
    EnemyLocation(24004, Area.SpeedHighway, Character.Tails, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(24005, Area.SpeedHighway, Character.Tails, 5, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24006, Area.SpeedHighway, Character.Tails, 6, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24007, Area.SpeedHighway, Character.Tails, 7, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24008, Area.SpeedHighway, Character.Tails, 8, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24009, Area.SpeedHighway, Character.Tails, 9, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24010, Area.SpeedHighway, Character.Tails, 10, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24011, Area.SpeedHighway, Character.Tails, 11, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24012, Area.SpeedHighway, Character.Tails, 12, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24013, Area.SpeedHighway, Character.Tails, 13, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24014, Area.SpeedHighway, Character.Tails, 14, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24015, Area.SpeedHighway, Character.Tails, 15, Enemy.Spinner, [], [], []),
    EnemyLocation(24016, Area.SpeedHighway, Character.Tails, 16, Enemy.Spinner, [], [], []),
    EnemyLocation(24017, Area.SpeedHighway, Character.Tails, 17, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24018, Area.SpeedHighway, Character.Tails, 18, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24019, Area.SpeedHighway, Character.Tails, 19, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24020, Area.SpeedHighway, Character.Tails, 20, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24021, Area.SpeedHighway, Character.Tails, 21, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24022, Area.SpeedHighway, Character.Tails, 22, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24023, Area.SpeedHighway, Character.Tails, 23, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24024, Area.SpeedHighway, Character.Tails, 24, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24025, Area.SpeedHighway, Character.Tails, 25, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24026, Area.SpeedHighway, Character.Tails, 26, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24027, Area.SpeedHighway, Character.Tails, 27, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24028, Area.SpeedHighway, Character.Tails, 28, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(24029, Area.SpeedHighway, Character.Tails, 29, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24030, Area.SpeedHighway, Character.Tails, 30, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(24031, Area.SpeedHighway, Character.Tails, 31, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30001, Area.SpeedHighway, Character.Knuckles, 1, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30002, Area.SpeedHighway, Character.Knuckles, 2, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30003, Area.SpeedHighway, Character.Knuckles, 3, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30004, Area.SpeedHighway, Character.Knuckles, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(30005, Area.SpeedHighway, Character.Knuckles, 5, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(30006, Area.SpeedHighway, Character.Knuckles, 6, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30007, Area.SpeedHighway, Character.Knuckles, 7, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30008, Area.SpeedHighway, Character.Knuckles, 8, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(30009, Area.SpeedHighway, Character.Knuckles, 9, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30010, Area.SpeedHighway, Character.Knuckles, 10, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(30011, Area.SpeedHighway, Character.Knuckles, 11, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(30012, Area.SpeedHighway, Character.Knuckles, 12, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(30013, Area.SpeedHighway, Character.Knuckles, 13, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30014, Area.SpeedHighway, Character.Knuckles, 14, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(30015, Area.SpeedHighway, Character.Knuckles, 15, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(30016, Area.SpeedHighway, Character.Knuckles, 16, Enemy.CopSpeeder, [], [], []),
    EnemyLocation(16001, Area.RedMountain, Character.Sonic, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(16002, Area.RedMountain, Character.Sonic, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(16003, Area.RedMountain, Character.Sonic, 3, Enemy.Kiki, [], [], []),
    EnemyLocation(16004, Area.RedMountain, Character.Sonic, 4, Enemy.Gola, [], [], []),
    EnemyLocation(16005, Area.RedMountain, Character.Sonic, 5, Enemy.Spinner, [], [], []),
    EnemyLocation(16006, Area.RedMountain, Character.Sonic, 6, Enemy.Spinner, [], [], []),
    EnemyLocation(16007, Area.RedMountain, Character.Sonic, 7, Enemy.Kiki, [], [], []),
    EnemyLocation(16008, Area.RedMountain, Character.Sonic, 8, Enemy.Kiki, [], [], []),
    EnemyLocation(16009, Area.RedMountain, Character.Sonic, 9, Enemy.Gola, [], [], []),
    EnemyLocation(16010, Area.RedMountain, Character.Sonic, 10, Enemy.Spinner, [], [], []),
    EnemyLocation(16011, Area.RedMountain, Character.Sonic, 11, Enemy.Spinner, [], [], []),
    EnemyLocation(16012, Area.RedMountain, Character.Sonic, 12, Enemy.Gola, [], [], []),
    EnemyLocation(16013, Area.RedMountain, Character.Sonic, 13, Enemy.Spinner, [], [], []),
    EnemyLocation(16014, Area.RedMountain, Character.Sonic, 14, Enemy.Spinner, [], [], []),
    EnemyLocation(16015, Area.RedMountain, Character.Sonic, 15, Enemy.Spinner, [], [], []),
    EnemyLocation(16016, Area.RedMountain, Character.Sonic, 16, Enemy.Spinner, [], [], []),
    EnemyLocation(16017, Area.RedMountain, Character.Sonic, 17, Enemy.Spinner, [], [], []),
    EnemyLocation(16018, Area.RedMountain, Character.Sonic, 18, Enemy.Spinner, [], [], []),
    EnemyLocation(16019, Area.RedMountain, Character.Sonic, 19, Enemy.Kiki, [], [], []),
    EnemyLocation(16020, Area.RedMountain, Character.Sonic, 20, Enemy.Spinner, [], [], []),
    EnemyLocation(16021, Area.RedMountain, Character.Sonic, 21, Enemy.Kiki, [], [], []),
    EnemyLocation(16022, Area.RedMountain, Character.Sonic, 22, Enemy.Gola, [], [], []),
    EnemyLocation(16023, Area.RedMountain, Character.Sonic, 23, Enemy.Spinner, [], [], []),
    EnemyLocation(16024, Area.RedMountain, Character.Sonic, 24, Enemy.Spinner, [], [], []),
    EnemyLocation(16025, Area.RedMountain, Character.Sonic, 25, Enemy.Spinner, [], [], []),
    EnemyLocation(16026, Area.RedMountain, Character.Sonic, 26, Enemy.Spinner, [], [], []),
    EnemyLocation(16027, Area.RedMountain, Character.Sonic, 27, Enemy.Spinner, [], [], []),
    EnemyLocation(16028, Area.RedMountain, Character.Sonic, 28, Enemy.Spinner, [], [], []),
    EnemyLocation(16029, Area.RedMountain, Character.Sonic, 29, Enemy.Spinner, [], [], []),
    EnemyLocation(16030, Area.RedMountain, Character.Sonic, 30, Enemy.Spinner, [], [], []),
    EnemyLocation(16031, Area.RedMountain, Character.Sonic, 31, Enemy.Gola, [], [], []),
    EnemyLocation(16032, Area.RedMountain, Character.Sonic, 32, Enemy.Kiki, [], [], []),
    EnemyLocation(16033, Area.RedMountain, Character.Sonic, 33, Enemy.Spinner, [], [], []),
    EnemyLocation(16034, Area.RedMountain, Character.Sonic, 34, Enemy.Spinner, [], [], []),
    EnemyLocation(16035, Area.RedMountain, Character.Sonic, 35, Enemy.Spinner, [], [], []),
    EnemyLocation(16036, Area.RedMountain, Character.Sonic, 36, Enemy.Gola, [], [], []),
    EnemyLocation(16037, Area.RedMountain, Character.Sonic, 37, Enemy.Gola, [], [], []),
    EnemyLocation(16038, Area.RedMountain, Character.Sonic, 38, Enemy.Gola, [], [], []),
    EnemyLocation(16039, Area.RedMountain, Character.Sonic, 39, Enemy.Kiki, [], [], []),
    EnemyLocation(16040, Area.RedMountain, Character.Sonic, 40, Enemy.Kiki, [], [], []),
    EnemyLocation(16041, Area.RedMountain, Character.Sonic, 41, Enemy.Gola, [], [], []),
    EnemyLocation(16042, Area.RedMountain, Character.Sonic, 42, Enemy.Spinner, [], [], []),
    EnemyLocation(16043, Area.RedMountain, Character.Sonic, 43, Enemy.Spinner, [], [], []),
    EnemyLocation(16044, Area.RedMountain, Character.Sonic, 44, Enemy.Spinner, [], [], []),
    EnemyLocation(16045, Area.RedMountain, Character.Sonic, 45, Enemy.Spinner, [], [], []),
    EnemyLocation(16046, Area.RedMountain, Character.Sonic, 46, Enemy.Kiki, [], [], []),
    EnemyLocation(16047, Area.RedMountain, Character.Sonic, 47, Enemy.Spinner, [], [], []),
    EnemyLocation(16048, Area.RedMountain, Character.Sonic, 48, Enemy.Spinner, [], [], []),
    EnemyLocation(16049, Area.RedMountain, Character.Sonic, 49, Enemy.Spinner, [], [], []),
    EnemyLocation(16050, Area.RedMountain, Character.Sonic, 50, Enemy.Kiki, [], [], []),
    EnemyLocation(16051, Area.RedMountain, Character.Sonic, 51, Enemy.Spinner, [], [], []),
    EnemyLocation(16052, Area.RedMountain, Character.Sonic, 52, Enemy.Spinner, [], [], []),
    EnemyLocation(16053, Area.RedMountain, Character.Sonic, 53, Enemy.Spinner, [], [], []),
    EnemyLocation(16054, Area.RedMountain, Character.Sonic, 54, Enemy.Spinner, [], [], []),
    EnemyLocation(16055, Area.RedMountain, Character.Sonic, 55, Enemy.Spinner, [], [], []),
    EnemyLocation(16056, Area.RedMountain, Character.Sonic, 56, Enemy.Kiki, [], [], []),
    EnemyLocation(16057, Area.RedMountain, Character.Sonic, 57, Enemy.Spinner, [], [], []),
    EnemyLocation(16058, Area.RedMountain, Character.Sonic, 58, Enemy.Kiki, [], [], []),
    EnemyLocation(16059, Area.RedMountain, Character.Sonic, 59, Enemy.Spinner, [], [], []),
    EnemyLocation(16060, Area.RedMountain, Character.Sonic, 60, Enemy.Spinner, [], [], []),
    EnemyLocation(16061, Area.RedMountain, Character.Sonic, 61, Enemy.Spinner, [], [], []),
    EnemyLocation(32001, Area.RedMountain, Character.Knuckles, 1, Enemy.Spinner, [], [], []),
    EnemyLocation(32002, Area.RedMountain, Character.Knuckles, 2, Enemy.Spinner, [], [], []),
    EnemyLocation(32003, Area.RedMountain, Character.Knuckles, 3, Enemy.Spinner, [], [], []),
    EnemyLocation(32004, Area.RedMountain, Character.Knuckles, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(32005, Area.RedMountain, Character.Knuckles, 5, Enemy.Kiki, [], [], []),
    EnemyLocation(32006, Area.RedMountain, Character.Knuckles, 6, Enemy.Spinner, [], [], []),
    EnemyLocation(32007, Area.RedMountain, Character.Knuckles, 7, Enemy.Spinner, [], [], []),
    EnemyLocation(32008, Area.RedMountain, Character.Knuckles, 8, Enemy.Spinner, [], [], []),
    EnemyLocation(32009, Area.RedMountain, Character.Knuckles, 9, Enemy.Gola, [], [], []),
    EnemyLocation(32010, Area.RedMountain, Character.Knuckles, 10, Enemy.Spinner, [], [], []),
    EnemyLocation(32011, Area.RedMountain, Character.Knuckles, 11, Enemy.Kiki, [], [], []),
    EnemyLocation(32012, Area.RedMountain, Character.Knuckles, 12, Enemy.Spinner, [], [], []),
    EnemyLocation(32013, Area.RedMountain, Character.Knuckles, 13, Enemy.Spinner, [], [], []),
    EnemyLocation(32014, Area.RedMountain, Character.Knuckles, 14, Enemy.Gola, [], [], []),
    EnemyLocation(32015, Area.RedMountain, Character.Knuckles, 15, Enemy.Spinner, [], [], []),
    EnemyLocation(32016, Area.RedMountain, Character.Knuckles, 16, Enemy.Spinner, [], [], []),
    EnemyLocation(32017, Area.RedMountain, Character.Knuckles, 17, Enemy.Spinner, [], [], []),
    EnemyLocation(32018, Area.RedMountain, Character.Knuckles, 18, Enemy.Kiki, [], [], []),
    EnemyLocation(32019, Area.RedMountain, Character.Knuckles, 19, Enemy.Spinner, [], [], []),
    EnemyLocation(32020, Area.RedMountain, Character.Knuckles, 20, Enemy.Kiki, [], [], []),
    EnemyLocation(32021, Area.RedMountain, Character.Knuckles, 21, Enemy.Spinner, [], [], []),
    EnemyLocation(32022, Area.RedMountain, Character.Knuckles, 22, Enemy.Kiki, [], [], []),
    EnemyLocation(53001, Area.RedMountain, Character.Gamma, 1, Enemy.Kiki, [], [], []),
    EnemyLocation(53002, Area.RedMountain, Character.Gamma, 2, Enemy.Kiki, [], [], []),
    EnemyLocation(53003, Area.RedMountain, Character.Gamma, 3, Enemy.Spinner, [], [], []),
    EnemyLocation(53004, Area.RedMountain, Character.Gamma, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(53005, Area.RedMountain, Character.Gamma, 5, Enemy.Spinner, [], [], []),
    EnemyLocation(53006, Area.RedMountain, Character.Gamma, 6, Enemy.Spinner, [], [], []),
    EnemyLocation(53007, Area.RedMountain, Character.Gamma, 7, Enemy.Spinner, [], [], []),
    EnemyLocation(53008, Area.RedMountain, Character.Gamma, 8, Enemy.Kiki, [], [], []),
    EnemyLocation(53009, Area.RedMountain, Character.Gamma, 9, Enemy.Kiki, [], [], []),
    EnemyLocation(53010, Area.RedMountain, Character.Gamma, 10, Enemy.Kiki, [], [], []),
    EnemyLocation(53011, Area.RedMountain, Character.Gamma, 11, Enemy.Kiki, [], [], []),
    EnemyLocation(53012, Area.RedMountain, Character.Gamma, 12, Enemy.Kiki, [], [], []),
    EnemyLocation(53013, Area.RedMountain, Character.Gamma, 13, Enemy.Spinner, [], [], []),
    EnemyLocation(53014, Area.RedMountain, Character.Gamma, 14, Enemy.Spinner, [], [], []),
    EnemyLocation(53015, Area.RedMountain, Character.Gamma, 15, Enemy.Spinner, [], [], []),
    EnemyLocation(53016, Area.RedMountain, Character.Gamma, 16, Enemy.Spinner, [], [], []),
    EnemyLocation(53017, Area.RedMountain, Character.Gamma, 17, Enemy.Spinner, [], [], []),
    EnemyLocation(53018, Area.RedMountain, Character.Gamma, 18, Enemy.Spinner, [], [], []),
    EnemyLocation(53019, Area.RedMountain, Character.Gamma, 19, Enemy.Spinner, [], [], []),
    EnemyLocation(53020, Area.RedMountain, Character.Gamma, 20, Enemy.Spinner, [], [], []),
    EnemyLocation(53021, Area.RedMountain, Character.Gamma, 21, Enemy.Spinner, [], [], []),
    EnemyLocation(53022, Area.RedMountain, Character.Gamma, 22, Enemy.Spinner, [], [], []),
    EnemyLocation(53023, Area.RedMountain, Character.Gamma, 23, Enemy.Spinner, [], [], []),
    EnemyLocation(53024, Area.RedMountain, Character.Gamma, 24, Enemy.Spinner, [], [], []),
    EnemyLocation(53025, Area.RedMountain, Character.Gamma, 25, Enemy.Spinner, [], [], []),
    EnemyLocation(53026, Area.RedMountain, Character.Gamma, 26, Enemy.Spinner, [], [], []),
    EnemyLocation(53027, Area.RedMountain, Character.Gamma, 27, Enemy.Spinner, [], [], []),
    EnemyLocation(53028, Area.RedMountain, Character.Gamma, 28, Enemy.Spinner, [], [], []),
    EnemyLocation(53029, Area.RedMountain, Character.Gamma, 29, Enemy.Spinner, [], [], []),
    EnemyLocation(53030, Area.RedMountain, Character.Gamma, 30, Enemy.Kiki, [], [], []),
    EnemyLocation(53031, Area.RedMountain, Character.Gamma, 31, Enemy.Spinner, [], [], []),
    EnemyLocation(53032, Area.RedMountain, Character.Gamma, 32, Enemy.Spinner, [], [], []),
    EnemyLocation(53033, Area.RedMountain, Character.Gamma, 33, Enemy.Kiki, [], [], []),
    EnemyLocation(53034, Area.RedMountain, Character.Gamma, 34, Enemy.Kiki, [], [], []),
    EnemyLocation(53035, Area.RedMountain, Character.Gamma, 35, Enemy.Kiki, [], [], []),
    EnemyLocation(53036, Area.RedMountain, Character.Gamma, 36, Enemy.Spinner, [], [], []),
    EnemyLocation(53037, Area.RedMountain, Character.Gamma, 37, Enemy.Spinner, [], [], []),
    EnemyLocation(53038, Area.RedMountain, Character.Gamma, 38, Enemy.Spinner, [], [], []),
    EnemyLocation(53039, Area.RedMountain, Character.Gamma, 39, Enemy.Spinner, [], [], []),
    EnemyLocation(53040, Area.RedMountain, Character.Gamma, 40, Enemy.Spinner, [], [], []),
    EnemyLocation(53041, Area.RedMountain, Character.Gamma, 41, Enemy.Spinner, [], [], []),
    EnemyLocation(53042, Area.RedMountain, Character.Gamma, 42, Enemy.Spinner, [], [], []),
    EnemyLocation(53043, Area.RedMountain, Character.Gamma, 43, Enemy.Spinner, [], [], []),
    EnemyLocation(53044, Area.RedMountain, Character.Gamma, 44, Enemy.Kiki, [], [], []),
    EnemyLocation(53045, Area.RedMountain, Character.Gamma, 45, Enemy.Kiki, [], [], []),
    EnemyLocation(53046, Area.RedMountain, Character.Gamma, 46, Enemy.Kiki, [], [], []),
    EnemyLocation(53047, Area.RedMountain, Character.Gamma, 47, Enemy.Spinner, [], [], []),
    EnemyLocation(53048, Area.RedMountain, Character.Gamma, 48, Enemy.Spinner, [], [], []),
    EnemyLocation(53049, Area.RedMountain, Character.Gamma, 49, Enemy.Spinner, [], [], []),
    EnemyLocation(53050, Area.RedMountain, Character.Gamma, 50, Enemy.Spinner, [], [], []),
    EnemyLocation(53051, Area.RedMountain, Character.Gamma, 51, Enemy.Spinner, [], [], []),
    EnemyLocation(17001, Area.SkyDeck, Character.Sonic, 1, Enemy.Spinner, [], [], []),
    EnemyLocation(17002, Area.SkyDeck, Character.Sonic, 2, Enemy.Spinner, [], [], []),
    EnemyLocation(17003, Area.SkyDeck, Character.Sonic, 3, Enemy.Spinner, [], [], []),
    EnemyLocation(17004, Area.SkyDeck, Character.Sonic, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(17005, Area.SkyDeck, Character.Sonic, 5, Enemy.Spinner, [], [], []),
    EnemyLocation(17006, Area.SkyDeck, Character.Sonic, 6, Enemy.Spinner, [], [], []),
    EnemyLocation(17007, Area.SkyDeck, Character.Sonic, 7, Enemy.Spinner, [], [], []),
    EnemyLocation(17008, Area.SkyDeck, Character.Sonic, 8, Enemy.Spinner, [], [], []),
    EnemyLocation(17009, Area.SkyDeck, Character.Sonic, 9, Enemy.Spinner, [], [], []),
    EnemyLocation(17010, Area.SkyDeck, Character.Sonic, 10, Enemy.Spinner, [], [], []),
    EnemyLocation(17011, Area.SkyDeck, Character.Sonic, 11, Enemy.Spinner, [], [], []),
    EnemyLocation(17012, Area.SkyDeck, Character.Sonic, 12, Enemy.Spinner, [], [], []),
    EnemyLocation(17013, Area.SkyDeck, Character.Sonic, 13, Enemy.Spinner, [], [], []),
    EnemyLocation(17014, Area.SkyDeck, Character.Sonic, 14, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17015, Area.SkyDeck, Character.Sonic, 15, Enemy.Spinner, [], [], []),
    EnemyLocation(17016, Area.SkyDeck, Character.Sonic, 16, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17017, Area.SkyDeck, Character.Sonic, 17, Enemy.Spinner, [], [], []),
    EnemyLocation(17018, Area.SkyDeck, Character.Sonic, 18, Enemy.Spinner, [], [], []),
    EnemyLocation(17019, Area.SkyDeck, Character.Sonic, 19, Enemy.Spinner, [], [], []),
    EnemyLocation(17020, Area.SkyDeck, Character.Sonic, 20, Enemy.Spinner, [], [], []),
    EnemyLocation(17021, Area.SkyDeck, Character.Sonic, 21, Enemy.Spinner, [], [], []),
    EnemyLocation(17022, Area.SkyDeck, Character.Sonic, 22, Enemy.Spinner, [], [], []),
    EnemyLocation(17023, Area.SkyDeck, Character.Sonic, 23, Enemy.Spinner, [], [], []),
    EnemyLocation(17024, Area.SkyDeck, Character.Sonic, 24, Enemy.Spinner, [], [], []),
    EnemyLocation(17025, Area.SkyDeck, Character.Sonic, 25, Enemy.Spinner, [], [], []),
    EnemyLocation(17026, Area.SkyDeck, Character.Sonic, 26, Enemy.Spinner, [], [], []),
    EnemyLocation(17027, Area.SkyDeck, Character.Sonic, 27, Enemy.Spinner, [], [], []),
    EnemyLocation(17028, Area.SkyDeck, Character.Sonic, 28, Enemy.Spinner, [], [], []),
    EnemyLocation(17029, Area.SkyDeck, Character.Sonic, 29, Enemy.Spinner, [], [], []),
    EnemyLocation(17030, Area.SkyDeck, Character.Sonic, 30, Enemy.Spinner, [], [], []),
    EnemyLocation(17031, Area.SkyDeck, Character.Sonic, 31, Enemy.Spinner, [], [], []),
    EnemyLocation(17032, Area.SkyDeck, Character.Sonic, 32, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17033, Area.SkyDeck, Character.Sonic, 33, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17034, Area.SkyDeck, Character.Sonic, 34, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17035, Area.SkyDeck, Character.Sonic, 35, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17036, Area.SkyDeck, Character.Sonic, 36, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17037, Area.SkyDeck, Character.Sonic, 37, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17038, Area.SkyDeck, Character.Sonic, 38, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17039, Area.SkyDeck, Character.Sonic, 39, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17040, Area.SkyDeck, Character.Sonic, 40, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17041, Area.SkyDeck, Character.Sonic, 41, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17042, Area.SkyDeck, Character.Sonic, 42, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17043, Area.SkyDeck, Character.Sonic, 43, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17044, Area.SkyDeck, Character.Sonic, 44, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17045, Area.SkyDeck, Character.Sonic, 45, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17046, Area.SkyDeck, Character.Sonic, 46, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17047, Area.SkyDeck, Character.Sonic, 47, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17048, Area.SkyDeck, Character.Sonic, 48, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17049, Area.SkyDeck, Character.Sonic, 49, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17050, Area.SkyDeck, Character.Sonic, 50, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17051, Area.SkyDeck, Character.Sonic, 51, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17052, Area.SkyDeck, Character.Sonic, 52, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17053, Area.SkyDeck, Character.Sonic, 53, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17054, Area.SkyDeck, Character.Sonic, 54, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(17055, Area.SkyDeck, Character.Sonic, 55, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17056, Area.SkyDeck, Character.Sonic, 56, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17057, Area.SkyDeck, Character.Sonic, 57, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(17058, Area.SkyDeck, Character.Sonic, 58, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(23001, Area.SkyDeck, Character.Tails, 1, Enemy.Spinner, [], [], []),
    EnemyLocation(23002, Area.SkyDeck, Character.Tails, 2, Enemy.Spinner, [], [], []),
    EnemyLocation(23003, Area.SkyDeck, Character.Tails, 3, Enemy.Spinner, [], [], []),
    EnemyLocation(23004, Area.SkyDeck, Character.Tails, 4, Enemy.Spinner, [], [], []),
    EnemyLocation(23005, Area.SkyDeck, Character.Tails, 5, Enemy.Spinner, [], [], []),
    EnemyLocation(23006, Area.SkyDeck, Character.Tails, 6, Enemy.Spinner, [], [], []),
    EnemyLocation(23007, Area.SkyDeck, Character.Tails, 7, Enemy.Spinner, [], [], []),
    EnemyLocation(23008, Area.SkyDeck, Character.Tails, 8, Enemy.Spinner, [], [], []),
    EnemyLocation(23009, Area.SkyDeck, Character.Tails, 9, Enemy.SpikySpinner, [], [], []),
    EnemyLocation(34001, Area.SkyDeck, Character.Knuckles, 1, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34002, Area.SkyDeck, Character.Knuckles, 2, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34003, Area.SkyDeck, Character.Knuckles, 3, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34004, Area.SkyDeck, Character.Knuckles, 4, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34005, Area.SkyDeck, Character.Knuckles, 5, Enemy.Spinner, [], [], []),
    EnemyLocation(34006, Area.SkyDeck, Character.Knuckles, 6, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34007, Area.SkyDeck, Character.Knuckles, 7, Enemy.Spinner, [], [], []),
    EnemyLocation(34008, Area.SkyDeck, Character.Knuckles, 8, Enemy.Spinner, [], [], []),
    EnemyLocation(34009, Area.SkyDeck, Character.Knuckles, 9, Enemy.Spinner, [], [], []),
    EnemyLocation(34010, Area.SkyDeck, Character.Knuckles, 10, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34011, Area.SkyDeck, Character.Knuckles, 11, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34012, Area.SkyDeck, Character.Knuckles, 12, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34013, Area.SkyDeck, Character.Knuckles, 13, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34014, Area.SkyDeck, Character.Knuckles, 14, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34015, Area.SkyDeck, Character.Knuckles, 15, Enemy.ElectroSpinner, [], [], []),
    EnemyLocation(34016, Area.SkyDeck, Character.Knuckles, 16, Enemy.ElectroSpinner, [], [], []),
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
    CapsuleLocation(15501, Area.SpeedHighway, Character.Sonic, 1, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(15502, Area.SpeedHighway, Character.Sonic, 2, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15503, Area.SpeedHighway, Character.Sonic, 3, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15504, Area.SpeedHighway, Character.Sonic, 4, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15505, Area.SpeedHighway, Character.Sonic, 5, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15506, Area.SpeedHighway, Character.Sonic, 6, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15507, Area.SpeedHighway, Character.Sonic, 7, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15508, Area.SpeedHighway, Character.Sonic, 8, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15509, Area.SpeedHighway, Character.Sonic, 9, Capsule.Invincibility, [], [], []),
    CapsuleLocation(15510, Area.SpeedHighway, Character.Sonic, 10, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15511, Area.SpeedHighway, Character.Sonic, 11, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15512, Area.SpeedHighway, Character.Sonic, 12, Capsule.RandomRings, [], [], []),
    CapsuleLocation(15513, Area.SpeedHighway, Character.Sonic, 13, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15514, Area.SpeedHighway, Character.Sonic, 14, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15515, Area.SpeedHighway, Character.Sonic, 15, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15516, Area.SpeedHighway, Character.Sonic, 16, Capsule.TenRings, [], [], []),
    CapsuleLocation(15517, Area.SpeedHighway, Character.Sonic, 17, Capsule.Shield, [], [], []),
    CapsuleLocation(15518, Area.SpeedHighway, Character.Sonic, 18, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15519, Area.SpeedHighway, Character.Sonic, 19, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15520, Area.SpeedHighway, Character.Sonic, 20, Capsule.Shield, [], [], []),
    CapsuleLocation(15521, Area.SpeedHighway, Character.Sonic, 21, Capsule.RandomRings, [], [], []),
    CapsuleLocation(15522, Area.SpeedHighway, Character.Sonic, 22, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15523, Area.SpeedHighway, Character.Sonic, 23, Capsule.Bomb, [], [], []),
    CapsuleLocation(15524, Area.SpeedHighway, Character.Sonic, 24, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15525, Area.SpeedHighway, Character.Sonic, 25, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15526, Area.SpeedHighway, Character.Sonic, 26, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15527, Area.SpeedHighway, Character.Sonic, 27, Capsule.TenRings, [], [], []),
    CapsuleLocation(15528, Area.SpeedHighway, Character.Sonic, 28, Capsule.RandomRings, [], [], []),
    CapsuleLocation(15529, Area.SpeedHighway, Character.Sonic, 29, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15530, Area.SpeedHighway, Character.Sonic, 30, Capsule.RandomRings, [], [], []),
    CapsuleLocation(15531, Area.SpeedHighway, Character.Sonic, 31, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15532, Area.SpeedHighway, Character.Sonic, 32, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(15533, Area.SpeedHighway, Character.Sonic, 33, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15534, Area.SpeedHighway, Character.Sonic, 34, Capsule.Shield, [], [], []),
    CapsuleLocation(15535, Area.SpeedHighway, Character.Sonic, 35, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15536, Area.SpeedHighway, Character.Sonic, 36, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15537, Area.SpeedHighway, Character.Sonic, 37, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15538, Area.SpeedHighway, Character.Sonic, 38, Capsule.FiveRings, [], [], []),
    CapsuleLocation(15539, Area.SpeedHighway, Character.Sonic, 39, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(15540, Area.SpeedHighway, Character.Sonic, 40, Capsule.RandomRings, [], [], []),
    CapsuleLocation(15541, Area.SpeedHighway, Character.Sonic, 41, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(15542, Area.SpeedHighway, Character.Sonic, 42, Capsule.RandomRings, [], [], []),
    CapsuleLocation(15543, Area.SpeedHighway, Character.Sonic, 43, Capsule.RandomRings, [], [], []),
    CapsuleLocation(24501, Area.SpeedHighway, Character.Tails, 1, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(24502, Area.SpeedHighway, Character.Tails, 2, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(24503, Area.SpeedHighway, Character.Tails, 3, Capsule.Shield, [], [], []),
    CapsuleLocation(24504, Area.SpeedHighway, Character.Tails, 4, Capsule.RandomRings, [], [], []),
    CapsuleLocation(24505, Area.SpeedHighway, Character.Tails, 5, Capsule.FiveRings, [], [], []),
    CapsuleLocation(24506, Area.SpeedHighway, Character.Tails, 6, Capsule.FiveRings, [], [], []),
    CapsuleLocation(24507, Area.SpeedHighway, Character.Tails, 7, Capsule.FiveRings, [], [], []),
    CapsuleLocation(24508, Area.SpeedHighway, Character.Tails, 8, Capsule.TenRings, [], [], []),
    CapsuleLocation(24509, Area.SpeedHighway, Character.Tails, 9, Capsule.Shield, [], [], []),
    CapsuleLocation(24510, Area.SpeedHighway, Character.Tails, 10, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(24511, Area.SpeedHighway, Character.Tails, 11, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(24512, Area.SpeedHighway, Character.Tails, 12, Capsule.Shield, [], [], []),
    CapsuleLocation(24513, Area.SpeedHighway, Character.Tails, 13, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(24514, Area.SpeedHighway, Character.Tails, 14, Capsule.TenRings, [], [], []),
    CapsuleLocation(24515, Area.SpeedHighway, Character.Tails, 15, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(24516, Area.SpeedHighway, Character.Tails, 16, Capsule.TenRings, [], [], []),
    CapsuleLocation(24517, Area.SpeedHighway, Character.Tails, 17, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(24518, Area.SpeedHighway, Character.Tails, 18, Capsule.RandomRings, [], [], []),
    CapsuleLocation(24519, Area.SpeedHighway, Character.Tails, 19, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(24520, Area.SpeedHighway, Character.Tails, 20, Capsule.FiveRings, [], [], []),
    CapsuleLocation(24521, Area.SpeedHighway, Character.Tails, 21, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(24522, Area.SpeedHighway, Character.Tails, 22, Capsule.RandomRings, [], [], []),
    CapsuleLocation(24523, Area.SpeedHighway, Character.Tails, 23, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(30501, Area.SpeedHighway, Character.Knuckles, 1, Capsule.Shield, [], [], []),
    CapsuleLocation(30502, Area.SpeedHighway, Character.Knuckles, 2, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(30503, Area.SpeedHighway, Character.Knuckles, 3, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(30504, Area.SpeedHighway, Character.Knuckles, 4, Capsule.RandomRings, [], [], []),
    CapsuleLocation(30505, Area.SpeedHighway, Character.Knuckles, 5, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(30506, Area.SpeedHighway, Character.Knuckles, 6, Capsule.TenRings, [], [], []),
    CapsuleLocation(30507, Area.SpeedHighway, Character.Knuckles, 7, Capsule.Shield, [], [], []),
    CapsuleLocation(30508, Area.SpeedHighway, Character.Knuckles, 8, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16501, Area.RedMountain, Character.Sonic, 1, Capsule.TenRings, [], [], []),
    CapsuleLocation(16502, Area.RedMountain, Character.Sonic, 2, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(16503, Area.RedMountain, Character.Sonic, 3, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16504, Area.RedMountain, Character.Sonic, 4, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16505, Area.RedMountain, Character.Sonic, 5, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16506, Area.RedMountain, Character.Sonic, 6, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16507, Area.RedMountain, Character.Sonic, 7, Capsule.TenRings, [], [], []),
    CapsuleLocation(16508, Area.RedMountain, Character.Sonic, 8, Capsule.TenRings, [], [], []),
    CapsuleLocation(16509, Area.RedMountain, Character.Sonic, 9, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16510, Area.RedMountain, Character.Sonic, 10, Capsule.FiveRings, [], [], []),
    CapsuleLocation(16511, Area.RedMountain, Character.Sonic, 11, Capsule.ExtraLife, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], []),
    CapsuleLocation(16512, Area.RedMountain, Character.Sonic, 12, Capsule.ExtraLife, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], []),
    CapsuleLocation(16513, Area.RedMountain, Character.Sonic, 13, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16514, Area.RedMountain, Character.Sonic, 14, Capsule.TenRings, [], [], []),
    CapsuleLocation(16515, Area.RedMountain, Character.Sonic, 15, Capsule.TenRings, [], [], []),
    CapsuleLocation(16516, Area.RedMountain, Character.Sonic, 16, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16517, Area.RedMountain, Character.Sonic, 17, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16518, Area.RedMountain, Character.Sonic, 18, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16519, Area.RedMountain, Character.Sonic, 19, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16520, Area.RedMountain, Character.Sonic, 20, Capsule.TenRings, [], [], []),
    CapsuleLocation(16521, Area.RedMountain, Character.Sonic, 21, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16522, Area.RedMountain, Character.Sonic, 22, Capsule.RandomRings, [], [], []),
    CapsuleLocation(16523, Area.RedMountain, Character.Sonic, 23, Capsule.TenRings, [], [], []),
    CapsuleLocation(16524, Area.RedMountain, Character.Sonic, 24, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(16525, Area.RedMountain, Character.Sonic, 25, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(16526, Area.RedMountain, Character.Sonic, 26, Capsule.TenRings, [], [], []),
    CapsuleLocation(16527, Area.RedMountain, Character.Sonic, 27, Capsule.TenRings, [], [], []),
    CapsuleLocation(16528, Area.RedMountain, Character.Sonic, 28, Capsule.Shield, [], [], []),
    CapsuleLocation(16529, Area.RedMountain, Character.Sonic, 29, Capsule.Shield, [], [], []),
    CapsuleLocation(32501, Area.RedMountain, Character.Knuckles, 1, Capsule.TenRings, [], [], []),
    CapsuleLocation(32502, Area.RedMountain, Character.Knuckles, 2, Capsule.TenRings, [], [], []),
    CapsuleLocation(32503, Area.RedMountain, Character.Knuckles, 3, Capsule.RandomRings, [], [], []),
    CapsuleLocation(32504, Area.RedMountain, Character.Knuckles, 4, Capsule.TenRings, [], [], []),
    CapsuleLocation(32505, Area.RedMountain, Character.Knuckles, 5, Capsule.FiveRings, [], [], []),
    CapsuleLocation(32506, Area.RedMountain, Character.Knuckles, 6, Capsule.TenRings, [], [], []),
    CapsuleLocation(32507, Area.RedMountain, Character.Knuckles, 7, Capsule.Shield, [], [], []),
    CapsuleLocation(32508, Area.RedMountain, Character.Knuckles, 8, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(32509, Area.RedMountain, Character.Knuckles, 9, Capsule.RandomRings, [], [], []),
    CapsuleLocation(32510, Area.RedMountain, Character.Knuckles, 10, Capsule.TenRings, [], [], []),
    CapsuleLocation(32511, Area.RedMountain, Character.Knuckles, 11, Capsule.Invincibility, [], [], []),
    CapsuleLocation(32512, Area.RedMountain, Character.Knuckles, 12, Capsule.TenRings, [], [], []),
    CapsuleLocation(32513, Area.RedMountain, Character.Knuckles, 13, Capsule.TenRings, [], [], []),
    CapsuleLocation(32514, Area.RedMountain, Character.Knuckles, 14, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(32515, Area.RedMountain, Character.Knuckles, 15, Capsule.RandomRings, [], [], []),
    CapsuleLocation(32516, Area.RedMountain, Character.Knuckles, 16, Capsule.RandomRings, [], [], []),
    CapsuleLocation(32517, Area.RedMountain, Character.Knuckles, 17, Capsule.TenRings, [], [], []),
    CapsuleLocation(32518, Area.RedMountain, Character.Knuckles, 18, Capsule.FiveRings, [], [], []),
    CapsuleLocation(32519, Area.RedMountain, Character.Knuckles, 19, Capsule.TenRings, [], [], []),
    CapsuleLocation(32520, Area.RedMountain, Character.Knuckles, 20, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(32521, Area.RedMountain, Character.Knuckles, 21, Capsule.TenRings, [], [], []),
    CapsuleLocation(32522, Area.RedMountain, Character.Knuckles, 22, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(32523, Area.RedMountain, Character.Knuckles, 23, Capsule.TenRings, [], [], []),
    CapsuleLocation(53501, Area.RedMountain, Character.Gamma, 1, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(53502, Area.RedMountain, Character.Gamma, 2, Capsule.FiveRings, [], [], []),
    CapsuleLocation(53503, Area.RedMountain, Character.Gamma, 3, Capsule.FiveRings, [], [], []),
    CapsuleLocation(53504, Area.RedMountain, Character.Gamma, 4, Capsule.FiveRings, [], [], []),
    CapsuleLocation(53505, Area.RedMountain, Character.Gamma, 5, Capsule.Shield, [], [], []),
    CapsuleLocation(53506, Area.RedMountain, Character.Gamma, 6, Capsule.FiveRings, [], [], []),
    CapsuleLocation(53507, Area.RedMountain, Character.Gamma, 7, Capsule.TenRings, [], [], []),
    CapsuleLocation(53508, Area.RedMountain, Character.Gamma, 8, Capsule.TenRings, [], [], []),
    CapsuleLocation(53509, Area.RedMountain, Character.Gamma, 9, Capsule.RandomRings, [], [], []),
    CapsuleLocation(53510, Area.RedMountain, Character.Gamma, 10, Capsule.TenRings, [], [], []),
    CapsuleLocation(17501, Area.SkyDeck, Character.Sonic, 1, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17502, Area.SkyDeck, Character.Sonic, 2, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17503, Area.SkyDeck, Character.Sonic, 3, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17504, Area.SkyDeck, Character.Sonic, 4, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17505, Area.SkyDeck, Character.Sonic, 5, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17506, Area.SkyDeck, Character.Sonic, 6, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17507, Area.SkyDeck, Character.Sonic, 7, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17508, Area.SkyDeck, Character.Sonic, 8, Capsule.Bomb, [], [], []),
    CapsuleLocation(17509, Area.SkyDeck, Character.Sonic, 9, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17510, Area.SkyDeck, Character.Sonic, 10, Capsule.Invincibility, [], [], []),
    CapsuleLocation(17511, Area.SkyDeck, Character.Sonic, 11, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(17512, Area.SkyDeck, Character.Sonic, 12, Capsule.TenRings, [], [], []),
    CapsuleLocation(17513, Area.SkyDeck, Character.Sonic, 13, Capsule.TenRings, [], [], []),
    CapsuleLocation(17514, Area.SkyDeck, Character.Sonic, 14, Capsule.TenRings, [], [], []),
    CapsuleLocation(17515, Area.SkyDeck, Character.Sonic, 15, Capsule.TenRings, [], [], []),
    CapsuleLocation(17516, Area.SkyDeck, Character.Sonic, 16, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17517, Area.SkyDeck, Character.Sonic, 17, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17518, Area.SkyDeck, Character.Sonic, 18, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17519, Area.SkyDeck, Character.Sonic, 19, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17520, Area.SkyDeck, Character.Sonic, 20, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17521, Area.SkyDeck, Character.Sonic, 21, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17522, Area.SkyDeck, Character.Sonic, 22, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17523, Area.SkyDeck, Character.Sonic, 23, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17524, Area.SkyDeck, Character.Sonic, 24, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17525, Area.SkyDeck, Character.Sonic, 25, Capsule.Shield, [], [], []),
    CapsuleLocation(17526, Area.SkyDeck, Character.Sonic, 26, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17527, Area.SkyDeck, Character.Sonic, 27, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17528, Area.SkyDeck, Character.Sonic, 28, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17529, Area.SkyDeck, Character.Sonic, 29, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17530, Area.SkyDeck, Character.Sonic, 30, Capsule.Bomb, [], [], []),
    CapsuleLocation(17531, Area.SkyDeck, Character.Sonic, 31, Capsule.Shield, [], [], []),
    CapsuleLocation(17532, Area.SkyDeck, Character.Sonic, 32, Capsule.TenRings, [], [], []),
    CapsuleLocation(17533, Area.SkyDeck, Character.Sonic, 33, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17534, Area.SkyDeck, Character.Sonic, 34, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17535, Area.SkyDeck, Character.Sonic, 35, Capsule.Shield, [], [], []),
    CapsuleLocation(17536, Area.SkyDeck, Character.Sonic, 36, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17537, Area.SkyDeck, Character.Sonic, 37, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17538, Area.SkyDeck, Character.Sonic, 38, Capsule.Shield, [], [], []),
    CapsuleLocation(17539, Area.SkyDeck, Character.Sonic, 39, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17540, Area.SkyDeck, Character.Sonic, 40, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17541, Area.SkyDeck, Character.Sonic, 41, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17542, Area.SkyDeck, Character.Sonic, 42, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17543, Area.SkyDeck, Character.Sonic, 43, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17544, Area.SkyDeck, Character.Sonic, 44, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17545, Area.SkyDeck, Character.Sonic, 45, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17546, Area.SkyDeck, Character.Sonic, 46, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17547, Area.SkyDeck, Character.Sonic, 47, Capsule.Invincibility, [], [], []),
    CapsuleLocation(17548, Area.SkyDeck, Character.Sonic, 48, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17549, Area.SkyDeck, Character.Sonic, 49, Capsule.Invincibility, [], [], []),
    CapsuleLocation(17550, Area.SkyDeck, Character.Sonic, 50, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(17551, Area.SkyDeck, Character.Sonic, 51, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17552, Area.SkyDeck, Character.Sonic, 52, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17553, Area.SkyDeck, Character.Sonic, 53, Capsule.TenRings, [], [], []),
    CapsuleLocation(17554, Area.SkyDeck, Character.Sonic, 54, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17555, Area.SkyDeck, Character.Sonic, 55, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17556, Area.SkyDeck, Character.Sonic, 56, Capsule.RandomRings, [], [], []),
    CapsuleLocation(17557, Area.SkyDeck, Character.Sonic, 57, Capsule.Invincibility, [], [], []),
    CapsuleLocation(17558, Area.SkyDeck, Character.Sonic, 58, Capsule.Shield, [], [], []),
    CapsuleLocation(17559, Area.SkyDeck, Character.Sonic, 59, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17560, Area.SkyDeck, Character.Sonic, 60, Capsule.FiveRings, [], [], []),
    CapsuleLocation(17561, Area.SkyDeck, Character.Sonic, 61, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(17562, Area.SkyDeck, Character.Sonic, 62, Capsule.TenRings, [], [], []),
    CapsuleLocation(17563, Area.SkyDeck, Character.Sonic, 63, Capsule.TenRings, [], [], []),
    CapsuleLocation(17564, Area.SkyDeck, Character.Sonic, 64, Capsule.TenRings, [], [], []),
    CapsuleLocation(17565, Area.SkyDeck, Character.Sonic, 65, Capsule.TenRings, [], [], []),
    CapsuleLocation(17566, Area.SkyDeck, Character.Sonic, 66, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23501, Area.SkyDeck, Character.Tails, 1, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23502, Area.SkyDeck, Character.Tails, 2, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(23503, Area.SkyDeck, Character.Tails, 3, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23504, Area.SkyDeck, Character.Tails, 4, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(23505, Area.SkyDeck, Character.Tails, 5, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23506, Area.SkyDeck, Character.Tails, 6, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(23507, Area.SkyDeck, Character.Tails, 7, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23508, Area.SkyDeck, Character.Tails, 8, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23509, Area.SkyDeck, Character.Tails, 9, Capsule.MagneticShield, [], [], []),
    CapsuleLocation(23510, Area.SkyDeck, Character.Tails, 10, Capsule.Invincibility, [], [], []),
    CapsuleLocation(23511, Area.SkyDeck, Character.Tails, 11, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(23512, Area.SkyDeck, Character.Tails, 12, Capsule.Invincibility, [], [], []),
    CapsuleLocation(23513, Area.SkyDeck, Character.Tails, 13, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(23514, Area.SkyDeck, Character.Tails, 14, Capsule.TenRings, [], [], []),
    CapsuleLocation(23515, Area.SkyDeck, Character.Tails, 15, Capsule.TenRings, [], [], []),
    CapsuleLocation(23516, Area.SkyDeck, Character.Tails, 16, Capsule.TenRings, [], [], []),
    CapsuleLocation(23517, Area.SkyDeck, Character.Tails, 17, Capsule.TenRings, [], [], []),
    CapsuleLocation(23518, Area.SkyDeck, Character.Tails, 18, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(23519, Area.SkyDeck, Character.Tails, 19, Capsule.Invincibility, [], [], []),
    CapsuleLocation(23520, Area.SkyDeck, Character.Tails, 20, Capsule.Shield, [], [], []),
    CapsuleLocation(23521, Area.SkyDeck, Character.Tails, 21, Capsule.Shield, [], [], []),
    CapsuleLocation(23522, Area.SkyDeck, Character.Tails, 22, Capsule.FiveRings, [], [], []),
    CapsuleLocation(23523, Area.SkyDeck, Character.Tails, 23, Capsule.FiveRings, [], [], []),
    CapsuleLocation(23524, Area.SkyDeck, Character.Tails, 24, Capsule.FiveRings, [], [], []),
    CapsuleLocation(23525, Area.SkyDeck, Character.Tails, 25, Capsule.TenRings, [], [], []),
    CapsuleLocation(23526, Area.SkyDeck, Character.Tails, 26, Capsule.TenRings, [], [], []),
    CapsuleLocation(23527, Area.SkyDeck, Character.Tails, 27, Capsule.TenRings, [], [], []),
    CapsuleLocation(23528, Area.SkyDeck, Character.Tails, 28, Capsule.FiveRings, [], [], []),
    CapsuleLocation(23529, Area.SkyDeck, Character.Tails, 29, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23530, Area.SkyDeck, Character.Tails, 30, Capsule.FiveRings, [], [], []),
    CapsuleLocation(23531, Area.SkyDeck, Character.Tails, 31, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23532, Area.SkyDeck, Character.Tails, 32, Capsule.FiveRings, [], [], []),
    CapsuleLocation(23533, Area.SkyDeck, Character.Tails, 33, Capsule.RandomRings, [], [], []),
    CapsuleLocation(23534, Area.SkyDeck, Character.Tails, 34, Capsule.TenRings, [], [], []),
    CapsuleLocation(23535, Area.SkyDeck, Character.Tails, 35, Capsule.TenRings, [], [], []),
    CapsuleLocation(23536, Area.SkyDeck, Character.Tails, 36, Capsule.TenRings, [], [], []),
    CapsuleLocation(34501, Area.SkyDeck, Character.Knuckles, 1, Capsule.SpeedUp, [], [], []),
    CapsuleLocation(34502, Area.SkyDeck, Character.Knuckles, 2, Capsule.RandomRings, [], [], []),
    CapsuleLocation(34503, Area.SkyDeck, Character.Knuckles, 3, Capsule.RandomRings, [], [], []),
    CapsuleLocation(34504, Area.SkyDeck, Character.Knuckles, 4, Capsule.Shield, [], [], []),
    CapsuleLocation(34505, Area.SkyDeck, Character.Knuckles, 5, Capsule.ExtraLife, [], [], []),
    CapsuleLocation(34506, Area.SkyDeck, Character.Knuckles, 6, Capsule.RandomRings, [], [], []),
    CapsuleLocation(34507, Area.SkyDeck, Character.Knuckles, 7, Capsule.FiveRings, [], [], []),
    CapsuleLocation(34508, Area.SkyDeck, Character.Knuckles, 8, Capsule.TenRings, [], [], []),
    CapsuleLocation(34509, Area.SkyDeck, Character.Knuckles, 9, Capsule.Shield, [], [], []),
    CapsuleLocation(34510, Area.SkyDeck, Character.Knuckles, 10, Capsule.TenRings, [], [], []),
    CapsuleLocation(34511, Area.SkyDeck, Character.Knuckles, 11, Capsule.RandomRings, [], [], []),
    CapsuleLocation(34512, Area.SkyDeck, Character.Knuckles, 12, Capsule.Shield, [], [], []),
]
