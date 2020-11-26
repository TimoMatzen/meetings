#Docker container

##Basic docker container with postgis 3.0

Execute in this folder

To build:
`
docker build -t <imageName>:<flag> .
`

To run:
`
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=letmein  <imageName>:<flag> 
`

This runs the container on port 5432 with user 'postgres' and password 'letmein'.
Please note that this container looses data on a rebuild.

For basic docker commands see https://www.edureka.co/blog/docker-commands/