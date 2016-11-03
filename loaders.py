import re
from network import *

class Article:
    def __init__(self, paper_title, authors, year, journal, paper_index, abstract, references_ids):
        self.paper_title = paper_title
        self.authors = [x.strip() for x in authors if len(x.strip()) > 3]       
        self.year = int(year)    
        self.journal = journal
        self.paper_index = paper_index
        self.abstract = abstract
        self.references_ids = references_ids          
    


def parse_dataset_file(filename):
    paper_title_regexp = re.compile('#\*(.*)\n')
    authors_regexp = re.compile('#@(.*)\n')
    year_regexp = re.compile('#t(.*)\n')
    publication_venue_regexp = re.compile('#c(.*)\n')
    paper_index_regexp = re.compile('#index(.*)\n')
    references_ids_regexp = re.compile('#%(.*)\n')
    
    f = open(filename, 'r')
    
    paper_title = authors = publication_venue = paper_index_id = ''
    year = -1
    references_ids = []
    
    for line in f:
        if paper_title_regexp.search(line) is not None:
            paper_title = paper_title_regexp.search(line).group(1)
        elif authors_regexp.search(line) is not None:
            authors = authors_regexp.search(line).group(1)
        elif year_regexp.search(line) is not None:
            year = year_regexp.search(line).group(1)
        elif publication_venue_regexp.search(line) is not None:
            publication_venue = publication_venue_regexp.search(line).group(1)
        elif paper_index_regexp.search(line) is not None:
            paper_index = paper_index_regexp.search(line).group(1)
        elif references_ids_regexp.search(line) is not None:
            references_ids.append(references_ids_regexp.search(line).group(1))
        elif line == "\n":
            yield Article(paper_title, authors.split(",") 
                          if authors != '' else [], year, publication_venue, paper_index, None, references_ids)
            paper_title = authors = publication_venue = paper_index_id = ''
            year = -1
            references_ids = []


def load_authors_dataset(filename):
    f = open(filename, 'r')
    for line in f:
        [journal, title, authors, year, abstract] = line.split("\t")
        yield Article(title, authors.split(",") if authors != "" else [], year, journal, abstract, None, []) 
