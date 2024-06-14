# TFG
# Script de Python para convertir GTF en BED filtrado

## Descripción

Este repositorio contiene un script en Python desarrollado para mi TFG en bioquímica. El script realiza las siguientes funciones:

1. Carga una lista de IDs de Ensembl desde un archivo `.txt`.
2. Filtra un archivo GTF utilizando los IDs de Ensembl.
3. Convierte los datos GTF filtrados al formato BED.

## Uso

1. Se requieren unos archivos de partida:
    - Un archivo `.txt` con los IDs de Ensembl.
    - Un archivo GTF (para este TFG: `Mus_musculus.GRCm39.109.gtf`).

2. Modifica las rutas de los archivos en el script `script.py` según sea necesario:
    ```python
    ensembl_ids_file = "<ruta_al_archivo_de_IDs>"
    gtf_file = "<ruta_al_archivo_de_anotación (Mus_musculus.GRCm39.109.gtf)>"
    bed_file = "<ruta_al_archivo_bed_filtrado>"
    ```

3. Ejecuta el script:
    ```sh
    python script.py
    ```
