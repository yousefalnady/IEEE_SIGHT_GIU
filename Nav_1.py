import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Define the locations (latitude and longitude) for your starting and ending points

latitude_origin = 29.9859
longitude_origin = 31.4235
latitude_destination = 30.0545
longitude_destination = 31.4888

origin_point = (latitude_origin, longitude_origin)
destination_point = (latitude_destination, longitude_destination)

# Get the street network for the specified area
graph = ox.graph_from_point(origin_point,  network_type='drive')

# Find the nearest nodes in the graph to the origin and destination points
origin_node = ox.distance.nearest_nodes(graph, origin_point[0], origin_point[1])
destination_node = ox.distance.nearest_nodes(graph, destination_point[0], destination_point[1])

# Calculate the shortest path between the origin and destination nodes
route = nx.shortest_path(graph, origin_node, destination_node, weight='length')

# Plot the route on the map
#fig, ax = ox.plot_graph_route(graph, route, origin_point=origin_point, destination_point=destination_point)

# Print the route
print("Route:", route)

#distance=500,