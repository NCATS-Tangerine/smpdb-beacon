# SMPDB Beacon

Knowledge beacon wrapper for http://smpdb.ca/

Hosted at https://kba.ncats.io/beacon/smpdb/

Python Beacon client https://github.com/NCATS-Tangerine/tkbeacon-python-client

## Getting started

The latest release of this project expects the use of Python 3.7, and it is advised that you use this version.

### Create virtual environment

It is helpful to keep a local virtual environment in which all local dependencies as well as the application can be installed.

```sh
virtualenv -p python3.7 venv
source venv/bin/activate
```

We assume, within the setup scripts, that the `python` executable within this `venv` will be a Python 3.7 binary.

### Configuring

The [config/config.yaml](config/config.yaml) file can be modified to change some behaviours of this application.

### Installing the application

The [Makefile](Makefile) in the root directory can be used to install the application. You will need to install this project before using some of the scripts in `data/scripts` to get and clean up the data, as they depend on some modules in `beacon_controller`.

```shell
make install
```

**Note:** if you make changes to `config/config.yaml` you will need to re-install the application for those results to be used. Alternatively, you can use the command `make dev-install` to avoid needing to re-install each time you make a change.

### Getting the data

A prepared [Makefile](data/Makefile) is used to download and pre-processing the files needed to build a local SMPDB dataset for publication by this beacon.

#### Prerequisites

Some of the data used by the Makefile are two large data archive files - *edges.zip* and *nodes.zip* - which must be manually downloaded from an existing (currently, Box) archive site **[here](https://app.box.com/s/5xq1a7bibcp49vbn6xv0o4f1sl6x4w0d)** (Unfortunately direct downloads are not supported on the free version of Box, where this data is currently hosted, thus the data/Makefile cannot automatically download it). These two files should be placed into the `data/downloads` directory of the cloned project.  The other files needed will be automatically downloaded by the Makefile.

#### Building the Dataset

After downloading the above prerequisite files, run the following to build the dataset:

```shell
cd data
make setup
```

This executes h the following subordinate make targets:

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
make run
```

View it at http://localhost:8080

Alternatively you can run the application within a [Docker](https://docs.docker.com/engine/installation/) container:

```shell
make docker-build
make docker-run
```

View it at http://localhost:8085/

To stop the docker container you can use the command:

```shell
make docker-stop
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
