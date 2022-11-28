import plotly.express as px
from skimage import io

import osmnx as ox

import plotly.graph_objects as go
import numpy as np

#funkcja do wyswietlania grafu w formie obrazu
def ImageGet():
    img = io.imread('WebAppCurrImage.jpg')
    fig = px.imshow(img)
    return fig


def Setup(a1, a2, a3, a4):
    north, east, south, west = a1, a2, a3, a4  # wspolrzedne mapy pobrane ze strony https://www.openstreetmap.org/
    # pobranie wszystkich wierzcholkow mapy
    G = ox.graph_from_bbox(north, south, east, west,
                           network_type='drive')  # opcjonalnie walk


    # nadanie indeksow wszystkim wezlom pobranym z mapy
    v = len(G.nodes)
    di = {}
    index = 0
    for node in G.nodes(data=True):
        di[node[0]] = [index]
        di[index] = [node[0]]
        index += 1

    li = []
    li.clear()
    for edge in G.edges(data=True):
        src_id = edge[0]
        dst_id = edge[1]
        new_src = di[src_id][0]
        new_dst = di[dst_id][0]
        weight = edge[2]['length']
        li.append([new_src, new_dst, weight])
    ox.plot_graph(G, edge_color="y", save=True, filepath="WebAppCurrImage.jpg")
    e = len(li)

    return G, v, e, li, di


def node_list_to_path(G, node_list):
    edge_nodes = list(zip(node_list[:-1], node_list[1:]))
    # print(edge_nodes)
    lines = []
    for u, v in edge_nodes:
        data = min(G.get_edge_data(u, v).values(), key=lambda x: x['length'])
        #jezlei wystepuje jakas geometria - krzywizna miedzy punktami
        if 'geometry' in data:
            xs, ys = data['geometry'].xy
            lines.append(list(zip(xs, ys)))
        else:
            #jezeli odleglosc miedzy punktami jest linia prosta
            x1 = G.nodes[u]['x']
            y1 = G.nodes[u]['y']
            x2 = G.nodes[v]['x']
            y2 = G.nodes[v]['y']
            line = [(x1, y1), (x2, y2)]
            lines.append(line)
    return lines


def calc_lat_long(G, path):
    lines = node_list_to_path(G, path)
    #     print(lines)
    long2 = []
    lat2 = []
    long2.clear()
    lat2.clear()
    for each_line_detail in lines:
        for coordinate in each_line_detail:
            long2.append(coordinate[0])
            lat2.append(coordinate[1])
    return lat2, long2


def plot_path(lat, long, origin_point, destination_point):
    # linie laczace wierzcholki
    fig = go.Figure(go.Scattermapbox(
        name="Path",
        mode="lines",
        lon=long,
        lat=lat,
        marker={'size': 10},
        line=dict(width=4.5, color='blue')))

    # znacznkik punku poczatkowego
    fig.add_trace(go.Scattermapbox(
        name="Source",
        mode="markers",
        lon=[origin_point[1]],
        lat=[origin_point[0]],
        marker={'size': 12, 'color': "red"}))

    # znacznki na punkcie koncowym
    fig.add_trace(go.Scattermapbox(
        name="Destination",
        mode="markers",
        lon=[destination_point[1]],
        lat=[destination_point[0]],
        marker={'size': 12, 'color': 'green'}))


    lat_center = np.mean(lat)
    long_center = np.mean(long)

    fig.update_layout(mapbox_style="open-street-map",
                      mapbox_center_lat=30, mapbox_center_lon=-80)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox={
                          'center': {'lat': lat_center, 'lon': long_center},
                          'zoom': 13})

    #     fig.show()
    return fig
