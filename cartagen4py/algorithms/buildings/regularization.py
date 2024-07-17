import shapely
import numpy as np
from shapely import Point, Polygon, LineString
from shapely.geometry.polygon import orient

import matplotlib.pyplot as plt

from cartagen4py.utils.geometry.angle import angle_2_pts
from cartagen4py.utils.geometry.polygon import enclosing_rectangle

from cartagen4py.utils.debug import plot_debug

def regularize_rectangle(polygon, factor=1.0):
    """
    Transform a polygon to a rectangle.

    This function transforms a polygon to a rectangle using
    the minimum rotated rectangle and scale it up or down.

    Parameters
    ----------
    polygon : Polygon
        The polygon to regularize.
    factor : float, optional
        The scaling factor to apply.

    Returns
    -------
    Polygon

    See Also
    --------
    regularize_regression :
        Regularize a polygon using recursive linear regression.

    Examples
    --------
    >>> polygon = Polygon([(0, 0), (0, 2), (1, 2), (1, 1), (2, 1), (2, 0), (0, 0)])
    >>> regularize_rectangle(polygon)
    <POLYGON ((2 0, 2 2, 0 2, 0 0, 2 0))>
    """
    mbr = polygon.minimum_rotated_rectangle
    return shapely.affinity.scale(mbr, xfact=factor, yfact=factor, origin=mbr.centroid)

def regularize_regression(polygon, sigma):
    """
    Regularize a polygon using recursive linear regression.

    This algorithm was proposed by Bayer :footcite:p:`bayer:2009` and used for remote
    sensing building regularization in Yang. :footcite:p:`yang:2024`
    It first defines the four sides of the polygon using an enclosing rectangle that has
    one side touching the side of the polygon. Then, every side is recursively
    subdivided until the standard deviation of the vertex composing the side
    is below the provided threshold.
    The standard deviation is calculated using the horizontal or vertical
    regression line which will output a squared polygon.
    
    Parameters
    ----------
    polygon : Polygon
        The polygon to regularize.
    sigma : float
        The standard deviation threshold above which
        the recursion continues.

    Returns
    -------
    Polygon

    See Also
    --------
    enclosing_rectangle :
        Construct an enclosing rectangle from a polygon.
    regularize_rectangle :
        Transform a polygon to a rectangle.

    Notes
    -----
    This algorithm always squares the provided polygon, this can create
    strange results when using on polygons that are not supposed to be square.

    References
    ----------
    .. footbibliography::

    Examples
    --------
    >>> polygon = Polygon([(0, 0), (0, 2), (1, 2), (1, 1), (2, 1), (2, 0), (0, 0)])
    >>> regularize_regression(polygon, 1.0)
    <POLYGON ((0 0, 0 2, 1.5 2, 1.5 0, 0 0))>
    """
    regressions = []

    # Calculate the standard deviation of the side from the regression line
    def __get_sigma(side, mean):
        # Storage for the sum of the squared difference from the mean
        square_total = []
        # Loop through side vertexes 
        for vertex in side:
            # Get the square difference between y and the mean,
            square_total.append(np.square(vertex.y - mean))
            
        # Calculate the standard deviation of the vertexes
        # as the suqrae root of the mean of the sum of the
        # squared distances from the regression line
        return np.sqrt(np.mean(square_total))

    # Find the closest vertex from the mbr corner
    def __closest_vertex(corner, vertices):
        distance = None
        closest = None
        for i, vertex in enumerate(vertices):
            d = shapely.distance(Point(corner), Point(vertex))
            if distance is None:
                distance, closest = d, i
            else:
                if d < distance:
                    distance, closest = d, i
        return closest

    # Recursive side treatment
    def __recursive_division(side, orientation):
        # Make sure the side has more than one point.
        if len(side) > 1:
            # Make the side horizontal
            hside = [ shapely.affinity.rotate(vertex, -orientation, origin=side[0]) for vertex in side ]

            # Get a list of vertex x to retrieve max and min x
            x = [ v.x for v in hside ]
            minx, maxx = min(x), max(x)
            add_length = (maxx - minx) / 4
            # Calculate the mean y
            mean = np.mean([ v.y for v in hside ])
            # Create the regression line using minx and maxx along with the mean y
            regression = shapely.LineString([(minx, mean), (maxx, mean)])

            # Calculate the standard deviation of the vertexes
            s = __get_sigma(hside, mean)

            # If the sigma is below the threshold or the side as only two points
            # add the regression line as the new side
            if s < sigma or len(hside) == 2:
                regressions.append(shapely.affinity.rotate(regression, orientation, origin=side[0]))

            # Here, continuing the division
            else:
                # Storage for the divided parts of the side by the regression line.
                temporary = []
                temp = []
                # Define the position of the first vertex from the regression line
                state = 'above' if hside[0].y > mean else 'below'
                # Loop through each vertex inside the horizontal side
                for vertex in hside:
                    # Get the position concerning the regression line
                    position = 'above' if vertex.y > mean else 'below'
                    # If its the same as the previous, increment the list
                    if position == state:
                        temp.append(vertex)
                    # Here, the position is different from the previous
                    else:
                        # append the current list and start a new one
                        temporary.append((temp, state))
                        state = position
                        temp = [vertex]

                # Append the last list
                temporary.append((temp, state))

                subsides = []
                subside = []
                # Loop through each temporary subsides
                for i, (temp, state) in enumerate(temporary):
                    # Here the side has only one vertex, this happens...
                    # This part reconstruct two points from the triangle
                    # formed by the previous and following side if exists
                    if len(temp) == 1:
                        v = temp[0]
                        v1, v2 = None, None
                        # If its the first subside of the side, set the start as the only vertex
                        if i == 0:
                            v1 = v
                        else:
                            # Calculate the slope and intercept of the line formed by the current vertex
                            # and the last point of the previous subside
                            # start point -> y as current vertex, x as the x of the intersection of the regression line
                            # and the segment formed by the current point and the last point of the previous subside
                            p = temporary[i - 1][0][-1]
                            slope = (v.y - p.y) / (v.x - p.x)
                            intercept = p.y - slope * p.x
                            v1 = Point((mean - intercept) / slope, v.y)
                        # If its the last subside of the side, set the end as the only vertex
                        if i == (len(temporary) - 1):
                            v2 = v
                        else:
                            # Calculate the slope and intercept of the line formed by the current vertex
                            # and the first point of the next subside
                            # start point -> y as current vertex, x as the x of the intersection of the regression line
                            # and the segment formed by the current point and the first point of the next subside
                            n = temporary[i + 1][0][0]
                            slope = (n.y - v.y) / (n.x - v.x)
                            intercept = n.y - slope * n.x
                            v2 = Point((mean - intercept) / slope, v.y)

                        # Increment the subside with the new points
                        if len(subside) > 0:
                            subsides.append(subside + [v1])
                        subsides.append([v1, v2])
                        subside = [v2]

                    # Here, only two vertexes exist, so both vertexes are used as start and end
                    elif len(temp) == 2:
                        v1, v2 = temp[0], temp[1]
                        # Increment the subside with the new points
                        if len(subside) > 0:
                            subsides.append(subside + [v1])
                        subsides.append([v1, v2])
                        subside = [v2]

                    # Here, 3 or more vertexes are present
                    else:
                        # Calculate the bounding rectangle
                        submbr = enclosing_rectangle(Polygon(temp + [temp[0]]), mode='input')
                        submbr_coords = list(submbr.boundary.coords)

                        # Set i1 and i2 as the index of the mbr vertex
                        # depending on the position from the regression line
                        if state == 'above':
                            i1, i2 = 1, 2
                        else:
                            i1, i2 = 0, 3

                        # Here, this is the first point of the side
                        if i == 0:
                            # start is the normal start of the side, end is the corner of the mbr with an index of i2
                            v1, v2 = temp[0], temp[__closest_vertex(submbr_coords[i2], temp)]
                            vi1, vi2 = 0, __closest_vertex(submbr_coords[i2], temp)
                        elif i == (len(temporary) - 1):
                            # start is the corner of the mbr with and index of i1 and end is the normal end of the side
                            v1, v2 = temp[__closest_vertex(submbr_coords[i1], temp)], temp[-1]
                            vi1, vi2 = __closest_vertex(submbr_coords[i1], temp), len(temp) - 1
                        else:
                            # start is the corner of the mbr with an index of i1
                            # end is the corner of the mbr with an index of i2
                            v1, v2 = temp[__closest_vertex(submbr_coords[i1], temp)], temp[__closest_vertex(submbr_coords[i2], temp)]
                            vi1, vi2 = __closest_vertex(submbr_coords[i1], temp), __closest_vertex(submbr_coords[i2], temp)

                        # Increment the subside with the new points
                        # It is different when the subside already has points
                        if len(subside) > 0:
                            for it, t in enumerate(temp):
                                subside.append(t)
                                if it in [vi1, vi2]:
                                    subsides.append(subside)
                                    subside = [t]
                        else:
                            for it, t in enumerate(temp):
                                subside.append(t)
                                if it == vi2:
                                    subsides.append(subside)
                                    subside = [t]
                
                # Loop through all the subsides created within the side
                for i, s in enumerate(subsides):
                    # Rotate the subside back to its original position
                    unrotated = [ shapely.affinity.rotate(p, orientation, origin=side[0]) for p in s]
                    # Even index side has the same orientation as the current side
                    if i % 2 == 0:
                        suborientation = orientation
                    # Uneven sides always are orthogonal to the current side
                    else:
                        suborientation = orientation - 90
                        # If the obtained orientation is below -90, switch back to 180
                        if suborientation < -90:
                            suborientation = 180
                    
                    # Continuing the recursive subdivision
                    __recursive_division(unrotated, suborientation)

    # Reverse the polygon if counter clockwise
    if shapely.is_ccw(polygon.boundary):
        polygon.reverse()

    # Calculate the minimum rotated rectangle touching one side of the building
    mbr = enclosing_rectangle(polygon, mode='input')

    # Retrieve coordinates and calculate angle of the last segment
    mbr_coords = list(mbr.boundary.coords)[:-1]
    original_angle = angle_2_pts(Point(mbr_coords[0]), Point(mbr_coords[-1]))

    # Rotate the polygon to reach horizontality
    rotated_mbr = shapely.affinity.rotate(mbr, -original_angle, origin=mbr_coords[0], use_radians=True)
    rotated_polygon = shapely.affinity.rotate(polygon, -original_angle, origin=mbr_coords[0], use_radians=True)

    # Get the coordinates of the four corner points
    mbr_coords = list(rotated_mbr.boundary.coords)
    extent = mbr_coords[:-1]

    # Get rotated polygon vertexes
    coords = list(rotated_polygon.boundary.coords)[:-1]

    # Reorder the polygon vertex so it starts
    # in the lower left corner of the mbr
    end = []
    start = []
    # Get the index of the lower left corner
    first = __closest_vertex(extent[0], coords)
    firsthalf = True
    for i, vertex in enumerate(coords):
        if i == first:
            firsthalf = False
        if firsthalf:
            end.append(vertex)
        else:
            start.append(vertex)

    # Replace the coords
    coords = start + end

    # Storage for the corners of the polygons
    corners = []
    # Loop through the mbr corners and store
    # the closest point of the polygon from the mbr corners
    for e in extent:
        corners.append(__closest_vertex(e, coords))

    # Storage for the sides of the polygon
    sides = []
    # Add a list of vertex coordinates as
    # each of the four sides of the polygon
    side = []
    for i, vertex in enumerate(coords):
        side.append(Point(vertex))
        if i in corners:
            sides.append(side)
            side = [Point(vertex)]
    sides.append(side)

    # Remove the last side and merge it with the first
    # Work when starting at 0 or more.
    last = sides.pop()
    first = sides.pop(0)
    sides.append(last + first)
    
    # Loop through each polygon side
    for i, side in enumerate(sides):        
        # Retrieve the associated mbr corners
        j = i + 1
        if j == len(extent):
            j = 0

        # Get the mbr corners coordinates
        mbr_side = [ extent[i], extent[j] ]
        # Get the angle of the mbr side in degree
        side_angle = round(np.rad2deg(angle_2_pts(Point(mbr_side[0]), Point(mbr_side[1]))))

        __recursive_division(side, side_angle)

    intersections = []
    # Reconstruct the polygon side by side
    for index in range(0, len(regressions)):
        # Get current segment and following one
        s1 = regressions[index]
        if index == len(regressions) - 1:
            s2 = regressions[0]
        else:
            s2 = regressions[index + 1]

        # Get p1 p2 and p3 p4 respectively the
        # start and end point of the segments
        p1, p2 = Point(s1.coords[0]), Point(s1.coords[-1])
        p3, p4 = Point(s2.coords[0]), Point(s2.coords[-1])

        # Calculate the line parameters for both infinite lines
        a1, a2 = p1.y - p2.y, p3.y - p4.y
        b1, b2 = p2.x - p1.x, p4.x - p3.x
        c1, c2 = -(p1.x * p2.y - p2.x * p1.y), -(p3.x * p4.y - p4.x * p3.y)

        # Calculate the line equations
        d = a1 * b2 - b1 * a2
        dx = c1 * b2 - b1 * c2
        dy = a1 * c2 - c1 * a2
        # Calculate the line intersections
        if d != 0:
            x, y = dx / d, dy / d
            intersections.append(Point(x, y))
    
    # Add the intersection between the last and first segment
    # as the first vertex of the polygon
    intersections.insert(0, intersections[-1])
    # Create the polygon, applying a buffer of 0 make the geometry
    # valid as sometimes the polygon may be self intersecting
    unrotated = Polygon(intersections).buffer(0)

    # Rotate the polygon back its original position
    return shapely.affinity.rotate(unrotated, original_angle, origin=mbr_coords[0], use_radians=True)

def regularize_reconstruction(polygon):
    """
    Regularize a polygon using feature edge reconstruction.
    """