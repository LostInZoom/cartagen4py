from cartagen4py.processes.AGENT.actions.generalisation_action import GeneralisationAction
from cartagen4py.algorithms.buildings.simplification import building_simplification
from cartagen4py.algorithms.buildings.squaring import Squarer
from shapely import affinity
from shapely.geometry import Polygon

class EnlargementAction(GeneralisationAction):
    goal_area = 0.0

    def __init__(self, constraint, agent, weight, goal_area):
        self.weight = weight
        self.agent = agent
        self.constraint = constraint
        self.goal_area = goal_area
        self.name = "Enlargement"

    def compute(self):
        """Compute the action, i.e. triggers the algorithm."""
        geom = self.agent.feature['geometry']
        factor = self.goal_area / geom.area
        self.agent.feature['geometry'] = affinity.scale(geom, xfact= factor, origin=geom.centroid)

class EnlargeToRectangleAction(GeneralisationAction):
    goal_area = 0.0

    def __init__(self, constraint, agent, weight, goal_area):
        self.weight = weight
        self.agent = agent
        self.constraint = constraint
        self.goal_area = goal_area
        self.name = "Enlarge to rectangle"

    def compute(self):
        """Compute the action, i.e. triggers the algorithm."""
        geom = self.agent.feature['geometry']
        ssr = geom.minimum_rotated_rectangle
        factor = self.goal_area / ssr.area
        self.agent.feature['geometry'] = affinity.scale(ssr, xfact= factor, origin=ssr.centroid)

class SimplificationAction(GeneralisationAction):
    edge_threshold = 0.0

    def __init__(self, constraint, agent, weight, edge_threshold):
        self.weight = weight
        self.agent = agent
        self.constraint = constraint
        self.edge_threshold = edge_threshold
        self.name = "Simplification"

    def compute(self):
        """Compute the action, i.e. triggers the algorithm."""
        geom = self.agent.feature['geometry']
        new_geom = building_simplification(geom,self.edge_threshold)
        self.agent.feature['geometry'] = new_geom

class SquaringAction(GeneralisationAction):
    
    def __init__(self, constraint, agent, weight):
        self.weight = weight
        self.agent = agent
        self.constraint = constraint
        self.name = "Squaring"
    
    def compute(self):
        """Compute the action, i.e. triggers the algorithm."""
        geom = self.agent.feature['geometry']
        squarer = Squarer()
        new_points = squarer.square([geom])
        new_geom = Polygon(squarer.get_shapes_from_new_points([geom],new_points)[0])
        self.agent.feature['geometry'] = new_geom