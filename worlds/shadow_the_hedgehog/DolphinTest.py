import time

import dolphin_memory_engine

addr = 0x80EFFE4C


changes = 0
previous_value = None

dolphin_memory_engine.hook()

while True:
    value = loaded_bytes = dolphin_memory_engine.read_bytes(addr, 3)

    if previous_value is None or value != previous_value:
        changes += 1
        previous_value = value
        print("Count=", changes)
    time.sleep(0.0005)

