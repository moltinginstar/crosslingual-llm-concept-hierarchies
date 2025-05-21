# The Representation of Concept Hierarchies Across Languages in LLMs

This repository contains the code and data for the paper "The Representation of Concept Hierarchies Across Languages in Large Language Models".

## Setting up the environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Repository structure

```plaintext
.
├── [cached_data/]                # Cached embeddings and other large files (not committed to the repo)
├── plots/                        # Plots
├── tables/                       # CSV files with the results of the experiments
├── build_wordnet_dataset.py      # Script to build the WordNet dataset (not used in the paper)
├── dataset.py                    # The main dataset used in the paper
├── main.ipynb                    # Notebook to run the experiments and generate the plots
├── pyproject.toml                # Linter configuration
├── README.md                     # This file
├── requirements.txt              # Project dependencies
└── wordnet_dataset.json          # The output of the build_wordnet_dataset.py script
```
