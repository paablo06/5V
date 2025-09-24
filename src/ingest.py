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

import pandas as pd
from datetime import datetime, timezone
from typing import List

def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade columnas de linaje:
    - source_file: nombre del archivo o sistema origen
    - ingested_at: timestamp UTC ISO
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena múltiples DataFrames asegurando esquema canónico mínimo:
    [date, partner, amount, source_file, ingested_at]
    """
    if not frames:
        return pd.DataFrame(columns=["date", "partner", "amount", "source_file", "ingested_at"])

    bronze = pd.concat(frames, ignore_index=True)
    expected_cols = ["date", "partner", "amount", "source_file", "ingested_at"]
    bronze = bronze.reindex(columns=expected_cols)
    return bronze
