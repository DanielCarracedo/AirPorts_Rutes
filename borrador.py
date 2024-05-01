import plotly.express as px
import pandas as pd
import sys

# Importar datos desde el archivo CSV local
data = pd.read_csv('flights_final.csv')

# Eliminar filas con valores faltantes o inválidos en las columnas de latitud y longitud
data = data.dropna(subset=['Source Airport Latitude', 'Source Airport Longitude',
                           'Destination Airport Latitude', 'Destination Airport Longitude'])

# Crear un DataFrame para almacenar las coordenadas de origen y destino
source_airports = data[['Source Airport Latitude', 'Source Airport Longitude',
                        'Source Airport Name', 'Source Airport Code',
                        'Source Airport Country']].drop_duplicates()

# Función para mostrar la información del aeropuerto seleccionado
def show_airport_info(airport_code):
    airport_info = data[data['Source Airport Code'] == airport_code].iloc[0]
    print(f"Airport Code: {airport_info['Source Airport Code']}")
    print(f"Airport Name: {airport_info['Source Airport Name']}")
    print(f"Country: {airport_info['Source Airport Country']}")
    print(f"Latitude: {airport_info['Source Airport Latitude']}")
    print(f"Longitude: {airport_info['Source Airport Longitude']}")
    return airport_info

# Buscar el aeropuerto por código
def search_by_code(airport_code):
    if airport_code in source_airports['Source Airport Code'].values:
        airport_info = show_airport_info(airport_code)
        plot_airport_location(airport_info)
    else:
        print("Airport not found!")

# Función para mostrar la ubicación del aeropuerto en el mapa
def plot_airport_location(airport_info):
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

# Verificar si se proporcionó un código de aeropuerto como argumento
if len(sys.argv) > 1:
    airport_code = sys.argv[1].upper()
    search_by_code(airport_code)
else:
    # Solicitar al usuario que ingrese el código del aeropuerto
    airport_code = input("Enter airport code: ").upper()
    search_by_code(airport_code)