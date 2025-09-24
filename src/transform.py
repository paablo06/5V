# transform.py
# Módulo de normalización y transformaciones hacia Bronze/Silver

def normalize_columns(df):
    """
    Normaliza nombres de columnas (minúsculas, sin espacios).
    """
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df
