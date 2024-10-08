from matplotlib import pyplot as plt
import cartagen as c4
import geopandas as gpd

network = gpd.read_file("data/detect_dead_ends.geojson")
deadends = c4.detect_dead_ends(network)
collapsed = c4.eliminate_dead_ends(network, deadends, 250)

original = network.plot(edgecolor='gray',linewidth=1)
collapsed.plot(ax=original, color='red', linewidth=1)
original.axes.get_xaxis().set_visible(False)
original.axes.get_yaxis().set_visible(False)

plt.show()