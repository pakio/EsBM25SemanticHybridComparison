# Elasticsearch BM25 vs KNN vs Hybrid comparison system

This is the ready-to-use demo repository to test Elasticsearch semantic search with embedded transformer using ingest pipeline.

- Data
  - wikimedia enwiki 20221201 dump [url](https://dumps.wikimedia.org/enwiki/20221201/)
- Model
  - sentence-transformers/msmarco-MiniLM-L-12-v3 [link(Hugging Face)](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L-12-v3)

# prerequisites
This repository uses the softwares/tools/frameworkds below.
- docker
- docker-compose
- python (>3.10)

# How to run
## 1. Launch Elasticsearch and upload model
Run `./Es/setup.sh` to launch Elasticsearch, upload model, and configure the ingest pipeline.

## 2. Ingest data
Run `./indexer/setup.sh` to download, and index the data.
If you observe 429 error, reduce the batch size and please retry.

## 3. Launch comparison tool
There is a GUI comparison tool under `./eval` directory.
Go `./eval` directory and run `streamlit run main.py` to launch the comparison tool.

# note
This repository enables Elasticsearch Trial License inorder to use ML node to run embedding transformer model in ingest pipeline.
