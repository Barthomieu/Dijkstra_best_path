import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import networkx as nx
import shapely
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
import osmnx as ox
from Dijkstra_algorithm import Node_Distance, Graph
from utils import *



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1("Najkrótsza ścieżka z wykorzystaniem algorytmu  Dijkstry"),
    dcc.Link("współrzędne mapy znajdziesz tutaj:   ",
             href="https://www.openstreetmap.org/export#map=14/50.2535/19.0245", target="_blank"),
    html.Br(),
    html.Div(["Północ: ",
              dcc.Input(id='input-1-state', value='50.2677', type='text')]),
    html.Br(),
    html.Div(["Wschód: ",
              dcc.Input(id='input-2-state', value='18.9835', type='text')]),
    html.Br(),
    html.Div(["Południe: ",
              dcc.Input(id='input-3-state', value='50.2393', type='text')]),
    html.Br(),
    html.Div(["Zachód: ",
              dcc.Input(id='input-4-state', value='19.1032', type='text')]),
    html.Br(),
    html.Div(["Start - dł. geograficzna: ",
              dcc.Input(id='source-long', value='19.04516', type='text')]), #współrzedne CNTI domyślnie w celach prezentacji
    html.Br(),
    html.Div(["start - sz. geograficzna: ",
              dcc.Input(id='source-lat', value='50.26037', type='text')]),
    html.Br(),
    html.Div(["koniec - dł. geograficzna: ",
              dcc.Input(id='destination-long', value='19.00277', type='text')]),
    html.Br(),
    html.Div(["koniec - sz. geograficzna: ",
              dcc.Input(id='destination-lat', value='50.25342', type='text')]),
    html.Br(),
    html.Button(id='submit-button-state1', n_clicks=0,
                children='Szukaj najkrótszej trasy'),
    html.Br(),
    html.Div(["Wprowadź nazwę zamkniętej ulicy: ",
              dcc.Input(id='closed_streets', value='W', type='text')]),
    html.Br(),
    html.Button(id='submit-button-state2', n_clicks=0,
                children='Szukaj nowej trasy'),

    html.Br(),
    html.Div(id='output-state'),
    html.Br(),
    html.Div(id='container1'),
    html.Br(),
    html.Div(id='container2')

])


def getPath(parent, output_node_id_zero_indexed, input_node_id_zero_index, di):
    route = []
    route.clear()
    curr = output_node_id_zero_indexed
    while (curr != input_node_id_zero_index):
        route.append(curr)
        curr = parent[curr]
    route.append(input_node_id_zero_index)
    route.reverse()
    path = []
    path.clear()
    for pa in route:
        path.append(di[pa][0])
    return path



@app.callback(Output('container1', 'children'),
              Input('submit-button-state1', 'n_clicks'),
                Input('submit-button-state2', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'),
              State('input-3-state', 'value'),
              State('input-4-state', 'value'),
              State('source-long', 'value'),
              State('source-lat', 'value'),
              State('destination-long', 'value'),
              State('destination-lat', 'value'),
                State('closed_streets', 'value'))
def update_output(btn1, btn2 , input1, input2, input3, input4, src_long, src_lat, dst_long, dst_lat,closed_streets):
    src_long = float(src_long)
    src_lat = float(src_lat)
    dst_long = float(dst_long)
    dst_lat = float(dst_lat)
    origin_point = (src_long, src_lat)
    destination_point = (dst_long, dst_lat)
    G, v, e, li, di = Setup(float(input1), float(
        input2), float(input3), float(input4))

    g = Graph(v)  # Graf z liczba wierzcholkow v
    for i in range(e):
        g.Add_Into_Adjlist(li[i][0], Node_Distance(li[i][1], li[i][2]))
    if btn1 is not None:
        # funkcja z biblioteki os fo pobierania najblizszych wezlow na podstawie wspolrzednych i listy wezlow
        origin_node = ox.nearest_nodes(G, src_long, src_lat)
        destination_node = ox.nearest_nodes(G, dst_long,dst_lat)
        input_node_id_zero_index = di[origin_node][0]
        output_node_id_zero_indexed = di[destination_node][0]

        ShortestDist, parent = g.Dijkstras_Shortest_Path(
            input_node_id_zero_index, output_node_id_zero_indexed, v)
        path = getPath(parent, output_node_id_zero_indexed,
                       input_node_id_zero_index, di)
        print("Path", path)
        lat2, long2 = calc_lat_long(G, path)
        fig1 = plot_path(lat2, long2, origin_point, destination_point)
        return html.Div([dcc.Graph(figure=ImageGet()), html.Br(),
                         html.H6("Najrótsza ścieżka wynosi = {} metrów".format(ShortestDist),
                                 style={'color': 'Red', 'text-align': 'center'}), html.Br(), dcc.Graph(figure=fig1)])
    if btn2 is not None:
        print("wywołanie z drugiego przyciku")
        G_copy = G.copy()
        closed_street = closed_streets
        print(closed_streets, " usuwam ulice")
        remove_edge_by_name(G_copy, closed_street)

        origin_node = ox.nearest_nodes(G_copy, src_long, src_lat)
        destination_node = ox.nearest_nodes(G_copy, dst_long, dst_lat)
        input_node_id_zero_index = di[origin_node][0]
        output_node_id_zero_indexed = di[destination_node][0]

        ShortestDist, parent = g.Dijkstras_Shortest_Path(
            input_node_id_zero_index, output_node_id_zero_indexed, v)
        path = getPath(parent, output_node_id_zero_indexed,
                       input_node_id_zero_index, di)
        print("Path2", path)
        lat2, long2 = calc_lat_long(G_copy, path)
        fig2 = plot_path(lat2, long2, origin_point, destination_point)
        return html.Div([dcc.Graph(figure=ImageGet()), html.Br(),
                         html.H6("Najrótsza ścieżka wynosi = {} metrów".format(ShortestDist),
                                 style={'color': 'Red', 'text-align': 'center'}), html.Br(), dcc.Graph(figure=fig2)])


if __name__ == '__main__':
    app.run_server(debug=False)