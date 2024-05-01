import plotly.express as px
import pandas as pd

# Importar datos desde el archivo CSV local
data = pd.read_csv('flights_final.csv')

# Eliminar filas con valores faltantes o inválidos en las columnas de latitud y longitud
data = data.dropna(subset=['Source Airport Latitude', 'Source Airport Longitude',
                           'Destination Airport Latitude', 'Destination Airport Longitude'])

# Crear un DataFrame para almacenar las coordenadas de origen y destino
source_airports = data[['Source Airport Latitude', 'Source Airport Longitude',
                        'Source Airport Name', 'Source Airport Code',
                        'Source Airport Country']].drop_duplicates()

# Crear scatter map
fig = px.scatter_geo(source_airports, lat='Source Airport Latitude', lon='Source Airport Longitude',
                     hover_name='Source Airport Name', title='Airports Locations',
                     color_discrete_sequence=['blue'], size_max=15,
                     custom_data=['Source Airport Code', 'Source Airport Country'])

# Configurar botones seleccionables
fig.update_traces(mode='markers', selector=dict(type='scattergeo'),
                  hovertemplate='<b>%{customdata[0]}</b><br>' +
                                'Name: %{hovertext}<br>' +
                                'Country: %{customdata[1]}<br>' +
                                'Latitude: %{lat}<br>' +
                                'Longitude: %{lon}')

# Función para mostrar la información del aeropuerto seleccionado
def show_airport_info(trace, points, selector):
    airport_code = points.point_vars['customdata'][0]
    airport_info = data[data['Source Airport Code'] == airport_code].iloc[0]
    print(airport_info)

fig.update_traces(customdata=source_airports[['Source Airport Code', 'Source Airport Country']])

# Actualizar la figura para mostrar la información del aeropuerto seleccionado
fig.update_traces(selector=dict(type='scattergeo'), hoverinfo='skip')
fig.update_layout(clickmode='event+select')
fig.for_each_trace(lambda t: t.on_click(show_airport_info))

fig.show()
"""import plotly.express as px
import pandas as pd

# Importar datos desde el archivo CSV local
data = pd.read_csv('flights_final.csv')

# Eliminar filas con valores faltantes o inválidos en las columnas de latitud y longitud
data = data.dropna(subset=['Source Airport Latitude', 'Source Airport Longitude',
                           'Destination Airport Latitude', 'Destination Airport Longitude'])

# Crear un DataFrame para almacenar las coordenadas de origen y destino
markers = pd.concat([data[['Source Airport Latitude', 'Source Airport Longitude', 'Source Airport Name','Source Airport Code','Source Airport Country']],
                   data[['Destination Airport Latitude', 'Destination Airport Longitude', 'Destination Airport Name','Destination Airport Code','Destination Airport Country']]])

# Crear scatter map
fig = px.scatter_geo(markers, lat='Source Airport Latitude', lon='Source Airport Longitude', 
                     hover_name='Source Airport Name', title='Airports Locations',
                     color_discrete_sequence=['blue'], size_max=15,
                     custom_data=['Source Airport Code', 'Source Airport Country'])

# Configurar botones seleccionables
fig.update_traces(mode='markers', selector=dict(type='scattergeo'),
                  hovertemplate='<b>%{customdata[0]}</b><br>' +
                                'Name: %{hovertext}<br>' +
                                'Country: %{customdata[1]}<br>' +
                                'Latitude: %{lat}<br>' +
                                'Longitude: %{lon}')

fig.show()"""
