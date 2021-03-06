# Contributing to `instruments`

## Overview
Please note our general guidelines for contributing to NDCLab projects [here](https://ndclab.github.io/wiki/docs/contributing.html).

* [Roadmap](#Roadmap)  
* [Directory Structure](#Directory-Structure)  
* [Container](#Container)
* [Adding Instruments](#Adding-Instruments)
* [Workflow](#Workflow)  

## Roadmap
Please see the roadmap available on the [README.md](https://github.com/NDCLab/template-tool/blob/main/README.md) file of this repository.

## Directory Structure

```yml
instruments
├── adexi
├── ambi
├── aq10
├── ...
├── scripts
    ├── __init__.py
    ├── json_scorer.py
    ├── score_type.py
    ├── subscore.py
    ├── survey.py
    ├── surveys.json
├── contributing.md
├── list-of-instruments.md
```


### Container
To ensure reproducibility of results and software, a default docker file is included with this template repository. The respective [README.md](https://github.com/NDCLab/template-tool/tree/main/container) contains a comprehensive guide on how to get started with containerization (special thanks to [Jonhas](https://github.com/Jonhas))!

A step-by-step guide to getting started also included in the following [video](https://www.youtube.com/watch?v=oO8n3y23b6M). 

## Adding Instruments
Instructions for adding an additional instrument to this repository are available on the associated [wiki page](https://ndclab.github.io/wiki/docs/technical-docs/instruments.html).

## Workflow
Workflow for both internal and external lab members is outlined on the [NDCLab contributing wiki page](https://ndclab.github.io/wiki/docs/contributing.html). 
