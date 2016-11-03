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
        self.auth_cited_by_year = {}
        self.cite_year = {}
        self.cite_count = {}
        
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
    
    def write_gml_gr(self,filename):
        nx.set_edge_attributes(self.gr, 'year', self.coauth_year)
        nx.set_edge_attributes(self.gr, 'times', self.coauth_count)
        nx.write_gml(self.gr, filename)

    def write_gml_cgr(self, filename):
        nx.set_edge_attributes(self.cgr, 'year', self.cite_year)
        nx.set_edge_attributes(self.cgr, 'times', self.cite_count)
        nx.write_gml(self.cgr, filename)



    def create_cite_graph(self):
        for article_id, article in self.articles.items():
            #add all author of current article nodes
            for author in article.authors:
                author = author.strip()
                self.cgr.add_node(author)                
            for cited_article_id in article.references_ids:
                cited_article = self.articles.get(cited_article_id)
                if cited_article != None:
                    for cited_author in cited_article.authors:
                        cited_author = cited_author.strip()                    
                        self.cgr.add_node(cited_author) 
                        self.cite_year[(author, cited_author)] = self.cite_year.get((author, cited_author), []) + [article.year]
                        self.cite_count[(author, cited_author)] = self.cite_count.get((author, cited_author), 0) + 1
                        self.cgr.add_edge(author, cited_author)
                        pair = (cited_author, author)
                        # self.auth_cited_by_year[pair] = self.auth_cited_by_year.get(pair, []) + [article.year]

                        year_number_dict =  self.auth_cited_by_year.get(author, {})
                        year_number_dict[article.year] = year_number_dict.get(article.year, 0) + 1
                        self.auth_cited_by_year[author] = year_number_dict




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
            cite_distribution[self.cgr.in_degree(cite_node)] = cite_distribution.get(self.cgr.in_degree(cite_node), 0) + 1


        coauthor_distribution = sorted(coauthor_distribution.items(), key=operator.itemgetter(0))
        cite_distribution = sorted(cite_distribution.items(), key=operator.itemgetter(0))

        print("coauth:", coauthor_distribution[:10])
        print("cite:", cite_distribution[:10])
        return (coauthor_distribution, cite_distribution)

    def top_authors_cite_coauth_stat(self):
        STEP = 3
        author_year_coauthors_num = {}
        author_year_cites_num = {}
            
        auth_coauth_pagerank = calc_pagerank(self.gr, 10)[2]

        author_year_coauthors_num = dict( (author, Counter(years) ) for author, years in self.author_year.items() )

        return [author_year_coauthors_num.get(author, {}) for author, weight in auth_coauth_pagerank ]



        # filtered_year_coauth = [for author, years_dict in author_year_coauthors_num.items()]

        # for author, weight in auth_coauth_pagerank:
        #     for coauthor in self.gr.neighbors(author):
        #         for year in self.coauth_year.get((author, coauthor), []):
        #             year_number_dict = author_year_coauthors_num.get(author, {})
        #             year_number_dict[year] = year_number_dict.get(year, 0) + 1
        #             author_year_coauthors_num[author] = year_number_dict

        # auth_cite_pagerank = calc_pagerank(self.cgr, 10)[2]
        # for author, weight in auth_cite_pagerank:
        #     for who_cited in self.cgr.in_edges(author):
        #         for year in self.auth_cited_by_year.get((author, who_cited), []):
        #             year_number_dict =  articles_cited_in_year.get(author, {})
        #             year_number_dict[year] = year_number_dict.get(year, 0) + 1
        #             author_year_cites_num[author] = year_number_dict

        # return (author_year_coauthors_num, self.auth_cited_by_year)





    

