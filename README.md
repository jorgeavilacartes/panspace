# Embedding bacteria
The goal is to build an embedding space for bacterial sequences and use them as an index of dense vector to perform fast queries using faiss

## 0. Create virtual environment and install dependencies
```bash
conda activate base
mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
conda activate snakemake
```

## 1. generate FCGR

This pipeline count kmers using `kmc` 
```bash
snakemake -s count_kmers.smk -c16
```

## 2. train VAR
Once FCGR (npy file) has been generated, we can train a VAR (see `params.yaml`)

```bash
python src/train.py
```

## 3. build and test the index
Build the index, query the most similar embeddings
```bash 
python src/index.py
```

After training the model, you should see this folder structure
(assuming `data/` contains the tar.xz files, and in also used to save the FCGR and training results)

```
.
├── data
│   ├── actinobacillus_pleuropneumoniae__01.tar.xz
│   ├── aeromonas_salmonicida__01.tar.xz
│   ├── bacillus_anthracis__01.tar.xz
│   ├── faiss-embeddings
│   ├── fcgr-6mer
│   ├── models
│   ├── test
│   └── train
├── env
├── params.yaml
├── README.md
├── requirements.txt
└── src
    ├── dnn
    ├── fcgr
    ├── fcgr.py
    ├── index.py__
    └── train.py
```

## Extras
___
### `fcgr CLI`
```bash
python src/fcgr.py --help

USAGE: fcgr [-h] [-k KMER] [--path-fcgr PATH_FCGR] [--path-tarfile PATH_TARFILE] [--dir-tarfiles DIR_TARFILES] [-w WORKERS]

generate FCGR

OPTIONAL ARGUMENTS:
  -h, --help            show this help message and exit
  -k, --kmer KMER       kmer size, the FCGR will be of size (2^kmer,2^kmer). Default 6
  --path-fcgr PATH_FCGR
                        directory where to save fcgr generated. A subfolder for each specie
                        will be created inside. If not provided data/fcgr-<kmer>mer will be created
  --path-tarfile PATH_TARFILE
                        path to tarfile with one or several fasta files
  --dir-tarfiles DIR_TARFILES
                        path to directory with tarfiles, each tarfile should contain one or several
                        fasta files. Used only if --dir-tarfiles is not provided
  -w, --workers WORKERS
                        number of workers to use with ThreadPoolExecutor in case --dir-tarfile is provided.
```