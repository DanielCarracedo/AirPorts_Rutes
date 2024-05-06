import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import networkx as nx
from math import inf
from Calculos import crear_matriz

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
        fig = px.scatter_geo(airport_info, lat='Source Airport Latitude', lon='Source Airport Longitude',
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
    
    def MostFar_10Airports(self):
        pass
    
    def shortest_path(self, airport1, airport2):
        G = crear_matriz()
        # Verificar si ambos aeropuertos están en el grafo
        if airport1 not in G.nodes or airport2 not in G.nodes:
            print("Al menos uno de los aeropuertos no está en el grafo.")
            return
        try:
            shortest_path = nx.shortest_path(G, airport1, airport2, weight='weight')
            print("El camino más corto entre {} y {} es: {}".format(airport1, airport2, shortest_path))
            
            # Filtrar los datos para obtener solo los aeropuertos en el camino más corto
            data_shortest_path = self.data[self.data['Source Airport Code'].isin(shortest_path)]
            
            # Crear un DataFrame para almacenar las coordenadas de los aeropuertos en el camino más corto
            airports_shortest_path = data_shortest_path[['Source Airport Latitude', 'Source Airport Longitude',
                                        'Source Airport Name', 'Source Airport Code',
                                        'Source Airport City', 'Source Airport Country']].drop_duplicates()
            
            edge_x = []
            edge_y = []
            for i in range(len(shortest_path)-1):
                source = shortest_path[i]
                target = shortest_path[i+1]
                source_data = data_shortest_path[data_shortest_path['Source Airport Code'] == source]
                target_data = data_shortest_path[data_shortest_path['Destination Airport Code'] == target]
                if not target_data.empty:
                    x0, y0 = source_data[['Source Airport Longitude', 'Source Airport Latitude']].iloc[0]
                    x1, y1 = target_data[['Destination Airport Longitude', 'Destination Airport Latitude']].iloc[0]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
            
            # Mostrar los aeropuertos y el camino más corto en el mismo mapa
            fig = go.Figure()

            # Agregar las líneas que representan las conexiones entre aeropuertos
            fig.add_trace(go.Scattergeo(
                lat=edge_y,
                lon=edge_x,
                mode='lines',
                line=dict(width=2, color='red'),
                name='Shortest Path'
            ))
            
            # Agregar los nodos que representan los aeropuertos
            fig.add_trace(go.Scattergeo(
                lat=airports_shortest_path['Source Airport Latitude'],
                lon=airports_shortest_path['Source Airport Longitude'],
                mode='markers',
                marker=dict(size=10, color='blue'),
                hoverinfo='text',
                text=airports_shortest_path.apply(lambda row: f"Code: {row['Source Airport Code']}<br>"
                                                                f"Name: {row['Source Airport Name']}<br>"
                                                                f"City: {row['Source Airport City']}<br>"
                                                                f"Country: {row['Source Airport Country']}<br>"
                                                                f"Latitude: {row['Source Airport Latitude']}<br>"
                                                                f"Longitude: {row['Source Airport Longitude']}",
                                                                axis=1)
            ))

            fig.update_geos(
                showcountries=True,
                countrycolor="Black"
            )
            
            fig.show()
            
        except nx.NetworkXNoPath:
            print("No existe un camino entre {} y {}.".format(airport1, airport2))
                      
airport_instance = Airport()