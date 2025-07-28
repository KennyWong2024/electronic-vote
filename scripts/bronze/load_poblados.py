import os
import logging
from utils.db_connection import get_engine
from utils.data_loader import cargar_csvs_en_lote

def main():
    engine = get_engine()
    logging.info("Conexión a base de datos obtenida.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(script_dir, '..', '..', 'data', 'poblados')
    logging.info(f"Directorio de poblados: {carpeta}")

    mapping = {
        'OBJECTID': 'id',
        'PROVINCIA': 'provincia',
        'CANTON': 'canton',
        'DISTRITO': 'distrito',
        'DISTRITO_ID': 'codigo_postal',
        'x': 'x',
        'y': 'y'
    }

    columnas_a_eliminar = [
        'POBLAC_'
    ]

    cargar_csvs_en_lote(
        carpeta=carpeta,
        engine=engine,
        tabla='distrito_electoral',
        schema='bronze',
        mapping_columnas=mapping,
        columnas_extra=None,
        eliminar_columnas=columnas_a_eliminar
    )

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    main()
