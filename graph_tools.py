import random
import operator

import networkx as nx
import math

def construct_graph_filtered(old_graph, node_predicate, egde_predicate):
    new_graph = nx.Graph()
    for node in old_graph.nodes():
        if node_predicate(node):
            new_graph.add_node(node)
    for edge in old_graph.edges():
        if node_predicate(edge[0]) and node_predicate(edge[1]) and egde_predicate(edge):
            new_graph.add_edge(edge)
    return new_graph


# calculate distance distribution for 
# detect small world phenomenon
def get_distance_stat(graph, n):
    stat = {}
    summ = len(graph.nodes()) * n
    for i in range(n): # iterative calculation of shortest path
        random_author = random.choice(graph.nodes())
        distances = nx.shortest_path_length(graph, random_author)
        for x in distances.values():
            stat[x] = stat.get(x, 0) + 1;
    return dict( (key, value / summ) for key, value in stat.items() )


#calculate centrality statistics
def get_centrality_stat(graph):
    N = len(graph.nodes())
    degree_centrality_full_stat = nx.degree_centrality(graph)
    betweenness_centrality_full_stat = nx.betweenness_centrality(graph, 100)
    closeness_centrality_full_stat = nx.closeness_centrality(graph)

    sorted_degree_centrality_stat = sorted(degree_centrality_full_stat.items(), key=operator.itemgetter(1), reverse=True)[:10]
    sorted_betweenness_centrality_stat = sorted(betweenness_centrality_full_stat.items(), key=operator.itemgetter(1), reverse=True)[:10]
    sorted_closeness_centrality_stat = sorted(closeness_centrality_full_stat.items(), key=operator.itemgetter(1), reverse=True)[:10]

    top_degree_authors = sorted_degree_centrality_stat[:10]
    top_betweenness_authors = sorted_betweenness_centrality_stat[:10]
    top_closeness_authors = sorted_closeness_centrality_stat[:10]

    print("Top 10 authors by degree centrality measurement:", top_degree_authors)
    print("Top 10 authors by betweenness centrality measurement:", top_betweenness_authors)
    print("Top 10 authors by closeness centrality measurement:", top_closeness_authors)
    # print("----------")
    # print("Average degree node centrality:", sum(centrality_stat.values())/len(centrality_stat) )
    
    # max_centrality = max(centrality_stat.values())
    # print("Maxumum degree node centrality:", max_centrality)
    
    # nodes_num = len(graph.nodes())
    # print("Degree graph centrality:", 
    #       sum([max_centrality - x for x in centrality_stat.values()])/((nodes_num - 1)*(nodes_num - 2)))
    
    # print("----------")
    return ([y for x,y in sorted_degree_centrality_stat], 
            [y for x,y in sorted_betweenness_centrality_stat],
            [y for x,y in sorted_closeness_centrality_stat])


def calc_pagerank(graph, TOP=50):
    percent_threshold = 0.1
    weighted_nodes = nx.pagerank(graph)
    sorted_nodes = sorted(weighted_nodes.items(), key = lambda pair: pair[1], reverse=True)
    node_ranks = dict( (val, idx) for idx, val in enumerate(sorted_nodes))
#     print(sorted_nodes[0:TOP])
    top_subgraph = graph.subgraph([x[0] for x in sorted_nodes[0:TOP]])
    return (top_subgraph, weighted_nodes, sorted_nodes[:TOP])


