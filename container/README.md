# Instruments Container 

## Overview
This folder contains a Docker file and a Singularity recipe file that can both be used to build containers using their respective software. 

The singularity image can only be built on Linux with a user that has root access. Follow [this tutorial](https://ndclab.github.io/wiki/docs/technical-docs/docker-usage.html) to build a Singularity image on a non-Linux OS.

Additionally, the singularity image is intended to be used on the HPC cluster, whereas the docker image can be used on any local operating system.


## Background
Setting	up software by hand is no trivial task.	

Especially in the field of open source software, the success of disseminating a project is dependent on how reliably one can set up and run a project on    
their own machine, whether that	be a local PC or a sophisticated computing cluster.

Containerization tools such as Docker & Singularity provide the set of technologies necessary to quickly replicate system tools, libraries, data, environment variables, and more. This ensures that software is reproducible and maintainable for the lifetime of a project, independent of how an operating system changes over time.

While Docker is the most widely used solution for containerization, Singularity is the preferred means for high performance computing (HPC) clusters.

## Usage

### Docker

To build the docker image using the dockerfile, follow the listed instructions:

1. Build the image using the dockerfile

> docker build -t [name] Dockerfile

2. Run the docker image

> docker run -dp 3000:3000 [name]

### Singularity

To build the Singularity image using the recipe file, follow the listed
instructions.

1. Build the Singularity image using root permissions:

> sudo singularity build [name].simg singularity.recipe

2. Run and access the Singularity environment through its shell:

> singularity shell [name].simg



