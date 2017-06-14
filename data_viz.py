import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import psycopg2


def trim_degrees(g, degree=1):
    g2 = g.copy()
    for drug, ae in g2.edges():
        if g2.number_of_edges(drug, ae) <= degree:
            g2.remove_edge(drug, ae)

    for node in g2.nodes():
        if len(g2.edges(node)) <= degree:
            g2.remove_node(node)
    return g2

def get_colors(g):
    color_list =[]
    for node, data in g.nodes(data=True):
        if data['node_type'] == 'AE':
            color_list.append('c')
        else:
            color_list.append('m')
    return color_list

def make_network_graph(ae_dict, degree_to_trim=1):
    G=nx.MultiGraph()
    for ae, drug_list in ae_dict.iteritems():
        G.add_node(ae, node_type='AE')
        for idx, drug in enumerate(drug_list):
            G.add_node(drug, node_type='Drug')
            G.add_edge(drug, ae)
    G=trim_degrees(G, degree_to_trim)
    return G