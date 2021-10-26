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
    ├── english
    ├── spanish_latAm
├── aq10
├── chexi
    ├── english
    ├── spanish_latAm
├── covid
├── demo
├── initStateA
├── postTaskA
├── pttfq
├── script
├── list-of-instruments.md
```


### Container
To ensure reproducibility of results and software, a default docker file is included with this template repository. The respective [README.md](https://github.com/NDCLab/template-tool/tree/main/container) contains a comprehensive guide on how to get started with containerization (special thanks to [Jonhas](https://github.com/Jonhas))!

A step-by-step guide to getting started also included in the following [video](https://www.youtube.com/watch?v=oO8n3y23b6M). 

## Adding Instruments
To add an additional instrument:
1. Follow the lab's [GitHub etiquette](https://ndclab.github.io/wiki/docs/etiquette/github-etiquette.html) to create a new branch off `dev` (`dev-NewInstrumentName`).
2. Create a new directory with the instrument's short name.
3. Upload the published PDF(s) and a REDCap import .zip that follows the lab's [naming conventions](https://ndclab.github.io/wiki/docs/etiquette/naming-conventions.html#redcap).
4. Add the instrument to the json file with the numerical values for subscale scoring.
5. Add the new instrument script to the instruments package located inside of the script folder.

## Workflow
Workflow for both internal and external lab members is outlined on the [NDCLab contributing wiki page](https://ndclab.github.io/wiki/docs/contributing.html). 
