# citation_analysis
iPython notebooks and tools citation and co-authorship analysis

Presenation with results: https://docs.google.com/presentation/d/1-rjhX4JgB94eDXsOjm7QxFtpktK8OpM4eX-mhCSNq4s/edit?usp=sharing

# Installation

Dependences:
 - anaconda package: https://www.continuum.io/downloads
 - Community detection package: https://pypi.python.org/pypi/python-louvain/0.3
 	- `pip3 install python-louvain`


# Launch

```
ipython notebook <file.ipynb>
```


# Notebooks

- `coauthors.ipynb`
	- Connected components analysis
	- Top authors trends
	- Author cited rank prediction (commented)
- `CommunityDetection.ipynb`
	- Detection of communities
	- Ploting graph
	- Detects most connected author for each community
- `Distributions.ipynb`
	- Calculates various statistics for citation and co-authorship graphs
- `Save GML.ipynb`
	- importing graphs


# Files

- `network.py`
	- main model class contains:
		- dataset representation 
		- graph import functions
		- graph export functions
- `graph_tools.py`
	- `get_distance_stat` - calculates distance distribution
	- `get_centrality_stat` - calculates centrality distribution
	- `calc_pagerank` - calculates PageRank
- `plot_n_fit.py`
	- contains functions for plotting data with fitting to Gaussian or power laws
- `loaders.py`
	- contains functions for reading dataset
	- Article class representation

# Example of use


```python
coauthorNetwork = CoauthorNetwork.load_with_loader("./data/dataset.txt", parse_dataset_file);
print("co-authors:")
for x in calc_pagerank(coauthorNetwork.gr, 10)[2]: # returns array of top 10 pairs: ("author", pageRank) sorted by pageRank
    print(x[0])
```

- `parse_dataset_file` - function for loading datasets from https://aminer.org/citation
- `"./data/dataset.txt"` - path to unzipped dataset
- `coauthorNetwork`
	- `coauthorNetwork.gr` - co-authorship graph
	- `coauthorNetwork.cgr` - cite graph

# Motivation

| Analysis | Purpose | Result | Method |
|----------|---------|--------|----------|
| Connected components | Define graph connectivity | Component count: 144877 Max component size: 338683  | `get_distance_stat` |
| Distance distribution| Define how close authors connected | Mean distance: 7.77 | `get_distance_stat`  |
| Centrality distributions |  Identify the most important authors | presentation, slide \#6 | `get_centrality_stat` |
| Most influent author anlysis | Define top 10 most influent authors | Donald E. Knuth one of them | `calc_pagerank` | 
| Co-authors count distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | see `Distributions.ipynb` |
| Co-authors count distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | see `Distributions.ipynb` |
| Cite count distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | see `Distributions.ipynb` |
| Cited from others count distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | see `Distributions.ipynb` |
| Publication count distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | see `Distributions.ipynb` |
| Publications count of pair of authors distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | see `Distributions.ipynb` |
| Citation-co-authorship distribution | Ckeck for how co-authorship and citattions correlated | It does not | see `Distributions.ipynb` |
| Publication count through years distribution | Check for how publication count changes | It growth | see `Distributions.ipynb` |
| Top 20 authors citation\co-authorship trends | Identify top20 authors and their trends| presentation, slide #16 | See `coauthors.ipynb` |
|Cliques in co-authorship graph distribution | Check for corresponding to properties of known graphs | graph fits small-world graph properties | `CliquesCompute.ipynb` |
|Community detection| Detect communities and it's leaders | presentation, slide 17 + `CommunityDetection.ipynb` | `CommunityDetection.ipynb` |



