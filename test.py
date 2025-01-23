from Main import main as M
from Generate import main as G
from BaseClasses import CollectionState

multi = M(*G())
#CHeck all available regions
x = multi.get_all_state(True).reachable_regions
l = multi.get_all_state(True).locations_checked
print(x)
print(l)


#locations = list(multi.get_filled_locations(1))
#for l in locations:
#    print(l)

# Check available regions in Sphere 1
#state = CollectionState(multi)
#state.update_reachable_regions(1)
#y = state.reachable_regions
###loc = state.multiworld.get_location("Boss:Black Bull Lethal Highway", 1)
#print(loc.name, loc.access_rule)
#print(y)

