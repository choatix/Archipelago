from . import Levels


def IsObjectForDesiredTypes():
    pass

def GetTypeId(objectType):
    if objectType == ObjectType.SHADOW_BOX:
        return 0x3A

    if objectType == ObjectType.VEHICLE:
        return 0x4F

    if objectType == ObjectType.ENERGY_CORE:
        return 0x33

    if objectType == ObjectType.LIGHT_DASH_TRAIL:
        return 0x10

    if objectType == ObjectType.STANDARD_PULLEY:
        return 0x08

    if objectType == ObjectType.SPACE_PULLEY:
        return 0xC88

    if objectType == ObjectType.GUN_PULLEY:
        return 0xC88

    if objectType == ObjectType.CIRCUS_PULLEY:
        return 0xC88

    if objectType == ObjectType.BOMB:
        return 0x0D

    if objectType == ObjectType.BOMB_SERVER:
        return 0x1006

    if objectType == ObjectType.HEAL_SERVER:
        return 0x1006

    if objectType == ObjectType.HEAL_UNIT:
        return 0x38

    if objectType == ObjectType.WARP_HOLE:
        return 0x1F

    if objectType == ObjectType.ROCKET:
        return 0x0E

    if objectType == ObjectType.KEY_DOOR:
        return 0x1E

    if objectType == ObjectType.BLACK_ASSASSIN:
        return 0x93

    if objectType == ObjectType.BLACK_HAWK:
        return 0x8E

    if objectType == ObjectType.BLACK_VOLT:
        return 0x8E

    if objectType == ObjectType.BLACK_WARRIOR:
        return 0x8D

    return None

def CheckVehicleAttributes(objectType, extra_bytes):

    if objectType == "Server":
        byte = extra_bytes[3]
        if byte == 0:
            return "Bomb Server"

        if byte == 1:
            return "Heal Server"

    if objectType == "Rings":
        byte_ghost = extra_bytes[(4*4)+3]
        if byte_ghost == 1:
            return "Light Dash Trail"


    if objectType == "Black Warrior":
        byte_saucer = extra_bytes[(23*4)+3]
        if byte_saucer == 0:
            return "Black Warrior"
        if byte_saucer == 1:
            return "Air Saucer Black Warrior"
        else:
            print("xx1", objectType, byte_saucer)
            return "Unknown Black Warrior"

    if objectType == "Black Assassin":
        byte_appear = extra_bytes[(7*4)+3]
        if byte_appear == 3:
            return "Air Saucer Assassin"

    if objectType == "Black Hawk":
        byte_death_type = extra_bytes[(14*4)+3]
        if byte_death_type == 0x00:
            return "Black Hawk"
        if byte_death_type == 0x01:
            return "Black Hawk Rideable"
        elif byte_death_type == 0x10:
            return "Black Volt"
        elif byte_death_type == 0x11:
            return "Black Volt Rideable"
        else:
            print("xx1", objectType, byte_death_type)
            return "Unknown Black Hawk"


    return objectType

class ObjectType:
    SHADOW_BOX = 1

    VEHICLE = 2
    LINKED_VEHICLE_ENEMY = 3
    class ObjectTypeVehicle:
        STANDARD_CAR = 1
        CONVERTIBLE = 2
        ARMORED_CAR = 3
        GUN_MOTORCYCLE = 4
        GUN_JUMPER = 5
        GUN_CANNON = 6
        AIR_SAUCER = 7
        BLACK_HAWK = 8
        BLACK_VOLT = 9
        GUN_TURRET = 10
        BLACK_TURRET = 11
        GUN_LIFT = 12

    ENERGY_CORE = 4

    LIGHT_DASH_TRAIL = 5
    STANDARD_PULLEY = 6
    SPACE_PULLEY = 7
    GUN_PULLEY = 8
    CIRCUS_PULLEY = 9

    BOMB = 10
    BOMB_SERVER= 11
    HEAL_UNIT = 12
    HEAL_SERVER = 13

    WARP_HOLE = 14
    ROCKET = 15

    KEY_DOOR = 16

    BLACK_ASSASSIN = 40
    BLACK_VOLT = 41
    BLACK_HAWK = 42
    BLACK_WARRIOR = 43


class SETObject:
    object_type: int
    stage: int
    index: int
    name: str
    extra: int

    def __init__(self, object_type, stage, index, name, extra=None):
        self.object_type = object_type
        self.stage = stage
        self.index = index
        self.name = name
        self.extra = extra


DESIRABLE_OBJECTS = \
[

    # Westopolis
    # 492 - Energy Core
    # 518 - Pulley (Key 2)
    # 482 - Shadow Box
    # 332 - Secret Door
    # 333 - Armored Car (Secret Door)
    # 516 - GUN vehicle



    # Digital Circuit
    # 63 - Shadow Box
    # 170 - Secret Door
    # 168 - Warp Hole in Secret Door
    # 167 - Warp Hole From Secret Door
    # 276 - Warp Hole After Goal Ring
    # 277 - Warp Hole Out Of After Goal Ring
    # 508 - Shadow Box 2

    # Glyphic Canyon
    # 260 - Shadow Box 1
    # 204 - Bomb
    # 261 - Shadow Box 2
    # 5 - Pulley
    # 73 - Bomb
    # 223 - LD
    # 3 - Secret Door
    # 212 - Black Volt Enemy
    # 234 - Black Volt
    # 292 - Shadow Box 3
    # 262 - Shadow Box 4




    # Lethal Highway
    # 395 - Heal Unit
    # 376 - Heal Unit 2 (Cage)

    # 541 - Heal Unit 3
    # 542 - Heal Unit 4

    # 320 - Shadow Box 1
    # 25 - Secret Door
    # 399 - Rocket

    # 154 - Motorbike
    # 342 - Convertible
    # 518 - Shadow Box 2
    # 141 - Shadow Box 3

    # 458 - Energy Core
    # 324 - Shadow Box 4
    # 53 - Pulley

    # 230 - Motorbike
    # 377 - Heal Unit
    # 381 - Rocket 2
    # 519 - Shadow Box 5
    # 343 - Convertible
    # 297 - Motorbike



    # Cryptic Castle
    # 425 - Zip Line?
    # 426 - Zip Line 2
    # 50 - Bomb
    # 51 - Bomb
    # 52 - Bomb
    # 465 - Shadow Box
    # 392 - Hawk Enemy
    # 421 - Hawk
    # 6 - Hawk Enemy
    # 237 - Hawk
    # 385 - Zip Line

    # 84 - Secret Door
    # 134 - Light Dash Trail
    # 314 - Shadow Box 2
    # 115 - Bomb
    # 112 - Bomb
    # 117 - Bomb
    # 114 - Bomb
    # 414 - Bomb
    # 187 - Special Weapons Box
    # 1 - Zip Line
    # 170 - Light Dash

    # 204 - Hawk
    # 3 - Hawk Enemy


    #Prison Island

    SETObject(ObjectType.LINKED_VEHICLE_ENEMY, Levels.STAGE_PRISON_ISLAND,
              164, "Air Saucer 1 Enemy", extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 462,
              "Air Saucer 1 Despawn", extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.BOMB, Levels.STAGE_PRISON_ISLAND, 266, "Key 2 Bomb 1"),
    SETObject(ObjectType.BOMB, Levels.STAGE_PRISON_ISLAND, 278, "Key 2 Bomb 2"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 282, "Air Saucer @ Key 2",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_PRISON_ISLAND, 383, "Special Weapon Box 1"),
    SETObject(ObjectType.KEY_DOOR, Levels.STAGE_PRISON_ISLAND, 432, "Secret Door"),

    SETObject(ObjectType.STANDARD_PULLEY, Levels.STAGE_PRISON_ISLAND, 565, "Pulley 1"),

    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_PRISON_ISLAND, 379, "Special Weapon Box 2"),
    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_PRISON_ISLAND, 514, "Special Weapon Box 3"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 551, "Air Saucer 2 Despawn",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),

    SETObject(ObjectType.LINKED_VEHICLE_ENEMY, Levels.STAGE_PRISON_ISLAND,
              562, "Air Saucer 2 Enemy", extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),

    SETObject(ObjectType.ENERGY_CORE, Levels.STAGE_PRISON_ISLAND, 597, "Dark Energy Core"),

    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 586, "Air Saucer Dark Split",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),

    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 577, "Air Saucer Hero Split",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),

    SETObject(ObjectType.LINKED_VEHICLE_ENEMY, Levels.STAGE_PRISON_ISLAND,
              330, "Air Saucer Hero Split 2 Enemy", extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.LINKED_VEHICLE_ENEMY, Levels.STAGE_PRISON_ISLAND,
              331, "Air Saucer Hero Split 2 Enemy", extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),

    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 337, "Air Saucer Hero Split 2 (Enemy)",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 344, "Air Saucer Hero Split 3",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),

    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_PRISON_ISLAND, 598, "Special Weapon Box 4"),
    SETObject(ObjectType.LINKED_VEHICLE_ENEMY, Levels.STAGE_PRISON_ISLAND,
              567, "Air Saucer 3 Enemy", extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 544, "Air Saucer 3 Despawn",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_PRISON_ISLAND, 520, "Air Saucer After 3",
              extra=ObjectType.ObjectTypeVehicle.AIR_SAUCER),



    # Circus Park
    # 325 - Zipline 1
    # 215 - Shadow Box 1
    # 66 - Gun Turret 1
    # 266 - Rocket 1
    # 265 - Light Dash Trail
    # 185 - Shadow Box 2
    # 64 - Secret Door
    # 292 - Rocket
    # 92 - Gun Turret 2
    # 116 - End Pulley
    # 328 - Zipline


# Central City
    # 637 - Rocket (H)
    # 108 - Pulley

    # 626 - Bomb (To First Big Bomb)
    # 48 - Pulley
    # 60 - Rocket
    # 690 - Hero Energy Core

    # 129 - Convertible 1
    # 565 - Convertible 2

    # 525 - Shadow Box 1
    # 275 - Gun Vehicle 1
    # 273 - Secret Door
    # 522 - Air Saucer (Secret Door)
    # 653 - Gun Vehicle 2
    # 665 - Bomb 2 (Progress Past Bomb 3)
    # 664 - Bomb 1 (Progress Past Bomb 3)

    # 603 - Gun Turret
    # 345 - Rocket 2
    # 356 - Gun Vehicle 3
    # 374 - Rocket 3
    # 673 - Gun Turret
    # 400 - Shadow Box 2

    # 422 - Bomb (After Last Check)
    # 334 - Bomb

    # Note - logic must factor in Bombs or Bazooka


    # The Doom

    # 397 - Heal Unit in Room 1
    # 396 - Heal Unit in Room 2
    # 258 - First Shadow Box
    # 178 - Secret Door
    # 189 - Pulley to Secret Door
    # 109 - Shadow Box 2 (Triangle Jump)
    # 214 - Bomb Server In Room
    # 398 - Heal Server After Bomb Wall
    # 285 - Bomb Server Up Lift
    # 403 - Heal Server By Researcher 5
    # 194 - Pulley to Key 4
    # 400 - Heal Server by researcher 6/7

    # 222 = Bomb Server After Lift Room
    # 399 - Heal Server After Lift Room
    # 401 - Heal Server After Secret / Other
    # 402 - Heal Server By Researcher 10

    # 265 - Shadow Box near End (3)



    # Sky Troops
    # 240 Shadow Box
    # 27 - Black Turret 1
    # 29 - Pulley after Sphere 1
    # 276 - Light Dash after Pulley
    # 101 - Shadow Box 2
    # 218 - Gun Jumper (1)
    # 314 - Rocket After Jumper
    # 171 - Shaodw Box By Ship 2
    # 59 - Black Turret 2
    # 47 - Gun Jumper (2)
    # 292 - Rocket After Jumper 2
    # 68 - Black Turret 3
    # 189 - Light Dash rings to Turret 4
    # 81 - Black Turret 4
    # 60 - Rocket in Storm
    # 4 - Secret Door
    # 239 - Shadow Box

    # 222 Volt -61 (0) (Change BodyAndDeath Type)
    # 223 Hawk -70 (216)






    # Mad Matrix

    SETObject(ObjectType.WARP_HOLE, Levels.STAGE_MAD_MATRIX, 165, "Warp Hole Into Green Tower"),
    SETObject(ObjectType.WARP_HOLE, Levels.STAGE_MAD_MATRIX, 163, "Warp Hole Exit Of Green Tower"),
    SETObject(ObjectType.WARP_HOLE, Levels.STAGE_MAD_MATRIX, 312, "Warp Hole Exit Of Red Tower"),
    SETObject(ObjectType.WARP_HOLE, Levels.STAGE_MAD_MATRIX, 324, "Warp Hole Exit From Top Of Red Tower"),
    SETObject(ObjectType.WARP_HOLE, Levels.STAGE_MAD_MATRIX, 107, "Warp Hole Into Yellow Tower"),

    SETObject(ObjectType.LIGHT_DASH_TRAIL, Levels.STAGE_MAD_MATRIX, 330, "Light Dash Near Green"),
    SETObject(ObjectType.LIGHT_DASH_TRAIL, Levels.STAGE_MAD_MATRIX, 269, "Light Dash Into Red"),
    SETObject(ObjectType.LIGHT_DASH_TRAIL, Levels.STAGE_MAD_MATRIX, 350, "Light Dash Out Of Red"),
    SETObject(ObjectType.LIGHT_DASH_TRAIL, Levels.STAGE_MAD_MATRIX, 552, "Light Dash Within Yellow"),

    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_MAD_MATRIX, 500, "Shadow Box Near Red"),
    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_MAD_MATRIX, 452, "Shadow Box Near Secret Door"),
    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_MAD_MATRIX, 444, "Shadow Box Near Blue"),
    SETObject(ObjectType.ENERGY_CORE, Levels.STAGE_MAD_MATRIX, 443, "Hero Core"),
    SETObject(ObjectType.KEY_DOOR, Levels.STAGE_MAD_MATRIX, 332, "Secret Door"),


    # 165 - Warp to Green
    # 163 - Warp Out of Green
    # 330 - Light Dash near Green, might be 494
    # 312 - Warp Out of red (exit warp)
    # 269 - LD to Red
    # 350 - LD out Red
    # 324 - Warp Out of Red Center
    # 107 - Warp into Yellow
    # 552 - LD in Yellow
    # 444 - Shadow Box in Blue
    # 443 - Energy Core
    # 332 - Secret Door

    # 452 - Shadow Box near Secret Door
    # 500 - Shadow Box in Red

    # Death Ruins

    #283 - Shadow Box
    #153 - Pulley 1
    # 341 - Secret Warp Hole Exit
    # 3 - Secret Door
    # 380 - Warp Hole Out of Secret Passage
    # 86 - Pulley Near Key 4
    # 40 - Pulley After 5 BA


    # The Ark
    # 1 - Black Volt 1
    # 261 - Shadow Box 1
    # 356 - Black Volt 2
    # 357 - Black Volt 3

    # 286 - Bomb 1
    # 283 - Bomb 2
    # 284 - Bomb 3
    # 250 - Bomb 4
    # 233 - Shadow Box 2
    # 362 - Black Volt 4
    # 358 - Black Volt 5
    # 15 - Black Volt 6
    # 81 - Secret Door
    # 363 - Black Volt 7
    # 20 - Black Volt 8


    # Air Fleet
    # 0 - Pulley
    # 1 - Secret Door
    # 49 - Air Saucer
    # 339 - Shadow Box in Secret Door
    # 169 - Shadow Box First Normal
    # 476 - Car
    # 472 - Gun Cannon 1
    # 275 - Shadow Box 3
    # 244 - Shadow Box on Rail
    # 475 - Car 2

    # 237 - Shadow Box 5
    # 156 - Gun Cannon

    # 466 - Gun Turret 1
    # 465 - Gun Turret 2

    # 162 - Gun Turret 3

    #
    #? 467 - Not found

    # 347 - Shadow Box 6 (Rail)
    # 329 = Light Dash Trail Outdoor
    # 471 - Gun Cannon2

    # Iron Jungle
    # 19 - Gun JUMPER
    # 193 - Shadow Box 1
    # 40 - Pulley (easy logic)
    # 111 - Secret Door
    # 279 - Rocket
    #6 - GUN Jumper
    # 11 - LD
    # 59 - LD
    # 63 - Gun Turret
    # 194 - Shadow Box 2
    # 102 - Pulley
    # 25 - Shadow Box 3

    # 272 - LD
    # 82 - LD
    # 104 - Pulley
    # 266 - Rocket












    # Space Gadget
    # 461 - Shadow Box 1
    # 572 - Hero Core
    # 80 - Hero zipline
    # 60 - Air Saucer
    # 212 - Warrior w/ Saucer
    # 211 - Warrior w/ Saucer 2
    # 275 - Warrior w/ Saucer 3
    # 23 - Secret Door
    # 466 - Secret Warp Hole
    # 467 - Warp Hole Exit
    # 81 - Zipline

    #75 - Dark Zipline
    #288 - Black Warrior Dark w/ Saucer
    # 71 - Air Saucer
    # 414 - Warp Hole Dark
    # 454 - Warp Hole Dark Exit



    # Lost Impact
    SETObject(ObjectType.SHADOW_BOX, Levels.STAGE_LOST_IMPACT,
              158, "Special Weapons Box 1"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              345, "Gun Lift 1 (First Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.BOMB, Levels.STAGE_LOST_IMPACT,
              211, "Bomb (Lift Room 1)"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              342, "Gun Lift 2 (Second Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.BOMB, Levels.STAGE_LOST_IMPACT,
              216, "Side Room Bomb"),
    SETObject(ObjectType.STANDARD_PULLEY, Levels.STAGE_LOST_IMPACT,
              107, "Pulley To Secret Door"),
    SETObject(ObjectType.KEY_DOOR, Levels.STAGE_LOST_IMPACT,
              106, "Secret Door"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              317, "Secret Door Armored Car", extra=ObjectType.ObjectTypeVehicle.ARMORED_CAR),
    SETObject(ObjectType.BOMB, Levels.STAGE_LOST_IMPACT,
              236, "Bomb (Between 2 AC)"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              340, "Gun Lift 3 (Fourth Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              341, "Gun Lift 4 (Fifth Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.ROCKET, Levels.STAGE_LOST_IMPACT,
              320, "Rocket to Key 3"),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              340, "Gun Lift 5 (Seventh Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              339, "Gun Lift 6 (Eighth Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.VEHICLE, Levels.STAGE_LOST_IMPACT,
              325, "Gun Lift 7 (Outer Room)", extra=ObjectType.ObjectTypeVehicle.GUN_LIFT),
    SETObject(ObjectType.BOMB, Levels.STAGE_LOST_IMPACT,
              277, "Bomb In Final Room")


    # Gun Fortress

    #421 - Armored Car (Start)
    # 80 - Shadow Box 1
    # 115 - GUN Turret 1
    # 281 - GUN Turret 2
    # 63 - Zip Line
    # 49/55 - Pulley - one is clearly passageway both?
    # Gun Turret 1 - Comp 1
    # 62 - Zipline (No Hard)
    # 419 - GUN Cannon
    # 7 - Pulley
    # 9 - Rocket
    # 209 - Pulley over Comp 2 (can be done reverse)
    # 259 - Pulley towards Comp 2
    # 431 - Pulley - towards Comp 2
    # 13 - GUN Cannon (Above Comp 2)

    # 366 - Gun Turret 4 (Comp 2)
    # 22 - Gun Turret 5 (Comp 2)

    # 21 - Pulley (Up Key Door) (Key 5, Check n-1)
    # 65 - Zip Line
    # 18 - Secret Door
    # 330 - Secret Door Armored Car

    # 223 - Pulley (Through 3)
    # 246 - Pulley (Through 3)
    # 268 - Gun Turret 6 (Comp 3)
    # 269 - Gun Turret 7 (Comp 3)



    # Black Comet
    # 0 - Air Saucer At Start
    # 370 - Shadow Box 1
    # 10 - Air Sacuer 2
    # 164 - Shadow Box 2
    # 30 - Air Saucer 2
    # 6 - Air Sacuer 3
    # 7 - Air Saucer 4

    # 66 - BA1
    # 143 - BA2
    # 144 - BA3
    # 28 - First Warp Hole Entrance
    # 13 - First Warp Hole Exit

    # 14 - Air Saucer 5
    # 15 - Air Saucer 5.5
    # 78 - BA4
    # 77 - BA5
    # 79 - BA6

    # 61 - Shadow Box 3
    # 99 - Air Saucer 6
    # 191 - Black Turret
    # 96 - Key Door
    # 374 - Shadow Box behind Key Door
    # 231 - Air Saucer 7
    # 109 - Black Turret 2
    # 5 - Air Saucer 8
    # 17 - Warp Hole 2 Entrance
    # 21 - Warp Hole 2 Exit

    # 122 - Air Saucer 9
    # 35 - Black Turret 3
    # 449 - Shadow Box 5
    # 31 - Air Saucer 10
    # 133 - BA7
    # 204 - BA8
    # 205 - BA9
    # 206 - BA10
    # 208 - BA11
    # 209 - BA12
    # 210 - BA13
    # 211 - BA14
    # 212 - BA15
    # 213 - BA16
    # 214 - BA17
    # 215 - BA18
    # 216 - BA19
    # 27 - Warp Hole 3 Entrance
    # 28 - Warp Hole 3 Exit

    # 22 - Air Saucer 11
    # 315 - Air Saucer 12
    # 34 - Air Saucer 13

    # 20 is unknown, near Check 5



    # Lava Shelter
    # 4 - Secret Door
    # 8 - Air Saucer (Secret Door)
    # 223 - Shadow Box 1
    # 179 - Light Dash Trail
    # 15 - Pulley (Over lava, key route an option)
    # 222- Shadow Box 2
    # 6 - Shadow Box 3
    # 344 - Easy logic Pulley?

    # 136 - Pulley (M4)
    # 335 - Light Dash Trail
    # 137 - Light Dash Trail
    # 129 - Light Dash Trail
    # 338 - Light Dash Trail




    # Cosmic Fall

    # 2 - Zipline at Start
    # 40 - Pulley (hard ok)
    # 135 - Shadow Box 1
    # 25 - Light Dash Trail
    # 247 - Zipline

    # 204 - Pulley?
    # 209 = Pulley - to core
    # 210 - Hero Core (req Pulley)
    # 5 - Zipline
    # 7 - Zipline

    ## 77 - Secret Door
    # 156 - LD1
    # 228 - LD2
    # 158 - LD3
    # 230 - LD
    # 231 - LD4
    # 229 = LD5
    # 6 - Zipline

    # 250 - LD
    # 291 - Pulley
    # 261 - Gun Jumper
    # 292 - Pulley
    # 293 - Pulley
    # 252 - Pulley
    # 331 - Shadow Box 2
    # 253 - Gun Cannon
    # 296 - Pulley
    # 236 - LD
    # 237 - LD
    # 250 - LD
    # 234 - LD
    # 239 - LD
    # 11 - Rocket
    # 108 - Rocket




# Final Haunt

    # 139 - Shadow Box 1
    # 417 - Black Turret
    # 454 - Black Volt Enemy
    # 446 - Black Volt (Vehicle)
    # (linked not handled)
    # 20 - Rocket


    # 166 - Shadow Box 2

    # 455 - Black Volt Enemy 2
    # 447 - Black Volt 2
    # 217 - Black Turret 2 (Volt 2 Section)
    # 219 - Black Turret 3 (Volt 2 Section)

    # 168 - Secret Door 1
    # 5 - Secret Door 2
    # 173 - Black Turret (Key Door 1)
    # 6 - Black Turret (Key Door 2)
    # 11 - Light Dash Trail

    # 456 - Black Volt Enemy 3
    # 448 - Black Volt 3

    # 164 - Shadow Box 3
    # 161 - Black Turret 5
    # 160 - Secret Door 3
    # 84 - Black Turret 6 (Door 3)

    # 159 - Secret Door 4
    # 7 - Black Turret 7 (Door 4)

    # The Last Way
    # 445 - Shadow Box 1
    # 26 - Secret Door
    # 142 - Black Turret
    # 14 - Warp Hole
    # 449 - Warp Hole Exit
    # (Linked enemy not handled)
    # 42 - Black Volt Vehicle

    # 192 - Shadow Box 2
    # 458 - Light Dash Trail (Hard ok)
    # 310 - Shadow Box 3
    # 311 - Shadow Box 4



]

def GetDesirableObjectsForStage(stage):
    return [ o for o in DESIRABLE_OBJECTS if o.stage == stage]


def TypeToString(type):

    if type == 0x01:
        return "Spring"

    elif type == 0x02:
        return "Long Spring"

    elif type == 0x03:
        return "Dash Panel"

    elif type == 0x04:
        return "Dash Ramp"

    elif type == 0x05:
        return "Checkpoint"

    elif type == 0x06:
        return "Dash Ring"

    elif type == 0x07:
        return "Locked Case"

    elif type == 0x08:
        return "Pulley"

    elif type == 0x09:
        return "Wood Box"

    elif type == 0x0A:
        return "Metal Box"

    elif type == 0x0A:
        return "Unbreakable Box"

    elif type == 0x0C:
        return "Box"

    elif type == 0x0D:
        return "GUN Bomb"

    elif type == 0x0E:
        return "Rocket"

    elif type == 0x0F:
        return "Platform"

    elif type == 0x10:
        return "Rings"

    elif type == 0x11:
        return "Hint Ball"

    elif type == 0x12:
        return "Item Capsule"

    elif type == 0x13:
        return "Balloon"

    elif type == 0x14:
        return "Goal Ring"

    elif type == 0x15:
        return "Ball Switch"

    elif type == 0x16:
        return "Target Switch"

    elif type == 0x18:
        return "GUN Turret"

    elif type == 0x19:
        return "Weight"

    elif type == 0x1A:
        return "Wind"

    elif type == 0x1B:
        return "Roadblock"

    elif type == 0x1C:
        return "Cocoon"

    elif type == 0x1E:
        return "Secret Door"

    elif type == 0x1F:
        return "Warp Hole"

    elif type == 0x20:
        return "Weapon"

    elif type == 0x22:
        return "Red Fruit"

    elif type == 0x23:
        return "OObject"

    elif type == 0x33:
        return "Energy Core"

    elif type == 0x34:
        return "Fire"

    elif type == 0x35:
        return "Gas"

    elif type == 0x37:
        return "Cage"

    elif type == 0x38:
        return "Heal Unit"

    elif type == 0x3A:
        return "Special Weapon Box"

    elif type == 0x4F:
        return "Vehicle"

    elif type == 0x5A:
        return "Pole"

    elif type == 0x61:
        return "Dark Spin Entry"

    elif type == 0x64:
        return "GUN Solider"

    elif type == 0x65:
        return "GUN Beetle"

    elif type == 0x66:
        return "Big Foot"

    elif type == 0x68:
        return "Gun Robot"

    elif type == 0x78:
        return "Egg Clown"

    elif type == 0x79:
        return "Egg Pawn"

    elif type == 0x7A:
        return "Shadow Android"

    elif type == 0x8C:
        return "Black Oak"

    elif type == 0x8D:
        return "Black Warrior"

    elif type == 0x8E:
        return "Black Hawk"

    elif type == 0x8F:
        return "Black Wing"

    elif type == 0x90:
        return "Black Worm"

    elif type == 0x91:
        return "Black Arm Larvae"

    elif type == 0x92:
        return "Artificial Chaos"

    elif type == 0x93:
        return "Black Assassin"

    elif type == 0x12C:
        return "Environment Weapon"

    elif type == 0x190:
        return "Partner"

    elif type == 0x03E8:
        return "Emerald"

    elif type == 0x03E9:
        return "Building"

    elif type == 0x03EA:
        return "City Laser"

    elif type == 0x7D7:
        return "Digital Tile"

    elif type == 0x7DC:
        return "Matrix Bomb"

    elif type == 0x7DD:
        return "Matrix Terminal"

    elif type == 0x07D4:
        return "Defense Program"

    elif type == 0xC88:
        return "Zipline"

    elif type == 0x1006:
        return "Server"

    elif type == 0x1133:
        return "Proximity Door"

    elif type == 0x138A:
        return "Meteor Large"

    elif type == 0x2589:
        return "Destructible"



    return str(type)

def StateToString(type, state):
    if type == "Rings" and type == 0x1000:
        return "All Collected"
    if type == "City Laser" and type == 0x1000:
        return "Expired"
    if state == 0x00:
        return "Destroyed"
    if state == 0x01:
        return "Loaded"
    if state == 0x02:
        return "10 02"
    if state == 0x03:
        return "Spawned"
    if state == 0x04:
        return "10 04"
    if state == 0x05:
        return "10 05"
    if state == 0x06:
        return "10 06"
    if state == 0x07:
        return "10 07"
    if state == 0x08:
        return "Defeated"
    if state == 0x09:
        return "10 09"

    if state == 0x0B:
        return "Corpsed"

    return state

def PrintSETChange(address, index, type, previous, new, additional_bytes):

    #if not use:
    #    return

    typeString = TypeToString(type)
    typeString = CheckVehicleAttributes(typeString, additional_bytes)

    found = False
    for v in ObjectType.__dict__.items():
        vIntValue = v[1]
        l = GetTypeId(vIntValue)
        if l is not None and l == type:
            found = True
            break

    if not found:
        return

    handle_types = []
    unhandled_types = ["GUN Solider", "Destructible",
                       "City Laser", "Rings",
                       "Black Assassin", "Black Hawk", "Black Volt", "Black Warrior"]

    if len(handle_types) > 0 and typeString not in handle_types:
        return

    if typeString in unhandled_types:
        return


    oldStateString = StateToString(typeString,previous)
    newStateString = StateToString(typeString,new)

    #if typeString == "Rings":
    #    print("RINGS", address)

    DontPrintStates  = \
    [
        #["Spawned", "Loaded"],
        #["Loaded", "Spawned"],
        #["Spawned", "Expired"]
    ]

    if [oldStateString,newStateString] in DontPrintStates:
        return

    print("SET has changed", index, typeString, oldStateString, newStateString)


def GetSETFileLength(level):
    if level == Levels.STAGE_WESTOPOLIS:
        return 504 + 71
    elif level == Levels.STAGE_DIGITAL_CIRCUIT:
        return 529 + 125
    elif level == Levels.STAGE_GLYPHIC_CANYON:
        return 328 + 86
    elif level == Levels.STAGE_LETHAL_HIGHWAY:
        return 378 + 174
    elif level == Levels.STAGE_CRYPTIC_CASTLE:
        return 373 + 177
    elif level == Levels.STAGE_PRISON_ISLAND:
        return 526 + 152
    elif level == Levels.STAGE_CIRCUS_PARK:
        return 236 + 143
    elif level == Levels.STAGE_CENTRAL_CITY:
        return 539 + 161
    elif level == Levels.STAGE_THE_DOOM:
        return 375 + 109
    elif level == Levels.STAGE_SKY_TROOPS:
        return 312 + 78
    elif level == Levels.STAGE_MAD_MATRIX:
        return 518 + 165
    elif level == Levels.STAGE_DEATH_RUINS:
        return 458 + 30
    elif level == Levels.STAGE_THE_ARK:
        return 355 + 51
    elif level == Levels.STAGE_AIR_FLEET:
        return 420 + 113
    elif level == Levels.STAGE_IRON_JUNGLE:
        return 257 + 78
    elif level == Levels.STAGE_SPACE_GADGET:
        return 592 + 73
    elif level == Levels.STAGE_LOST_IMPACT:
        return 339 + 79
    elif level == Levels.STAGE_GUN_FORTRESS:
        return 416 + 86
    elif level == Levels.STAGE_BLACK_COMET:
        return 433 + 43
    elif level == Levels.STAGE_LAVA_SHELTER:
        return 341 + 74
    elif level == Levels.STAGE_COSMIC_FALL:
        return 252 + 87
    elif level == Levels.STAGE_FINAL_HAUNT:
        return 446 + 97
    elif level == Levels.STAGE_THE_LAST_WAY:
        return 457 + 40

    # Could add boxsanity for bosses too?

    return None