from matplotlib import pyplot as plt
from matplotlib import colormaps
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import numpy as np
import geopandas as gpd
from geopandas import GeoDataFrame
import shapely
from shapely.ops import unary_union
from shapely.wkt import loads
import cartagen as c4
from shapely import LineString, Polygon, Point
from cartagen.utils.debug import plot_debug, geojson_debug, geojson_to_variable

ls = c4.LeastSquaresMethod()

buildings = [
    loads('Polygon ((286265.7069888447294943 6248247.47732277866452932, 286319.47627075260970742 6248266.54097727406769991, 286305.30073279509088024 6248310.04521445371210575, 286283.793020031938795 6248302.71303964778780937, 286290.6363831838243641 6248283.64938515331596136, 286258.37481403909623623 6248272.40671711787581444, 286265.7069888447294943 6248247.47732277866452932))'),
    loads('Polygon ((286450.05008374946191907 6248317.71344727091491222, 286452.52469274640316144 6248393.05154339876025915, 286491.97247210604837164 6248393.63200724218040705, 286492.07261060422752053 6248418.89745958987623453, 286525.86341342981904745 6248419.70196210686117411, 286524.41055656992830336 6248375.1793673112988472, 286491.78237868490396068 6248374.69055565819144249, 286490.56034955062204972 6248336.07443501520901918, 286506.31094728148309514 6248336.27810654044151306, 286506.69113412301521748 6248300.63559012208133936, 286475.46150069189025089 6248300.64916822593659163, 286475.89599993941374123 6248317.01078052073717117, 286450.05008374946191907 6248317.71344727091491222))'),
    loads('Polygon ((286525.10303974617272615 6248349.63895840663462877, 286524.7771653103409335 6248314.77039377484470606, 286564.20797204284463078 6248315.74801708292216063, 286564.53384647861821577 6248351.59420502092689276, 286525.10303974617272615 6248349.63895840663462877))'),
    loads('Polygon ((286543.08523103164043278 6248101.27760393265634775, 286578.81604175514075905 6248108.37859461177140474, 286582.44004972599213943 6248073.61352123972028494, 286546.07036398607306182 6248067.11947654001414776, 286543.08523103164043278 6248101.27760393265634775))'),
    loads('Polygon ((286680.02917776902904734 6248259.26311487890779972, 286671.71937965601682663 6248220.15818258281797171, 286675.14106123195961118 6248177.63156871031969786, 286690.78303415060508996 6248178.60919201746582985, 286692.24946911173174158 6248161.50078413728624582, 286744.55231605854351074 6248168.8329589432105422, 286724.02222660282859579 6248267.57291299197822809, 286680.02917776902904734 6248259.26311487890779972))'),
]

roads = [
    loads('LineString (286211.80192592216189951 6248180.75453205406665802, 286237.22013191500445828 6248209.10560796875506639, 286265.57120783010032028 6248228.65807411726564169, 286311.51950327871600166 6248245.27767034340649843, 286363.3335385718382895 6248251.14341018814593554, 286416.12519717233953997 6248251.14341018814593554)'),
    loads('LineString (286416.12519717233953997 6248251.14341018814593554, 286425.90143024653661996 6248304.91269209608435631, 286428.83430016878992319 6248353.79385746642947197, 286429.81192347616888583 6248411.47363260481506586, 286421.01331370940897614 6248476.97439420130103827)'),
    loads('LineString (286416.12519717233953997 6248251.14341018814593554, 286409.28183402045397088 6248207.15036135446280241, 286399.50560094625689089 6248159.24681929033249617, 286392.66223779431311414 6248108.41040730476379395, 286379.95313479792093858 6248054.64112539682537317)'),
    loads('LineString (286416.12519717233953997 6248251.14341018814593554, 286457.18537608388578519 6248250.16578688099980354, 286508.02178806957090273 6248249.18816357292234898, 286560.81344667007215321 6248252.12103349529206753, 286597.9631323519279249 6248258.96439664717763662, 286657.59815410437295213 6248277.53923948854207993)'),
    loads('LineString (286657.59815410437295213 6248277.53923948854207993, 286670.30725710076512769 6248325.44278155174106359, 286677.15062025270890445 6248384.1001799963414669, 286680.08349017496220767 6248436.89183859713375568, 286679.10586686752503738 6248486.75062727555632591, 286676.20015314809279516 6248515.29179660696536303)'),
    loads('LineString (286657.59815410437295213 6248277.53923948854207993, 286645.86667441535973921 6248217.90421773586422205, 286635.11281803378369659 6248176.84403882455080748, 286630.22470149671426043 6248125.03000353090465069, 286632.17994811153039336 6248061.48448854871094227, 286635.19428664265433326 6248036.63656281586736441)'),
    loads('LineString (286657.59815410437295213 6248277.53923948854207993, 286706.47931947524193674 6248288.29309586994349957, 286782.73393745376961306 6248305.8903154032304883, 286853.12281558779068291 6248320.55466501414775848, 286923.51169372181175277 6248339.12950785551220179)'),
]

rivers = [
    loads('LineString (286646.8675102861598134 6248507.72460084408521652, 286648.86468927329406142 6248455.79794717952609062, 286645.86892079265089706 6248404.86988300830125809, 286643.37244705861667171 6248351.69499247521162033, 286635.38373111025430262 6248297.27186507824808359, 286623.89995193463983014 6248246.09415353555232286, 286610.91828851855825633 6248198.161857845261693, 286603.92816206376301125 6248149.23097266163676977, 286601.93098307668697089 6248097.30431899707764387, 286608.92110953148221597 6248033.39459141064435244)')
]

ls.add(gpd.GeoDataFrame(geometry=buildings, crs='EPSG:3857'), movement=2, stiffness=10)
ls.add(gpd.GeoDataFrame(geometry=roads, crs='EPSG:3857'), movement=2, curvature=5)
ls.add(gpd.GeoDataFrame(geometry=rivers, crs='EPSG:3857'), movement=2, curvature=5)

d = ls.get_objects_number()
distances = np.zeros((d, d))
spatial_weights = np.zeros((d, d))
for i in range(d):
    for j in range(d):
        distances[i][j] = 20
        spatial_weights[i][j] = 5

distances[0][0] = 25
distances[0][1] = 28
distances[0][2] = 30

spatial_weights[1][2] = 8

ls.add_spatial_conflicts(distances, spatial_weights)

gbuildings, groads, grivers = ls.generalize()

nodetonode = ls.get_vertexes_conflicts()
nodetolink = ls.get_links_conflicts()

fig = plt.figure(1, (10, 6))

sub1 = fig.add_subplot(111)
sub1.axes.get_xaxis().set_visible(False)
sub1.axes.get_yaxis().set_visible(False)

for b in buildings:
    poly = Path.make_compound_path(Path(np.asarray(b.exterior.coords)[:, :2]),*[Path(np.asarray(ring.coords)[:, :2]) for ring in b.interiors])
    sub1.add_patch(PathPatch(poly, facecolor="grey", edgecolor='none'))

for r in rivers:
    path = Path(np.asarray(r.coords)[:, :2])
    sub1.add_patch(PathPatch(path, facecolor="none", edgecolor='lightsteelblue', linewidth=1))

for r in roads:
    path = Path(np.asarray(r.coords)[:, :2])
    sub1.add_patch(PathPatch(path, facecolor="none", edgecolor='red', linewidth=1))

for r in nodetolink.geometry:
    path = Path(np.asarray(r.coords)[:, :2])
    sub1.add_patch(PathPatch(path, facecolor="none", edgecolor='gray', linestyle='--', linewidth=1))

for r in nodetonode.geometry:
    path = Path(np.asarray(r.coords)[:, :2])
    sub1.add_patch(PathPatch(path, facecolor="none", edgecolor='gray', linestyle='--', linewidth=1))

sub1.autoscale_view()
plt.show()