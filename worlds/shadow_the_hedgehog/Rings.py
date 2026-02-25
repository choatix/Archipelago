from enum import IntEnum

from worlds.shadow_the_hedgehog.Names import REGION_INDICES, STAGE_CIRCUS_PARK


class RingObtainType(IntEnum):
    GroundOrCapsule = 1
    Bell = 2
    ShootingGallery = 3
    SecretShootingGallery = 4
    FlameRing = 5
    LightDash = 6
    HardToRepeatBell = 7
    TurretShootingGallery = 8

class RingInfo:
    stage: int
    region: int
    obtain_type: int
    count: int

    def __init__(self, stage, region, obtain_type, count):
        self.stage = stage
        self.region = region
        self.obtain_type = obtain_type
        self.count = count


RingInformation = [
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ZERO, RingObtainType.GroundOrCapsule, 4),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ZERO, RingObtainType.HardToRepeatBell, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ONE, RingObtainType.GroundOrCapsule, 36),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ONE, RingObtainType.ShootingGallery, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_ZIP_WIRE, RingObtainType.GroundOrCapsule, 5),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, RingObtainType.GroundOrCapsule, 16),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, RingObtainType.FlameRing, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, RingObtainType.FlameRing, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, RingObtainType.ShootingGallery, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, RingObtainType.LightDash, 10),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_THREE, RingObtainType.GroundOrCapsule, 36),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_THREE, RingObtainType.ShootingGallery, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_THREE_BELL, RingObtainType.Bell, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR, RingObtainType.GroundOrCapsule, 28),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_FOUR_LOWER, RingObtainType.ShootingGallery, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_FOUR_LOWER, RingObtainType.GroundOrCapsule, 21),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_FOUR_LOWER, RingObtainType.Bell, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_KEY_DOOR, RingObtainType.SecretShootingGallery, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FIVE, RingObtainType.GroundOrCapsule, 8),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FIVE, RingObtainType.ShootingGallery, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_ROCKET, RingObtainType.FlameRing, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_ROCKET, RingObtainType.FlameRing, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_TURRET, RingObtainType.ShootingGallery, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_BACK, RingObtainType.GroundOrCapsule, 17),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_BACK, RingObtainType.Bell, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SIX, RingObtainType.GroundOrCapsule, 40),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SIX, RingObtainType.ShootingGallery, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SIX, RingObtainType.FlameRing, 4),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_PULLEY, RingObtainType.GroundOrCapsule, 12),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ZERO, RingObtainType.FlameRing, None),

    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_ZIPWIRE, RingObtainType.FlameRing, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_ZIPWIRE, RingObtainType.FlameRing, None),
    RingInfo(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_ZIPWIRE, RingObtainType.FlameRing, None)
]