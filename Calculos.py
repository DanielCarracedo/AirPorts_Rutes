from math import radians, cos, sin, acos
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def haversine(lat1, lon1, lat2, lon2) -> float:
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dif = lon1 - lon2
    distancia = acos(sin(lat1)*sin(lat2) + cos(lat1)
                     * cos(lat2)*cos(dif)) * 6371
    return distancia


def crear_matriz():
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


# Create the graph
matriz = crear_matriz()
