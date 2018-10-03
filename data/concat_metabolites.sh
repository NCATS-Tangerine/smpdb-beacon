head -1 metabolites/SMP0028016_metabolites.csv > metabolites.csv
for filename in $(ls metabolites/SMP*.csv); do sed 1d $filename >> metabolites.csv; done
