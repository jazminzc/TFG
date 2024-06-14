import pandas as pd

# Paso 1: Cargar la lista de IDs de Ensembl desde un archivo .txt
def load_ensembl_ids(file_path):
    # Leer el archivo en un DataFrame
    df = pd.read_csv(file_path, sep='\t', header=None, dtype=str, low_memory=False)
    print("DataFrame cargado desde el archivo:")
    print(df)
    
    # Extraer los IDs de Ensembl de la primera columna
    ensembl_ids = df.iloc[:, 0].tolist()
    
    # Verificar si hay entradas faltantes o mal formadas
    missing_ids = df.iloc[:, 0].isnull().sum()
    if missing_ids > 0:
        print(f"Advertencia: {missing_ids} entradas están faltantes en la lista de IDs de Ensembl.")
    
    # Imprimir la lista de IDs de Ensembl
    print("IDs de Ensembl cargados:")
    print(ensembl_ids)
    
    return ensembl_ids

# Paso 2: Analizar el archivo GTF y asegurar la extracción adecuada de gene_id
def filter_gtf_by_ensembl_ids(gtf_file_path, ensembl_ids):
    # Leer el archivo GTF
    gtf_data = pd.read_csv(gtf_file_path, sep="\t", comment='#', header=None, dtype=str, low_memory=False)
    gtf_data.columns = ['seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute']

    # Mejora en la extracción de gene_id de la columna de atributos
    gtf_data['gene_id'] = gtf_data['attribute'].str.extract(r'gene_id "([A-Za-z0-9]+)"')

    # Verificar si hay gene_id faltantes en las extracciones
    missing_gene_ids = gtf_data['gene_id'].isnull().sum()
    if missing_gene_ids > 0:
        print(f"Advertencia: {missing_gene_ids} entradas tienen gene_id faltante.")

    # Imprimir los valores extraídos de gene_id
    print("Valores de gene_id extraídos:")
    print(gtf_data['gene_id'].unique())
    
    # Imprimir el número de valores únicos de gene_id extraídos
    print("Número de valores únicos de gene_id extraídos:", len(gtf_data['gene_id'].unique()))

    # Filtrar los datos para incluir solo las filas con IDs de Ensembl en la lista
    filtered_gtf_data = gtf_data[gtf_data['gene_id'].isin(ensembl_ids)].copy()
    print("Número de entradas después de filtrar por IDs de Ensembl:", len(filtered_gtf_data))

    # Filtrar aún más los datos para incluir solo las filas donde feature es 'gene'
    filtered_gtf_data = filtered_gtf_data[filtered_gtf_data['feature'] == 'gene'].copy()
    print("Número de entradas después de filtrar por 'feature' == 'gene':", len(filtered_gtf_data))

    return filtered_gtf_data

# Paso 3: Convertir los datos GTF filtrados al formato BED
def gtf_to_bed(gtf_data, bed_file_path):
    # Extraer las columnas relevantes para el formato BED
    bed_data = gtf_data[['seqname', 'start', 'end', 'gene_id', 'score', 'strand', 'feature']]

    # Establecer chromStart para que sea basado en cero
    bed_data.loc[:, 'start'] = bed_data['start'].astype(int) - 1
    
    # Renombrar las columnas para que coincidan con el formato BED
    bed_data.columns = ['chrom', 'chromStart', 'chromEnd', 'name', 'score', 'strand', 'feature']
    
    # Guardar el archivo BED
    bed_data.to_csv(bed_file_path, sep='\t', header=False, index=False)

# Script
ensembl_ids_file = "<ruta_al_archivo_de_IDs>"
gtf_file = "<ruta_al_archivo_de_anotación (Mus_musculus.GRCm39.109.gtf)>"
bed_file = "<ruta_al_archivo_bed_filtrado>"

ensembl_ids = load_ensembl_ids(ensembl_ids_file)
filtered_gtf_data = filter_gtf_by_ensembl_ids(gtf_file, ensembl_ids)

# Imprimir algunas filas de los datos GTF filtrados para depuración
print("Datos GTF filtrados:")
print(filtered_gtf_data.head())

gtf_to_bed(filtered_gtf_data, bed_file)
