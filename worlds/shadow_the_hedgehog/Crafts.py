from .Names import REGION_INDICES, STAGE_AIR_FLEET, STAGE_LETHAL_HIGHWAY, STAGE_IRON_JUNGLE


class CraftSpawn:
    region: int
    hit_rate: int
    caveat: bool

    def __init__(self, region, hit_rate, caveat=False):
        self.region = region
        self.hit_rate = hit_rate
        self.caveat = caveat


class CraftInfo:
    name: str
    health: int
    stage: int
    spawns: list

    def __init__(self, name, health, stage, caveat=False):
        self.name = name
        self.health = health
        self.stage = stage
        self.spawns = []

    def AddSpawn(self, spawn: CraftSpawn):
        self.spawns.append(spawn)
        return self

Crafts = [
    CraftInfo("Black Tank", 350, STAGE_LETHAL_HIGHWAY)
        .AddSpawn(CraftSpawn(REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_ZERO, 45))
        .AddSpawn(CraftSpawn(REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_ONE, 180))
        .AddSpawn(CraftSpawn(REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_THREE, 400, True))
        .AddSpawn(CraftSpawn(REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FOUR, 120))
        .AddSpawn(CraftSpawn(REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET, 250)),


    CraftInfo("Egg Balloon", 400, STAGE_IRON_JUNGLE)
        .AddSpawn(CraftSpawn(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ZERO, 10))
        .AddSpawn(CraftSpawn(REGION_INDICES.IRON_JUNGLE_EARLY_JUMPER, 30))
        .AddSpawn(CraftSpawn(REGION_INDICES.IRON_JUNGLE_ROCKET, 25))
        .AddSpawn(CraftSpawn(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FIVE, 10))
        .AddSpawn(CraftSpawn(REGION_INDICES.IRON_JUNGLE_HERO_ROCKET, 60)),


    CraftInfo("President Aircraft", 800, STAGE_AIR_FLEET)
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE, 100))
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_CHECKPOINT_TWO, 40))
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_CHECKPOINT_FOUR, 80))
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE, 20))
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_FIVE_TURRET, 20))
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_CHECKPOINT_SIX, 30))
        .AddSpawn(CraftSpawn(REGION_INDICES.AIR_FLEET_CHECKPOINT_SEVEN, 60))
]