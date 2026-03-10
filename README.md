# RSNA SeuTao Reproduction

Dette repo pakker SeuTaos 1.-plads-løsning til RSNA 2019, så hele pipelinen kan køres nemt på en ny maskine.

## Formål
- Klone originalkode
- Hente nødvendige eksterne filer
- Køre preprocessing
- Bruge SeuTaos pretrained 2D-modeller
- Køre sequence-modellen færdig

## Hurtig start

```bash
conda env create -f environment.yml
conda activate rsna-seutao
cp config.env.example config.env
# redigér config.env
bash download_all.sh
bash smoke_test.sh
bash run_full_pipeline.sh
