
from dataclasses import dataclass
from .. import Options, Names


@dataclass
class LevelRegion:
    stageId: int
    regionIndex: int
    restrictionTypes: list[Names.REGION_RESTRICTION_TYPES]
    logicType: int
    chaosControlLogicType: int
    fromRegions: list
    hardLogicOnly: bool = False
    iccLogicOnly: bool = False
    isDiversion: bool = False

    def __init__(self, stageId, regionIndex,
                 restrictionTypes: list[Names.REGION_RESTRICTION_TYPES] | Names.REGION_RESTRICTION_TYPES):
        self.stageId = stageId
        self.regionIndex = regionIndex

        ##if type(restrictionTypes) == int:
        #    print("INT TYPE", stageId, regionIndex, restrictionTypes)

        if type(restrictionTypes) != list:
            self.restrictionTypes = [restrictionTypes]
        else:
            self.restrictionTypes = restrictionTypes
        self.fromRegions = None if regionIndex is None else [regionIndex - 1]
        self.logicType = Options.LogicLevel.option_normal
        self.chaosControlLogicType = Options.ChaosControlLogicLevel.option_off
        self.chaosControlLogicRequiresHeal = False

    def setHardLogicOnly(self):
        self.hardLogicOnly = True
        return self

    def setICCLogicOnly(self):
        self.iccLogicOnly = True
        return self

    def setLogicType(self, logicLevel,
                     chaosControlLogicLevel=Options.ChaosControlLogicLevel.option_off,
                     chaosControlRequiresHeal=False):


        self.logicType = logicLevel
        self.chaosControlLogicType = chaosControlLogicLevel
        self.chaosControlLogicRequiresHeal = chaosControlRequiresHeal
        return self

    def setFromRegion(self, fromRegion):
        if type(fromRegion) is int:
            self.fromRegions = [fromRegion]
        elif type(fromRegion) is list:
            self.fromRegions = fromRegion

        return self

    def setAsDiversion(self):
        self.isDiversion = True
        return self