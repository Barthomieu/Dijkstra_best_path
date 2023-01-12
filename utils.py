import osmnx.utils_graph
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


def remove_edge_by_name(G_copy, searched_name):
    print("jestem w funkcji do usuwnia")

    #print(G_copy.edges(data=True))
    #for u, v, name in G_copy.edges(data='name'):
    #selected_edges = [(u, v) for u, v, key, e in G_copy.edges(data=True,keys=True) if e['name'] == 'Szkolna']
    #print("selected edges", selected_edges)
    searched_edges_ids = [(u, v) for u, v, key, data in G_copy.edges(data=True, keys=True) if 'name' in data and data['name'] == searched_name]
    print(len(searched_edges_ids), searched_edges_ids)
    if len(searched_edges_ids) > 0:
        G_copy.remove_edges_from(searched_edges_ids)
    else:
        print("Nie znaleziono ")
    return G_copy
    #for u, v, key, data in G_copy.edges(data=True, keys=True):
    #   if 'name' in data and data['name'] == 'Szkolna':
    #        print("searched_edges_id", u, v, key, data)
    #        G_copy.remove_edge(u,v)







def Setup(a1, a2, a3, a4, skip_nodes = None):
    north, east, south, west = a1, a2, a3, a4  # wspolrzedne mapy pobrane ze strony https://www.openstreetmap.org/
    # pobranie wszystkich wierzcholkow mapy
    G = ox.graph_from_bbox(north, south, east, west,
                           network_type='drive')  # opcjonalnie walk
    #warunek do usunięcia zamknietych ulic z modelu
    if skip_nodes is not None:
        print(" G edges przed usunięciem  ", len(G.edges))
        G2 = remove_edge_by_name(G, skip_nodes)
        print(" G edges po usunięciu ", len(G.edges))
        print(G2)
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
    #print("usuwam z pliku #########", )
    #for u, v, keys, name in G.edges(data="name", keys=True):
      #  print(u, v, keys, name)
      #  if name  == '1 Maja':
       #     print("Znalazłem ######", name)
        #    pass


    return G, v, e, li, di


def node_list_to_path(G, node_list):
    edge_nodes = list(zip(node_list[:-1], node_list[1:]))
    # print(edge_nodes)
    lines = []
    for u, v in edge_nodes:
        data = min(G.get_edge_data(u, v).values(), key=lambda x: x['length'])
        #print("#### g edge data", G.get_edge_data(u, v).values())
        #print(data)
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

    # znacznkik punktu poczatkowego
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
