SPECIFICATION=api/1.3.0.yaml

install:
	pip install .
	pip install beacon/

venv:
	virtualenv -p python3.6 venv

dev-install:
	pip install -e .
	pip install beacon/

run:
	cd beacon && python -m swagger_server

docker-build:
	docker build -t ncats:smpdb-beacon .

docker-run:
	docker run -d --rm -v `pwd`/data:/usr/src/app/data/ --name smpdb-beacon -p 8085:8080 ncats:smpdb-beacon

docker-stop:
	docker stop smpdb-beacon

docker-logs:
	docker logs smpdb-beacon

regenerate:
	wget --no-clobber http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar | true
	java -jar swagger-codegen-cli generate -i $SPECIFICATION -l python-flask -o beacon
