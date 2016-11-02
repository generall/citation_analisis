# from pygraph.classes.graph import graph
# from pygraph.classes.digraph import digraph
# from pygraph.readwrite import dot
# from pygraph.algorithms.minmax import shortest_path
# from pygraph.algorithms.accessibility import connected_components
# from pygraph.algorithms.pagerank import pagerank


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import re
import networkx as nx

import itertools
import random
import statistics

class CoauthorNetwork:
    def __init__(self):
        self.articles = {}
        self.author_to_article = {}
        self.gr = nx.Graph()
        self.cgr = nx.DiGraph()
        
    def add_article(self, article):
        article_id = article.paper_index
        self.articles[article_id] = article
        # Lookup table for each author
        for author in article.authors:
            author = author.strip()
            articles_of_author = self.author_to_article.get(author, [])
            articles_of_author.append(article_id)
            self.author_to_article[author] = articles_of_author
            # Add author to graph if not exists
            self.gr.add_node(author)
        # Add authors to graph
        for pair in itertools.combinations(article.authors, 2):
            self.gr.add_edge(pair[0], pair[1]);

        # self.cgr.add_node(article.paper_index, title=article.paper_title)

        # for cite in article.references_ids:
        #     if not self.cgr.has_node(cite):
        #         self.cgr.add_node(cite)
        #     self.cgr.add_edge(article.paper_index, cite)
        # self.cgr.add_node()
    
    def get_articles_by_author(author):
        [self.articles.get(idx) for idx in author_to_article.get(author, [])]
    
    def write_dot(filename):
        f = open(filename, 'w')
        f.write(dot.write(self.gr))
        f.close()

    def create_cite_graph(self):
        for article_id, article in articles.items():
            #add all author of current article nodes
            for author in article.authors:
                author = author.strip()
                self.cgr.add_node(author)                
            for cited_article in article.references_ids:
                for cited_author in articles.get(cited_article).authors or []:
                    cited_author = cited_author.strip()                    
                    self.cgr.add_node(cited_author) 
                    self.cgr.add_edge(author, cited_author)




class Article:
    def __init__(self, paper_title, authors, year, journal, paper_index, abstract, references_ids):
        self.paper_title = paper_title
        self.authors = [x.strip() for x in authors if len(x.strip()) > 3]       
        self.year = int(year)    
        self.journal = journal
        self.paper_index = paper_index
        self.abstract = abstract
        self.references_ids = references_ids          
    
