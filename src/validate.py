# validate.py
# Módulo de validación de calidad de datos

def validate_schema(df, expected_columns):
    """
    Valida que el DataFrame tenga las columnas esperadas.
    """
    missing = [col for col in expected_columns if col not in df.columns]
    return {"missing_columns": missing}

import pandas as pd
from typing import List

def basic_checks(df: pd.DataFrame) -> List[str]:
    """
    Realiza validaciones mínimas sobre un DataFrame canónico.
    Retorna lista de errores encontrados.
    - Columnas requeridas: date, partner, amount
    - amount numérico >= 0
    - date en datetime válido
    """
    errors: List[str] = []

    required_cols = {"date", "partner", "amount"}
    missing = required_cols - set(df.columns)
    if missing:
        errors.append(f"Faltan columnas requeridas: {', '.join(missing)}")
        return errors  # No seguir si no están las columnas básicas

    # Validar tipo y valores de date
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        try:
            df["date"] = pd.to_datetime(df["date"], errors="raise")
        except Exception:
            errors.append("Columna 'date' no convertible a datetime.")

    # Validar amount numérico y >= 0
    if not pd.api.types.is_numeric_dtype(df["amount"]):
        errors.append("Columna 'amount' no es numérica.")
    else:
        if (df["amount"] < 0).any():
            errors.append("Existen valores negativos en 'amount'.")

    return errors
