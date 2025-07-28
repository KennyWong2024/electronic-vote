import os
import logging
import pandas as pd
from sqlalchemy import text

def cargar_csvs_en_lote(carpeta, engine, tabla, schema, mapping_columnas=None, columnas_extra=None, eliminar_columnas=None):
    if not os.path.isdir(carpeta):
        logging.error(f"El directorio '{carpeta}' no existe.")
        return

    archivos_csv = sorted(f for f in os.listdir(carpeta) if f.lower().endswith('.csv'))

    if not archivos_csv:
        logging.warning(f"No se encontraron archivos CSV en '{carpeta}'.")
        return

    for archivo in archivos_csv:
        ruta = os.path.join(carpeta, archivo)
        logging.info(f"Cargando archivo: {archivo}")

        try:
            df = pd.read_csv(ruta)

            if mapping_columnas:
                df = df.rename(columns=mapping_columnas)

            if eliminar_columnas:
                df.drop(columns=[col for col in eliminar_columnas if col in df.columns], inplace=True)

            if columnas_extra:
                for columna, valor in columnas_extra.items():
                    df[columna] = valor

            df.to_sql(
                name=tabla,
                con=engine,
                schema=schema,
                if_exists='append',
                index=False
            )
            logging.info(f"{len(df)} registros cargados desde '{archivo}'.")
        except Exception as e:
            logging.error(f"Error cargando '{archivo}': {e}")

    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{tabla}"))
            total = result.scalar()
            logging.info(f"Total de registros en {schema}.{tabla}: {total}")
            print(f"Datos cargados exitosamente. Total registros en '{schema}.{tabla}': {total}")
    except Exception as e:
        logging.warning(f"No se pudo verificar el total de registros en {schema}.{tabla}: {e}")
        print(f"Advertencia: No se pudo verificar la cantidad de registros en '{schema}.{tabla}'.")
