# SMPDB Beacon

Knowledge beacon wrapper for http://smpdb.ca/

## Getting started

### Create virtual environment

It is helpful to keep a local virtual environment in which all local dependencies can be installed.

```sh
~/smpdb-beacon$ virtualenv -p python3.6 venv
~/smpdb-beacon$ source venv/bin/activate
```

### Configuring

The [config/config.yaml](config/config.yaml) file can be modified to change some behaviours of this application.

### Installing the application

The [Makefile](Makefile) in the root directory can be used to install the application. You will need to install this project before using some of the scripts in `data/scripts` to get and clean up the data, as they depend on some modules in `beacon_controller`.

```shell
~/smpdb-beacon$ make install
```

### Getting the data

See [data/Makefile](data/Makefile) for downloading and pre-processing the files needed.

Some of the data is hosted on box, and can be downloaded [here](https://app.box.com/s/5xq1a7bibcp49vbn6xv0o4f1sl6x4w0d). Unfortunately direct downloads are not supported on the free version of box, and so the data/Makefile cannot automatically download it. After downloading edges.zip and nodes.zip place them in the `data/downloads` directory. The other files needed will be automatically downloaded by the Makefile.

```shell
~/smpdb-beacon$ cd data
~/smpdb-beacon/data$ make setup
```

This will run through the following commands:

1. `make install-requirements`
Installs the packages that are needed to run the data pre-processing scripts
2. `make download`
Downloads a majority of the data (as mentioned above, some of it will need to be manually downloaded)
3. `make unzip`
Unzips the downloaded zip files
4. `make concat-dir`
The unzipped directories contain individual files for each record. This command combines them into a single CSV.
5. `make setup-biopax-files`
This command processes the biopax zip files that needed to be manually downloaded
6. `make build-data-sets`
This does the bulk of the pre-processing work, cleaning up identifiers and removing duplicate records
7. `make clean`
Deletes everything in the `data/downloads` directory except for `data/downloads/.gitignore`

### Running

The [Makefile](Makefile) in the root directory can be used to run the application:

```shell
~/smpdb-beacon$ make run
```

Alternatively you can run the application as a Docker container:

```shell
~/smpdb-beacon$ make docker-build
~/smpdb-beacon$ make docker-run
```

## Project structure


The `beacon` package was generated with Swagger, and the `beacon_controller` package is where all the implementation details are kept.

The `beacon` package can be regenerated with the Make command. But first make sure to update the `SPECIFICATION` parameter in [Makefile](Makefile) first if the specification file has a new name.

```
make regenerate
```

Alternatively, you can run swagger-codegen-cli.jar directly:

```
java -jar swagger-codegen-cli.jar generate -i <path-to-specification-file> -l python-flask -o beacon
```

Do a careful `git diff` review of the project after regenerating to make sure that nothing vital was overwritten, and to see all the changes made. Since we keep all implementation details in `beacon_controller` there shouldn't be much to worry about, and the only thing you will need to do is plug the `beacon_controller` package back in. Again, a `git diff` will show where this needs to be done.
