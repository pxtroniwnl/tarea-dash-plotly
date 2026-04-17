import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json

# ==========================================
# 1. PREPARACIÓN DE DATOS (CRÍTICO)
# ==========================================
print("Procesando datos...")

# Cargar Shapefile
geo_dpto = gpd.read_file("data/MGN2024_DPTO_POLITICO.zip")
geo_dpto = geo_dpto.to_crs(epsg=4326) 

# Asegurar que el código sea de 2 dígitos
geo_dpto['dpto_ccdgo'] = geo_dpto['dpto_ccdgo'].astype(str).str.zfill(2)

# Simplificar la geometría para fluidez
geo_dpto['geometry'] = geo_dpto['geometry'].simplify(0.01)

# Crear el GeoJSON
geojson_dict = json.loads(geo_dpto.to_json())

# Cargar CSV de IPM
df = pd.read_csv("data/ipm_dpto_ajust.csv")
df['cod_dpto'] = df['cod_dpto'].astype(str).str.zfill(2)
df['brecha_urbano_rural'] = df['resto'] - df['cabecera']

# --- DEFINICIÓN DE ESCALA DE COLOR "CAFÉ POBREZA" ---
# Va desde un tono hueso (limpio) hasta un café barro oscuro (carencia)
color_pobreza_cafe = [
    [0, "#fbfaf0"],      # Blanco hueso (0% pobreza)
    [0.5, "#8d6e63"],    # Café medio
    [1, "#3e2723"]       # Café oscuro "barro" (Pobreza máxima)
]

# ==========================================
# 2. INTERFAZ
# ==========================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Brechas de Pobreza en Colombia", className="text-center mt-4"),
            html.P("Análisis visual del impacto de la pobreza multidimensional", className="text-center text-muted")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Perspectiva de área:"),
            dbc.Select(
                id='tipo-area',
                options=[
                    {'label': 'Pobreza Total', 'value': 'total'},
                    {'label': 'Pobreza Urbana (Cabecera)', 'value': 'cabecera'},
                    {'label': 'Pobreza Rural (Resto)', 'value': 'resto'}
                ],
                value='total'
            ),
        ], md=4),
        dbc.Col([
            html.Label("Año de análisis:"),
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(), max=df['year'].max(),
                value=df['year'].max(),
                marks={str(y): str(y) for y in df['year'].unique()},
                step=None
            )
        ], md=8)
    ], className="bg-light p-3 rounded mb-4 shadow-sm"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='mapa-colombia'), md=7),
        dbc.Col([
            html.H5("Brecha Crítica (Rural vs Urbano)", className="text-center"),
            html.P("Top 10 departamentos con mayor desigualdad campo-ciudad", 
                   className="text-center small text-muted"),
            dcc.Graph(id='grafico-brecha')
        ], md=5)
    ])
], fluid=True)

# ==========================================
# 3. CALLBACK
# ==========================================
@app.callback(
    [Output('mapa-colombia', 'figure'),
     Output('grafico-brecha', 'figure')],
    [Input('year-slider', 'value'),
     Input('tipo-area', 'value')]
)
def update_visuals(selected_year, selected_area):
    dff = df[df['year'] == selected_year]
    
    # 1. MAPA CHOROPLETH (Con escala café)
    fig_map = px.choropleth_mapbox(
        dff,
        geojson=geojson_dict,
        locations="cod_dpto",
        featureidkey="properties.dpto_ccdgo",
        color=selected_area,
        color_continuous_scale=color_pobreza_cafe, # Aplicando el color café
        hover_name="nombre_dpto",
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 4.5709, "lon": -74.2973},
        opacity=0.8,
        title=f"Distribución IPM {selected_area.upper()} (%)"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    # 2. GRÁFICO DE BARRAS (Brecha con misma escala de color)
    top_brechas = dff.sort_values('brecha_urbano_rural', ascending=True).tail(10)
    fig_bar = px.bar(
        top_brechas,
        x='brecha_urbano_rural',
        y='nombre_dpto',
        orientation='h',
        color='brecha_urbano_rural',
        color_continuous_scale=color_pobreza_cafe, # Aplicando el color café
        labels={'brecha_urbano_rural': 'Diferencia de puntos %'}
    )
    fig_bar.update_layout(
        margin={"r":10,"t":20,"l":0,"b":0}, 
        showlegend=False,
        xaxis_title="Brecha (Resto - Cabecera)"
    )

    return fig_map, fig_bar

if __name__ == '__main__':
    app.run(debug=True)