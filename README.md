# LOTUS dataset
This repository contains the code to download the LOTUS database with different versions.

## Installation
To install this package simply run : 
```bash
pip install git+https://github.com/mvisani/lotus-dataset
```

## Usage
To download all the files of all the versions of LOTUS, you can run the following command:
```bash
python examples/build_lotus.py all
```

You can also do : 
```python
from lotus_dataset import Dataset
dataset = Dataset.load("v10")
lotus_df = dataset.dataframe
```

You can also query LOTUS from Wikidata using the Qlever engine. This will load the most recent information about LOTUS (without metadata). The result is a dataframe of triples : species, molecule, reference.
```python
from lotus_dataset import Dataset
df = Dataset.get_lotus_from_wikidata()
```