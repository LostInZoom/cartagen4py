# import geopandas as gpd
# import shapely
# import numpy
# from matplotlib import pyplot as plt
# from matplotlib.path import Path
# from matplotlib.patches import PathPatch

# from cartagen4py.algorithms.network.dual_carriageways import collapse_dual_carriageways
# from cartagen4py.enrichment.network.dual_carriageways import detect_dual_carriageways

# roads = gpd.read_file("cartagen4py/data/routes_noz.geojson")
# crs = roads.crs
# ro = roads.to_dict('records')

# duals = detect_dual_carriageways(roads)
# duals.to_file("cartagen4py/data/duals.geojson", driver="GeoJSON")

# collapsed = collapse_dual_carriageways(roads, duals)

# from cartagen4py.utils.debug import *
# geojson_to_variable("docs/code/data/test1.geojson")

from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import numpy
import geopandas as gpd
import shapely
from shapely.wkt import loads
import cartagen4py as c4

buildings = [
    loads('Polygon ((483127.74420795019250363 6044736.3644003514200449, 483114.73178073146846145 6044726.71342246327549219, 483105.54601464356528595 6044745.89678345806896687, 483126.689473906182684 6044760.17289155162870884, 483131.8525651500094682 6044752.51116773299872875, 483120.7926855415571481 6044744.87053745705634356, 483124.51392676471732557 6044739.6514466255903244, 483130.07537209440488368 6044743.6170473350211978, 483128.97353314666543156 6044745.52951406966894865, 483138.98800764861516654 6044753.24484121147543192, 483142.85408783901948482 6044747.99430864583700895, 483127.74420795019250363 6044736.3644003514200449))'),
    loads('Polygon ((483162.60420556488679722 6044749.90797633398324251, 483167.29305910837138072 6044741.50208449736237526, 483158.54631337692262605 6044736.39747273270040751, 483164.02214775263564661 6044727.26683164667338133, 483160.10401825612643734 6044724.26727752014994621, 483158.94143492548028007 6044723.54596658423542976, 483156.44691042724298313 6044721.9793161153793335, 483152.05093409406254068 6044730.33950771857053041, 483148.83314704877557233 6044727.98296463023871183, 483143.6222503071767278 6044734.96569846104830503, 483162.60420556488679722 6044749.90797633398324251))'),
    loads('Polygon ((483134.49167914234567434 6044719.08061139564961195, 483123.53526283032260835 6044711.08918826468288898, 483117.88398461748147383 6044718.7685501417145133, 483125.24604345660191029 6044724.59082455839961767, 483131.69380232668481767 6044728.94176229648292065, 483134.3939773467136547 6044730.82876554876565933, 483140.0452489098533988 6044723.14938258472830057, 483136.44334064348367974 6044720.53428473882377148, 483134.49167914234567434 6044719.08061139564961195))'),
]

fig = plt.figure(1, (12, 10))

#############################################################

sub1 = fig.add_subplot(111)
sub1.axes.get_xaxis().set_visible(False)
sub1.axes.get_yaxis().set_visible(False)

generalized = c4.square_polygons(buildings)

for building in buildings:
    poly = Path.make_compound_path(Path(numpy.asarray(building.exterior.coords)[:, :2]),*[Path(numpy.asarray(ring.coords)[:, :2]) for ring in building.interiors])
    sub1.add_patch(PathPatch(poly, facecolor="lightgray", edgecolor='none'))

for g in generalized:
    poly = Path.make_compound_path(Path(numpy.asarray(g.exterior.coords)[:, :2]),*[Path(numpy.asarray(ring.coords)[:, :2]) for ring in g.interiors])
    sub1.add_patch(PathPatch(poly, facecolor="none", edgecolor='red', linewidth=1.5))

sub1.autoscale_view()
plt.show()