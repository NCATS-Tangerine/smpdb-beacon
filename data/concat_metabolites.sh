# Here I've broken up the concatenation commands because otherwise there are too many inputs

head -1 metabolites/SMP0028016_metabolites.csv > metabolites.csv
for filename in $(ls metabolites/SMP000*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP001*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP002*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP003*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP004*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP005*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP006*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP007*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP008*.csv); do sed 1d $filename >> metabolites.csv; done
for filename in $(ls metabolites/SMP009*.csv); do sed 1d $filename >> metabolites.csv; done

