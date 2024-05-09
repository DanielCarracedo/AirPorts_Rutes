import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import networkx as nx
from math import inf
from Calculos import crear_grafo, longest_paths, retrieve_path_nodes, dijkstra

class Airport():
    def __init__(self) -> None:
        # Importar datos desde el archivo CSV local
        self.data = pd.read_csv('flights_final.csv')

        # Eliminar filas con valores faltantes o inválidos en las columnas de latitud y longitud
        self.data = self.data.dropna(subset=['Source Airport Latitude', 'Source Airport Longitude',
                           'Destination Airport Latitude', 'Destination Airport Longitude'])

        # Crear un DataFrame para almacenar las coordenadas de origen y destino
        self.source_airports = self.data[['Source Airport Latitude', 'Source Airport Longitude',
                        'Source Airport Name', 'Source Airport Code',
                        'Source Airport Country']].drop_duplicates()
        
        self.fig = px.scatter_geo(self.source_airports, lat='Source Airport Latitude', lon='Source Airport Longitude',
                     hover_name='Source Airport Name', title='Airports Locations',
                     color_discrete_sequence=['blue'], size_max=15,
                     custom_data=['Source Airport Code', 'Source Airport Country'])

        # Configurar botones seleccionables
        self.fig.update_traces(mode='markers', selector=dict(type='scattergeo'),
                  hovertemplate='<b>%{customdata[0]}</b><br>' +
                                'Name: %{hovertext}<br>' +
                                'Country: %{customdata[1]}<br>' +
                                'Latitude: %{lat}<br>' +
                                'Longitude: %{lon}')
        
        self.fig.update_traces(customdata=self.source_airports[['Source Airport Code', 'Source Airport Country']])
       
        # Actualizar la figura para mostrar la información del aeropuerto seleccionado
        self.fig.update_traces(selector=dict(type='scattergeo'), hoverinfo='skip')
        self.fig.update_layout(clickmode='event+select')
        self.fig.for_each_trace(lambda t: t.on_click(self.show_airport_info))    
        
        Continue = True
        print("Bienvenido a Final Flights")
        while(Continue):
            Choise = int(input("Que desea hacer?:"+"\n"+
                  "1. Mostrar mapa de todos los aeropuertos"+"\n"+
                  "2. Informacion del aeropuerto"+"\n"+
                  "3. Camino minimo entre 2 aeropuertos"+"\n"+
                  "4. Salir del programa"+"\n"))
            if Choise == 1:
                self.fig.show()
            elif Choise==2:
                # Verificar si se proporcionó un código de aeropuerto como argumento
                if len(sys.argv) > 1:
                    airport_code = sys.argv[1].upper()
                    self.search_by_code(airport_code)
                else:
                    # Solicitar al usuario que ingrese el código del aeropuerto
                    airport_code = input("Enter airport code: ").upper()
                    self.search_by_code(airport_code)
                    print("\n")
                    self.MostFar_10Airports(airport_code)
            elif Choise == 3:
                airport1 = input("Ingrese el código del primer aeropuerto: ").upper()
                airport2 = input("Ingrese el código del segundo aeropuerto: ").upper()
                self.shortest_path(airport1, airport2)
            elif Choise ==4:
                Continue =False
            else:
                print("Por Favor, USAR UNA DE LAS OPCIONES VALIDAS")
                
    
    # Función para mostrar la información del aeropuerto seleccionado
    def show_airport_info(self,trace, points, selector):
        airport_code = points.point_vars['customdata'][0]
        airport_info = self.data[self.data['Source Airport Code'] == airport_code].iloc[0]
        print(airport_info)
        
    # Función para mostrar la información del aeropuerto seleccionado
    def airport_info(self,airport_code):
        airport_info = self.data[self.data['Source Airport Code'] == airport_code].iloc[0]
        print(f"Airport Code: {airport_info['Source Airport Code']}")
        print(f"Airport Name: {airport_info['Source Airport Name']}")
        print(f"Country: {airport_info['Source Airport Country']}")
        print(f"Latitude: {airport_info['Source Airport Latitude']}")
        print(f"Longitude: {airport_info['Source Airport Longitude']}")
        return airport_info
    
    # Función para mostrar la ubicación del aeropuerto en el mapa
    def plot_airport_location(self, airport_info):
        fig = px.scatter_geo([airport_info], lat='Source Airport Latitude', lon='Source Airport Longitude',
                            hover_name='Source Airport Name', title='Airport Location',
                            color_discrete_sequence=['blue'], size_max=15,
                            custom_data=['Source Airport Code', 'Source Airport Country', 'Source Airport Name',
                                        'Source Airport City', 'Source Airport Country', 'Source Airport Latitude',
                                        'Source Airport Longitude'])

        fig.update_traces(mode='markers',
                        hovertemplate='<b>%{customdata[0]}</b><br>' +
                                        'Name: %{customdata[2]}<br>' +
                                        'City: %{customdata[3]}<br>' +
                                        'Country: %{customdata[4]}<br>' +
                                        'Latitude: %{customdata[5]}<br>' +
                                        'Longitude: %{customdata[6]}')
        fig.show()
    
    # Buscar el aeropuerto por código
    def search_by_code(self,airport_code):
        if airport_code in self.source_airports['Source Airport Code'].values:
            airport_info = self.airport_info(airport_code)
            self.plot_airport_location(airport_info)
        else:
            print("Airport not found!")
    
     # Función para obtener la latitud y longitud de un aeropuerto dado su código
    def get_airport_location(self, airport_code):
        airport = self.data[self.data['Source Airport Code'] == airport_code].iloc[0]
        latitude = airport['Source Airport Latitude']
        longitude = airport['Source Airport Longitude']
        return latitude, longitude
    
    def plot_airports_on_map(self, airports):
        # Filtrar los datos para obtener solo los aeropuertos seleccionados
        data_airports = self.data[self.data['Source Airport Code'].isin(airports)]

        # Crear un DataFrame para almacenar las coordenadas de los aeropuertos seleccionados
        airports_selected = data_airports[['Source Airport Latitude', 'Source Airport Longitude',
                                           'Source Airport Name', 'Source Airport Code',
                                           'Source Airport Country']].drop_duplicates()

        # Crear el mapa con los aeropuertos seleccionados
        fig = px.scatter_geo(airports_selected, lat='Source Airport Latitude', lon='Source Airport Longitude',
                             hover_name='Source Airport Name', title='Selected Airports',
                             color_discrete_sequence=['blue'], size_max=15,
                             custom_data=['Source Airport Code', 'Source Airport Country'])

        fig.update_traces(mode='markers',
                          hovertemplate='<b>%{customdata[0]}</b><br>' +
                                        'Name: %{hovertext}<br>' +
                                        'Country: %{customdata[1]}<br>' +
                                        'Latitude: %{lat}<br>' +
                                        'Longitude: %{lon}')

        fig.show()
    
    def MostFar_10Airports(self, airport):
        G = crear_grafo()

        if airport not in G.nodes:
            print("El aeropuerto no se encuentra en el grafo.")
            return

        try:
            longest_paths_result = longest_paths(G, airport)
            longest_paths_result = sorted(longest_paths_result, key=lambda x: x[1], reverse=True)[:10]

            
            farthest_airports = [path[-1] for path in longest_paths_result]
            print(farthest_airports)

            # Mostrar los 10 nodos más lejanos en un mapa
            self.plot_airports_on_map(farthest_airports)

        except KeyError:
            print("Error: No se encontró una ruta válida.")
    
    def shortest_path(self, airport1, airport2):
        G = crear_grafo()
        distancias, predecesores = dijkstra(G, airport1)

        # Verificar si ambos aeropuertos están en el grafo
        if airport1 not in G.nodes or airport2 not in G.nodes:
            print("Al menos uno de los aeropuertos no está en el grafo.")
            return

        try:
            shortest_distance = distancias[airport2]
            print(f"La distancia más corta entre {airport1} y {airport2} es: {shortest_distance} km")

            retrieve_path_nodes(airport1, airport2, (distancias, predecesores))

            shortest_path_result = nx.dijkstra_path(G, airport1, airport2, weight='weight')

            # Filtrar los datos para obtener solo los aeropuertos en el camino más corto
            data_shortest_path = self.data[self.data['Source Airport Code'].isin(shortest_path_result)]

            # Mostrar los aeropuertos y el camino más corto en el mismo mapa
            fig = px.scatter_geo(data_shortest_path, lat='Source Airport Latitude', lon='Source Airport Longitude',
                                hover_name='Source Airport Name', title='Shortest Path',
                                color_discrete_sequence=['blue'], size_max=15,
                                custom_data=['Source Airport Code', 'Source Airport Country',
                                            'Source Airport Name', 'Source Airport City',
                                            'Source Airport Country', 'Source Airport Latitude',
                                            'Source Airport Longitude'])

            fig.update_traces(mode='markers',
                            hovertemplate='<b>%{customdata[0]}</b><br>' +
                                            'Name: %{customdata[2]}<br>' +
                                            'City: %{customdata[3]}<br>' +
                                            'Country: %{customdata[4]}<br>' +
                                            'Latitude: %{customdata[5]}<br>' +
                                            'Longitude: %{customdata[6]}')

            fig.add_trace(go.Scattergeo(
                lon=data_shortest_path['Source Airport Longitude'],
                lat=data_shortest_path['Source Airport Latitude'],
                mode='markers',
                marker=dict(size=10, color='blue'),
                name='Shortest Path Nodes',
                hoverinfo='text',
                text=['Code: {}<br>Name: {}<br>City: {}<br>Country: {}<br>Latitude: {}<br>Longitude: {}'.format(
                    code, name, city, country, lat, lon)
                    for code, name, city, country, lat, lon in zip(
                        data_shortest_path['Source Airport Code'],
                        data_shortest_path['Source Airport Name'],
                        data_shortest_path['Source Airport City'],
                        data_shortest_path['Source Airport Country'],
                        data_shortest_path['Source Airport Latitude'],
                        data_shortest_path['Source Airport Longitude']
                    )]
            ))

            # Agregar la línea de la ruta más corta
            fig.add_trace(go.Scattergeo(
                lon=data_shortest_path['Source Airport Longitude'],
                lat=data_shortest_path['Source Airport Latitude'],
                mode='lines',
                line=dict(width=2, color='red'),
                name='Shortest Path'
            ))

            fig.show()

        except KeyError:
            print(f"No se encontró una ruta válida entre {airport1} y {airport2}.")
                      
airport_instance = Airport()