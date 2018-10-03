# SMPDB

Knowledge beacon wrapper for http://smpdb.ca/

Uses the three CSV [downloads](http://smpdb.ca/downloads). These files must be
downloaded, unzipped, and concatenated by running `data/Makefile`:

```
cd data
make setup
```

Then install and run the application:

```
cd ..
make install
make run
```
