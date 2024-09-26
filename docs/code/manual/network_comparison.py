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
from shapely import LineString, Polygon, Point, distance
from cartagen.algorithms.network import branching_crossroads
from cartagen.utils.debug import plot_debug, geojson_debug, geojson_to_variable

lines = [
    loads('LINESTRING (343787.51587500545 5626698.956064817, 343789.3860424508 5626702.610528383, 343790.109619141 5626706.643041626, 343789.44170219614 5626711.226877227, 343787.29323602386 5626715.306650393)'), 
    loads('LINESTRING (343762.93653143826 5626709.5571636455, 343755.26661852264 5626710.9118369045, 343745.4259755365 5626712.943847176, 343733.29215104005 5626715.023113975, 343668.4485476529 5626724.584597017, 343649.7357412506 5626727.2624441665, 343623.3975497289 5626731.216208178)'), 
    loads('LINESTRING (343819.66209875507 5626703.612652717, 344117.58223004895 5626666.734592623)'), 
    loads('LINESTRING (343772.92188976245 5626693.726404013, 343771.35228494223 5626688.055690907, 343770.1055066454 5626684.243713547, 343761.2667390764 5626657.292134477, 343757.00320257904 5626649.683959292, 343751.59307532647 5626643.966018194, 343745.4259755365 5626639.00417142, 343737.0992776252 5626636.5941325445, 343726.7354330323 5626636.641388203, 343716.36045649037 5626638.4528552815, 343699.98535939463 5626646.171284303, 343675.12771710055 5626660.095977053, 343664.1293514102 5626663.939448071, 343649.29046328744 5626667.562393563)'), 
    loads('LINESTRING (343779.6678509045 5626720.300043229, 343781.8163170768 5626727.152179856, 343783.00743562833 5626731.830538201, 343791.7460156556 5626765.855035559, 343793.9278776751 5626772.644198316, 343812.93011475354 5626835.369373113, 343826.26138593064 5626881.863769734)'), 
    loads('LINESTRING (343851.41326272074 5626969.563647444, 343855.33170879673 5626968.980806154, 343859.25015487266 5626969.610904847, 343862.81237857806 5626971.359428952, 343865.68442144047 5626974.100359311, 343867.59911668213 5626977.565904636, 343868.40061701584 5626981.456768476)'), 
    loads('LINESTRING (343867.59911668213 5626977.565904636, 343886.2562633391 5626973.3442386845)'), 
    loads('LINESTRING (343842.79713413335 5626986.27703127, 343829.5278508308 5626991.758903379, 343753.98644437845 5627015.93903996, 343738.7245421907 5627023.216722431, 343731.2327404603 5627030.305379836, 343703.3360760675 5627078.791945955)'), 
    loads('LINESTRING (343831.4982058179 5626899.512695328, 343832.77837996196 5626903.813086645, 343833.4462969067 5626906.2389493175, 343847.17199012154 5626954.346776395, 343851.41326272074 5626969.563647444)'), 
    loads('LINESTRING (343762.93653143826 5626709.5571636455, 343762.78068415116 5626705.461641074, 343763.8382193137 5626701.492136358, 343766.0312132824 5626698.026697163, 343769.14815902454 5626695.348858697, 343772.92188976245 5626693.726404013)'), 
    loads('LINESTRING (343779.6678509045 5626720.300043229, 343775.24846712 5626720.6465879455, 343770.95153477543 5626719.559697744, 343767.2334637829 5626717.165389359, 343764.46160846215 5626713.715696159, 343762.93653143826 5626709.5571636455)'), 
    loads('LINESTRING (343787.29323602386 5626715.306650393, 343783.89799155464 5626718.457055646, 343779.6678509045 5626720.300043229)'), 
    loads('LINESTRING (343819.66209875507 5626703.612652717, 343787.29323602386 5626715.306650393)'), 
    loads('LINESTRING (343819.66209875507 5626703.612652717, 343787.51587500545 5626698.956064817)'), 
    loads('LINESTRING (343886.2562633391 5626973.3442386845, 343894.28998473746 5626975.8128224695, 343901.68565043673 5626976.17358665, 343922.0149993855 5626971.3721883185, 343948.0970745665 5626965.027899761, 343977.2338072012 5626957.978690253, 344006.9755085266 5626950.385021432)'), 
    loads('LINESTRING (343886.2562633391 5626973.3442386845, 343892.9534617257 5626967.169950226, 343900.6059733061 5626962.06827584, 343921.54505208496 5626956.803822001, 343948.33204821683 5626950.224559793, 343972.29936054535 5626944.585192187, 344001.43609318003 5626937.301009028, 344029.86790486384 5626930.25179952, 344061.9669785924 5626922.303034855, 344083.67687077785 5626917.093275104, 344117.0431291176 5626908.634223694, 344144.268222914 5626901.380785659, 344153.51722785283 5626901.051864104, 344163.1797606023 5626903.467497292)'), 
    loads('LINESTRING (343826.26138593064 5626881.863769734, 343831.4982058179 5626899.512695328)'), 
    loads('LINESTRING (343826.26138593064 5626881.863769734, 343854.12571688904 5626883.143643448)'), 
    loads('LINESTRING (343831.4982058179 5626899.512695328, 343854.12571688904 5626883.143643448)'), 
    loads('LINESTRING (343854.12571688904 5626883.143643448, 343920.3214341006 5626869.931704531)'), 
    loads('LINESTRING (343920.3214341006 5626869.931704531, 343910.1822262391 5626816.804126068)'), 
    loads('LINESTRING (343920.3214341006 5626869.931704531, 343984.23436197144 5626858.222465837)'), 
    loads('LINESTRING (343984.23436197144 5626858.222465837, 343980.3312824068 5626832.364563722, 343976.4282028422 5626822.118979865, 343967.1583888762 5626815.288590627, 343955.4491501823 5626811.873396007, 343937.3974071959 5626813.337050844, 343910.1822262391 5626816.804126068)'), 
    loads('LINESTRING (343910.1822262391 5626816.804126068, 343906.1727706788 5626792.357998185)'), 
    loads('LINESTRING (343984.23436197144 5626858.222465837, 344070.1021123933 5626843.58591747)'), 
    loads('LINESTRING (344163.1797606023 5626903.467497292, 344190.3142522235 5626896.204003948, 344225.639906203 5626887.290053878)'), 
    loads('LINESTRING (344225.639906203 5626887.290053878, 344262.0146912733 5626889.080535417)'), 
    loads('LINESTRING (344225.639906203 5626887.290053878, 344255.5495038449 5626862.681020085)'), 
    loads('LINESTRING (344262.0146912733 5626889.080535417, 344280.33272232057 5626963.430190844)'), 
    loads('LINESTRING (344262.0146912733 5626889.080535417, 344255.5495038449 5626862.681020085)'), 
    loads('LINESTRING (344255.5495038449 5626862.681020085, 344225.5595472175 5626726.458738531)'), 
    loads('LINESTRING (343649.29046328744 5626667.562393563, 343640.35150817677 5626668.381494485, 343627.62769037904 5626667.137091191, 343589.5786884259 5626658.820071054)'), 
    loads('LINESTRING (343649.29046328744 5626667.562393563, 343653.95788003854 5626694.962311408)'), 
    loads('LINESTRING (344220.37136320607 5626631.610446766, 344228.7795384526 5626635.7376151625, 344235.5586297449 5626642.207232093, 344240.07802394 5626650.387210337, 344241.9698633704 5626659.571098756, 344241.33925022685 5626667.602356648, 344238.6591443671 5626675.1874363385, 344234.0871990768 5626681.842974169)'), 
    loads('LINESTRING (344198.53638311266 5626689.57678611, 344190.3121366998 5626684.2969718855, 344184.137383003 5626676.711888954)'), 
    loads('LINESTRING (344234.0871990768 5626681.842974169, 344226.598667998 5626687.977968991, 344217.55987960787 5626691.473057738, 344207.89047807443 5626692.030784717, 344198.53638311266 5626689.57678611)'), 
    loads('LINESTRING (344198.53638311266 5626689.57678611, 344225.5595472175 5626726.458738531)'), 
    loads('LINESTRING (344225.5595472175 5626726.458738531, 344234.0871990768 5626681.842974169)'), 
    loads('LINESTRING (344184.137383003 5626676.711888954, 344181.5361037861 5626670.948715001, 344180.1697753086 5626664.77654334, 344180.09094866563 5626658.455646509, 344181.2733483097 5626652.246296743, 344183.69069869304 5626646.445947701)'), 
    loads('LINESTRING (344183.69069869304 5626646.445947701, 344188.3677461741 5626639.939147774, 344194.56877541833 5626634.845254358, 344201.87337766355 5626631.498901686, 344211.1223704349 5626630.1231790725, 344220.37136320607 5626631.610446766)'), 
    loads('LINESTRING (344117.58223004895 5626666.734592623, 344184.137383003 5626676.711888954)'), 
    loads('LINESTRING (344117.58223004895 5626666.734592623, 344183.69069869304 5626646.445947701)'), 
    loads('LINESTRING (343772.92188976245 5626693.726404013, 343776.9961831255 5626693.285348423, 343781.0259486922 5626694.088699693, 343784.63270019385 5626696.026194233, 343787.51587500545 5626698.956064817)'), 
    loads('LINESTRING (343843.8991970922 5626988.718668637, 343842.79713413335 5626986.27703127, 343842.21827278123 5626983.662117146, 343842.184876934 5626980.984193831, 343842.6858146426 5626978.353528759, 343843.7099539579 5626975.896141723, 343845.69144089404 5626973.139458344, 343848.31858087674 5626970.9813696565, 343851.41326272074 5626969.563647444)'), 
    loads('LINESTRING (343868.40061701584 5626981.456768476, 343868.1334502379 5626984.85930665, 343866.99799143185 5626988.072816108, 343865.061032292 5626990.892514073, 343861.88842680445 5626993.491677785, 343858.0590363211 5626994.97241381, 343853.96247905993 5626995.208701495, 343849.9995051877 5626994.1690357225, 343846.5152051259 5626991.932179468, 343843.8991970922 5626988.718668637)'), 
    loads('LINESTRING (344220.37136320607 5626631.610446766, 344225.63811219606 5626616.248714371, 344234.9934581181 5626601.244857703, 344252.115506315 5626588.006160644, 344274.0034854534 5626579.533394526)'), 
    loads('LINESTRING (344006.9755085266 5626950.385021432, 344145.7335209158 5626915.6798650725, 344157.2748794776 5626910.043387636, 344163.1797606023 5626903.467497292)'), 
    loads('LINESTRING (344006.9755085266 5626950.385021432, 344010.59690176864 5626962.697758455, 344014.942573659 5626979.356167369, 344017.47754892847 5626994.928158309, 344017.83968825266 5627013.397263844, 344014.2182950106 5627031.866369378)'), 
    loads('LINESTRING (344071.7830367043 5626848.642468961, 344070.6809737454 5626846.200831594, 344070.1021123933 5626843.58591747, 344070.06871654605 5626840.907994155, 344070.56965425465 5626838.2773290835, 344071.59379356995 5626835.819942047, 344073.5752805061 5626833.063258668, 344076.2024204888 5626830.905169981, 344079.2971023328 5626829.487447768, 344083.2155484088 5626828.904606478, 344087.1339944847 5626829.534705171, 344090.69621819013 5626831.283229277, 344093.56826105254 5626834.024159635, 344095.4829562942 5626837.48970496, 344096.2844566279 5626841.3805688005, 344096.01728985 5626844.783106974, 344094.8818310439 5626847.996616432, 344092.9448719041 5626850.816314397, 344089.7722664165 5626853.415478109, 344085.9428759332 5626854.896214134, 344081.846318672 5626855.132501819, 344077.88334479975 5626854.092836047, 344074.399044738 5626851.855979792, 344071.7830367043 5626848.642468961)'), 
]

network = GeoDataFrame(geometry=lines, crs='EPSG:3857')
roundabouts = c4.detect_roundabouts(network)
crossroads = c4.detect_branching_crossroads(network, roundabouts)

n1 = c4.collapse_branching_crossroads(network, crossroads)
n2 = c4.collapse_roundabouts(n1, roundabouts, crossroads)

carriageways = c4.detect_dual_carriageways(n2)
n3 = c4.collapse_dual_carriageways(n2, carriageways, 5)

deadends = c4.detect_dead_ends(n3, True)
n4 = c4.eliminate_dead_ends(deadends, 200, keep_longest=True)

fig = plt.figure(1, (12, 4))

sub1 = fig.add_subplot(121)
sub1.axes.get_xaxis().set_visible(False)
sub1.axes.get_yaxis().set_visible(False)

sub2 = fig.add_subplot(122)
sub2.axes.get_xaxis().set_visible(False)
sub2.axes.get_yaxis().set_visible(False)

for line in lines:
    path = Path(np.asarray(line.coords)[:, :2])
    sub1.add_patch(PathPatch(path, facecolor="none", edgecolor='gray', linewidth=1))

for line in n4.geometry:
    path = Path(np.asarray(line.coords)[:, :2])
    sub2.add_patch(PathPatch(path, facecolor="none", edgecolor='gray', linewidth=1))

sub1.autoscale_view()
sub2.autoscale_view()
plt.show()