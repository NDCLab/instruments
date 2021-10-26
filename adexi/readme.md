## ADEXI

This repo contains:

### English
* self-report
    * .docx format
    * .pdf format, as published on [chexi.se](https://chexi.se/downloads)
    * REDCap import .zip
* other-report
    * .docx format
    * .pdf format, as published on [chexi.se](https://chexi.se/downloads)

### Spanish for Latin America (ESLA)
* self-report
    * .docx format
    * .pdf format
* other-report
    * .docx format
    * .pdf format
* a .csv file providing transparency on the translation process used to accomplish the translation of the English ADEXI into Spanish for Latin America, which was performed by members of the NDCLab in 2021:

    | Name | Contribution |
    | :--  | :--  |
    | Aitana Fischer | performed the draft translation |
    | Laura Gallardo | independently edited the draft |
    | Emily Machado | back translated the translation to English |
    | Jessica Alexander | reconciled the forward and back translations |

Please report any issues with the ADEXI translations by posting an issue in this GitHub repository.


### Scoring Script
The English self-report is included in the repository scoring script.

| Variable | Details |
| :--  | :--  |
| adexi_scored-total_sX_rX_eX | total score: sum of all items (NaN if partial response prevents calculation of score) |
| adexi_scored-inh_sX_rX_eX | inhibition subscore: sum of 3, 4, 6, 10, and 14 (NaN if partial response prevents calculation of subscore) |
| adexi_scored-wm_sX_rX_eX | working memory subscore: sum of 1, 2, 5, 7, 8, 9, 11, 12, and 13 (NaN if partial response prevents calculation of subscore) |
| adexi_per-complete-total_sX_rX_eX | percentage of response for all items |
| adexi_per-complete-inh_sX_rX_eX | percentage of response for inhibition subscore |
| adexi_per-complete-wm_sX_rX_eX | percentage of response for working memory subscore |
