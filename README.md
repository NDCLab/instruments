# instruments

## Project Goal
A home for all surveys, questionnaires, and inventories used by the NDCLab, with an automatic scoring script.


## Background & Design
Each instrument used by the lab exists in the repo as a folder, containing (as applicable):
* the published instrument (in English and any other languages used for lab research)
* a REDCap import .zip for the instrument
* any translations completed by the NDCLab

Additionally, this repo holds the scoring script for all scorable instruments. For more information on development and planning, consult [CONTRIBUTING.md](https://github.com/NDCLab/instruments/blob/main/CONTRIBUTING.md).


## Roadmap
The following software iterations are planned for development. Each iteration is subject to change as the project progresses.

### 0.01 

* Scripts to handle automatic scoring of: ADEXI, AQ-10
* Upload of unscored instruments: CHEXI, COVID, DEMO, initStateA, postTaskA, PTTFQ

### 0.02

* Scripts to handle automatic scoring of: BFNE, EDS/HVS, ERQ, IUS, SCAARED, SIAS6, SSSQ
* Upload of unscored instruments: SICS

### 0.03

* Scripts to handle automatic scoring of: AMBI/RMBI, IDEA, IERQ, PANAS-N/RTQ, PHQ8, PSQI

### 0.1

* Scripts to handle automatic scoring of: ARI, BAARS4, HSPS, SPS6, SRQ, TAI, TEXI, THQ
* Cron jobs on the lab's HPC queue to handle automatic running of scripts on unprocessed data
* Generate comprehensive documentation on usage and functions
* Generate comprehensive testing suite to ensure stable release

### Future Directions

* Configure repository for proper packaging
* Release for pip/conda usage


## Usage
When using an instrument from this repo in an NDCLab project on REDCap:
1. Use the PDF for submission to the FIU IRB.
2. Import the zip to REDCap. Note that the zip file uses "_s1_r1_e1". These numerical values may need to be adjusted to meet the specific needs of your study's protocol; this requires changing the numerical values in each variable. No other change should be made to the variable names: other changes will break the link with the automated scoring script. See further details on the [lab's naming conventions for REDCap surveys](https://ndclab.github.io/wiki/docs/etiquette/naming-conventions.html#redcap).
3. Save REDCap data to the HPC in accordance with your study's IRB-approved protocol. Following release of version 0.1, the script will automatically output a copy of the data with the addition of all scoring columns.


## Work in Development
This `main` branch contains completed releases for this project. For all work-in-progress, please switch over to the `dev` branch.


## Contributors to the Scoring Script
| Name | Role |
| ---  | ---  |
| Osmany Pujol | created the original scoring script |
| Farukh Saidmuratov | collaborated on original script |
| Jess Alexander | management of initial releases and testing |
| Ana Lopez-Nuñez | testing and organization of initial releases |

Learn more about us [here](www.ndclab.com/people).

## Contributing
If you are interested in contributing, please read our [CONTRIBUTING.md](CONTRIBUTING.md) file.
