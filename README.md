# citation_analisis
iPython notebooks and tools citation and co-authorship analysis


# Installation

Dependences:
 - anaconda package: 
 - Community detection package: https://pypi.python.org/pypi/python-louvain/0.3
 	- `pip3 install python-louvain`


# Launch

```ipython notebook <file.ipynb>```


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
