install-requirements:
	pip install click pandas

setup:
	make install-requirements
	make download
	make unzip
	make concat-dir
	make setup-biopax-files
	make build-data-sets
	make clean

download:
	mkdir -p downloads
	wget http://smpdb.ca/downloads/smpdb_pathways.csv.zip -O downloads/pathways.zip
	wget http://smpdb.ca/downloads/smpdb_metabolites.csv.zip -O downloads/metabolites.zip
	wget http://smpdb.ca/downloads/smpdb_proteins.csv.zip -O downloads/proteins.zip


unzip:
	unzip -o downloads/pathways.zip -d downloads/pathways
	unzip -o downloads/metabolites.zip -d downloads/metabolites
	unzip -o downloads/proteins.zip -d downloads/proteins

concat-dir:
	sh scripts/concat_dir.sh downloads/proteins downloads/proteins.csv header
	sh scripts/concat_dir.sh downloads/metabolites downloads/metabolites.csv header

setup-biopax-files:
	# Cannot do a direct download from box: https://app.box.com/s/5xq1a7bibcp49vbn6xv0o4f1sl6x4w0d
	# Download into downloads/edges.zip and downloads/nodes.zip
	unzip -o downloads/edges.zip -d downloads/biopax-edges
	unzip -o downloads/nodes.zip -d downloads/biopax-nodes
	sh scripts/concat_dir.sh downloads/biopax-edges/edges downloads/biopax-edges.tsv noheader
	sh scripts/concat_dir.sh downloads/biopax-nodes/nodes downloads/biopax-nodes.tsv header


build-data-sets:
	python3 scripts/make_data.py downloads/metabolites.csv downloads/proteins.csv downloads/pathways/smpdb_pathways.csv
	# Comment out the line below if biopax-edges.tsv biopax-nodes.tsv are absent
	python3 scripts/add_biopax_sets.py edges.csv nodes.csv downloads/biopax-edges.tsv downloads/biopax-nodes.tsv
	python3 scripts/fill_edges.py edges.csv nodes.csv

	python3 scripts/fix_curies.py --file nodes.csv --out nodes.csv
	python3 scripts/fix_predicates.py --file edges.csv --out edges.csv

clean:
	# Delete everything in downloads directory except for .gitignore
	cd downloads && export GLOBIGNORE='.gitignore' && rm -rf *
