head -1 proteins/SMP0028016_proteins.csv > proteins.csv
for filename in $(ls proteins/SMP*.csv); do sed 1d $filename >> proteins.csv; done
