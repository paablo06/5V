# validate.py
# Módulo de validación de calidad de datos

def validate_schema(df, expected_columns):
    """
    Valida que el DataFrame tenga las columnas esperadas.
    """
    missing = [col for col in expected_columns if col not in df.columns]
    return {"missing_columns": missing}
