import plotly.express as px
import pandas as pd
import sys

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
                pass
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
    def plot_airport_location(self,airport_info):
        fig = px.scatter_geo(data_frame=airport_info.to_frame().T, lat='Source Airport Latitude', lon='Source Airport Longitude',
                         hover_name='Source Airport Name', title='Airport Location',
                         color_discrete_sequence=['blue'], size_max=15,
                         custom_data=['Source Airport Code', 'Source Airport Country'])

        fig.update_traces(mode='markers', selector=dict(type='scattergeo'),
                      hovertemplate='<b>%{customdata[0]}</b><br>' +
                                    'Name: %{hovertext}<br>' +
                                    'Country: %{customdata[1]}<br>' +
                                    'Latitude: %{lat}<br>' +
                                    'Longitude: %{lon}')

        fig.show()
    
    # Buscar el aeropuerto por código
    def search_by_code(self,airport_code):
        if airport_code in self.source_airports['Source Airport Code'].values:
            airport_info = self.airport_info(airport_code)
            self.plot_airport_location(airport_info)
        else:
            print("Airport not found!")
    
    def MostFar_10Airports(self):
        pass
    
    def Airports_min(self):
        pass
airport_instance = Airport()