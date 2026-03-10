# RSNA SeuTao reproduction wrapper

Dette repo er gjort klar til at køre SeuTaos RSNA-løsning så nemt som muligt på en ny maskine.

Det gør følgende:
- bruger den uploadede SeuTao-kode i `external/SeuTao_repo`
- downloader de eksterne Google Drive-filer fra README (`data.zip`, pretrained weights, `csv.zip`)
- forbereder RSNA DICOM -> PNG
- bygger 3-slice konkatenerede billeder til 2D-modellen
- kører inference med SeuTaos pretrained 2D-modeller
- bygger de feature/probability-filer som sequence-modellen forventer
- træner sequence-modellen færdig

## Hurtig start

```bash
conda env create -f environment.yml
conda activate rsna-seutao
cp config.env.example config.env
# redigér config.env så paths passer
bash download_all.sh
bash smoke_test.sh
bash run_full_pipeline.sh
