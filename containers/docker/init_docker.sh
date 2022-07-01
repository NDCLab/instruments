#!/bin/bash

# create data volume
docker volume create data

# bind the volume by running the container with the specified tags
docker run -it -d --name instruments -w /projects/pepper-pipeline --mount source=data,destination=/projects ndclab/instruments_container:flute-0.1.0

# copy all data from local to container
docker cp ../../scripts instruments:/projects/instruments
docker cp ../../data instruments:/projects/instruments

# copy in git metadata
docker cp ../../.github instruments:/projects/instruments
docker cp ../../.git instruments:/projects/instruments
docker cp ../../.gitignore instruments:/projects/instruments

# run container instance
docker exec -u root -it instruments bash
