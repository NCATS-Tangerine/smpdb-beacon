install-requirements:
	pip install click pandas

run:
	make download
	make unzip
	make concat-dir
	make build-data-sets
	make clean

download:
	# Cannot do a direct download from box. We will need the files:
	# 		https://stanford.box.com/v/smpdb-nodes
	# 		https://stanford.box.com/s/ecgwch0fmfnfft6q6yzqheuevttivyuw
	# save them as biopax-nodes.tsv, and biopax-edges.tsv
	mkdir -p downloads
	wget http://smpdb.ca/downloads/smpdb_pathways.csv.zip -O downloads/pathways.zip
	wget http://smpdb.ca/downloads/smpdb_metabolites.csv.zip -O downloads/metabolites.zip
	wget http://smpdb.ca/downloads/smpdb_proteins.csv.zip -O downloads/proteins.zip

unzip:
	unzip downloads/pathways.zip -d downloads/pathways
	unzip downloads/metabolites.zip -d downloads/metabolites
	unzip downloads/proteins.zip -d downloads/proteins

concat-dir:
	sh scripts/concat_dir.sh downloads/proteins downloads/proteins.csv header
	sh scripts/concat_dir.sh downloads/metabolites downloads/metabolites.csv header

build-data-sets:
	python3 scripts/make_data.py downloads/metabolites.csv downloads/proteins.csv downloads/pathways/smpdb_pathways.csv
	# Comment out the line below if biopax-edges.tsv biopax-nodes.tsv are absent
	python3 scripts/add_biopax_sets.py edges.csv nodes.csv biopax-edges.tsv biopax-nodes.tsv
	python3 scripts/fill_edges.py edges.csv nodes.csv

	python3 scripts/fix_curies.py --file nodes.csv --out nodes.csv

clean:
	rm -rf downloads
