import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import psycopg2
import seaborn as sns


def trim_degrees(g, degree=1):
    """
    Removes the nodes and edges according to the 
    desired degrees-to-trim (input value).
    """

    g2 = g.copy()
    for drug, ae in g2.edges():
        if g2.number_of_edges(drug, ae) <= degree:
            g2.remove_edge(drug, ae)

    for node in g2.nodes():
        if len(g2.edges(node)) <= degree:
            g2.remove_node(node)
    return g2

def get_colors(g):
    """
    Dictionary key nodes are colored magenta, 
    and dictionary value nodes are colored cyan.
    """

    color_list =[]
    for node, data in g.nodes(data=True):
        if data['node_type'] == 'AE':
            color_list.append('m')
        else:
            color_list.append('c')
    return color_list

def make_network_graph(ae_dict, degree_to_trim=1):
    """
    Given an input dictionary, makes a network graph.
    """

    G=nx.MultiGraph()
    for ae, drug_list in ae_dict.iteritems():
        G.add_node(ae, node_type='AE')
        for idx, drug in enumerate(drug_list):
            G.add_node(drug, node_type='Drug')
            G.add_edge(drug, ae)
    G=trim_degrees(G, degree_to_trim)
    return G


def plot_related_terms(term1, term2, term3, term4, term5):
    """
    Returns a dictionary of preferred terms most related to the input
    preferred terms. This dictionary is stored as pt_dict, and can be
    used to make a network graph. Alternatively, can be modified to
    return a pandas dataframe, to create a heatmap of related terms.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')
    cur = con.cursor()
    cur.execute("""SELECT reac1.caseid, reac1.pt FROM reac1 \
            WHERE reac1.caseid IN (SELECT caseid FROM reac1 \
            WHERE pt LIKE term1 OR \
            pt LIKE term2 OR \
            pt LIKE term3 OR \
            pt LIKE term4 OR \
            pt LIKE term5)""")

    pt_dict = {term1:[], term2:[], term3:[], term4:[], term5:[]}
    terms_to_add = []
    first_case = cur.fetchone()[0]

    for row in cur:
        if row[0] == first_case:
            terms_to_add.append(row[1])
        else:
            if term1 in terms_to_add:
                pt_dict[term1].append(terms_to_add)
            if term2 in terms_to_add:
                pt_dict[term2].append(terms_to_add)
            if term3 in terms_to_add:
                pt_dict[term3].append(terms_to_add)
            if term4 in terms_to_add:
                pt_dict[term4].append(terms_to_add)
            if term5 in terms_to_add:
                pt_dict[term5].append(terms_to_add)
        
            terms_to_add = []
            terms_to_add.append(row[1])
            first_case = row[0]
        
    for key, val in pt_dict.iteritems():
        pt_dict[key] = [item for sublist in val for item in sublist]
    
    cur.close()
    con.close()

    tuple_list = []
    for key, val in pt_dict.iteritems():
        for term in val:
            tuple_list.append(tuple([key, term]))
        
    tuple_dict={}
    for pair in tuple_list:
        tuple_dict[pair] = 0
    for pair in tuple_list:
        tuple_dict[pair] += 1

    triplet_list = []
    for key, val in tuple_dict.iteritems():
        triplet_list.append(tuple([val, key]))

    #print sorted(triplet_list, reverse=True)

    filtered_tuple_dict = {}
    for key, val in tuple_dict.iteritems():
        if (val > 450)&(key != (term1,term1))&(key != (term2,term2)
                            )&(key != (term3, term3)
                            )&(key != (term4, term4)
                            )&(key != (term5, term5)):
            filtered_tuple_dict[key] = val
    
    ser = pd.Series(list(filtered_tuple_dict.values()), 
        index=pd.MultiIndex.from_tuples(filtered_tuple_dict.keys()))
    df = ser.unstack().fillna(0)

    return pt_dict  