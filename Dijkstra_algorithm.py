
from collections import defaultdict


class Node_Distance:

    def __init__(self, name, dist):
        self.name = name
        self.dist = dist


class Graph:

    def __init__(self, node_count):
        # lista wierzcholkow przekazywana jest do slownika
        self.adjlist = defaultdict(list)
        self.node_count = node_count

    def Add_Into_Adjlist(self, src, node_dist):
        self.adjlist[src].append(node_dist)

    def Dijkstras_Shortest_Path(self, source, dst, v):

        # początkowa odleglosc ustawiona na jak najwieksza
        distance = [999999999999] * self.node_count
        distance[source] = 0
        parent = []
        parent.clear()
        for i in range(v):
            parent.append(i)

        # Slownik z wartosciami:  { node, distance_from_source }
        dict_node_length = {source: 0}

        while dict_node_length:

            # wybieram ze slownika wezel o najkrotszej odleglosci
            current_source_node = min(
                dict_node_length, key=lambda k: dict_node_length[k])
            del dict_node_length[current_source_node]
            if (current_source_node == dst):
                break

            for node_dist in self.adjlist[current_source_node]:
                adjnode = node_dist.name
                length_to_adjnode = node_dist.dist


                if distance[adjnode] > distance[current_source_node] + length_to_adjnode:
                    parent[adjnode] = current_source_node
                    distance[adjnode] = distance[current_source_node] + \
                                        length_to_adjnode
                    dict_node_length[adjnode] = distance[adjnode]
        return distance[dst], parent






