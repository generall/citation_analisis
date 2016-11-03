import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import power_divergence


import re
import itertools
import random
import statistics
import operator
import math

from loaders import *
from graph_tools import *


def plot_dict(stat, xlbl, ylbl):
    plt.plot([x for x in stat.keys()], [x for x in stat.values()])
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.show()

def plot_list(stat, xlbl, ylbl):
    plt.plot(stat)
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.show()

class CoauthorNetwork:
    def __init__(self):
        self.articles = {}
        self.author_to_article = {}
        self.gr = nx.Graph()
        self.cgr = nx.DiGraph()
        self.coauth_count = {}
        self.coauth_year = {}
        self.author_year = {}
        
    def add_article(self, article):
        article_id = article.paper_index
        self.articles[article_id] = article
        # Lookup table for each author
        for author in article.authors:
            author = author.strip()
            articles_of_author = self.author_to_article.get(author, [])
            articles_of_author.append(article_id)
            self.author_to_article[author] = articles_of_author
            self.author_year[author] = self.author_year.get(author, []) + [article.year]
            # Add author to graph if not exists
            self.gr.add_node(author)
        # Add authors to graph
        for pair in itertools.combinations(article.authors, 2):
            self.coauth_count[pair] = self.coauth_count.get(pair, 0) + 1
            self.coauth_year[pair] = self.coauth_year.get(pair, []) + [article.year]
            self.gr.add_edge(pair[0], pair[1])

    
    def get_articles_by_author(author):
        [self.articles.get(idx) for idx in author_to_article.get(author, [])]
    
    def write_dot(filename):
        f = open(filename, 'w')
        f.write(dot.write(self.gr))
        f.close()

    def create_cite_graph(self):
        for article_id, article in self.articles.items():
            #add all author of current article nodes
            for author in article.authors:
                author = author.strip()
                self.cgr.add_node(author)                
            for cited_article in article.references_ids:
                if self.articles.get(cited_article) != None:
                    for cited_author in self.articles.get(cited_article).authors:
                        cited_author = cited_author.strip()                    
                        self.cgr.add_node(cited_author) 
                        self.cgr.add_edge(author, cited_author)


    def load_with_loader(file, loader, article_filter = None):
        coauthorNetwork = CoauthorNetwork()
        if article_filter == None:
            article_filter = lambda x: True
        for article in loader(file):
            if article_filter(article):
                coauthorNetwork.add_article(article)
        coauthorNetwork.create_cite_graph()

        print("Uniq authors:", len([x for x in coauthorNetwork.author_to_article.keys()]))
        return coauthorNetwork
    

    def gen_components(self):
        self.components = [c for c in sorted(nx.connected_components(self.gr), key=len, reverse=True)]
        self.components_sizes = dict((idx, math.log(float(len(c)))) for idx, c in enumerate(self.components))
        self.component_count = len(self.components)



    def analize_component(self):
        the_component = self.components[0]
        self.component_subgraph = self.gr.subgraph(the_component)
        


    def print_info_component(self):
        PRECISION = 50 # number of authors to calc avg distance
        print(" ")
        print("Connected component distribution (log-scale)")
        plot_dict(self.components_sizes, "rank", "size(log)")

        print(power_divergence([len(c) for c in self.components]))
        print("Connected component count:", self.component_count)

        print("----------")
        print("Authors count:",len(self.component_subgraph.nodes()))
        stat = get_distance_stat(self.component_subgraph, PRECISION)
        
        print("Mean distance:", sum([value * key for key, value in stat.items()]))
        print(" ")
        print("Distance distribution")
        plot_dict(stat, "rank", "density")
        
        cstat = get_centrality_stat(self.cgr)
        
        plot_list(cstat[0], "rank", "log node degree centrality")
        plot_list(cstat[1], "rank", "log node betweenness centrality")
        plot_list(cstat[2], "rank", "log node closeness centrality")

    def calc_coauthor_cite_distribution(self):
        coauthor_distribution = {}
        cite_distribution = {}
        for article_id, article in self.articles.items():
            coauthor_distribution[len(article.authors)] = coauthor_distribution.get(len(article.authors), 0) + 1

        for cite_node in self.cgr.nodes():
            in_nodes = self.cgr.in_edges(cite_node)
            if len(in_nodes) != 0:
                cite_distribution[len(in_nodes[0])] = cite_distribution.get(len(in_nodes[0]), 0) + 1

        coauthor_distribution = sorted(coauthor_distribution.items(), key=operator.itemgetter(0))
        cite_distribution = sorted(cite_distribution.items(), key=operator.itemgetter(0))

        print("coauth:", coauthor_distribution[:10])
        print("cite:", cite_distribution[:10])
        return (coauthor_distribution, cite_distribution)


    

