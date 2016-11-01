from pygraph.classes.graph import graph
from pygraph.readwrite import dot
from pygraph.algorithms.minmax import shortest_path
from pygraph.algorithms.accessibility import connected_components
from pygraph.algorithms.pagerank import pagerank


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import re

import itertools
import random
import statistics

class CoathorNetwork:
    def __init__(self):
        self.articles = []
        self.author_to_article = {}
        self.gr = graph()
        
    def add_article(self, atricle):
        idx = len(self.articles)
        self.articles.append(atricle)
        # Lookup table for each author
        for author in atricle.authors:
            author = author.strip()
            articles_of_author = self.author_to_article.get(author, [])
            articles_of_author.append(idx)
            self.author_to_article[author] = articles_of_author
            # Add author to graph if not exists
            if not self.gr.has_node(author):
                self.gr.add_node(author)
        # Add authors to graph
        for pair in itertools.combinations(atricle.authors, 2):
            if not self.gr.has_edge(pair):
                self.gr.add_edge(pair);
    
    def get_articles_by_author(author):
        [self.articles[idx] for idx in author_to_article.get(author, [])]
    
    def write_dot(filename):
        f = open(filename, 'w')
        f.write(dot.write(self.gr))
        f.close()

class Article:
    def __init__(self, paper_title, authors, year, journal, paper_index, abstract, references_ids):
        self.paper_title = paper_title
        self.authors = [x.strip() for x in authors]       
        self.year = int(year)    
        self.journal = journal
        self.paper_index = paper_index
        self.abstract = abstract
        self.cite = references_ids          
    
