# ingest.py
# Módulo de ingesta de CSVs heterogéneos

def ingest_data(file_path: str):
    """
    Ingesta básica de un archivo CSV.
    :param file_path: ruta del archivo CSV
    :return: DataFrame (pandas)
    """
    import pandas as pd
    df = pd.read_csv(file_path)
    return df
