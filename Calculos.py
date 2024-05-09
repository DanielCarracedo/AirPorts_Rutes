from math import radians, cos, sin, acos
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq


def haversine(lat1, lon1, lat2, lon2) -> float:
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dif = lon1 - lon2
    distancia = acos(sin(lat1)*sin(lat2) + cos(lat1)
                     * cos(lat2)*cos(dif)) * 6371
    return distancia


def crear_df():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('flights_final.csv')

    # Concatenate the two columns, sort the values within each row
    df['Concatenated'] = df[['Source Airport Code', 'Destination Airport Code']
                            ].apply(sorted, axis=1).str.join(',')

    # Drop exact duplicates based on the concatenated and sorted column
    df.drop_duplicates(subset='Concatenated', inplace=True)

    # Remove the concatenated column
    df.drop(columns=['Concatenated'], inplace=True)

    # Reset the index after dropping duplicates
    df.reset_index(drop=True, inplace=True)

    return df


def crear_grafo():
    df = crear_df()
    # Create a directed graph
    G = nx.Graph()

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        source = row['Source Airport Code']
        destination = row['Destination Airport Code']
        lat1 = row['Source Airport Latitude']
        lat2 = row['Destination Airport Latitude']
        lon1 = row['Source Airport Longitude']
        lon2 = row['Destination Airport Longitude']
        weight = haversine(lat1, lon1, lat2, lon2)

        # Add source airport as a node if it doesn't exist
        if not G.has_node(source):
            G.add_node(source)

        # Add destination airport as a node if it doesn't exist
        if not G.has_node(destination):
            G.add_node(destination)

        # Add an edge from source to destination
        G.add_edge(source, destination, weight=weight)

    return G


def save_edge_list_as_csv(G, filename):
    # Extract edges and edge weights from the graph
    edges = [(source, target, weight)
             for source, target, weight in G.edges(data='weight', default=1)]

    # Create a DataFrame to store the edge list
    edge_list_df = pd.DataFrame(
        edges, columns=['Source Airport Code', 'Destination Airport Code', 'Weight'])

    # Save the edge list DataFrame to a CSV file
    edge_list_df.to_csv(filename, index=False)


def dijkstra(graph, source):

    # Initialize distances to all nodes as infinity
    distancias = {}
    predecesores = {}

    for node in graph.nodes():
        distancias[node] = float('inf')
        predecesores[node] = None

    distancias[source] = 0

    # Priority queue to store nodes with their tentative distances
    queue = [(0, source)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # Iterate over neighbors of the current node
        for neighbor, edge_attrs in graph[current_node].items():
            # Extract the weight of the edge
            # Assuming default weight is 0 if not provided
            weight = edge_attrs.get('weight', 0)

            distance = current_distance + weight

            # If the new distance is shorter than the current distance, update it
            if distance < distancias[neighbor]:
                distancias[neighbor] = distance
                # Store predecessor for the shortest path
                predecesores[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distancias, predecesores


def retrieve_path_nodes(source, destination, dijkstra):
    for node, distance in dijkstra[0].items():
        if node == destination:
            print(f"Shortest distance from {source} to {node}: {distance}")

    path = [destination]
    predecesores = dijkstra[1].get(destination)
    while predecesores is not None:
        path.insert(0, predecesores)
        predecesores = dijkstra[1].get(predecesores)
    print(f"Shortest path from {source} to {destination}: {' -> '.join(path)}")


def longest_paths(graph, source):
    weights = [0] * 10
    paths = [0] * 10
    dijk = dijkstra(graph, source)

    for nodes, distance in dijk[0].items():
        if distance > min(weights):
            if distance != float('inf'):
                min_index = weights.index(min(weights))
                # Replace the value at the minimum index with the new value
                weights[min_index] = distance

                path = [nodes]
                predecesores = dijk[1].get(nodes)
                while predecesores is not None:
                    path.insert(0, predecesores)
                    predecesores = dijk[1].get(predecesores)

                paths[min_index] = path

    for i, path in enumerate(paths):
        if path:
            print(
                f"El camino mas largo #{i + 1} desde {source} a {path[-1]}: {' -> '.join(path)} y su peso es: {weights[i]}")
    
    return paths
